"""Agent Biên kịch: viết kịch bản cho một đơn đặt video bằng Claude Code chạy trên máy (headless).

Dùng trong bot Telegram, hoặc chạy tay để thử:
  python tools/script_writer.py "chào hỏi trong tiếng Hàn" ["phản hồi trả về nếu viết lại"]
  python tools/script_writer.py --dh "Học bổng trường Catholic"

Claude đọc CLAUDE.md, brand.md và hướng dẫn kịch bản của đúng kênh rồi trả về JSON kịch bản.
Cần Claude Code đã đăng nhập (lệnh `claude`, hoặc bản đi kèm Claude desktop).
"""
import glob
import json
import os
import re
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Mỗi kênh: tên, file hướng dẫn kịch bản, các dạng kịch bản, hashtag mẫu, ghi chú bắt buộc.
CHANNELS = {
    "TH": {"name": "Tiếng Hàn Thầy Tư", "guide": "huong-dan-kich-ban-tieng-han.md",
           "style": "phong-cach-tieng-han.md", "formats": "A (series chuyên môn) hoặc B (bán khóa)",
           "hashtags": '["#TiengHanThayTu", "#TOPIK"]',
           "rules": "không khuyến mãi, không số liệu bịa, giá chỉ lấy từ bảng giá (brand.md 1.5), "
                    "cam kết TOPIK 3+ kèm điều khoản, không nêu số buổi học.\n"
                    "- Nội dung tiếng Hàn (từ, ngữ pháp, ví dụ) phải chính xác; nếu không chắc thì chọn ví dụ đơn giản, phổ biến."},
    "DH": {"name": "Du học Thầy Tư", "guide": "huong-dan-kich-ban-du-hoc.md",
           "style": None, "formats": "T (giới thiệu trường, series Đúng ngành trúng trường) | S (hậu trường, sự kiện) | C (chi phí minh bạch) | H (hỏi đáp) | P (phá lời đồn)",
           "hashtags": '["#DuHocThayTu", "#DuHocHanQuoc"]',
           "rules": "xưng mình – bạn; chi phí chỉ lấy từ brand.md 2.3a (kèm 'chi phí tham khảo'), số liệu trường chỉ lấy "
                    "từ brand.md 2.3b (kèm 'theo thông tin trường công bố'); không cam kết visa, không 'gói 60 triệu', "
                    "không phí dịch vụ, không bịa ngày sự kiện; chữ nhỏ bắt buộc ghi vào dòng cuối của 'screen' trong ngoặc tròn."},
}


def channel_of(name_or_key):
    if name_or_key in CHANNELS:
        return name_or_key
    for k, c in CHANNELS.items():
        if c["name"] == name_or_key:
            return k
    return "TH"


SCHEMA = """{
  "title": "tên ngắn của video",
  "format": "__FORMATS__",
  "template": "K4 (chữ động) | K5 (kết quả học viên) | K1 (phủ lên video Thầy Tư quay)",
  "duration_s": 35,
  "axis": "sản phẩm | điểm đau | khác biệt",
  "course_code": "mã khóa trong bảng giá nếu có nhắc, không thì null",
  "scenes": [
    {"name": "Hook", "time": "0–3s", "voice": "lời đọc viết cho TTS (TOPIK → Tốp pích, số viết bằng chữ)",
     "screen": "chữ trên màn hình, ngắn", "visual": "hình ảnh/chất liệu gợi ý"}
  ],
  "caption_facebook": "...",
  "caption_tiktok": "...",
  "hashtags": __HASHTAGS__,
  "sources": ["dữ liệu đã dùng: brand.md mục …, bảng giá dòng …"],
  "check": ["tự kiểm: không khuyến mãi, không số liệu bịa, giá đúng bảng giá, …"]
}"""


def find_claude():
    if os.environ.get("CLAUDE_CLI"):
        return os.environ["CLAUDE_CLI"]
    found = shutil.which("claude")
    if found:
        return found
    bundled = glob.glob(os.path.join(os.environ.get("APPDATA", ""), "Claude", "claude-code", "*", "*", "claude.exe"))
    if bundled:
        return sorted(bundled, key=lambda p: [int(x) if x.isdigit() else x for x in re.split(r"[.\\/]", p)])[-1]
    return None


