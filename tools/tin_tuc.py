"""Agent Bản tin du học Hàn Quốc: gom tin mới → kịch bản bản tin có dẫn nguồn → (bot) An duyệt → dựng video.

  python tools/tin_tuc.py gom              # tìm tin mới (Claude chạy ngầm, có WebSearch/WebFetch) → data/tin_tuc/<ngày>.json
  python tools/tin_tuc.py kichban [ngày]   # từ file tin trong ngày → kịch bản JSON (in ra)
  python tools/tin_tuc.py thu              # gom + viết kịch bản + chấm, không gửi Telegram

Nguyên tắc (An chốt 18/11/2026):
- Chỉ tin có nguồn uy tín, Claude phải MỞ được trang gốc và đọc ngày đăng; không có ngày / không mở được → bỏ.
- Ưu tiên nguồn chính thức (Bộ Tư pháp/Cục Xuất nhập cảnh, HiKorea, Study in Korea/NIIED, Bộ Giáo dục Hàn,
  Đại sứ quán Hàn tại VN, trang tuyển sinh trường), rồi báo lớn (Yonhap, Korea Herald, Korea JoongAng Daily,
  Korea Times, VnExpress, Tuổi Trẻ, Thanh Niên, VietnamPlus).
- Viết lại bằng lời mình, không chép nguyên văn; mỗi tin hiện tên nguồn + ngày trên hình; link đủ trong caption.
- Tin đã đưa (theo link) ghi vào data/tin_tuc/da_dung.json để không lặp.
"""
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from script_writer import ROOT, find_claude  # noqa: E402

DIR = os.path.join(ROOT, "data", "tin_tuc")
USED = os.path.join(DIR, "da_dung.json")
DAYS = 7          # chỉ lấy tin đăng trong 7 ngày gần nhất
MAX_ITEMS = 3     # mỗi bản tin 2–3 tin

SOURCES = """Nguồn chính thức (ưu tiên): immigration.go.kr / moj.go.kr (Bộ Tư pháp, Cục Xuất nhập cảnh Hàn Quốc), hikorea.go.kr,
studyinkorea.go.kr và niied.go.kr (Study in Korea, học bổng GKS), moe.go.kr (Bộ Giáo dục Hàn), overseas.mofa.go.kr/vn-vi
(Đại sứ quán Hàn tại Việt Nam), topik.go.kr, trang tuyển sinh quốc tế của các trường đại học Hàn.
Báo lớn: yna.co.kr / en.yna.co.kr (Yonhap), koreaherald.com, koreajoongangdaily.joins.com, koreatimes.co.kr,
vnexpress.net, tuoitre.vn, thanhnien.vn, vietnamplus.vn, dantri.com.vn (mục giáo dục/du học)."""

TOPICS = """visa du học D-2/D-4 (thủ tục, điều kiện, thay đổi chính sách), quy định làm thêm của du học sinh, visa sau tốt nghiệp
(D-10, E-7, visa vùng/khu vực), học bổng (GKS và học bổng trường), kỳ thi TOPIK (lịch thi, thay đổi), chính sách thu hút
du học sinh quốc tế của Hàn Quốc (Study Korea 300K…), tuyển sinh kỳ mới của các trường, số liệu chính thức về du học sinh
Việt Nam tại Hàn, cảnh báo lừa đảo/du học chui/bất hợp pháp liên quan du học sinh."""


def used_urls():
    return set(json.load(open(USED, encoding="utf-8"))) if os.path.exists(USED) else set()


