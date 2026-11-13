"""Bot Telegram duyệt video — Nhà máy nội dung Thầy Tư (bản sơ bộ).

Không cần thư viện ngoài. Đọc cấu hình trong .env (không bao giờ in token):
  TELEGRAM_BOT_TOKEN=...          token lấy từ @BotFather
  TELEGRAM_CHAT_ID=...            id nhóm duyệt (lấy bằng lệnh `whoami`)
  TELEGRAM_ALLOWED_USERS=111,222  id những người được bấm duyệt (lấy bằng `whoami`)

Lệnh:
  python tools/telegram_bot.py whoami
      Liệt kê các nhóm và người đã nhắn cho bot gần đây (để điền CHAT_ID, ALLOWED_USERS).
  python tools/telegram_bot.py send VIDEO.mp4 MA_VIDEO "Chú thích"
      Gửi video vào nhóm duyệt kèm nút Duyệt / Trả về; ghi vào hàng chờ.
  python tools/telegram_bot.py run
      Chạy bot (long polling, không cần máy chủ công khai): nhận nút bấm, lý do trả về,
      lệnh /ping, /cho (danh sách đang chờ duyệt).

Trạng thái lưu ở data/review_queue.json (sau này đồng bộ sang Notion).
"""
import json
import mimetypes
import os
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import script_writer  # noqa: E402
import video_maker  # noqa: E402
import meta_post  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
QUEUE = os.path.join(DATA, "review_queue.json")
OFFSET = os.path.join(DATA, "tg_offset.txt")
os.makedirs(DATA, exist_ok=True)
sys.stdout.reconfigure(encoding="utf-8")


def load_env():
    env = {}
    with open(os.path.join(ROOT, ".env"), encoding="utf-8") as fh:
        for row in fh:
            row = row.strip()
            if row and not row.startswith("#") and "=" in row:
                k, v = row.split("=", 1)
                env[k.strip()] = v.strip().strip('"').strip("'")
    return env


