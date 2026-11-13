"""Agent Dựng video: từ kịch bản (JSON của script_writer) ra video MP4, khuôn K4 Chữ động.

  python tools/video_maker.py MA_DON          (đọc kịch bản trong data/orders.json)

Các bước: tạo giọng Vbee cho từng cảnh → sinh dự án HyperFrames trong video/jobs/<MA_DON>/
(mỗi cảnh một khung chữ động, thời lượng theo giọng đọc) → render MP4.

Hai giao diện (theme), chọn theo mã đơn (TH-… / DH-…):
  TH — Tiếng Hàn (brand.md + phong-cach-tieng-han.md): nền xanh tươi, hook đỏ viền trắng.
  DH — Du học (brand.md mục 2.6): nền trắng, mảng màu xanh/vàng ở góc, hook đỏ, tiêu đề xanh đậm,
       dòng có con số đặt trong nhãn vàng, dòng trong ngoặc tròn là chữ nhỏ (ghi chú bắt buộc) ở cuối khung.
Chung: Be Vietnam Pro, chữ Hàn Noto Sans KR, logo TT, end card xanh sóng.
"""
import html
import json
import os
import re
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
K4 = os.path.join(ROOT, "video", "th-k4-chu-dong")
COMMON = os.path.join(ROOT, "video", "_chung")
NPX = shutil.which("npx") or "npx"
HF = "hyperframes@0.9.37"

FONT_FACES = """    @font-face { font-family: "BVP"; src: url("assets/fonts/BeVietnamPro-Black.ttf"); font-weight: 900; }
    @font-face { font-family: "BVP"; src: url("assets/fonts/BeVietnamPro-ExtraBold.ttf"); font-weight: 800; }
    @font-face { font-family: "BVP"; src: url("assets/fonts/BeVietnamPro-Bold.ttf"); font-weight: 700; }
    @font-face { font-family: "BVP"; src: url("assets/fonts/BeVietnamPro-Medium.ttf"); font-weight: 500; }
    @font-face { font-family: "KR"; src: url("assets/fonts/NotoSansKR.ttf"); font-weight: 100 900; }"""

THEMES = {
    "TH": {"speed": "1.05", "bg": "#1e6fe8", "max_lines": 4, "css": """
    #root { position: absolute; inset: 0; overflow: hidden; font-family: "BVP", "KR", sans-serif;
      background: linear-gradient(180deg, #1e6fe8 0%, #3f8ff0 55%, #6fbcf5 100%); }
    .hook { font-weight: 900; line-height: 1.22; color: #e81e37; -webkit-text-stroke: 9px #ffffff;
      paint-order: stroke fill; text-shadow: 0 6px 14px rgba(20, 40, 110, 0.35); text-wrap: balance; }
    .head { font-weight: 900; line-height: 1.24; color: #ffffff; -webkit-text-stroke: 7px #263e8b;
      paint-order: stroke fill; text-shadow: 0 5px 10px rgba(20, 40, 110, 0.3); text-wrap: balance; }
    .sub { font-weight: 800; line-height: 1.3; color: #ffffff; -webkit-text-stroke: 5px #263e8b;
      paint-order: stroke fill; text-wrap: balance; }
    .phon { font-weight: 700; font-size: 44px; line-height: 1.3; color: #263e8b; background: #ffe360;
      border-radius: 999px; padding: 10px 34px; }"""},
    "DH": {"speed": "1.0", "bg": "#ffffff", "max_lines": 5, "css": """
    #root { position: absolute; inset: 0; overflow: hidden; font-family: "BVP", "KR", sans-serif;
      background: linear-gradient(180deg, #ffffff 0%, #ffffff 62%, #eaf3fe 100%); }
    .blob { position: absolute; border-radius: 50%; }
    .b1 { width: 620px; height: 520px; left: -300px; top: -230px; background: #1e6fe8; }
    .b2 { width: 480px; height: 420px; right: -250px; top: 60px; background: #ffe360; }
    .b3 { width: 560px; height: 480px; left: -290px; bottom: -230px; background: #ffe360; }
    .b4 { width: 640px; height: 560px; right: -300px; bottom: -290px; background: #1e6fe8; }
    .hook { font-weight: 900; line-height: 1.22; color: #e81e37; text-wrap: balance;
      text-shadow: 0 8px 0 rgba(38, 62, 139, 0.12); }
    .head { font-weight: 900; line-height: 1.24; color: #263e8b; text-wrap: balance; }
    .sub { font-weight: 800; line-height: 1.3; color: #263e8b; text-wrap: balance; }
    .num { font-weight: 900; line-height: 1.2; color: #e81e37; background: #ffe360; border-radius: 28px;
      padding: 14px 44px; box-shadow: 0 10px 0 rgba(38, 62, 139, 0.18); }
    .note { position: absolute; left: 0; right: 0; bottom: -60px; font-weight: 500; font-size: 34px;
      line-height: 1.3; color: #4a5a8c; font-style: italic; }"""},
}


