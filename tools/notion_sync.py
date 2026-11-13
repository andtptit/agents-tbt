"""Đồng bộ Nhà máy nội dung sang Notion (chỉ để XEM và theo dõi; duyệt vẫn trên Telegram).

  python tools/notion_sync.py check          kiểm tra token + quyền vào trang gốc
  python tools/notion_sync.py setup          tạo 3 bảng trong trang gốc (chạy 1 lần), ghi id vào data/notion.json
  python tools/notion_sync.py seed           đổ sẵn "Việc chờ PM quyết" + ý tưởng lịch tháng 12 (chạy 1 lần)
  python tools/notion_sync.py sync           đẩy đơn trong data/orders.json lên bảng "Đơn video"
  python tools/notion_sync.py setup-th       tạo trang con "Tiếng Hàn Thầy Tư" (3 bảng riêng cho PM Tiếng Hàn)
  python tools/notion_sync.py setup-dh       tạo trang con "Du học Thầy Tư" (3 bảng riêng cho PM Du học),
                                             chuyển ý tưởng + việc chờ quyết của Du học từ bảng chung sang

Mỗi kênh một trang riêng để chia sẻ cho PM của kênh đó (mời PM dạng khách vào ĐÚNG trang con của kênh).
Đơn mã DH-… đồng bộ vào bảng của trang Du học; đơn khác vào bảng ở trang gốc (sẽ tách trang Tiếng Hàn sau).

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


def orders_db_for(st, code):
    """Bảng Đơn video đúng kênh: DH-… → trang Du học, TH-… → trang Tiếng Hàn (mỗi kênh một trang riêng)."""
    if code.startswith("DH-") and st.get("DH", {}).get("orders_db"):
        return st["DH"]["orders_db"]
    if code.startswith("TH-") and st.get("TH", {}).get("orders_db"):
        return st["TH"]["orders_db"]
    return st.get("orders_db")


def sync_orders(verbose=False):
    """Đẩy các đơn có thay đổi lên Notion. Trả về số đơn đã gửi."""
    st = load_state()
    if not TOKEN or not os.path.exists(ORDERS):
        return 0
    orders = json.load(open(ORDERS, encoding="utf-8"))
    synced = st.setdefault("synced", {})
    sent = 0
    for code, o in orders.items():
        db = orders_db_for(st, code)
        if not db:  # kênh chưa có bảng trên Notion (Tiếng Hàn: tạm ẩn từ 13/11/2026) → bỏ qua
            continue
        props = order_props(code, o)
        digest = hashlib.sha1(json.dumps([db, props], sort_keys=True, ensure_ascii=False).encode()).hexdigest()
        rec = synced.get(code, {})
        if rec.get("hash") == digest:
            continue
        if rec.get("page") and rec.get("db", db) != db:  # đơn nằm nhầm bảng → bỏ vào thùng rác, tạo lại đúng bảng
            api("PATCH", f"pages/{rec['page']}", {"archived": True})
            rec = {}
        if rec.get("page"):
            api("PATCH", f"pages/{rec['page']}", {"properties": props})
        else:
            page = api("POST", "pages", {"parent": {"database_id": db}, "properties": props})
            rec["page"] = page["id"]
        rec["db"] = db
        rec["hash"] = digest
        synced[code] = rec
        save_state(st)
        sent += 1
        if verbose:
            print("Đã đồng bộ", code, "-", o.get("status"))
    return sent


# ---------- Trang riêng kênh Du học ----------
DH_DECISIONS = [
    ("Kỳ nhập học đang tuyển (tháng 3/6/9/12?) và hạn nộp hồ sơ từng kỳ", "Lịch", True),
    ("Số video mỗi tuần cho kênh Du học", "Lịch", True),
    ("Người dạy kịch bản Du học (bộ phận Du học) và ngày dạy", "Lịch", True),
    ("Quyền đăng lên fanpage Du học Thầy Tư thật (Admin Business Portfolio)", "Đăng bài", True),
    ("Mức phí dịch vụ du học (gói 60 triệu?) — hiện cấm nêu trong video", "Chi phí", False),
    ("Bảng chi phí: dòng 'gửi hồ sơ' và 'ký túc xá' ghi đảo 500 nghìn / 1 triệu giữa PDF và ảnh", "Chi phí", False),
    ("Số liệu Catholic, Pyeongtaek, Woosong còn hiệu lực không; bổ sung trường khác", "Trường", False),
    ("Điều kiện câu 'Có TOPIK 3 – Có ngay VISA' (hiện cấm dùng)", "Chi phí", False),
    ("Danh sách trường đối tác chính thức được nêu tên", "Trường", False),
    ("Học viên du học nào đồng ý xuất hiện trong video", "Chất liệu", False),
    ("Video/banner cũ của kênh Du học để phân tích phong cách", "Chất liệu", False),
    ("Phòng tư vấn có ghi được khách đến từ video nào không", "Đo lường", False),
]
DH_FORMATS = ["T giới thiệu trường", "S hậu trường", "C chi phí minh bạch", "H hỏi đáp"]


def _query_all(db):
    out, cursor = [], None
    while True:
        body = {"page_size": 100} | ({"start_cursor": cursor} if cursor else {})
        r = api("POST", f"databases/{db}/query", body)
        out += r["results"]
        if not r.get("has_more"):
            return out
        cursor = r["next_cursor"]


def setup_dh():
    st = load_state()
    dh = st.setdefault("DH", {})
    if not dh.get("page"):
        page = api("POST", "pages", {
            "parent": {"type": "page_id", "page_id": ROOT_PAGE}, "icon": {"type": "emoji", "emoji": "🎓"},
            "properties": {"title": {"title": txt("Du học Thầy Tư")}},
            "children": [{"object": "block", "type": "callout", "callout": {
                "icon": {"type": "emoji", "emoji": "📌"}, "color": "red_background",
                "rich_text": txt("Trang riêng của kênh Du học Thầy Tư (PC01), dành cho PM Du học. Chỉ để XEM và theo dõi: "
                                 "duyệt kịch bản/video vẫn bấm trên Telegram. Bảng \"Đơn video Du học\" do bot tự cập nhật "
                                 "mỗi phút, đừng sửa tay. \"Lịch nội dung\" và \"Việc chờ PM quyết\" thì PM sửa thoải mái. "
                                 "Đặt video Du học trên Telegram: /tao dh <chủ đề>.")}}]})
        dh["page"] = page["id"]
        save_state(st)
    parent = {"type": "page_id", "page_id": dh["page"]}
    status_colors = {s: ("red" if s.startswith("Lỗi") else "yellow" if s.startswith(("Chờ duyệt", "Trả về"))
                         else "green" if s in ("Đã đăng", "Đã duyệt video", "Đã lên lịch") else "blue")
                     for s in STATUSES}
    if not dh.get("orders_db"):
        dh["orders_db"] = api("POST", "databases", {
            "parent": parent, "is_inline": True, "icon": {"type": "emoji", "emoji": "🎬"},
            "title": txt("Đơn video Du học"),
            "properties": {
                "Chủ đề": {"title": {}}, "Mã đơn": {"rich_text": {}},
                "Kênh": {"select": opts(["Du học Thầy Tư"], {"Du học Thầy Tư": "red"})},
                "Trạng thái": {"select": opts(STATUSES, status_colors)},
                "Tiêu đề kịch bản": {"rich_text": {}}, "Dạng": {"rich_text": {}},
                "Thời lượng (giây)": {"number": {}}, "Bản kịch bản": {"number": {}},
                "Người đặt": {"rich_text": {}}, "Ngày đặt": {"date": {}},
                "Duyệt kịch bản": {"rich_text": {}}, "Duyệt video": {"rich_text": {}},
                "Góp ý gần nhất": {"rich_text": {}}, "Link Facebook": {"url": {}},
                "Lịch đăng": {"date": {}}, "Lỗi": {"rich_text": {}}}})["id"]
        save_state(st)
    if not dh.get("calendar_db"):
        dh["calendar_db"] = api("POST", "databases", {
            "parent": parent, "is_inline": True, "icon": {"type": "emoji", "emoji": "🗓️"},
            "title": txt("Lịch nội dung Du học"),
            "properties": {
                "Chủ đề": {"title": {}}, "Ngày đăng": {"date": {}},
                "Dạng": {"select": opts(DH_FORMATS)},
                "Trục": {"select": opts(["Điểm đau", "Câu chuyện sản phẩm", "Điểm khác biệt"])},
                "Người xem chính": {"select": opts(["Học sinh", "Phụ huynh", "Sinh viên và người đi làm"])},
                "Trạng thái": {"select": opts(["Ý tưởng", "PM đã chốt", "Đã đặt đơn", "Đã đăng"],
                                              {"Ý tưởng": "gray", "PM đã chốt": "yellow", "Đã đặt đơn": "blue",
                                               "Đã đăng": "green"})},
                "Mã đơn": {"rich_text": {}}, "Ghi chú": {"rich_text": {}}}})["id"]
        save_state(st)
    if not dh.get("decisions_db"):
        dh["decisions_db"] = api("POST", "databases", {
            "parent": parent, "is_inline": True, "icon": {"type": "emoji", "emoji": "❓"},
            "title": txt("Việc chờ PM Du học quyết"),
            "properties": {
                "Việc": {"title": {}},
                "Nhóm": {"select": opts(["Lịch", "Chi phí", "Trường", "Chất liệu", "Đăng bài", "Đo lường"])},
                "Chặn lịch tháng 12": {"checkbox": {}},
                "Trạng thái": {"select": opts(["Chờ PM", "Đã trả lời", "Đã đưa vào brand.md"],
                                              {"Chờ PM": "yellow", "Đã trả lời": "blue", "Đã đưa vào brand.md": "green"})},
                "Câu trả lời của PM": {"rich_text": {}}}})["id"]
        save_state(st)

    if not dh.get("seeded"):
        for title, group, blocking in DH_DECISIONS:
            api("POST", "pages", {"parent": {"database_id": dh["decisions_db"]}, "properties": {
                "Việc": {"title": txt(title)}, "Nhóm": {"select": {"name": group}},
                "Chặn lịch tháng 12": {"checkbox": blocking}, "Trạng thái": {"select": {"name": "Chờ PM"}}}})
        audience = {"C chi phí minh bạch": "Phụ huynh"}
        moved = 0
        # Ý tưởng Du học ở bảng chung → chép sang lịch Du học, rồi bỏ khỏi bảng chung (vào thùng rác Notion).
        for p in _query_all(st["calendar_db"]):
            pr = p["properties"]
            if (pr["Kênh"]["select"] or {}).get("name") != "Du học Thầy Tư":
                continue
            fmt = (pr["Dạng"]["select"] or {}).get("name")
            api("POST", "pages", {"parent": {"database_id": dh["calendar_db"]}, "properties": {
                "Chủ đề": {"title": txt("".join(t["plain_text"] for t in pr["Chủ đề"]["title"]))},
                "Ngày đăng": {"date": pr["Ngày đăng"]["date"]},
                "Dạng": {"select": {"name": fmt} if fmt else None},
                "Trục": {"select": pr["Trục"]["select"] and {"name": pr["Trục"]["select"]["name"]}},
                "Người xem chính": {"select": {"name": audience.get(fmt, "Học sinh")}},
                "Trạng thái": {"select": pr["Trạng thái"]["select"] and {"name": pr["Trạng thái"]["select"]["name"]}},
                "Ghi chú": {"rich_text": txt("".join(t["plain_text"] for t in pr["Ghi chú"]["rich_text"]))}}})
            api("PATCH", f"pages/{p['id']}", {"archived": True})
            moved += 1
        # Việc chờ quyết của Du học ở bảng chung đã có bản đầy đủ hơn ở trang Du học → bỏ khỏi bảng chung.
        dh_words = ("du học", "Du học", "Kỳ nhập học", "3 trường")
        removed = 0
        for p in _query_all(st["decisions_db"]):
            title = "".join(t["plain_text"] for t in p["properties"]["Việc"]["title"])
            if (p["properties"]["Nhóm"]["select"] or {}).get("name") == "Kênh Du học" or any(w in title for w in dh_words):
                api("PATCH", f"pages/{p['id']}", {"archived": True})
                removed += 1
        dh["seeded"] = True
        save_state(st)
        print(f"Trang Du học: {len(DH_DECISIONS)} việc chờ quyết; chuyển {moved} ý tưởng; "
              f"bỏ {removed} việc Du học khỏi bảng chung.")
    # Đơn DH-… đã đồng bộ vào bảng chung sẽ được sync_orders chuyển sang bảng Du học.
    print("Đã có trang Du học Thầy Tư với 3 bảng riêng.")
    return dh


# ---------- Trang riêng kênh Tiếng Hàn (khóa học) — tách hoàn toàn với Du học ----------
TH_DECISIONS = [
    ("Ưu đãi đang chạy trên page ('giảm tới 10%', 'giảm sâu 60%', voucher -10% sách): còn hiệu lực không, điều kiện, "
     "thời hạn? (brand.md đang ghi không có khuyến mãi → hiện cấm viết)", "Giá và ưu đãi", True),
    ("Số video mỗi tuần cho kênh Tiếng Hàn", "Lịch", True),
    ("Người dạy kịch bản Tiếng Hàn và ngày dạy", "Lịch", True),
    ("Lịch thi TOPIK 2027 và lịch thi thử của trung tâm", "Lịch", True),
    ("Quyền đăng lên fanpage Tiếng Hàn Thầy Tư thật", "Đăng bài", True),
    ("Số buổi học chính thức (bảng giá 40 buổi, banner 89/43, video 28/27 đang lệch)", "Giá và ưu đãi", False),
    ("Điều kiện và quyền lợi cam kết TOPIK 3+ (học lại hay hoàn phí), danh sách khóa áp dụng", "Giá và ưu đãi", False),
    ("Giá khóa Giao tiếp nâng cao, Từ vựng, EPS (có trên web, chưa có trong bảng giá)", "Giá và ưu đãi", False),
    ("Giáo viên trong livestream (Cô Thúy, Cô My) có đồng ý cắt clip đăng lại không", "Chất liệu", False),
    ("Bài nào trong top lượt xem đã chạy quảng cáo", "Đo lường", False),
    ("Học viên nào đồng ý xuất hiện trong video (kết quả, cảm nhận)", "Chất liệu", False),
]
TH_FORMATS = ["A series chuyên môn", "B bán khóa", "Lưu về (từ vựng và mẫu câu)", "Clip ngắn bắt trend"]
TH_IDEAS = [
    ("Học chăm, làm nhiều đề mà điểm TOPIK không nhúc nhích? (không phải A mà là B)", "A series chuyên môn", "Điểm đau", "Người ôn TOPIK II"),
    ("Series mẹo theo dạng câu: Đọc TOPIK II câu 5–8 — mất điểm oan ở đâu", "A series chuyên môn", "Điểm đau", "Người ôn TOPIK II"),
    ("Viết câu 54: viết đúng trước, viết hay sau", "A series chuyên môn", "Điểm đau", "Người ôn TOPIK II"),
    ("Lưu về: 10 từ Hán Hàn gốc 학 (học 1 từ biết thêm 5 từ)", "Lưu về (từ vựng và mẫu câu)", "Điểm khác biệt", "Người mới học"),
    ("Học xong sơ cấp mà vẫn 'đứng hình' khi làm đề TOPIK I", "A series chuyên môn", "Điểm đau", "Người mới học"),
    ("Chinh phục TOPIK 4 từ số 0 (cam kết TOPIK 3+ theo điều khoản)", "B bán khóa", "Câu chuyện sản phẩm", "Người mới học"),
]


def setup_th():
    st = load_state()
    th = st.setdefault("TH", {})
    if not th.get("page"):
        th["page"] = api("POST", "pages", {
            "parent": {"type": "page_id", "page_id": ROOT_PAGE}, "icon": {"type": "emoji", "emoji": "📘"},
            "properties": {"title": {"title": txt("Tiếng Hàn Thầy Tư")}},
            "children": [{"object": "block", "type": "callout", "callout": {
                "icon": {"type": "emoji", "emoji": "📌"}, "color": "blue_background",
                "rich_text": txt("Trang riêng của kênh Tiếng Hàn Thầy Tư (PC02 – khóa học), dành cho PM Tiếng Hàn. Tách riêng "
                                 "hoàn toàn với kênh Du học. Chỉ để XEM và theo dõi: duyệt kịch bản/video vẫn bấm trên "
                                 "Telegram. Bảng \"Đơn video Tiếng Hàn\" do bot tự cập nhật mỗi phút, đừng sửa tay. "
                                 "\"Lịch nội dung\" và \"Việc chờ PM quyết\" thì PM sửa thoải mái. Đặt video trên "
                                 "Telegram: /tao <chủ đề>.")}}]})["id"]
        save_state(st)
    parent = {"type": "page_id", "page_id": th["page"]}
    status_colors = {s: ("red" if s.startswith("Lỗi") else "yellow" if s.startswith(("Chờ duyệt", "Trả về"))
                         else "green" if s in ("Đã đăng", "Đã duyệt video", "Đã lên lịch") else "blue")
                     for s in STATUSES}
    if not th.get("orders_db"):
        th["orders_db"] = api("POST", "databases", {
            "parent": parent, "is_inline": True, "icon": {"type": "emoji", "emoji": "🎬"},
            "title": txt("Đơn video Tiếng Hàn"),
            "properties": {
                "Chủ đề": {"title": {}}, "Mã đơn": {"rich_text": {}},
                "Kênh": {"select": opts(["Tiếng Hàn Thầy Tư"], {"Tiếng Hàn Thầy Tư": "blue"})},
                "Trạng thái": {"select": opts(STATUSES, status_colors)},
                "Tiêu đề kịch bản": {"rich_text": {}}, "Dạng": {"rich_text": {}},
                "Thời lượng (giây)": {"number": {}}, "Bản kịch bản": {"number": {}},
                "Người đặt": {"rich_text": {}}, "Ngày đặt": {"date": {}},
                "Duyệt kịch bản": {"rich_text": {}}, "Duyệt video": {"rich_text": {}},
                "Góp ý gần nhất": {"rich_text": {}}, "Link Facebook": {"url": {}},
                "Lịch đăng": {"date": {}}, "Lỗi": {"rich_text": {}}}})["id"]
        save_state(st)
    if not th.get("calendar_db"):
        th["calendar_db"] = api("POST", "databases", {
            "parent": parent, "is_inline": True, "icon": {"type": "emoji", "emoji": "🗓️"},
            "title": txt("Lịch nội dung Tiếng Hàn"),
            "properties": {
                "Chủ đề": {"title": {}}, "Ngày đăng": {"date": {}},
                "Dạng": {"select": opts(TH_FORMATS)},
                "Trục": {"select": opts(["Điểm đau", "Câu chuyện sản phẩm", "Điểm khác biệt"])},
                "Người xem chính": {"select": opts(["Người mới học", "Người ôn TOPIK II", "Người chuẩn bị du học",
                                                    "Lao động EPS"])},
                "Khóa liên quan (mã bảng giá)": {"rich_text": {}},
                "Trạng thái": {"select": opts(["Ý tưởng", "PM đã chốt", "Đã đặt đơn", "Đã đăng"],
                                              {"Ý tưởng": "gray", "PM đã chốt": "yellow", "Đã đặt đơn": "blue",
                                               "Đã đăng": "green"})},
                "Mã đơn": {"rich_text": {}}, "Ghi chú": {"rich_text": {}}}})["id"]
        save_state(st)
    if not th.get("decisions_db"):
        th["decisions_db"] = api("POST", "databases", {
            "parent": parent, "is_inline": True, "icon": {"type": "emoji", "emoji": "❓"},
            "title": txt("Việc chờ PM Tiếng Hàn quyết"),
            "properties": {
                "Việc": {"title": {}},
                "Nhóm": {"select": opts(["Lịch", "Giá và ưu đãi", "Chất liệu", "Đăng bài", "Đo lường"])},
                "Chặn lịch tháng 12": {"checkbox": {}},
                "Trạng thái": {"select": opts(["Chờ PM", "Đã trả lời", "Đã đưa vào brand.md"],
                                              {"Chờ PM": "yellow", "Đã trả lời": "blue", "Đã đưa vào brand.md": "green"})},
                "Câu trả lời của PM": {"rich_text": {}}}})["id"]
        save_state(st)
    if not th.get("seeded"):
        for title, group, blocking in TH_DECISIONS:
            api("POST", "pages", {"parent": {"database_id": th["decisions_db"]}, "properties": {
                "Việc": {"title": txt(title)}, "Nhóm": {"select": {"name": group}},
                "Chặn lịch tháng 12": {"checkbox": blocking}, "Trạng thái": {"select": {"name": "Chờ PM"}}}})
        for title, fmt, axis, aud in TH_IDEAS:
            api("POST", "pages", {"parent": {"database_id": th["calendar_db"]}, "properties": {
                "Chủ đề": {"title": txt(title)}, "Dạng": {"select": {"name": fmt}}, "Trục": {"select": {"name": axis}},
                "Người xem chính": {"select": {"name": aud}}, "Trạng thái": {"select": {"name": "Ý tưởng"}},
                "Ghi chú": {"rich_text": txt("Ý tưởng từ phân tích fanpage 13/11/2026; PM điền ngày đăng và chốt.")}}})
        th["seeded"] = True
        save_state(st)
        print(f"Trang Tiếng Hàn: {len(TH_DECISIONS)} việc chờ quyết, {len(TH_IDEAS)} ý tưởng.")
    print("Đã có trang Tiếng Hàn Thầy Tư với 3 bảng riêng.")
    return th


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
    elif cmd == "setup-th":
        setup_th()
        print("Số đơn đã gửi:", sync_orders(verbose=True))
    elif cmd == "setup-dh":
        setup_dh()
        print("Số đơn đã gửi:", sync_orders(verbose=True))
    elif cmd == "sync":
        print("Số đơn đã gửi:", sync_orders(verbose=True))
    else:
        sys.exit(__doc__)