ENV = load_env()
TOKEN = ENV.get("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    sys.exit("Thiếu TELEGRAM_BOT_TOKEN trong .env")
API = f"https://api.telegram.org/bot{TOKEN}/"
CHAT_ID = ENV.get("TELEGRAM_CHAT_ID")
ALLOWED = {int(x) for x in ENV.get("TELEGRAM_ALLOWED_USERS", "").replace(" ", "").split(",") if x}
# Chủ đề trong nhóm (tạo bằng API, lưu ở data/telegram_topics.json): dat_video, duyet_kich_ban,
# duyet_video, bao_cao, canh_bao -> message_thread_id.
TOPICS_FILE = os.path.join(DATA, "telegram_topics.json")
TOPICS = ({k: v["thread_id"] for k, v in json.load(open(TOPICS_FILE, encoding="utf-8"))["topics"].items()}
          if os.path.exists(TOPICS_FILE) else {})
ORDERS = os.path.join(DATA, "orders.json")


def thread_of(m):
    """Chủ đề (topic) của một tin nhắn, để trả lời đúng chỗ."""
    return m.get("message_thread_id") if m.get("is_topic_message") else None


def say(chat, text, thread=None, reply_to=None, markup=None):
    p = {"chat_id": chat, "text": text}
    if thread:
        p["message_thread_id"] = thread
    if reply_to:
        p["reply_to_message_id"] = reply_to
    if markup:
        p["reply_markup"] = markup
    return api("sendMessage", p)


def api(method, params=None, timeout=70):
    data = urllib.parse.urlencode({k: (json.dumps(v) if isinstance(v, (dict, list)) else v)
                                   for k, v in (params or {}).items()}).encode()
    try:
        with urllib.request.urlopen(API + method, data=data, timeout=timeout) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return json.loads(e.read() or b"{}")


def api_upload(method, fields, file_field, path):
    boundary = uuid.uuid4().hex
    body = bytearray()
    for k, v in fields.items():
        v = json.dumps(v) if isinstance(v, (dict, list)) else str(v)
        body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"{k}\"\r\n\r\n{v}\r\n".encode()
    fname = os.path.basename(path)
    ctype = mimetypes.guess_type(fname)[0] or "application/octet-stream"
    body += (f"--{boundary}\r\nContent-Disposition: form-data; name=\"{file_field}\"; "
             f"filename=\"{fname}\"\r\nContent-Type: {ctype}\r\n\r\n").encode()
    body += open(path, "rb").read() + f"\r\n--{boundary}--\r\n".encode()
    req = urllib.request.Request(API + method, data=bytes(body),
                                 headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return json.loads(e.read() or b"{}")


def load_queue():
    return json.load(open(QUEUE, encoding="utf-8")) if os.path.exists(QUEUE) else {}


def save_queue(q):
    json.dump(q, open(QUEUE, "w", encoding="utf-8"), ensure_ascii=False, indent=2)


def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def buttons(code):
    return {"inline_keyboard": [[{"text": "✅ Duyệt", "callback_data": f"ok|{code}"},
                                 {"text": "↩️ Trả về", "callback_data": f"back|{code}"}]]}


def cmd_whoami():
    res = api("getUpdates", {"timeout": 0})
    if not res.get("ok"):
        sys.exit(f"Lỗi Telegram: {res.get('description')}")
    me = api("getMe")["result"]
    print(f"Bot: @{me['username']}")
    chats, users = {}, {}
    for u in res["result"]:
        m = u.get("message") or u.get("my_chat_member") or u.get("callback_query", {}).get("message") or {}
        c = m.get("chat")
        if c:
            chats[c["id"]] = c.get("title") or c.get("username") or c.get("first_name")
        frm = (u.get("message") or u.get("callback_query") or u.get("my_chat_member") or {}).get("from")
        if frm:
            users[frm["id"]] = (frm.get("first_name", "") + " " + frm.get("last_name", "")).strip()
    if not chats:
        print("Chưa thấy tin nhắn nào. Hãy gửi /start trong nhóm có bot rồi chạy lại.")
    for cid, name in chats.items():
        print(f"Nhóm/chat: {name}  →  TELEGRAM_CHAT_ID={cid}")
    for uid, name in users.items():
        print(f"Người dùng: {name}  →  id {uid}")


def cmd_send(path, code, caption):
    if not CHAT_ID:
        sys.exit("Thiếu TELEGRAM_CHAT_ID trong .env (chạy `whoami` để lấy).")
    text = f"🎬 {code}\n{caption}\n\nAI đã chấm: chưa áp dụng (bản sơ bộ)\nBấm Duyệt hoặc Trả về."
    fields = {"chat_id": CHAT_ID, "caption": text, "supports_streaming": "true", "reply_markup": buttons(code)}
    if TOPICS.get("duyet_video"):
        fields["message_thread_id"] = TOPICS["duyet_video"]
    res = api_upload("sendVideo", fields, "video", path)
    if not res.get("ok"):
        sys.exit(f"Gửi thất bại: {res.get('description')}")
    q = load_queue()
    q[code] = {"file": os.path.relpath(path, ROOT), "caption": caption, "status": "Chờ duyệt",
               "sent_at": now(), "message_id": res["result"]["message_id"], "history": []}
    save_queue(q)
    print(f"Đã gửi {code} vào nhóm duyệt.")


# ---------- Đơn đặt video (orders) ----------
ORDERS_LOCK = threading.Lock()
RUNNING = set()


def load_orders():
    with ORDERS_LOCK:
        return json.load(open(ORDERS, encoding="utf-8")) if os.path.exists(ORDERS) else {}


def update_order(code, **fields):
    with ORDERS_LOCK:
        orders = json.load(open(ORDERS, encoding="utf-8")) if os.path.exists(ORDERS) else {}
        orders.setdefault(code, {}).update(fields)
        json.dump(orders, open(ORDERS, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        return orders[code]


def progress(code, text):
    """Cập nhật dòng tiến độ ngay trên tin nhắn xác nhận đơn (chủ đề Đặt video)."""
    o = load_orders().get(code, {})
    full = f"📥 Đơn {code}: «{o.get('topic', '')}»\n{text}"
    if o.get("ack_id"):
        api("editMessageText", {"chat_id": CHAT_ID, "message_id": o["ack_id"], "text": full})
    else:
        r = say(CHAT_ID, full, TOPICS.get("dat_video"))
        if r.get("ok"):
            update_order(code, ack_id=r["result"]["message_id"])


def script_buttons(code):
    return {"inline_keyboard": [[{"text": "✅ Duyệt kịch bản", "callback_data": f"ks_ok|{code}"},
                                 {"text": "↩️ Trả về", "callback_data": f"ks_back|{code}"}]]}


def write_script_job(code):
    o = load_orders()[code]
    rewrite = o.get("status") == "Viết lại kịch bản"
    start = datetime.now().strftime("%H:%M")
    update_order(code, status="Đang viết kịch bản")
    progress(code, f"⏳ Claude đang {'viết lại' if rewrite else 'viết'} kịch bản… (bắt đầu {start}, thường 1–3 phút)")
    try:
        s = script_writer.write_script(o["topic"], script_writer.channel_of(o.get("channel", "TH")),
                                       feedback=o.get("feedback") if rewrite else None,
                                       previous=o.get("script") if rewrite else None)
        r = say(CHAT_ID, script_writer.format_script(code, s), TOPICS.get("duyet_kich_ban"),
                markup=script_buttons(code))
        if not r.get("ok"):
            raise RuntimeError(f"Gửi Telegram lỗi: {r.get('description')}")
        version = o.get("script_version", 0) + 1
        update_order(code, status="Chờ duyệt kịch bản", script=s, script_version=version,
                     script_msg_id=r["result"]["message_id"], script_at=now())
        progress(code, f"✅ Kịch bản bản {version} đã gửi sang ✍️ Duyệt kịch bản lúc {datetime.now():%H:%M}.")
    except Exception as e:  # noqa: BLE001
        update_order(code, status="Lỗi viết kịch bản", error=str(e)[:300])
        progress(code, f"⚠️ Chưa viết được kịch bản: {str(e)[:200]}\nSửa xong gõ /lai {code} để chạy lại.")
        say(CHAT_ID, f"🚨 {code}: lỗi khi viết kịch bản — {str(e)[:300]}", TOPICS.get("canh_bao"))
    finally:
        RUNNING.discard(code)


def video_buttons(code):
    return {"inline_keyboard": [[{"text": "✅ Duyệt video", "callback_data": f"vd_ok|{code}"},
                                 {"text": "↩️ Trả về", "callback_data": f"vd_back|{code}"}]]}


def make_video_job(code):
    o = load_orders()[code]
    start = datetime.now().strftime("%H:%M")
    update_order(code, status="Đang dựng video")
    try:
        path, total = video_maker.make_video(
            code, o["script"], log=lambda msg: progress(code, f"{msg} (bắt đầu {start}, thường 2–4 phút)"))
        s = o["script"]
        caption = (f"🎬 {code} — {s.get('title', '')}\n{o.get('channel', 'Tiếng Hàn Thầy Tư')} · {total:.0f} giây · "
                   f"khuôn {s.get('template', 'K4')} · giọng Vbee\n"
                   f"Kịch bản đã duyệt bởi {o.get('script_approved_by', '?')}.\nBấm Duyệt hoặc Trả về.")
        fields = {"chat_id": CHAT_ID, "caption": caption[:1000], "supports_streaming": "true",
                  "reply_markup": video_buttons(code)}
        if TOPICS.get("duyet_video"):
            fields["message_thread_id"] = TOPICS["duyet_video"]
        r = api_upload("sendVideo", fields, "video", path)
        if not r.get("ok"):
            raise RuntimeError(f"Gửi video lỗi: {r.get('description')}")
        update_order(code, status="Chờ duyệt video", video=os.path.relpath(path, ROOT), video_s=round(total, 1),
                     video_msg_id=r["result"]["message_id"], video_at=now())
        progress(code, f"✅ Video {total:.0f}s đã gửi sang 🎬 Duyệt video lúc {datetime.now():%H:%M}.")
    except Exception as e:  # noqa: BLE001
        update_order(code, status="Lỗi dựng video", error=str(e)[:300])
        progress(code, f"⚠️ Chưa dựng được video: {str(e)[:200]}\nGõ /dung {code} để thử lại.")
        say(CHAT_ID, f"🚨 {code}: lỗi khi dựng video — {str(e)[:300]}", TOPICS.get("canh_bao"))
    finally:
        RUNNING.discard(code)


def next_slot(hour=20):
    """Lần tới của HH:00 (Meta yêu cầu lịch đăng cách hiện tại ít nhất 10 phút)."""
    from datetime import timedelta
    t = datetime.now().replace(hour=hour, minute=0, second=0, microsecond=0)
    if t <= datetime.now() + timedelta(minutes=15):
        t += timedelta(days=1)
    return t


def publish_job(code, action, who, chat, thread):
    o = load_orders()[code]
    s = o.get("script", {})
    desc = (s.get("caption_facebook", "") + "\n\n" + " ".join(s.get("hashtags", []))).strip()
    state, when = {"pb_now": ("PUBLISHED", None), "pb_20": ("SCHEDULED", next_slot(20)),
                   "pb_draft": ("DRAFT", None)}[action]
    update_order(code, status="Đang đăng")
    say(chat, f"⏳ Đang tải {code} lên Facebook…", thread)
    try:
        r = meta_post.post_reel(os.path.join(ROOT, o["video"]), desc, state,
                                when.timestamp() if when else None)
        status = {"PUBLISHED": "Đã đăng", "SCHEDULED": "Đã lên lịch", "DRAFT": "Đã lưu nháp"}[state]
        update_order(code, status=status, fb_video_id=r["video_id"], fb_link=r.get("link"), published_by=who,
                     published_at=now(), scheduled_for=when.strftime("%Y-%m-%d %H:%M") if when else None)
        extra = f" lúc {when:%H:%M %d/%m}" if when else ""
        say(chat, f"✅ {code}: {status}{extra} trên «{ENV.get('META_PAGE_NAME', '')}».\n{r.get('link') or ''}", thread)
        progress(code, f"📣 {status}{extra} trên Facebook. {r.get('link') or ''}")
    except Exception as e:  # noqa: BLE001
        update_order(code, status="Lỗi đăng bài", error=str(e)[:300])
        say(chat, f"⚠️ {code}: đăng lỗi — {str(e)[:250]}", thread)
        say(CHAT_ID, f"🚨 {code}: lỗi khi đăng Facebook — {str(e)[:300]}", TOPICS.get("canh_bao"))
    finally:
        RUNNING.discard(code)


def dispatch_jobs():
    for code, o in load_orders().items():
        if code in RUNNING:
            continue
        if o.get("status") in ("Chờ viết kịch bản", "Viết lại kịch bản"):
            RUNNING.add(code)
            threading.Thread(target=write_script_job, args=(code,), daemon=True).start()
        elif o.get("status") == "Kịch bản đã duyệt":
            RUNNING.add(code)
            threading.Thread(target=make_video_job, args=(code,), daemon=True).start()


def person(u):
    return (u.get("first_name", "") + " " + u.get("last_name", "")).strip()


def handle_callback(cb, q):
    user = cb["from"]
    if ALLOWED and user["id"] not in ALLOWED:
        api("answerCallbackQuery", {"callback_query_id": cb["id"], "text": "Bạn không có quyền duyệt.",
                                    "show_alert": True})
        return
    action, code = cb["data"].split("|", 1)
    name = person(user)
    msg = cb["message"]

    def mark(label):
        api("editMessageReplyMarkup", {"chat_id": msg["chat"]["id"], "message_id": msg["message_id"],
                                       "reply_markup": {"inline_keyboard": [[{"text": label, "callback_data": "noop|x"}]]}})

    if action in ("pb_now", "pb_20", "pb_draft"):
        o = load_orders().get(code)
        if not o or not o.get("video"):
            api("answerCallbackQuery", {"callback_query_id": cb["id"], "text": "Không tìm thấy video của đơn này."})
            return
        if code in RUNNING or o.get("status") in ("Đang đăng", "Đã đăng", "Đã lên lịch"):
            api("answerCallbackQuery", {"callback_query_id": cb["id"], "text": f"Đơn đang ở trạng thái: {o.get('status')}"})
            return
        labels = {"pb_now": "📤 đăng ngay", "pb_20": "⏰ lên lịch 20:00", "pb_draft": "💾 lưu nháp"}
        mark(f"{name} chọn {labels[action]}")
        api("answerCallbackQuery", {"callback_query_id": cb["id"], "text": "Đang xử lý…"})
        RUNNING.add(code)
        threading.Thread(target=publish_job, args=(code, action, name, msg["chat"]["id"], thread_of(msg)),
                         daemon=True).start()
        return

    if action in ("vd_ok", "vd_back"):
        if code not in load_orders():
            api("answerCallbackQuery", {"callback_query_id": cb["id"], "text": "Không tìm thấy đơn này."})
            return
        if action == "vd_ok":
            update_order(code, status="Đã duyệt video", video_approved_by=name, video_approved_at=now())
            mark(f"✅ {name} đã duyệt video")
            api("answerCallbackQuery", {"callback_query_id": cb["id"], "text": "Đã duyệt video"})
            say(msg["chat"]["id"], f"✅ Video {code} đã được {name} duyệt lúc {now()}.\n"
                                   "Video sẵn sàng đăng (đăng tự động lên Facebook/TikTok sẽ nối khi có Meta App).",
                thread_of(msg), msg["message_id"])
            progress(code, f"🎉 Video đã được {name} duyệt lúc {datetime.now():%H:%M}. Sẵn sàng đăng.")
            page = ENV.get("META_PAGE_NAME", "(chưa cấu hình page)")
            say(msg["chat"]["id"], f"📤 Đăng {code} lên Facebook page «{page}»?", thread_of(msg),
                markup={"inline_keyboard": [[{"text": "📤 Đăng ngay", "callback_data": f"pb_now|{code}"},
                                             {"text": "⏰ Lên lịch 20:00", "callback_data": f"pb_20|{code}"}],
                                            [{"text": "💾 Lưu nháp trên page", "callback_data": f"pb_draft|{code}"}]]})
        else:
            ask = say(msg["chat"]["id"], f"↩️ {code}: {name} ơi, trả lời tin nhắn này kèm lý do cần sửa video nhé.",
                      thread_of(msg), msg["message_id"], {"force_reply": True, "selective": True})
            update_order(code, status="Trả về video (chờ lý do)", reason_kind="video",
                         reason_prompt_id=ask.get("result", {}).get("message_id"))
            mark(f"↩️ {name} đã trả về")
            api("answerCallbackQuery", {"callback_query_id": cb["id"], "text": "Gửi lý do giúp mình nhé"})
        return

    if action in ("ks_ok", "ks_back"):
        if code not in load_orders():
            api("answerCallbackQuery", {"callback_query_id": cb["id"], "text": "Không tìm thấy đơn này."})
            return
        if action == "ks_ok":
            update_order(code, status="Kịch bản đã duyệt", script_approved_by=name, script_approved_at=now())
            mark(f"✅ {name} đã duyệt kịch bản")
            api("answerCallbackQuery", {"callback_query_id": cb["id"], "text": "Đã duyệt kịch bản"})
            say(msg["chat"]["id"], f"✅ Kịch bản {code} đã được {name} duyệt lúc {now()}.\n"
                                   "Hệ thống đang tạo giọng và dựng video, xong sẽ gửi sang 🎬 Duyệt video.",
                thread_of(msg), msg["message_id"])
            progress(code, f"✅ Kịch bản đã được {name} duyệt lúc {datetime.now():%H:%M}. Đang xếp hàng dựng video…")
        else:
            ask = say(msg["chat"]["id"], f"↩️ {code}: {name} ơi, trả lời tin nhắn này kèm lý do cần sửa kịch bản nhé.",
                      thread_of(msg), msg["message_id"], {"force_reply": True, "selective": True})
            update_order(code, status="Trả về kịch bản (chờ lý do)",
                         reason_prompt_id=ask.get("result", {}).get("message_id"))
            mark(f"↩️ {name} đã trả về")
            api("answerCallbackQuery", {"callback_query_id": cb["id"], "text": "Gửi lý do giúp mình nhé"})
        return

    item = q.get(code)
    if not item:
        api("answerCallbackQuery", {"callback_query_id": cb["id"]})
        return
    if action == "ok":
        item["status"] = "Đã duyệt"
        item["history"].append({"at": now(), "by": name, "action": "Duyệt"})
        mark(f"✅ {name} đã duyệt")
        api("answerCallbackQuery", {"callback_query_id": cb["id"], "text": "Đã duyệt"})
        say(msg["chat"]["id"], f"✅ {code} đã được {name} duyệt lúc {now()}.", thread_of(msg), msg["message_id"])
    elif action == "back":
        item["status"] = "Trả về (chờ lý do)"
        item["history"].append({"at": now(), "by": name, "action": "Trả về"})
        ask = say(msg["chat"]["id"], f"↩️ {code}: {name} ơi, trả lời tin nhắn này kèm lý do cần sửa nhé.",
                  thread_of(msg), msg["message_id"], {"force_reply": True, "selective": True})
        item["reason_prompt_id"] = ask.get("result", {}).get("message_id")
        mark(f"↩️ {name} đã trả về")
        api("answerCallbackQuery", {"callback_query_id": cb["id"], "text": "Gửi lý do giúp mình nhé"})
    else:
        api("answerCallbackQuery", {"callback_query_id": cb["id"]})
    save_queue(q)


def handle_message(m, q):
    text = (m.get("text") or "").strip()
    chat = m["chat"]["id"]
    reply_to = (m.get("reply_to_message") or {}).get("message_id")
    allowed = not ALLOWED or m["from"]["id"] in ALLOWED
    if reply_to:
        for code, o in load_orders().items():
            if o.get("reason_prompt_id") == reply_to and allowed:
                fb = f"(Góp ý sau khi xem video) {text}" if o.get("reason_kind") == "video" else text
                update_order(code, status="Viết lại kịch bản", feedback=fb, reason_prompt_id=None, reason_kind=None)
                say(chat, f"Đã ghi lý do cho {code}. Claude sẽ viết lại kịch bản theo góp ý, "
                          "gửi sang ✍️ Duyệt kịch bản rồi dựng lại video.", thread_of(m), m["message_id"])
                return
        for code, item in q.items():
            if item.get("reason_prompt_id") == reply_to and allowed:
                item["status"] = "Trả về"
                item["return_reason"] = text
                item["history"].append({"at": now(), "by": person(m["from"]), "reason": text})
                save_queue(q)
                say(chat, f"Đã ghi lý do cho {code}. Hệ thống sẽ sửa và gửi lại bản mới.",
                    thread_of(m), m["message_id"])
                return
    cmd = text.split("@", 1)[0].split(" ", 1)[0].lower() if text.startswith("/") else ""
    arg = text.split(" ", 1)[1].strip() if " " in text else ""
    if cmd == "/ping":
        ok, status = script_writer.claude_status()
        busy = ", ".join(sorted(RUNNING)) or "không có"
        say(chat, f"🟢 Bot đang chạy ({now()}).\n{'🟢' if ok else '🔴'} {status}.\nĐang xử lý: {busy}.", thread_of(m))
    elif cmd == "/baocao":
        send_report()
        if thread_of(m) != TOPICS.get("bao_cao"):
            say(chat, "Đã gửi báo cáo vào chủ đề 📊 Báo cáo.", thread_of(m), m["message_id"])
    elif cmd == "/cho":
        pending = [f"• {c}: {v['status']}" for c, v in q.items() if v["status"] != "Đã duyệt"]
        pending += [f"• {c}: {o['status']} — {o['topic']}" for c, o in load_orders().items()
                    if o["status"] not in ("Đã duyệt video", "Hủy")]
        say(chat, "\n".join(pending) or "Không có việc nào đang chờ.", thread_of(m))
    elif cmd == "/dung":
        if allowed and arg in load_orders() and load_orders()[arg].get("script"):
            update_order(arg, status="Kịch bản đã duyệt", error=None)
            say(chat, f"🔁 Đã xếp lại {arg} để dựng video.", thread_of(m), m["message_id"])
        else:
            say(chat, "Gõ /dung <mã đơn> (đơn đã có kịch bản duyệt).", thread_of(m), m["message_id"])
    elif cmd == "/lai":
        if allowed and arg in load_orders():
            update_order(arg, status="Chờ viết kịch bản", error=None)
            say(chat, f"🔁 Đã xếp lại {arg} để Claude viết kịch bản.", thread_of(m), m["message_id"])
        else:
            say(chat, "Gõ /lai <mã đơn>, ví dụ /lai TH-261112-01", thread_of(m), m["message_id"])
    elif cmd in ("/tao", "/taodh", "/taoth"):
        if not allowed:
            say(chat, "Bạn chưa có quyền đặt video.", thread_of(m), m["message_id"])
            return
        # Chọn kênh: /tao dh <chủ đề> hoặc /taodh <chủ đề> → Du học; còn lại → Tiếng Hàn.
        chan = "DH" if cmd == "/taodh" else "TH"
        first = arg.split(" ", 1)[0].lower()
        if cmd == "/tao" and first in ("dh", "duhoc", "th", "tienghan"):
            chan = "DH" if first in ("dh", "duhoc") else "TH"
            arg = arg.split(" ", 1)[1].strip() if " " in arg else ""
        if not arg:
            say(chat, "Gõ kèm chủ đề, ví dụ:\n/tao Học 1 từ biết thêm 5 từ (gốc Hán Hàn)  → kênh Tiếng Hàn\n"
                      "/tao dh Trượt visa có mất tiền hồ sơ không?  → kênh Du học", thread_of(m), m["message_id"])
            return
        day = datetime.now().strftime("%y%m%d")
        n = 1 + sum(1 for c in load_orders() if c.startswith(f"{chan}-{day}-"))
        code = f"{chan}-{day}-{n:02d}"
        cname = script_writer.CHANNELS[chan]["name"]
        r = say(chat, f"📥 Đơn {code} ({cname}): «{arg}»\n🕒 Đã nhận, đang xếp hàng cho Claude viết kịch bản…",
                thread_of(m), m["message_id"])
        update_order(code, topic=arg, channel=cname, status="Chờ viết kịch bản",
                     by=person(m["from"]), at=now(), order_message_id=m["message_id"],
                     ack_id=r.get("result", {}).get("message_id"))


# ---------- Báo cáo ----------
REPORT_STATE = os.path.join(DATA, "report_state.json")
REPORT_HOUR = 8  # 8h sáng hằng ngày


def build_report():
    orders = load_orders()
    videos = load_queue()
    today = datetime.now().strftime("%Y-%m-%d")
    since = datetime.now().timestamp() - 24 * 3600

    def recent(ts):
        try:
            return datetime.strptime(ts, "%Y-%m-%d %H:%M").timestamp() >= since
        except (TypeError, ValueError):
            return False

    new = [c for c, o in orders.items() if recent(o.get("at"))]
    scripts_ok = [c for c, o in orders.items() if recent(o.get("script_approved_at"))]
    videos_ok = [c for c, o in orders.items() if recent(o.get("video_approved_at"))]
    waiting_script = [c for c, o in orders.items() if o.get("status") == "Chờ duyệt kịch bản"]
    waiting_video = [c for c, o in orders.items() if o.get("status") == "Chờ duyệt video"]
    errors = [f"{c} ({o.get('status')})" for c, o in orders.items() if str(o.get("status", "")).startswith("Lỗi")]
    working = [c for c, o in orders.items() if str(o.get("status", "")).startswith(("Đang", "Chờ viết", "Viết lại",
                                                                                   "Kịch bản đã duyệt"))]
    ready = [c for c, o in orders.items() if o.get("status") == "Đã duyệt video"]
    lines = [f"📊 BÁO CÁO NGÀY {datetime.now():%d/%m/%Y} (24 giờ qua)",
             f"• Đơn mới: {len(new)}",
             f"• Kịch bản đã duyệt: {len(scripts_ok)}",
             f"• Video đã duyệt: {len(videos_ok)}",
             "",
             f"⏳ Chờ An duyệt kịch bản: {len(waiting_script)}" + (f" — {', '.join(waiting_script)}" if waiting_script else ""),
             f"⏳ Chờ An duyệt video: {len(waiting_video)}" + (f" — {', '.join(waiting_video)}" if waiting_video else ""),
             f"⚙️ Đang xử lý: {len(working)}" + (f" — {', '.join(working)}" if working else ""),
             f"✅ Video sẵn sàng đăng: {len(ready)}" + (f" — {', '.join(ready)}" if ready else ""),
             f"🚨 Lỗi cần xử lý: {len(errors)}" + (f" — {', '.join(errors)}" if errors else "")]
    ok, status = script_writer.claude_status()
    lines.append("")
    lines.append(f"{'🟢' if ok else '🔴'} {status}. Bot đang chạy.")
    if not ok:
        lines.append("→ Cần đăng nhập lại Claude Code trên máy Cowork thì mới viết được kịch bản.")
    return "\n".join(lines), today


def send_report():
    text, today = build_report()
    r = say(CHAT_ID, text, TOPICS.get("bao_cao"))
    if r.get("ok"):
        json.dump({"last_report": today}, open(REPORT_STATE, "w", encoding="utf-8"))
    return r


def maybe_report():
    if datetime.now().hour < REPORT_HOUR:
        return
    today = datetime.now().strftime("%Y-%m-%d")
    last = json.load(open(REPORT_STATE, encoding="utf-8")).get("last_report") if os.path.exists(REPORT_STATE) else None
    if last != today:
        send_report()


NOTION_LAST = [0.0]


def maybe_notion():
    """Mỗi phút đẩy các đơn có thay đổi lên Notion (chạy nền, lỗi không làm dừng bot)."""
    if time.time() - NOTION_LAST[0] < 60 or "notion" in RUNNING:
        return
    NOTION_LAST[0] = time.time()

    def job():
        try:
            import notion_sync
            notion_sync.sync_orders()
        except Exception as e:  # noqa: BLE001
            print("Lỗi đồng bộ Notion:", e)
        finally:
            RUNNING.discard("notion")
    RUNNING.add("notion")
    threading.Thread(target=job, daemon=True).start()


def cmd_run():
    offset = int(open(OFFSET).read()) if os.path.exists(OFFSET) else 0
    me = api("getMe").get("result", {})
    ok, status = script_writer.claude_status()
    print(f"Bot @{me.get('username')} đang chạy. {status}. Ctrl+C để dừng.")
    while True:
        dispatch_jobs()
        maybe_notion()
        try:
            maybe_report()
        except Exception as e:  # noqa: BLE001
            print("Lỗi báo cáo:", e)
        res = api("getUpdates", {"timeout": 20, "offset": offset,
                                 "allowed_updates": ["message", "callback_query"]})
        if not res.get("ok"):
            print("Lỗi:", res.get("description"))
            time.sleep(5)
            continue
        q = load_queue()
        for u in res["result"]:
            offset = u["update_id"] + 1
            try:
                if "callback_query" in u:
                    handle_callback(u["callback_query"], q)
                elif "message" in u:
                    handle_message(u["message"], q)
            except Exception as e:  # keep the bot alive on one bad update
                print("Lỗi xử lý:", e)
        open(OFFSET, "w").write(str(offset))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    if sys.argv[1] == "whoami":
        cmd_whoami()
    elif sys.argv[1] == "send":
        cmd_send(sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else "")
    elif sys.argv[1] == "run":
        cmd_run()
    else:
        sys.exit(__doc__)