def has_hangul(s):
    """Dòng 'thuần Hàn' (đa số chữ là Hangul) mới hiện dạng thẻ chữ Hàn; dòng lẫn Việt–Hàn giữ kiểu chữ Việt."""
    letters = [ch for ch in s if ch.isalpha()]
    ko = [ch for ch in letters if "가" <= ch <= "힣"]
    return bool(letters) and len(ko) / len(letters) >= 0.6


def fit(text, width, em, cap, floor):
    """Cỡ chữ để một dòng chữ vừa bề ngang (cho phép xuống tối đa 2 dòng)."""
    n = max(len(text), 1)
    return int(max(floor, min(cap, 2 * width / (em * n))))


def part_html(sid, idx, text, first_scene, theme="TH"):
    raw = text.strip()
    t = html.escape(raw)
    in_brackets = raw.startswith("(") and raw.endswith(")")
    if has_hangul(text):
        size = fit(text, 820, 1.05, 120, 64)
        return f'<div id="{sid}-l{idx}" class="ko" style="font-size:{size}px">{t}</div>'
    if theme == "DH" and in_brackets:
        return f'<div id="{sid}-l{idx}" class="note">{t}</div>'
    if idx == 1 and first_scene:
        size = fit(text, 960, 0.66, 128, 76)
        return f'<div id="{sid}-l{idx}" class="hook" style="font-size:{size}px">{t}</div>'
    if theme == "DH" and idx > 1 and re.search(r"\d", raw):
        size = fit(text, 900, 0.62, 80, 48)
        return f'<div id="{sid}-l{idx}" class="num" style="font-size:{size}px">{t}</div>'
    if idx == 1:
        size = fit(text, 960, 0.64, 96, 60)
        return f'<div id="{sid}-l{idx}" class="head" style="font-size:{size}px">{t}</div>'
    if in_brackets:
        return f'<div id="{sid}-l{idx}" class="phon">{t}</div>'
    if idx == 2:
        # Dòng ngay dưới tiêu đề: chữ trắng trên nền đỏ (kiểu nhãn), kết hợp với dòng chữ viền ở trên.
        size = int(max(40, min(60, 900 / (0.62 * max(len(raw), 1)))))  # ưu tiên 1 dòng, nhãn ôm sát chữ
        return f'<div id="{sid}-l{idx}" class="tag" style="font-size:{size}px">{t}</div>'
    size = fit(text, 960, 0.6, 58, 40)
    return f'<div id="{sid}-l{idx}" class="sub" style="font-size:{size}px">{t}</div>'


