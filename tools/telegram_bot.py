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
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from datetime import datetime

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
    res = api_upload("sendVideo", {"chat_id": CHAT_ID, "caption": text, "supports_streaming": "true",
                                   "reply_markup": buttons(code)}, "video", path)
    if not res.get("ok"):
        sys.exit(f"Gửi thất bại: {res.get('description')}")
    q = load_queue()
    q[code] = {"file": os.path.relpath(path, ROOT), "caption": caption, "status": "Chờ duyệt",
               "sent_at": now(), "message_id": res["result"]["message_id"], "history": []}
    save_queue(q)
    print(f"Đã gửi {code} vào nhóm duyệt.")


def handle_callback(cb, q):
    user = cb["from"]
    if ALLOWED and user["id"] not in ALLOWED:
        api("answerCallbackQuery", {"callback_query_id": cb["id"], "text": "Bạn không có quyền duyệt.",
                                    "show_alert": True})
        return
    action, code = cb["data"].split("|", 1)
    name = (user.get("first_name", "") + " " + user.get("last_name", "")).strip()
    item = q.get(code)
    if not item:
        api("answerCallbackQuery", {"callback_query_id": cb["id"], "text": "Không tìm thấy video này."})
        return
    msg = cb["message"]
    if action == "ok":
        item["status"] = "Đã duyệt"
        item["history"].append({"at": now(), "by": name, "action": "Duyệt"})
        api("editMessageReplyMarkup", {"chat_id": msg["chat"]["id"], "message_id": msg["message_id"],
                                       "reply_markup": {"inline_keyboard": [[{"text": f"✅ {name} đã duyệt",
                                                                              "callback_data": "noop|x"}]]}})
        api("answerCallbackQuery", {"callback_query_id": cb["id"], "text": "Đã duyệt"})
        api("sendMessage", {"chat_id": msg["chat"]["id"], "reply_to_message_id": msg["message_id"],
                            "text": f"✅ {code} đã được {name} duyệt lúc {now()}."})
    elif action == "back":
        item["status"] = "Trả về (chờ lý do)"
        item["history"].append({"at": now(), "by": name, "action": "Trả về"})
        ask = api("sendMessage", {"chat_id": msg["chat"]["id"], "reply_to_message_id": msg["message_id"],
                                  "text": f"↩️ {code}: {name} ơi, trả lời tin nhắn này kèm lý do cần sửa nhé.",
                                  "reply_markup": {"force_reply": True, "selective": True}})
        item["reason_prompt_id"] = ask.get("result", {}).get("message_id")
        api("editMessageReplyMarkup", {"chat_id": msg["chat"]["id"], "message_id": msg["message_id"],
                                       "reply_markup": {"inline_keyboard": [[{"text": f"↩️ {name} đã trả về",
                                                                              "callback_data": "noop|x"}]]}})
        api("answerCallbackQuery", {"callback_query_id": cb["id"], "text": "Gửi lý do giúp mình nhé"})
    else:
        api("answerCallbackQuery", {"callback_query_id": cb["id"]})
    save_queue(q)


def handle_message(m, q):
    text = (m.get("text") or "").strip()
    chat = m["chat"]["id"]
    reply_to = (m.get("reply_to_message") or {}).get("message_id")
    if reply_to:
        for code, item in q.items():
            if item.get("reason_prompt_id") == reply_to:
                if ALLOWED and m["from"]["id"] not in ALLOWED:
                    return
                item["status"] = "Trả về"
                item["return_reason"] = text
                item["history"].append({"at": now(), "by": (m["from"].get("first_name", "") + " " + m["from"].get("last_name", "")).strip(), "reason": text})
                save_queue(q)
                api("sendMessage", {"chat_id": chat, "reply_to_message_id": m["message_id"],
                                    "text": f"Đã ghi lý do cho {code}. Hệ thống sẽ sửa và gửi lại bản mới."})
                return
    if text.startswith("/ping"):
        api("sendMessage", {"chat_id": chat, "text": f"🟢 Bot đang chạy ({now()})."})
    elif text.startswith("/cho"):
        pending = [f"• {c}: {v['status']}" for c, v in q.items() if v["status"] != "Đã duyệt"]
        api("sendMessage", {"chat_id": chat, "text": "\n".join(pending) or "Không có video nào đang chờ."})


def cmd_run():
    offset = int(open(OFFSET).read()) if os.path.exists(OFFSET) else 0
    me = api("getMe").get("result", {})
    print(f"Bot @{me.get('username')} đang chạy. Ctrl+C để dừng.")
    while True:
        res = api("getUpdates", {"timeout": 50, "offset": offset,
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
