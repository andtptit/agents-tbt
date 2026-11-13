"""Đồng bộ Nhà máy nội dung sang Notion (chỉ để XEM và theo dõi; duyệt vẫn trên Telegram).

  python tools/notion_sync.py check          kiểm tra token + quyền vào trang gốc
  python tools/notion_sync.py setup          tạo 3 bảng trong trang gốc (chạy 1 lần), ghi id vào data/notion.json
  python tools/notion_sync.py seed           đổ sẵn "Việc chờ PM quyết" + ý tưởng lịch tháng 12 (chạy 1 lần)
  python tools/notion_sync.py sync           đẩy đơn trong data/orders.json lên bảng "Đơn video"

Cấu hình trong .env: NOTION_TOKEN (integration nội bộ "Thay Tu Bot"), NOTION_ROOT_PAGE (id trang gốc, không bắt buộc).
Không bao giờ in token. Không đưa họ tên/số điện thoại khách hàng lên Notion.
Bot gọi sync_orders() mỗi phút; chỉ đơn có thay đổi mới được gửi.
"""
import hashlib
import json
import os
import sys
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE = os.path.join(ROOT, "data", "notion.json")
ORDERS = os.path.join(ROOT, "data", "orders.json")
DEFAULT_ROOT_PAGE = "417ed9301be1808cbeb8d279000f2432"
VERSION = "2022-06-28"

STATUSES = ["Chờ viết kịch bản", "Đang viết kịch bản", "Viết lại kịch bản", "Chờ duyệt kịch bản",
            "Trả về kịch bản (chờ lý do)", "Kịch bản đã duyệt", "Đang dựng video", "Chờ duyệt video",
            "Trả về video (chờ lý do)", "Đã duyệt video", "Đang đăng", "Đã lên lịch", "Đã lưu nháp",
            "Đã đăng", "Lỗi viết kịch bản", "Lỗi dựng video", "Lỗi đăng bài", "Hủy"]


def _env():
    env = {}
    for row in open(os.path.join(ROOT, ".env"), encoding="utf-8"):
        row = row.strip()
        if row and not row.startswith("#") and "=" in row:
            k, v = row.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    return env


ENV = _env()
TOKEN = ENV.get("NOTION_TOKEN")
ROOT_PAGE = ENV.get("NOTION_ROOT_PAGE", DEFAULT_ROOT_PAGE)


