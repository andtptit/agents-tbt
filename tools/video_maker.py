"""Agent Dựng video: từ kịch bản (JSON của script_writer) ra video MP4, khuôn K4 Chữ động.

  python tools/video_maker.py MA_DON          (đọc kịch bản trong data/orders.json)

Các bước: tạo giọng Vbee cho từng cảnh (một yêu cầu cho cả kịch bản) → sinh dự án HyperFrames trong
video/jobs/<MA_DON>/ (mỗi cảnh một khung chữ động, thời lượng theo giọng đọc) → render MP4.
Phong cách theo brand.md + phong-cach-tieng-han.md: nền xanh tươi, hook đỏ viền trắng, Be Vietnam Pro,
chữ Hàn Noto Sans KR, logo TT, end card xanh sóng.
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
    @font-face { font-family: "KR"; src: url("assets/fonts/NotoSansKR.ttf"); font-weight: 100 900; }"""


def has_hangul(s):
    """Dòng 'thuần Hàn' (đa số chữ là Hangul) mới hiện dạng thẻ chữ Hàn; dòng lẫn Việt–Hàn giữ kiểu chữ Việt."""
    letters = [ch for ch in s if ch.isalpha()]
    ko = [ch for ch in letters if "가" <= ch <= "힣"]
    return bool(letters) and len(ko) / len(letters) >= 0.6


def fit(text, width, em, cap, floor):
    """Cỡ chữ để một dòng chữ vừa bề ngang (cho phép xuống tối đa 2 dòng)."""
    n = max(len(text), 1)
    return int(max(floor, min(cap, 2 * width / (em * n))))


def part_html(sid, idx, text, first_scene):
    t = html.escape(text.strip())
    if has_hangul(text):
        size = fit(text, 820, 1.05, 120, 64)
        return f'<div id="{sid}-l{idx}" class="ko" style="font-size:{size}px">{t}</div>'
    if idx == 1 and first_scene:
        size = fit(text, 960, 0.66, 128, 76)
        return f'<div id="{sid}-l{idx}" class="hook" style="font-size:{size}px">{t}</div>'
    if idx == 1:
        size = fit(text, 960, 0.64, 96, 60)
        return f'<div id="{sid}-l{idx}" class="head" style="font-size:{size}px">{t}</div>'
    if text.strip().startswith("(") and text.strip().endswith(")"):
        return f'<div id="{sid}-l{idx}" class="phon">{t}</div>'
    size = fit(text, 960, 0.6, 58, 40)
    return f'<div id="{sid}-l{idx}" class="sub" style="font-size:{size}px">{t}</div>'


def scene_html(sid, parts, dur, first_scene):
    lines = "\n      ".join(part_html(sid, i + 1, p, first_scene) for i, p in enumerate(parts))
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
    #root {{ position: absolute; inset: 0; overflow: hidden; font-family: "BVP", "KR", sans-serif;
      background: linear-gradient(180deg, #1e6fe8 0%, #3f8ff0 55%, #6fbcf5 100%); }}
    #{sid}-logo {{ position: absolute; top: 196px; right: 56px; width: 150px; height: 150px; }}
    #{sid}-box {{ position: absolute; left: 60px; right: 60px; top: 230px; height: 1080px;
      display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 34px; text-align: center;
      word-break: keep-all; }}
    .hook {{ font-weight: 900; line-height: 1.22; color: #e81e37; -webkit-text-stroke: 22px #ffffff;
      paint-order: stroke fill; text-shadow: 0 0 30px rgba(255, 92, 140, 0.7); text-wrap: balance; }}
    .head {{ font-weight: 900; line-height: 1.24; color: #ffffff; -webkit-text-stroke: 14px #263e8b;
      paint-order: stroke fill; text-wrap: balance; }}
    .sub {{ font-weight: 800; line-height: 1.3; color: #ffffff; -webkit-text-stroke: 10px #e81e37;
      paint-order: stroke fill; text-wrap: balance; }}
    .phon {{ font-weight: 700; font-size: 44px; line-height: 1.3; color: #263e8b; background: #ffe360;
      border-radius: 999px; padding: 10px 34px; }}
    .ko {{ font-family: "KR", sans-serif; font-weight: 800; line-height: 1.25; color: #263e8b; background: #ffffff;
      border-radius: 32px; padding: 20px 48px; box-shadow: 0 14px 0 rgba(38, 62, 139, 0.35); }}
  </style>
  <div id="root" data-composition-id="{sid}" data-width="1080" data-height="1920">
    <img id="{sid}-logo" src="assets/logo/tt-tron.png" alt="Logo Tiếng Hàn Thầy Tư" />
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


def make_video(code, script, log=print):
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
            "voice_id_dh", os.path.join(job, "assets", "audio"), "1.05"]
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
        parts = [x for x in re.split(r"\s*/\s*", sc.get("screen", "")) if x.strip()][:4] or [sc.get("name", "")]
        open(os.path.join(job, "compositions", f"{n}.html"), "w", encoding="utf-8").write(
            scene_html(n, parts, dur, i == 0))
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
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: #1e6fe8; }}
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
    order = json.load(open(os.path.join(ROOT, "data", "orders.json"), encoding="utf-8"))[code]
    path, total = make_video(code, order["script"])
    print("OK", path, total)
