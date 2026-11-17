"""Agent ⑥ Chấm điểm kịch bản: chấm trước khi gửi An duyệt, chưa đạt thì bot tự cho viết lại.

Hai lớp:
  1. Luật cứng (Python, không tốn Claude): từ cấm, khuyến mãi, số tiền (kênh Du học), số buổi học,
     thời lượng, tốc độ nói, chữ số trong lời đọc.
  2. Claude chấm theo brand.md + hướng dẫn kịch bản của kênh: điểm 0–10 theo 6 tiêu chí + lỗi + cách sửa.

Đạt khi: không có lỗi luật cứng, Claude không báo "lỗi", điểm ≥ PASS_SCORE.

Chạy thử:
  python tools/script_judge.py DH-261117-01        # chấm kịch bản của một đơn trong data/orders.json
  python tools/script_judge.py file.json [--dh]     # chấm một file JSON kịch bản
"""
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from script_writer import CHANNELS, ROOT, channel_of, find_claude  # noqa: E402

PASS_SCORE = 7.5

# (mẫu, mô tả, mức) — mức "lỗi" thì bắt buộc sửa, "nên sửa" chỉ nhắc.
BANNED_ALL = [
    (r"giảm\s*giá|giảm\s*\d+\s*%|giảm sâu|ưu đãi|khuyến (mãi|mại)|voucher", "khuyến mãi (brand.md: không có khuyến mãi)", "lỗi"),
    (r"chỉ (còn )?hôm nay|duy nhất hôm nay|hết hạn|chỉ còn\s*\d+|còn\s*\d+\s*suất|suất cuối|số lượng có hạn", "khan hiếm, gấp gáp giả", "lỗi"),
    (r"giá rẻ|siêu rẻ|rẻ nhất|chi phí rẻ", "từ cấm 'giá rẻ'", "lỗi"),
    (r"bao đậu|bao đỗ|đỗ 100|đậu 100|chắc chắn (có|đỗ|đậu)|cam kết (có )?visa|100% (có )?visa", "cam kết kết quả/visa", "lỗi"),
    (r"\b\d{2,3}\s*%\s*(người|học viên|bạn|các bạn)", "số liệu % có thể là bịa", "lỗi"),
    (r"phao cứu sinh|giết chết", "câu quá đà (hướng dẫn mục 5)", "nên sửa"),
]
BANNED_DH = [
    (r"\d[\d.,]*\s*(triệu|tr\b|nghìn|ngàn|đồng|đ\b|vnđ|vnd|won|krw|usd|\$)", "số tiền (Du học: video không nêu số tiền)", "lỗi"),
    (r"(một|hai|ba|bốn|năm|sáu|bảy|tám|chín|mười|trăm)[^.!?]{0,20}\b(triệu|nghìn đồng|won)\b", "số tiền đọc bằng chữ (Du học: không nêu số tiền)", "lỗi"),
    (r"thu nhập|lương cao|trải thảm đỏ|đổi đời", "hứa hẹn thu nhập (câu cũ cấm dùng lại)", "lỗi"),
    (r"học bổng xanh|250 triệu", "chương trình đã dừng", "lỗi"),
]
BANNED_TH = [
    (r"\d+\s*buổi|(hai|ba|bốn)\s*mươi[^.]{0,10}buổi", "số buổi học (đang chờ chốt, không nêu)", "lỗi"),
]


def _texts(s):
    """(chỗ, chữ) của mọi phần sẽ hiện ra với người xem."""
    out = []
    for i, sc in enumerate(s.get("scenes", []), 1):
        out.append((f"cảnh {i} lời đọc", sc.get("voice", "")))
        out.append((f"cảnh {i} chữ", sc.get("screen", "")))
    out.append(("caption Facebook", s.get("caption_facebook", "")))
    out.append(("caption TikTok", s.get("caption_tiktok", "")))
    return out


def syllables(text):
    return len(re.findall(r"[0-9A-Za-zÀ-ỹđĐ]+", text or ""))


