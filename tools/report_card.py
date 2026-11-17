"""Vẽ thẻ ảnh báo cáo fanpage (PNG) cho Telegram: 4 ô chỉ số lớn + biểu đồ lượt xem 8 ngày + top Reels.

  python tools/report_card.py     -> vẽ thử 2 thẻ từ số liệu thật, lưu vào data/report_cards/

Chỉ dùng Pillow (có sẵn). Màu thương hiệu: xanh tươi #1E6FE8, xanh đậm #263E8B, đỏ #E81E37, vàng #FFE360.
"""
import os
import sys
import unicodedata
from datetime import datetime

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import page_stats as ps  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = os.path.join(ROOT, "video", "th-k4-chu-dong", "assets", "fonts")
LOGO = os.path.join(ROOT, "video", "th-k4-chu-dong", "assets", "logo", "tt-tron.png")
OUT_DIR = os.path.join(ROOT, "data", "report_cards")

BLUE, NAVY, RED, YELLOW = "#1E6FE8", "#263E8B", "#E81E37", "#FFE360"
INK, MUTED, LINE, BG, CARD = "#141A33", "#5B6383", "#E3E7F2", "#F4F6FB", "#FFFFFF"
GREEN = "#17834F"
W, H = 1080, 1440
S = 2  # vẽ to gấp đôi rồi thu nhỏ cho nét


def font(weight, size):
    name = {"black": "Black", "xbold": "ExtraBold", "bold": "Bold", "semi": "SemiBold", "med": "Medium"}[weight]
    return ImageFont.truetype(os.path.join(FONTS, f"BeVietnamPro-{name}.ttf"), size * S)


def rr(d, box, r, fill, outline=None, width=1):
    d.rounded_rectangle([c * S for c in box], radius=r * S, fill=fill, outline=outline, width=width * S)


def text(d, xy, s, f, fill, anchor="la"):
    d.text((xy[0] * S, xy[1] * S), s, font=f, fill=fill, anchor=anchor)


def fit_text(d, s, f, max_w):
    if d.textlength(s, font=f) <= max_w * S:
        return s
    while s and d.textlength(s + "…", font=f) > max_w * S:
        s = s[:-1]
    return s.rstrip() + "…"


def clean(s):
    """Bỏ emoji/ký hiệu mà font không vẽ được, gom khoảng trắng."""
    s = "".join(ch for ch in s if ord(ch) <= 0xFFFF and unicodedata.category(ch) not in ("So", "Sk", "Cs", "Co"))
    return " ".join(s.split())


