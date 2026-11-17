"""Agent Banner: viết nội dung banner bằng Claude rồi ghép vào khuôn HTML và chụp thành ảnh PNG.

Chạy thử (chưa nối Telegram):
  python tools/banner_maker.py "Cần TOPIK mấy để du học Hàn?"          # Claude viết nội dung + dựng ảnh
  python tools/banner_maker.py --json banner/jobs/<mã>/banner.json     # chỉ dựng lại ảnh từ nội dung có sẵn
Kết quả: banner/jobs/<mã>/banner.json + banner.png (2160×2160). Không đưa lên Git.

Khuôn: banner/b1-the/index.html (Du học Thầy Tư). Cần Chrome hoặc Edge trên máy.
"""
import datetime
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from script_writer import CHANNELS, ROOT, find_claude  # noqa: E402

TEMPLATES = {"B1": "b1-the"}
BROWSERS = [r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"]

SCHEMA = """{
  "title": "TIÊU ĐỀ TO, tối đa 16 ký tự (ví dụ: CẦN TOPIK MẤY?)",
  "eyebrow": "dòng nhỏ trên tiêu đề, tối đa 34 ký tự",
  "label": "dòng nhấn trên dải đỏ, IN HOA, tối đa 30 ký tự",
  "items": [{"title": "ý chính, tối đa 28 ký tự", "desc": "giải thích ngắn, tối đa 42 ký tự, có thể bỏ trống"}],
  "numbered": true,
  "highlight_last": true,
  "note": "một câu chốt dưới các thẻ, tối đa 55 ký tự; bọc **chữ** để tô vàng; có thể bỏ trống",
  "small": "chữ nhỏ bắt buộc nếu có (điều khoản, 'theo thông tin trường công bố'…), không thì để trống",
  "cta": "Nhận tư vấn ngay | Nhắn tin nhận lộ trình | …, tối đa 20 ký tự",
  "caption_facebook": "caption đăng kèm ảnh",
  "hashtags": ["#DuHocThayTu", "#DuHocHanQuoc"],
  "sources": ["dữ liệu đã dùng: brand.md mục …"],
  "check": ["tự kiểm: không số tiền, không khuyến mãi, không cam kết visa, …"]
}"""


def write_banner(topic, channel="DH", feedback=None, previous=None, timeout=600):
    cli = find_claude()
    if not cli:
        raise RuntimeError("Không tìm thấy Claude Code trên máy")
    ch = CHANNELS[channel]
    prompt = f"""Bạn là Agent Banner của hệ thống nhà máy nội dung (xem CLAUDE.md).
Đọc kỹ: CLAUDE.md, brand.md, {ch['guide']}, phong-cach-du-hoc.md (mục 3 banner, mục 4 câu cấm).

Đơn đặt banner (ảnh vuông đăng Facebook):
- Kênh: {ch['name']}
- Chủ đề: {topic}

Yêu cầu:
- Viết nội dung cho MỘT banner khuôn B1 "Thẻ": tiêu đề to, dải đỏ, 2–6 thẻ ý (số thứ tự hoặc dấu tích), một câu chốt, nút CTA.
- Người xem lướt 2 giây: chữ ít, ý rõ, mỗi thẻ một ý. Không viết câu dài.
- Tuân thủ tuyệt đối brand.md mục 4 và mục "Không được viết" trong hướng dẫn kịch bản: {ch['rules']}
- Chỉ dùng dữ liệu đã xác nhận (✅) trong brand.md; mục ⚠️ chưa xác nhận thì không dùng.
- Đặt "numbered": true nếu các thẻ là các bước theo thứ tự, false nếu là danh sách ý ngang hàng.
"""
    if feedback:
        prompt += f"""
ĐÂY LÀ BẢN VIẾT LẠI. Người duyệt trả về bản trước với lý do: «{feedback}».
Bản trước (JSON): {json.dumps(previous, ensure_ascii=False) if previous else "(không có)"}
"""
    prompt += f"\nChỉ trả về đúng MỘT khối JSON hợp lệ theo mẫu sau, không thêm chữ nào khác:\n{SCHEMA}\n"
    proc = subprocess.run([cli, "-p", prompt, "--output-format", "json", "--allowedTools", "Read,Glob,Grep"],
                          capture_output=True, text=True, encoding="utf-8", timeout=timeout, cwd=ROOT)
    try:
        out = json.loads(proc.stdout)
    except json.JSONDecodeError:
        raise RuntimeError(f"Claude không trả về kết quả: {proc.stderr[-300:] or proc.stdout[-300:]}")
    if out.get("is_error"):
        raise RuntimeError(f"Claude báo lỗi: {out.get('result')}")
    m = re.search(r"\{.*\}", out.get("result", ""), re.S)
    if not m:
        raise RuntimeError("Claude không trả về JSON banner")
    return json.loads(m.group(0))


def find_browser():
    for p in BROWSERS:
        if os.path.exists(p):
            return p
    raise RuntimeError("Không tìm thấy Chrome hoặc Edge để chụp banner")


def render(data, out_png, template="B1"):
    """Ghép nội dung vào khuôn HTML rồi chụp thành PNG 2160×2160."""
    tdir = os.path.join(ROOT, "banner", TEMPLATES[template])
    with open(os.path.join(tdir, "index.html"), encoding="utf-8") as f:
        html = f.read()
    base = "file:///" + tdir.replace("\\", "/") + "/"
    html = html.replace("__BASE__", base).replace("__DATA__", json.dumps(data, ensure_ascii=False))
    out_png = os.path.abspath(out_png)
    page = os.path.splitext(out_png)[0] + ".html"
    with open(page, "w", encoding="utf-8") as f:
        f.write(html)
    subprocess.run([find_browser(), "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=2", "--window-size=1080,1080",
                    "--allow-file-access-from-files", "--virtual-time-budget=5000",
                    f"--screenshot={out_png}", "file:///" + page.replace("\\", "/")],
                   capture_output=True, timeout=120)
    if not os.path.exists(out_png):
        raise RuntimeError("Chụp banner không thành công")
    return out_png


def job_dir(code):
    d = os.path.join(ROOT, "banner", "jobs", code)
    os.makedirs(d, exist_ok=True)
    return d


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    args = sys.argv[1:]
    if args[:1] == ["--json"]:
        path = args[1]
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        print(render(data, os.path.join(os.path.dirname(path), "banner.png")))
    elif args:
        code = "DH-B-THU-" + datetime.datetime.now().strftime("%H%M%S")
        d = job_dir(code)
        print(f"{code}: Claude đang viết nội dung…")
        data = write_banner(args[0])
        with open(os.path.join(d, "banner.json"), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(json.dumps(data, ensure_ascii=False, indent=2))
        print(render(data, os.path.join(d, "banner.png")))
    else:
        print(__doc__)