def hard_checks(s, channel="TH", topic=""):
    ch = channel_of(channel)
    rules = BANNED_ALL + (BANNED_DH if ch == "DH" else BANNED_TH)
    issues = []
    for where, text in _texts(s):
        low = (text or "").lower()
        money_hit = False
        for pat, why, level in rules:
            m = re.search(pat, low)
            if m and "tiền" in why:
                if money_hit:
                    continue
                money_hit = True
            if m:
                # Số liệu chính PM ghi trong đơn (vd. học bổng trường) thì cho dùng, chỉ nhắc kèm nguồn.
                lv = "nên sửa" if (ch == "DH" and "tiền" in why and m.group(0).strip() in topic.lower()) else level
                issues.append({"level": lv, "where": where, "text": f"{why}: «{m.group(0)}»"})
    voices = [sc.get("voice", "") for sc in s.get("scenes", [])]
    allv = " ".join(voices)
    if ch == "DH" and re.search(r"có tốp pích ba,? có ngay visa|có topik 3,? có ngay visa", allv.lower()):
        issues.append({"level": "lỗi", "where": "lời đọc", "text": "đọc câu 'Có TOPIK 3 – Có ngay VISA' (chỉ được hiện chữ ở cảnh cuối)"})
    if ch == "TH" and re.search(r"(cam kết|đảm bảo)[^.]{0,40}(topik|tốp pích)", " ".join(t for _, t in _texts(s)).lower()) \
            and "điều khoản" not in json.dumps(s, ensure_ascii=False).lower():
        issues.append({"level": "lỗi", "where": "toàn bài", "text": "cam kết TOPIK thiếu 'áp dụng theo điều khoản khóa học'"})
    dur = s.get("duration_s") or 0
    if not 30 <= dur <= 90:
        issues.append({"level": "lỗi", "where": "thời lượng", "text": f"{dur} giây, ngoài khoảng 30–90 giây"})
    syl = syllables(allv)
    if dur:
        rate = syl / dur
        if rate > 5.0:
            issues.append({"level": "nên sửa", "where": "thời lượng",
                           "text": f"{syl} âm tiết trong {dur}s = {rate:.1f} âm tiết/giây, đọc sẽ dài hơn dự kiến (Vbee thực tế khoảng 3,5–4,5)"})
        elif rate < 3.0:
            issues.append({"level": "nên sửa", "where": "thời lượng",
                           "text": f"{syl} âm tiết trong {dur}s = {rate:.1f} âm tiết/giây, lời thưa, video sẽ ngắn hơn dự kiến"})
    if voices and syllables(voices[0]) > 25:
        issues.append({"level": "nên sửa", "where": "cảnh 1", "text": f"hook {syllables(voices[0])} âm tiết, dài hơn một câu 3 giây (15–20)"})
    for i, v in enumerate(voices, 1):
        if re.search(r"\d", v):
            issues.append({"level": "nên sửa", "where": f"cảnh {i} lời đọc", "text": "còn chữ số, Vbee có thể đọc sai (viết số bằng chữ)"})
    return issues


JUDGE_SCHEMA = """{
  "score": 8.0,
  "criteria": {"hook": 0-10, "cau_truc": 0-10, "dung_du_lieu": 0-10, "loi_doc_tts": 0-10, "giu_chan": 0-10, "cta": 0-10},
  "issues": [{"level": "lỗi | nên sửa", "where": "cảnh 2 lời đọc", "text": "vấn đề, ngắn gọn"}],
  "fix": "hướng dẫn sửa cụ thể cho Agent Biên kịch, 1–4 câu; để trống nếu không cần sửa",
  "strengths": "1 câu: điểm tốt nên giữ"
}"""