def scene_html(sid, parts, dur, first_scene, theme="TH"):
    lines = "\n      ".join(part_html(sid, i + 1, p, first_scene, theme) for i, p in enumerate(parts))
    blobs = ('<div class="blob b1"></div><div class="blob b2"></div>'
             '<div class="blob b3"></div><div class="blob b4"></div>') if theme == "DH" else ""
    ids = [f"#{sid}-l{i + 1}" for i in range(len(parts))]
    tweens = []
    for i, sel in enumerate(ids):
        if first_scene and i == 0:
            # Khung 0 là ảnh bìa: hook hiện sẵn, chỉ nhún nhẹ.
            tweens.append(f'tl.fromTo("{sel}", {{ scale: 1.12 }}, {{ scale: 1, duration: 0.3, ease: "power3.out" }}, 0);')
        else:
            at = 0.08 + i * 0.22
            tweens.append(f'tl.fromTo("{sel}", {{ opacity: 0, y: 40, scale: 0.92 }}, '
                          f'{{ opacity: 1, y: 0, scale: 1, duration: 0.3, ease: "back.out(1.7)" }}, {at:.2f});')
    exit_at = max(0.6, dur - 0.25)
    tweens.append(f'tl.fromTo("#{sid}-box", {{ opacity: 1 }}, {{ opacity: 0, duration: 0.2, ease: "power2.in", '
                  f'immediateRender: false }}, {exit_at:.2f});')
    tw = "\n    ".join(tweens)
    return f"""<template>
  <style>
{FONT_FACES}
{THEMES[theme]["css"]}
    #{sid}-logo {{ position: absolute; top: 70px; right: 48px; width: 108px; height: 108px; }}
    .tag {{ font-weight: 800; line-height: 1.3; color: #ffffff; background: #e81e37; border-radius: 18px;
      padding: 10px 30px; max-width: 960px; text-wrap: balance; box-shadow: 0 8px 18px rgba(20, 40, 110, 0.25); }}
    #{sid}-box {{ position: absolute; left: 60px; right: 60px; top: 230px; height: 1080px;
      display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 34px; text-align: center;
      word-break: keep-all; }}
    .ko {{ font-family: "KR", sans-serif; font-weight: 800; line-height: 1.25; color: #263e8b; background: #ffffff;
      border-radius: 32px; padding: 20px 48px; box-shadow: 0 14px 0 rgba(38, 62, 139, 0.35); }}
  </style>
  <div id="root" data-composition-id="{sid}" data-width="1080" data-height="1920">
    {blobs}
    <img id="{sid}-logo" src="assets/logo/tt-tron.png" alt="Logo Thầy Tư" />
    <div id="{sid}-box" data-layout-allow-overlap>
      {lines}
    </div>
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    {tw}
    window.__timelines["{sid}"] = tl;
  </script>
</template>
"""


