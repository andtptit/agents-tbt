"""Gửi một tin nhắn chữ vào một chủ đề (topic) của nhóm Telegram "Nhà máy nội dung Thầy Tư".

Dùng cho các agent chạy theo lịch (ví dụ agent bình luận nhóm Facebook lúc 8h).

    python tools/tg_notify.py <khóa_chủ_đề> <file_nội_dung.txt>
    python tools/tg_notify.py binh_luan_nhom data/binh-luan-nhom/2026-11-19.txt

Khóa chủ đề lấy trong data/telegram_topics.json. Riêng `binh_luan_nhom` nếu chưa có thì
tự tạo chủ đề "💬 Bình luận nhóm" rồi lưu lại. Không in token ra màn hình.
"""
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOPICS_FILE = os.path.join(ROOT, "data", "telegram_topics.json")
NEW_TOPICS = {"binh_luan_nhom": "💬 Bình luận nhóm"}
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
API = f"https://api.telegram.org/bot{ENV.get('TELEGRAM_BOT_TOKEN', '')}/"


def api(method, params):
    data = urllib.parse.urlencode(params).encode()
    try:
        with urllib.request.urlopen(API + method, data=data, timeout=60) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return json.loads(e.read() or b"{}")


def topic_id(key):
    d = json.load(open(TOPICS_FILE, encoding="utf-8"))
    if key in d["topics"]:
        return d["chat_id"], d["topics"][key]["thread_id"]
    if key not in NEW_TOPICS:
        sys.exit(f"Không có chủ đề '{key}' trong data/telegram_topics.json")
    res = api("createForumTopic", {"chat_id": d["chat_id"], "name": NEW_TOPICS[key]})
    if not res.get("ok"):
        sys.exit(f"Không tạo được chủ đề: {res.get('description')}")
    d["topics"][key] = {"name": NEW_TOPICS[key], "thread_id": res["result"]["message_thread_id"]}
    json.dump(d, open(TOPICS_FILE, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"Đã tạo chủ đề {NEW_TOPICS[key]}")
    return d["chat_id"], d["topics"][key]["thread_id"]


def send(key, text):
    chat, thread = topic_id(key)
    parts, cur = [], ""
    for para in text.split("\n\n"):  # Telegram giới hạn 4096 ký tự/tin
        if len(cur) + len(para) + 2 > 3800 and cur:
            parts.append(cur)
            cur = ""
        cur = (cur + "\n\n" + para) if cur else para
    if cur:
        parts.append(cur)
    for p in parts:
        res = api("sendMessage", {"chat_id": chat, "message_thread_id": thread, "text": p,
                                  "disable_web_page_preview": "true"})
        if not res.get("ok"):
            sys.exit(f"Gửi thất bại: {res.get('description')}")
    print(f"Đã gửi {len(parts)} tin vào chủ đề {key}.")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    send(sys.argv[1], open(sys.argv[2], encoding="utf-8").read())