def claude_judge(s, channel="TH", topic="", timeout=420):
    cli = find_claude()
    if not cli:
        raise RuntimeError("Không tìm thấy Claude Code trên máy")
    ch = CHANNELS[channel_of(channel)]
    fanpage = "phan-tich-fanpage-du-hoc.md" if channel_of(channel) == "DH" else "phan-tich-fanpage-tieng-han.md"
    prompt = f"""Bạn là Agent ⑥ Chấm điểm kịch bản của nhà máy nội dung (xem CLAUDE.md). Bạn KHÔNG viết lại kịch bản, chỉ chấm.
Đọc: CLAUDE.md, brand.md (mục 0.2 phát âm, 1–2 dữ liệu, 4 quy tắc), {ch['guide']}, {fanpage}{', ' + ch['style'] if ch['style'] else ''}.

Đơn: kênh {ch['name']}, chủ đề «{topic}».
Kịch bản (JSON):
{json.dumps(s, ensure_ascii=False)}

Chấm như người duyệt khó tính (An) sẽ chấm, theo 6 tiêu chí (0–10):
- hook: 3 giây đầu có giữ người xem không (một câu, đánh trúng người xem, không rao bán).
- cau_truc: đúng công thức của dạng đã chọn trong hướng dẫn kịch bản.
- dung_du_lieu: mọi giá, phí, số liệu, visa, cam kết, tên trường đều có trong brand.md đã xác nhận (✅) hoặc trong chủ đề đơn; không dùng mục ⚠️; không vi phạm brand.md mục 4 và các điều cấm của kênh: {ch['rules']}
- loi_doc_tts: lời đọc tự nhiên, câu ngắn, viết đúng cách đọc theo bảng phát âm brand.md 0.2.
- giu_chan: nhịp, độ dài hợp với bài học fanpage, mỗi cảnh một ý, chữ trên màn hình ngắn.
- cta: rõ, đúng kiểu CTA của kênh/dạng.
"score" = điểm chung (không phải trung bình máy móc: một lỗi dữ liệu/quy tắc thì score ≤ 6).
Chỉ ghi "lỗi" khi vi phạm quy tắc, sai dữ liệu hoặc An chắc chắn sẽ trả về; còn lại là "nên sửa". Không bới lỗi vụn.
Chỉ trả về đúng MỘT khối JSON theo mẫu, không thêm chữ nào khác:
{JUDGE_SCHEMA}
"""
    proc = subprocess.run([cli, "-p", prompt, "--output-format", "json", "--allowedTools", "Read,Glob,Grep"],
                          capture_output=True, text=True, encoding="utf-8", timeout=timeout, cwd=ROOT)
    try:
        out = json.loads(proc.stdout)
    except json.JSONDecodeError:
        raise RuntimeError(f"Claude chấm không trả về kết quả: {proc.stderr[-300:] or proc.stdout[-300:]}")
    if out.get("is_error"):
        raise RuntimeError(f"Claude chấm báo lỗi: {out.get('result')}")
    m = re.search(r"\{.*\}", out.get("result", ""), re.S)
    if not m:
        raise RuntimeError("Claude chấm không trả về JSON")
    return json.loads(m.group(0))


def evaluate(s, channel="TH", topic=""):
    """Kết quả gộp: {passed, score, hard, judge, issues, fix}."""
    hard = hard_checks(s, channel, topic)
    try:
        j = claude_judge(s, channel, topic)
    except Exception as e:  # noqa: BLE001
        j = {"score": None, "issues": [], "fix": "", "error": str(e)[:200]}
    issues = hard + [i for i in j.get("issues", []) if isinstance(i, dict)]
    score = j.get("score")
    errors = [i for i in issues if i.get("level") == "lỗi"]
    passed = not errors and (score is None or score >= PASS_SCORE)
    fix_lines = [f"- {i['where']}: {i['text']}" for i in errors]
    if j.get("fix"):
        fix_lines.append(j["fix"])
    if not passed and not fix_lines:
        fix_lines.append(f"Điểm {score}/10 dưới mức đạt {PASS_SCORE}: làm hook và giữ chân tốt hơn.")
    return {"passed": passed, "score": score, "criteria": j.get("criteria", {}), "issues": issues,
            "strengths": j.get("strengths", ""), "fix": "\n".join(fix_lines), "judge_error": j.get("error")}


def format_result(r, rewrites=0):
    """Khối chữ đặt trên đầu tin kịch bản gửi An."""
    sc = r.get("score")
    head = f"🧮 Agent chấm: {sc}/10" if sc is not None else "🧮 Agent chấm: (không chấm được, chỉ kiểm luật cứng)"
    head += " · ✅ đạt" if r["passed"] else " · ⚠️ CHƯA ĐẠT, An xem kỹ"
    if rewrites:
        head += f" · đã tự viết lại {rewrites} lần"
    lines = [head]
    names = {"hook": "Hook", "cau_truc": "Cấu trúc", "dung_du_lieu": "Dữ liệu", "loi_doc_tts": "Lời đọc",
             "giu_chan": "Giữ chân", "cta": "CTA"}
    if r.get("criteria"):
        lines.append(" · ".join(f"{names.get(k, k)} {v}" for k, v in r["criteria"].items()))
    for i in r.get("issues", [])[:5]:
        lines.append(f"{'❌' if i.get('level') == 'lỗi' else '•'} {i.get('where', '')}: {i.get('text', '')}")
    return "\n".join(lines)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit()
    if args[0].endswith(".json"):
        with open(args[0], encoding="utf-8") as f:
            script = json.load(f)
        chan, topic = ("DH" if "--dh" in args else "TH"), ""
    else:
        with open(os.path.join(ROOT, "data", "orders.json"), encoding="utf-8") as f:
            o = json.load(f)[args[0]]
        script, chan, topic = o["script"], channel_of(o.get("channel", "TH")), o.get("topic", "")
    res = evaluate(script, chan, topic)
    print(format_result(res))
    print("\nCách sửa gửi Agent Biên kịch:\n" + (res["fix"] or "(không cần)"))