def render(p, path):
    img = Image.new("RGB", (W * S, H * S), BG)
    d = ImageDraw.Draw(img)

    # Dải đầu
    d.rectangle([0, 0, W * S, 200 * S], fill=BLUE)
    if os.path.exists(LOGO):
        lg = Image.open(LOGO).convert("RGBA").resize((120 * S, 120 * S))
        img.paste(lg, (48 * S, 40 * S), lg)
    text(d, (190, 58), p["name"].upper(), font("black", 46), "#FFFFFF")
    text(d, (190, 124), f"Số liệu ngày {p['day']:%d/%m/%Y} · Facebook", font("med", 28), "#DCE6FF")

    # 4 ô chỉ số
    ch = p["change"]
    up = ch >= 0
    net = p["follows"] - p["unfollows"]
    tiles = [
        ("LƯỢT XEM", ps.fmt(p["views"]), (f"{'Tăng' if up else 'Giảm'} {abs(ch) * 100:.0f}% so với TB 7 ngày", GREEN if up else RED)),
        ("NGƯỜI XEM", ps.fmt(p["reach"]), ("không trùng lặp", MUTED)),
        ("THEO DÕI MỚI", f"{'+' if net >= 0 else ''}{net}", (f"+{p['follows']} / -{p['unfollows']} · tổng {ps.fmt(p['followers'])}",
                                                              GREEN if net >= 0 else RED)),
        ("LƯỢT VÀO TRANG", ps.fmt(p["visits"]), ("trong ngày", MUTED)),
    ]
    tw, th, gap, x0, y0 = 480, 200, 24, 48, 236
    for i, (label, value, (sub, sub_c)) in enumerate(tiles):
        x = x0 + (i % 2) * (tw + gap)
        y = y0 + (i // 2) * (th + gap)
        rr(d, (x, y, x + tw, y + th), 22, CARD, LINE, 2)
        text(d, (x + 30, y + 26), label, font("bold", 24), MUTED)
        text(d, (x + 30, y + 64), value, font("black", 72), NAVY if i else (INK))
        text(d, (x + 30, y + 156), fit_text(d, sub, font("semi", 24), tw - 60), font("semi", 24), sub_c)

    # Biểu đồ lượt xem 8 ngày
    cy = y0 + 2 * (th + gap) + 8
    rr(d, (48, cy, W - 48, cy + 430), 22, CARD, LINE, 2)
    text(d, (78, cy + 26), "LƯỢT XEM 8 NGÀY GẦN NHẤT", font("bold", 24), MUTED)
    if p["avg"]:
        text(d, (W - 78, cy + 28), f"- - -  TB 7 ngày: {ps.fmt(p['avg'])}", font("semi", 22), MUTED, "ra")
    series = p["views_series"]
    if series:
        vmax = max(v for _, v in series) or 1
        n = len(series)
        left, right, top, bottom = 90, W - 90, cy + 92, cy + 360
        slot = (right - left) / n
        bw = slot * 0.58
        avg = p["avg"]
        if avg:
            ya = bottom - (bottom - top) * avg / vmax
            for xx in range(int(left), int(right), 18):
                d.line([(xx * S, ya * S), ((xx + 9) * S, ya * S)], fill="#9AA6C9", width=2 * S)

        for i, (day, v) in enumerate(series):
            last = i == n - 1
            bx = left + i * slot + (slot - bw) / 2
            bh = (bottom - top) * v / vmax
            rr(d, (bx, bottom - bh, bx + bw, bottom), 8, RED if last else "#9DB8F2")
            text(d, (bx + bw / 2, bottom - bh - 30), f"{v / 1000:.0f}k".replace(".", ","),
                 font("bold" if last else "semi", 20), RED if last else MUTED, "ma")
            text(d, (bx + bw / 2, bottom + 14), f"{day:%d/%m}", font("bold" if last else "med", 20),
                 INK if last else MUTED, "ma")

    # Top Reels
    ry = cy + 450
    rr(d, (48, ry, W - 48, H - 40), 22, CARD, LINE, 2)
    text(d, (78, ry + 24), f"TOP REELS 7 NGÀY ({p.get('reel_count', 0)} VIDEO)", font("bold", 24), MUTED)
    top = p.get("top") or []
    if not top:
        text(d, (78, ry + 74), "Chưa có Reels mới trong 7 ngày", font("semi", 26), MUTED)
    for i, (plays, avg_s, title) in enumerate(top[:3]):
        yy = ry + 70 + i * 62
        medal = ["#E8B21E", "#A7B0C2", "#C98A55"][i]
        d.ellipse([(78 * S, (yy + 2) * S), (118 * S, (yy + 42) * S)], fill=medal)
        text(d, (98, yy + 22), str(i + 1), font("black", 22), "#FFFFFF", "mm")
        stat = f"{ps.fmt(plays)} lượt · {ps.sec(avg_s)}"
        title = clean(title)
        text(d, (136, yy + 6), stat, font("xbold", 26), NAVY)
        sw = d.textlength(stat, font=font("xbold", 26)) / S
        text(d, (136 + sw + 18, yy + 8), fit_text(d, title, font("med", 24), W - 120 - (136 + sw + 18)),
             font("med", 24), INK)

    img = img.resize((W, H), Image.LANCZOS)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path, optimize=True)
    return path


def render_all(user_tok):
    paths = []
    stamp = datetime.now().strftime("%Y%m%d")
    for key, pid, name in ps.PAGES:
        p = ps.page_data(key, pid, name, user_tok)
        if p["ok"]:
            paths.append((p, render(p, os.path.join(OUT_DIR, f"{key}_{stamp}.png"))))
    return paths


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    env = ps.m.load_env()
    for p, path in render_all(env["META_READ_TOKEN"]):
        print(path)