def mark_used(urls):
    os.makedirs(DIR, exist_ok=True)
    u = sorted(used_urls() | set(urls))
    json.dump(u, open(USED, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def _claude(prompt, tools, timeout=900):
    proc = subprocess.run([find_claude(), "-p", prompt, "--output-format", "json", "--allowedTools", tools],
                          capture_output=True, text=True, encoding="utf-8", timeout=timeout, cwd=ROOT)
    try:
        out = json.loads(proc.stdout)
    except json.JSONDecodeError:
        raise RuntimeError(f"Claude không trả về kết quả: {proc.stderr[-300:] or proc.stdout[-300:]}")
    if out.get("is_error"):
        raise RuntimeError(f"Claude báo lỗi: {out.get('result')}")
    m = re.search(r"\{.*\}", out.get("result", ""), re.S)
    if not m:
        raise RuntimeError("Claude không trả về JSON")
    return json.loads(m.group(0))


def gather(day=None):
    """Tìm tin mới, trả dict {date, items:[...], skipped:[...]} và lưu data/tin_tuc/<ngày>.json."""
    day = day or datetime.now().strftime("%Y-%m-%d")
    since = (datetime.strptime(day, "%Y-%m-%d") - timedelta(days=DAYS)).strftime("%d/%m/%Y")
    seen = sorted(used_urls())[-80:]
    prompt = f"""Bạn là Agent Bản tin của kênh Du học Thầy Tư (tư vấn du học Hàn Quốc cho học sinh, phụ huynh Việt Nam).
Hôm nay {datetime.strptime(day, '%Y-%m-%d'):%d/%m/%Y}. Tìm tin MỚI (đăng từ {since} đến nay) về du học Hàn Quốc.

Chủ đề cần: {TOPICS}

{SOURCES}

Cách làm:
1. Dùng WebSearch nhiều lần (tiếng Việt, tiếng Anh và tiếng Hàn, ví dụ "유학생 비자", "외국인 유학생 정책", "du học Hàn Quốc visa").
2. Với mỗi tin định chọn, BẮT BUỘC dùng WebFetch mở trang gốc, đọc nội dung và ngày đăng. Không mở được hoặc không thấy ngày → bỏ.
3. Chỉ giữ tin có ích thật cho người Việt muốn du học Hàn. Bỏ tin quảng cáo của trung tâm du học khác, tin đồn, tin cũ đăng lại.
4. Bỏ các link đã dùng: {json.dumps(seen, ensure_ascii=False)}
5. Không bịa. Mọi con số, ngày, điều kiện phải đúng như trang gốc. Chỗ nào trang gốc nói chưa rõ thì ghi "chưa rõ".
6. Chọn tối đa {MAX_ITEMS + 2} tin tốt nhất, xếp quan trọng trước. Không có tin đạt thì trả items rỗng.

Chỉ trả về MỘT khối JSON, không thêm chữ:
{{"items": [{{"title_vi": "tiêu đề ngắn tiếng Việt", "publisher": "tên nguồn ngắn, ví dụ Yonhap / Bộ Tư pháp Hàn Quốc",
  "url": "link trang gốc", "published": "YYYY-MM-DD", "official": true,
  "facts": ["2–4 ý chính, đúng như nguồn, viết bằng lời mình"],
  "why": "vì sao người Việt muốn du học Hàn cần biết (1 câu)", "importance": 1-10}}],
 "skipped": [{{"url": "...", "reason": "vì sao bỏ"}}]}}"""
    data = _claude(prompt, "WebSearch,WebFetch", timeout=1200)
    data["date"] = day
    data["items"] = [i for i in data.get("items", []) if i.get("url") and i.get("published")
                     and i["url"] not in used_urls()]
    os.makedirs(DIR, exist_ok=True)
    json.dump(data, open(os.path.join(DIR, f"{day}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return data


SCRIPT_SCHEMA = """{
  "title": "Bản tin du học Hàn <ngày dd/mm>",
  "format": "N (bản tin du học)",
  "template": "BT (bản tin)",
  "duration_s": 60,
  "axis": "điểm đau",
  "course_code": null,
  "lines": [
    {"id": "l01", "part": "hook", "text": "lời đọc cho Vbee"},
    {"id": "l02", "part": "t1", "text": "..."},
    {"id": "l09", "part": "cta", "text": "..."}
  ],
  "news": [
    {"part": "t1", "kicker": "VISA", "headline": "tiêu đề trên màn hình, ≤ 32 ký tự", "points": ["ý ngắn ≤ 38 ký tự", "..."],
     "publisher": "Yonhap", "published": "YYYY-MM-DD", "url": "..."}
  ],
  "hook_screen": "BẢN TIN DU HỌC HÀN",
  "hook_sub": "1 dòng ≤ 30 ký tự gợi tò mò về tin chính, ví dụ: 268.000 du học sinh D-2",
  "scenes": [
    {"name": "Hook", "time": "0–4s", "voice": "...", "screen": "...", "visual": "..."}
  ],
  "caption_facebook": "tóm tắt + danh sách nguồn kèm link",
  "hashtags": ["#DuHocThayTu", "#DuHocHanQuoc", "#BanTinDuHoc"],
  "sources": ["Tên nguồn – ngày – link"],
  "check": ["tự kiểm"]
}"""


def write_script(news, feedback=None, previous=None):
    items = sorted(news["items"], key=lambda i: -int(i.get("importance", 0)))[:MAX_ITEMS]
    if not items:
        raise RuntimeError("Hôm nay không có tin mới đủ tin cậy")
    prompt = f"""Bạn là Agent Biên kịch kênh Du học Thầy Tư. Đọc CLAUDE.md, brand.md (mục 0.2 phát âm, mục 4 quy tắc),
huong-dan-kich-ban-du-hoc.md. Viết kịch bản video dọc "Bản tin du học Hàn" 45–75 giây từ các tin dưới đây (đã kiểm nguồn):
{json.dumps(items, ensure_ascii=False, indent=1)}

Cấu trúc: hook (1 câu, ≤ 20 âm tiết: tin đáng chú ý nhất + vì sao người muốn du học Hàn phải quan tâm, gợi tò mò)
→ mỗi tin 2–3 câu (part t1, t2, t3): câu 1 tin gì + theo nguồn nào; câu 2 chi tiết chính; câu CUỐI "điều này có nghĩa gì
với bạn" (dựa vào "why", không suy đoán quá nguồn) → 1 câu "Du học Thầy Tư cập nhật tin mới mỗi ngày" + CTA nhắn tin
để được tư vấn (part cta).
- Không nói kiểu ghi chú nội bộ ("bài viết chưa nêu…", "chưa rõ"); điều chưa có thì nói tự nhiên ("hiện chưa có chính
  sách mới được công bố") hoặc bỏ.
- Năm đọc gọn: "năm hai không hai bảy" (không "hai nghìn không trăm…"); có thể nói "năm sau" nếu đúng.
- Tên riêng Hàn ít người biết: nói chung ("một báo địa phương Hàn Quốc", "một số trường cao đẳng gần Xơ-un"),
  tên đầy đủ để trên màn hình và caption.
Bắt buộc:
- Chỉ nói đúng những gì có trong facts. Không thêm số, không suy đoán, không cam kết visa, không "chắc chắn đậu".
- Mỗi tin nói rõ nguồn bằng lời ("theo Yonhap", "theo Bộ Tư pháp Hàn Quốc").
- Không khuyến mãi; không nói giá dịch vụ của trung tâm. Số tiền trong lời đọc: không đọc (chỉ nói "xem chi tiết tại nguồn").
- Lời đọc viết cho Vbee: số viết bằng chữ, D-2 → "đê hai", D-4 → "đê bốn", TOPIK → "Tốp pích", E-7 → "e bảy", GKS → "gờ ca ét".
- Câu ngắn, mỗi câu ≤ 30 âm tiết. Xưng mình – bạn.
- news: mỗi tin 1 mục, kicker 1 từ in hoa (VISA / HỌC BỔNG / TOPIK / CHÍNH SÁCH / TUYỂN SINH / ĐỜI SỐNG / CẢNH BÁO), chọn đúng bản chất tin, points 2–3 ý.
- caption_facebook: 2–3 câu + "Nguồn:" và từng dòng "• Tên nguồn (dd/mm/yyyy): link".
"""
    if feedback:
        prompt += f"\nĐÂY LÀ BẢN VIẾT LẠI. Lý do trả về: «{feedback}». Bản trước: {json.dumps(previous, ensure_ascii=False)}\n"
    prompt += f"\nChỉ trả về MỘT khối JSON hợp lệ theo mẫu, không thêm chữ:\n{SCRIPT_SCHEMA}"
    s = _claude(prompt, "Read,Glob,Grep", timeout=600)
    # scenes (để chấm và hiển thị) dựng lại từ lines để chắc khớp lời đọc
    by_part = {}
    for l in s.get("lines", []):
        by_part.setdefault(l["part"], []).append(l["text"])
    names = {"hook": "Hook", "cta": "Kết + CTA"}
    news_by = {n["part"]: n for n in s.get("news", [])}
    s["scenes"] = [{"name": names.get(p, f"Tin {p[1:]}"), "time": "",
                    "voice": " ".join(t),
                    "screen": (s.get("hook_screen", "") + " / " + s.get("hook_sub", "") if p == "hook" else
                               f"{news_by[p]['kicker']} / {news_by[p]['headline']} / " + " · ".join(news_by[p]['points'])
                               + f" (Nguồn: {news_by[p]['publisher']}, {news_by[p]['published']})" if p in news_by else ""),
                    "visual": "footage TBT + thẻ tin"} for p, t in by_part.items()]
    s["duration_s"] = s.get("duration_s", 60)
    return s


def format_news(code, s):
    """Tin gửi An: kịch bản + danh sách nguồn có link để An bấm kiểm."""
    out = [f"📰 {code} — {s.get('title', '')} · 🎓 Du học Thầy Tư", ""]
    for l in s.get("lines", []):
        out.append(f"🎙 [{l['part']}] {l['text']}")
    out.append("")
    for n in s.get("news", []):
        out.append(f"🖥 {n['kicker']} · {n['headline']}")
        out += [f"   – {p}" for p in n.get("points", [])]
        out.append(f"   🔗 {n['publisher']} ({n['published']}): {n['url']}")
    out.append("")
    out.append(f"Caption FB: {s.get('caption_facebook', '')}")
    return "\n".join(out)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    a = sys.argv[1:]
    if a[:1] == ["gom"]:
        print(json.dumps(gather(), ensure_ascii=False, indent=1))
    elif a[:1] == ["kichban"]:
        day = a[1] if len(a) > 1 else datetime.now().strftime("%Y-%m-%d")
        news = json.load(open(os.path.join(DIR, f"{day}.json"), encoding="utf-8"))
        print(json.dumps(write_script(news), ensure_ascii=False, indent=1))
    elif a[:1] == ["thu"]:
        import script_judge
        news = gather()
        print(f"{len(news['items'])} tin")
        s = write_script(news)
        json.dump(s, open(os.path.join(DIR, f"{news['date']}-kichban.json"), "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
        print(format_news("DH-BT-THU", s))
        print(script_judge.format_result(script_judge.evaluate(s, "DH", "Bản tin du học Hàn"), 0))
    else:
        print(__doc__)