def claude_status():
    cli = find_claude()
    if not cli:
        return False, "Không tìm thấy Claude Code trên máy"
    try:
        out = subprocess.run([cli, "auth", "status"], capture_output=True, text=True, encoding="utf-8",
                             timeout=60, cwd=ROOT).stdout
        logged = json.loads(out).get("loggedIn")
    except Exception as e:  # noqa: BLE001
        return False, f"Không kiểm tra được Claude: {e}"
    return bool(logged), ("Claude đã đăng nhập" if logged else "Claude chưa đăng nhập")


def write_script(topic, channel="TH", feedback=None, previous=None, timeout=600):
    cli = find_claude()
    if not cli:
        raise RuntimeError("Không tìm thấy Claude Code trên máy")
    ch = CHANNELS[channel_of(channel)]
    extra = f" (và {ch['style']} nếu cần)" if ch["style"] else ""
    prompt = f"""Bạn là Agent Biên kịch của hệ thống nhà máy nội dung (xem CLAUDE.md).
Đọc kỹ: CLAUDE.md, brand.md, {ch['guide']}{extra}.

Đơn đặt video:
- Kênh: {ch['name']}
- Chủ đề: {topic}

Yêu cầu:
- Viết MỘT kịch bản video dọc theo đúng công thức của kênh trong {ch['guide']}.
- Tuân thủ tuyệt đối brand.md mục 4 và mục "Không được viết" trong hướng dẫn kịch bản: {ch['rules']}
- Lời đọc viết cho Vbee theo bảng phát âm trong brand.md mục 0.2.
- Thời lượng 30–90 giây.
"""
    if feedback:
        prompt += f"""
ĐÂY LÀ BẢN VIẾT LẠI. Người duyệt đã trả về bản trước với lý do: «{feedback}».
Bản trước (JSON): {json.dumps(previous, ensure_ascii=False) if previous else "(không có)"}
Sửa đúng theo lý do, giữ lại phần đã ổn.
"""
    prompt += f"""
Chỉ trả về đúng MỘT khối JSON hợp lệ theo mẫu sau, không thêm chữ nào khác:
{SCHEMA.replace("__FORMATS__", ch["formats"]).replace("__HASHTAGS__", ch["hashtags"])}
"""
    proc = subprocess.run([cli, "-p", prompt, "--output-format", "json", "--allowedTools", "Read,Glob,Grep"],
                          capture_output=True, text=True, encoding="utf-8", timeout=timeout, cwd=ROOT)
    try:
        out = json.loads(proc.stdout)
    except json.JSONDecodeError:
        raise RuntimeError(f"Claude không trả về kết quả: {proc.stderr[-300:] or proc.stdout[-300:]}")
    if out.get("is_error"):
        raise RuntimeError(f"Claude báo lỗi: {out.get('result')}")
    text = out.get("result", "")
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        raise RuntimeError("Claude không trả về JSON kịch bản")
    return json.loads(m.group(0))


def format_script(code, s):
    """Kịch bản dạng chữ để gửi Telegram (tối đa ~4000 ký tự)."""
    lines = [f"✍️ {code} — {s.get('title', '')}" + (" · 🎓 Du học Thầy Tư" if code.startswith("DH-") else ""),
             f"Khuôn {s.get('template', '?')} · ~{s.get('duration_s', '?')}s · Dạng {s.get('format', '?')} · Trục: {s.get('axis', '?')}",
             ""]
    for i, sc in enumerate(s.get("scenes", []), 1):
        lines.append(f"{i}. {sc.get('name', '')} ({sc.get('time', '')})")
        lines.append(f"🎙 {sc.get('voice', '')}")
        lines.append(f"🖥 {sc.get('screen', '')}")
        if sc.get("visual"):
            lines.append(f"🎞 {sc['visual']}")
        lines.append("")
    lines.append(f"Caption FB: {s.get('caption_facebook', '')}")
    lines.append(f"Hashtag: {' '.join(s.get('hashtags', []))}")
    if s.get("sources"):
        lines.append(f"Nguồn: {'; '.join(s['sources'])}")
    text = "\n".join(lines)
    return text if len(text) <= 4000 else text[:3990] + "…"


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    ok, msg = claude_status()
    print(msg)
    args = sys.argv[1:]
    chan = "DH" if args[:1] == ["--dh"] else "TH"
    args = args[1:] if chan == "DH" else args
    if ok and args:
        print(format_script(f"{chan}-THU", write_script(args[0], chan, feedback=args[1] if len(args) > 1 else None)))