def make_video(code, script, log=print, theme=None):
    theme = theme or ("DH" if code.startswith("DH-") else "TH")
    job = os.path.join(ROOT, "video", "jobs", code)
    shutil.rmtree(job, ignore_errors=True)
    os.makedirs(os.path.join(job, "compositions"))
    os.makedirs(os.path.join(job, "assets", "audio"))
    shutil.copytree(os.path.join(K4, "assets", "fonts"), os.path.join(job, "assets", "fonts"))
    shutil.copy(os.path.join(COMMON, "fonts", "NotoSansKR.ttf"), os.path.join(job, "assets", "fonts"))
    shutil.copytree(os.path.join(K4, "assets", "logo"), os.path.join(job, "assets", "logo"))
    shutil.copy(os.path.join(K4, "compositions", "endcard.html"), os.path.join(job, "compositions"))
    for f in ("hyperframes.json", "package.json"):
        shutil.copy(os.path.join(K4, f), job)
    json.dump({"id": code.lower(), "name": code.lower()}, open(os.path.join(job, "meta.json"), "w"))

    scenes = script["scenes"]
    names = [f"s{i + 1:02d}" for i in range(len(scenes))]
    # 1) Giọng đọc
    log("🎙 Đang tạo giọng Vbee…")
    args = [sys.executable, "-I", os.path.join(ROOT, "tools", "vbee_tts.py"), os.path.join(ROOT, ".env"),
            "voice_id_dh", os.path.join(job, "assets", "audio"), THEMES[theme]["speed"]]
    for n, sc in zip(names, scenes):
        args += [n, sc["voice"]]
    p = subprocess.run(args, capture_output=True, text=True, encoding="utf-8", cwd=ROOT, timeout=900)
    if p.returncode != 0:
        raise RuntimeError("Tạo giọng lỗi: " + (p.stdout + p.stderr)[-300:])
    voice = json.load(open(os.path.join(job, "assets", "audio", "voice.json"), encoding="utf-8"))

    # 2) Dựng các cảnh
    log("🎬 Đang dựng video…")
    hosts, audios, t = [], [], 0.0
    for i, (n, sc) in enumerate(zip(names, scenes)):
        vd = voice[n]["duration"]
        dur = round(max(2.2, vd + 0.45), 2)
        # Du học: chỉ tách dòng ở " / " có khoảng trắng, để "WON/NĂM" không bị tách.
        sep = r"\s+/\s+" if theme == "DH" else r"\s*/\s*"
        parts = ([x for x in re.split(sep, sc.get("screen", "")) if x.strip()][:THEMES[theme]["max_lines"]]
                 or [sc.get("name", "")])
        open(os.path.join(job, "compositions", f"{n}.html"), "w", encoding="utf-8").write(
            scene_html(n, parts, dur, i == 0, theme))
        hosts.append(f'      <div id="{n}" class="clip" data-composition-id="{n}" data-composition-src="compositions/{n}.html" '
                     f'data-start="{t:.2f}" data-duration="{dur}" data-track-index="1" data-track-kind="graphics" '
                     f'data-width="1080" data-height="1920"></div>')
        audios.append(f'      <audio id="vo-{n}" src="assets/audio/{n}.mp3" data-start="{t + 0.15:.2f}" '
                      f'data-duration="{vd}" data-track-index="5" data-volume="1"></audio>')
        t += dur
    end_dur = 2.8
    hosts.append(f'      <div id="endcard" class="clip" data-composition-id="endcard" data-composition-src="compositions/endcard.html" '
                 f'data-start="{t:.2f}" data-duration="{end_dur}" data-track-index="1" data-track-kind="graphics" '
                 f'data-width="1080" data-height="1920" '
                 "data-variable-values='{\"ec_name\":\"TIẾNG HÀN VÀ DU HỌC\\nTHẦY TƯ\",\"ec_hotline\":\"HOTLINE: 0967 593 548\"}'></div>")
    total = round(t + end_dur, 2)
    index = f"""<!doctype html>
<html lang="vi">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>{html.escape(code)} – {html.escape(script.get('title', ''))}</title>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: {THEMES[theme]["bg"]}; }}
      #root {{ position: relative; width: 100%; height: 100%; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{total}" data-width="1080" data-height="1920">
{chr(10).join(hosts)}
{chr(10).join(audios)}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""
    open(os.path.join(job, "index.html"), "w", encoding="utf-8").write(index)

    # 3) Render
    out = os.path.join(job, "renders", f"{code}.mp4")
    p = subprocess.run([NPX, "--yes", HF, "render", "-o", out], capture_output=True, text=True,
                       encoding="utf-8", errors="replace", cwd=job, timeout=1200, shell=os.name == "nt")
    if p.returncode != 0 or not os.path.exists(out):
        raise RuntimeError("Render lỗi: " + (p.stdout + p.stderr)[-400:])
    log(f"✅ Đã dựng xong {total:.0f}s")
    return out, total


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    code = sys.argv[1]
    if len(sys.argv) > 2:  # thử với file kịch bản JSON: python tools/video_maker.py DH-THU kichban.json
        path, total = make_video(code, json.load(open(sys.argv[2], encoding="utf-8")))
    else:
        order = json.load(open(os.path.join(ROOT, "data", "orders.json"), encoding="utf-8"))[code]
        path, total = make_video(code, order["script"])
    print("OK", path, total)
