"""Gửi báo cáo dạng mới lên Telegram: mỗi page 1 thẻ ảnh (kèm chú thích ngắn) + 1 tin Nhà máy nội dung gọn.

  python tools/report_send.py test     -> gửi BẢN THỬ vào chủ đề Báo cáo (không đổi lịch báo cáo 8h)
"""
import html
import json
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import page_stats as ps  # noqa: E402
import report_card as rc  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ICON = {"tienghan": "📘", "duhoc": "🎓"}


def card_caption(p):
    ch, net = p["change"], p["follows"] - p["unfollows"]
    trend = f"{'tăng' if ch >= 0 else 'giảm'} {abs(ch) * 100:.0f}%"
    warn = " ⚠️" if p["avg"] and ch <= -ps.DROP_ALERT else ""
    return (f"{ICON.get(p['key'], '📊')} <b>{html.escape(p['name'])}</b> · {p['day']:%d/%m}{warn}\n"
            f"👁 <b>{ps.fmt(p['views'])}</b> lượt xem ({trend}) · 👥 <b>{'+' if net >= 0 else ''}{net}</b> theo dõi")


def factory_message(orders, claude_ok=True):
    def recent(ts):
        try:
            return (datetime.now() - datetime.strptime(ts, "%Y-%m-%d %H:%M")).total_seconds() <= 86400
        except (TypeError, ValueError):
            return False

    by = lambda st: [c for c, o in orders.items() if o.get("status") == st]  # noqa: E731
    w_script, w_video = by("Chờ duyệt kịch bản"), by("Chờ duyệt video")
    ready = by("Đã duyệt video")
    working = [c for c, o in orders.items() if str(o.get("status", "")).startswith(
        ("Đang", "Chờ viết", "Viết lại", "Kịch bản đã duyệt"))]
    errors = [c for c, o in orders.items() if str(o.get("status", "")).startswith("Lỗi")]
    posted = [c for c, o in orders.items() if recent(o.get("published_at"))]
    new = [c for c, o in orders.items() if recent(o.get("at"))]

    lines = [f"🏭 <b>NHÀ MÁY NỘI DUNG</b> · {datetime.now():%d/%m}"]
    todo = []
    if w_video:
        todo.append(f"{len(w_video)} video")
    if w_script:
        todo.append(f"{len(w_script)} kịch bản")
    if todo:
        lines.append(f"\n👉 <b>An cần duyệt: {' · '.join(todo)}</b>")
        detail = []
        if w_video:
            detail.append("🎬 " + ", ".join(w_video))
        if w_script:
            detail.append("✍️ " + ", ".join(w_script))
        lines.append("<blockquote expandable>" + "\n".join(detail) + "</blockquote>")
    else:
        lines.append("\n✅ Không có gì chờ duyệt")
    if errors:
        lines.append(f"🚨 <b>Lỗi cần xử lý: {len(errors)}</b> — {', '.join(errors)}")
    if ready:
        lines.append(f"📤 Sẵn sàng đăng: {len(ready)} — {', '.join(ready)}")
    if working:
        lines.append(f"⚙️ Đang xử lý: {len(working)} — {', '.join(working)}")
    lines.append(f"\n<i>24 giờ qua: {len(new)} đơn mới · {len(posted)} video đã đăng</i>")
    lines.append("🟢 Bot và Claude hoạt động bình thường" if claude_ok
                 else "🔴 Claude chưa đăng nhập — chưa viết được kịch bản")
    return "\n".join(lines)


def send(tb, test=False):
    env = ps.m.load_env()
    thread = tb.TOPICS.get("bao_cao")
    if test:
        tb.say(tb.CHAT_ID, "🧪 BẢN THỬ GIAO DIỆN BÁO CÁO MỚI", thread)
    alerts = []
    for p, path in rc.render_all(env["META_READ_TOKEN"]):
        if p["avg"] and p["change"] <= -ps.DROP_ALERT:
            alerts.append(f"⚠️ {p['name']}: lượt xem ngày {p['day']:%d/%m} giảm {abs(p['change']) * 100:.0f}% so với "
                          f"trung bình 7 ngày ({ps.fmt(p['views'])} so với {ps.fmt(p['avg'])}).")
        fields = {"chat_id": tb.CHAT_ID, "caption": card_caption(p), "parse_mode": "HTML"}
        if thread:
            fields["message_thread_id"] = thread
        r = tb.api_upload("sendPhoto", fields, "photo", path)
        print("photo", p["key"], r.get("ok"), r.get("description", ""))
    orders = tb.load_orders()
    ok, _ = tb.script_writer.claude_status()
    text = factory_message(orders, ok)
    warn = ps.token_warning(env)
    if warn:
        text += "\n" + html.escape(warn)
    p = {"chat_id": tb.CHAT_ID, "text": text, "parse_mode": "HTML"}
    if thread:
        p["message_thread_id"] = thread
    r = tb.api("sendMessage", p)
    print("factory", r.get("ok"), r.get("description", ""))
    if not r.get("ok"):
        raise RuntimeError(f"Gửi tin nhà máy lỗi: {r.get('description')}")
    return alerts


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.argv = sys.argv[:2]
    import telegram_bot as tb  # noqa: E402
    send(tb, test=True)