def api(method, path, body=None):
    if not TOKEN:
        raise RuntimeError("Thiếu NOTION_TOKEN trong .env")
    req = urllib.request.Request("https://api.notion.com/v1/" + path, method=method,
                                 data=json.dumps(body).encode() if body is not None else None,
                                 headers={"Authorization": "Bearer " + TOKEN, "Notion-Version": VERSION,
                                          "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        msg = json.loads(e.read() or b"{}").get("message", "")
        raise RuntimeError(f"Notion lỗi {e.code}: {msg}") from None


def load_state():
    return json.load(open(STATE, encoding="utf-8")) if os.path.exists(STATE) else {}


def save_state(s):
    json.dump(s, open(STATE, "w", encoding="utf-8"), ensure_ascii=False, indent=2)


def txt(s):
    return [{"type": "text", "text": {"content": str(s)[:1900]}}] if s else []


def opts(names, colors=None):
    colors = colors or {}
    return {"options": [{"name": n, "color": colors.get(n, "default")} for n in names]}


# ---------- Dựng bảng ----------
def setup():
    st = load_state()
    if st.get("orders_db"):
        print("Đã dựng từ trước, bỏ qua (xóa data/notion.json nếu muốn dựng lại).")
        return st
    parent = {"type": "page_id", "page_id": ROOT_PAGE}
    status_colors = {s: ("red" if s.startswith("Lỗi") else "yellow" if s.startswith(("Chờ duyệt", "Trả về"))
                         else "green" if s in ("Đã đăng", "Đã duyệt video", "Đã lên lịch") else "blue")
                     for s in STATUSES}
    orders = api("POST", "databases", {
        "parent": parent, "is_inline": True, "icon": {"type": "emoji", "emoji": "🎬"},
        "title": txt("Đơn video"),
        "properties": {
            "Chủ đề": {"title": {}},
            "Mã đơn": {"rich_text": {}},
            "Kênh": {"select": opts(["Tiếng Hàn Thầy Tư", "Du học Thầy Tư"],
                                    {"Tiếng Hàn Thầy Tư": "blue", "Du học Thầy Tư": "red"})},
            "Trạng thái": {"select": opts(STATUSES, status_colors)},
            "Tiêu đề kịch bản": {"rich_text": {}},
            "Dạng": {"rich_text": {}},
            "Thời lượng (giây)": {"number": {}},
            "Bản kịch bản": {"number": {}},
            "Người đặt": {"rich_text": {}},
            "Ngày đặt": {"date": {}},
            "Duyệt kịch bản": {"rich_text": {}},
            "Duyệt video": {"rich_text": {}},
            "Góp ý gần nhất": {"rich_text": {}},
            "Link Facebook": {"url": {}},
            "Lịch đăng": {"date": {}},
            "Lỗi": {"rich_text": {}},
        }})
    calendar = api("POST", "databases", {
        "parent": parent, "is_inline": True, "icon": {"type": "emoji", "emoji": "🗓️"},
        "title": txt("Lịch nội dung"),
        "properties": {
            "Chủ đề": {"title": {}},
            "Ngày đăng": {"date": {}},
            "Kênh": {"select": opts(["Tiếng Hàn Thầy Tư", "Du học Thầy Tư"],
                                    {"Tiếng Hàn Thầy Tư": "blue", "Du học Thầy Tư": "red"})},
            "Dạng": {"select": opts(["A series chuyên môn", "B bán khóa", "T giới thiệu trường",
                                     "S hậu trường", "C chi phí minh bạch", "H hỏi đáp"])},
            "Trục": {"select": opts(["Điểm đau", "Câu chuyện sản phẩm", "Điểm khác biệt"])},
            "Trạng thái": {"select": opts(["Ý tưởng", "PM đã chốt", "Đã đặt đơn", "Đã đăng"],
                                          {"Ý tưởng": "gray", "PM đã chốt": "yellow", "Đã đặt đơn": "blue",
                                           "Đã đăng": "green"})},
            "Mã đơn": {"rich_text": {}},
            "Ghi chú": {"rich_text": {}},
        }})
    decisions = api("POST", "databases", {
        "parent": parent, "is_inline": True, "icon": {"type": "emoji", "emoji": "❓"},
        "title": txt("Việc chờ PM quyết"),
        "properties": {
            "Việc": {"title": {}},
            "Nhóm": {"select": opts(["Lịch", "Kênh Du học", "Kênh Tiếng Hàn", "Đăng bài", "Đo lường", "Công cụ"])},
            "Chặn lịch tháng 12": {"checkbox": {}},
            "Trạng thái": {"select": opts(["Chờ PM", "Đã trả lời", "Đã đưa vào brand.md"],
                                          {"Chờ PM": "yellow", "Đã trả lời": "blue", "Đã đưa vào brand.md": "green"})},
            "Câu trả lời của PM": {"rich_text": {}},
        }})
    st.update(orders_db=orders["id"], calendar_db=calendar["id"], decisions_db=decisions["id"], synced={})
    save_state(st)
    print("Đã dựng 3 bảng: Đơn video, Lịch nội dung, Việc chờ PM quyết.")
    return st


# ---------- Dữ liệu ban đầu ----------
DECISIONS = [
    ("Kỳ nhập học Du học đang tuyển và hạn nộp hồ sơ từng kỳ", "Lịch", True),
    ("Lịch thi TOPIK 2027 và lịch thi thử của trung tâm", "Lịch", True),
    ("Số video mỗi tuần cho từng kênh", "Lịch", True),
    ("Tên người dạy kịch bản cho mỗi kênh và ngày dạy", "Lịch", True),
    ("Quyền Admin Business Portfolio để đăng lên 2 fanpage thật", "Đăng bài", True),
    ("Mức phí dịch vụ du học (gói 60 triệu?) và dòng lệch 500 nghìn / 1 triệu trong bảng chi phí", "Kênh Du học", False),
    ("Xác nhận số liệu 3 trường Catholic, Pyeongtaek, Woosong còn hiệu lực", "Kênh Du học", False),
    ("Số buổi học chính thức (bảng giá, banner, video đang lệch nhau)", "Kênh Tiếng Hàn", False),
    ("Phòng tư vấn có ghi được khách đến từ video nào không", "Đo lường", False),
]
IDEAS = [
    ("Học bổng Pyeongtaek kỳ tháng 12/2026", "Du học Thầy Tư", "T giới thiệu trường", "Câu chuyện sản phẩm"),
    ("Trượt visa có mất tiền hồ sơ không?", "Du học Thầy Tư", "C chi phí minh bạch", "Điểm khác biệt"),
    ("2k9 cần chuẩn bị gì để kịp đi du học", "Du học Thầy Tư", "H hỏi đáp", "Điểm đau"),
    ("Catholic: TOPIK 3 đã có học bổng 70%", "Du học Thầy Tư", "T giới thiệu trường", "Câu chuyện sản phẩm"),
    ("Woosong: học bằng tiếng Hàn hay tiếng Anh?", "Du học Thầy Tư", "T giới thiệu trường", "Câu chuyện sản phẩm"),
    ("Mẹo Nghe TOPIK II: vì sao nghe được mà vẫn chọn sai", "Tiếng Hàn Thầy Tư", "A series chuyên môn", "Điểm đau"),
    ("Viết câu 54 TOPIK II: viết đúng trước, viết hay sau", "Tiếng Hàn Thầy Tư", "A series chuyên môn", "Điểm đau"),
    ("Học 1 từ biết thêm 5 từ (gốc Hán Hàn)", "Tiếng Hàn Thầy Tư", "A series chuyên môn", "Điểm khác biệt"),
    ("Chinh phục TOPIK 4 từ số 0 (cam kết TOPIK 3+ theo điều khoản)", "Tiếng Hàn Thầy Tư", "B bán khóa", "Câu chuyện sản phẩm"),
]


def seed():
    st = load_state()
    if st.get("seeded"):
        print("Đã đổ dữ liệu ban đầu từ trước, bỏ qua.")
        return
    for title, group, blocking in DECISIONS:
        api("POST", "pages", {"parent": {"database_id": st["decisions_db"]}, "properties": {
            "Việc": {"title": txt(title)}, "Nhóm": {"select": {"name": group}},
            "Chặn lịch tháng 12": {"checkbox": blocking}, "Trạng thái": {"select": {"name": "Chờ PM"}}}})
    for title, channel, fmt, axis in IDEAS:
        api("POST", "pages", {"parent": {"database_id": st["calendar_db"]}, "properties": {
            "Chủ đề": {"title": txt(title)}, "Kênh": {"select": {"name": channel}},
            "Dạng": {"select": {"name": fmt}}, "Trục": {"select": {"name": axis}},
            "Trạng thái": {"select": {"name": "Ý tưởng"}},
            "Ghi chú": {"rich_text": txt("Ý tưởng tháng 12/2026 do Claude đề xuất; PM điền ngày đăng và chốt.")}}})
    st["seeded"] = True
    save_state(st)
    print(f"Đã thêm {len(DECISIONS)} việc chờ PM quyết và {len(IDEAS)} ý tưởng lịch tháng 12.")


# ---------- Đồng bộ đơn ----------
def _date(s):
    return {"date": {"start": s.replace(" ", "T") + ":00+07:00"}} if s else {"date": None}


def order_props(code, o):
    s = o.get("script") or {}
    status = o.get("status") or ""
    approve_s = f"{o.get('script_approved_by', '')} {o.get('script_approved_at', '')}".strip()
    approve_v = f"{o.get('video_approved_by', '')} {o.get('video_approved_at', '')}".strip()
    return {
        "Chủ đề": {"title": txt(o.get("topic", code))},
        "Mã đơn": {"rich_text": txt(code)},
        "Kênh": {"select": {"name": o.get("channel") or "Tiếng Hàn Thầy Tư"}},
        "Trạng thái": {"select": {"name": status[:100]} if status else None},
        "Tiêu đề kịch bản": {"rich_text": txt(s.get("title"))},
        "Dạng": {"rich_text": txt(s.get("format"))},
        "Thời lượng (giây)": {"number": o.get("video_s") or s.get("duration_s")},
        "Bản kịch bản": {"number": o.get("script_version")},
        "Người đặt": {"rich_text": txt(o.get("by"))},
        "Ngày đặt": _date(o.get("at")),
        "Duyệt kịch bản": {"rich_text": txt(approve_s)},
        "Duyệt video": {"rich_text": txt(approve_v)},
        "Góp ý gần nhất": {"rich_text": txt(o.get("feedback"))},
        "Link Facebook": {"url": o.get("fb_link") or None},
        "Lịch đăng": _date(o.get("scheduled_for")),
        "Lỗi": {"rich_text": txt(o.get("error") if status.startswith("Lỗi") else "")},
    }


def sync_orders(verbose=False):
    """Đẩy các đơn có thay đổi lên Notion. Trả về số đơn đã gửi."""
    st = load_state()
    if not TOKEN or not st.get("orders_db") or not os.path.exists(ORDERS):
        return 0
    orders = json.load(open(ORDERS, encoding="utf-8"))
    synced = st.setdefault("synced", {})
    sent = 0
    for code, o in orders.items():
        props = order_props(code, o)
        digest = hashlib.sha1(json.dumps(props, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
        rec = synced.get(code, {})
        if rec.get("hash") == digest:
            continue
        if rec.get("page"):
            api("PATCH", f"pages/{rec['page']}", {"properties": props})
        else:
            page = api("POST", "pages", {"parent": {"database_id": st["orders_db"]}, "properties": props})
            rec["page"] = page["id"]
        rec["hash"] = digest
        synced[code] = rec
        save_state(st)
        sent += 1
        if verbose:
            print("Đã đồng bộ", code, "-", o.get("status"))
    return sent


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "check":
        print("Có NOTION_TOKEN:", bool(TOKEN))
        p = api("GET", f"pages/{ROOT_PAGE}")
        print("Vào được trang gốc:", p.get("object") == "page")
    elif cmd == "setup":
        setup()
    elif cmd == "seed":
        seed()
    elif cmd == "sync":
        print("Số đơn đã gửi:", sync_orders(verbose=True))
    else:
        sys.exit(__doc__)
