"""Khung dựng HyperFrames dùng chung cho series review trường (KOL Linh AI + footage + thẻ thông tin).

Mỗi video có một build.py trong video/jobs/<mã>/ khai báo các cảnh rồi gọi write_project().
Phong cách theo brand.md 0.1: chữ đỏ viền trắng mỏng, chữ trắng viền xanh đậm, nhãn viên thuốc.
Font (An chốt 18/11/2026): SVN-Gilroy (tu-lieu/font) — Medium cho chữ thường, XBold cho tiêu đề.
Kết video: outro chính thức tu-lieu/chung/Outro THDHTT-Dọc.mp4 (4,25 s, có tiếng) thay thẻ kết tự vẽ.
Logo trên cùng: vùng y 100–220; chữ ở cảnh có logo phải bắt đầu từ y ≥ 280 (không đè logo).
Cảnh có Linh: gốc trong suốt (avatar chạy bên dưới), có nhãn "Hình ảnh AI".
"""
import json
import os
import shutil
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTRO_SRC = os.path.join(ROOT, "tu-lieu", "chung", "Outro THDHTT-Dọc.mp4")
OUTRO_DUR = 4.25
FONT_FILES = {"Gilroy-Medium.otf": "SVN-Gilroy Medium.otf", "Gilroy-XBold.otf": "SVN-Gilroy XBold.otf"}
LOGO_FILES = {"tt-tron.png": "Logo TT tròn trắng.png", "tt-ngang.png": "Logo TH va DH-ngang.png",
              "icon-tt.png": "Icon TT ko nền.png"}

FONTS = ('@font-face { font-family: "TT"; src: url("assets/fonts/Gilroy-Medium.otf"); font-weight: 400 600; }\n'
         '@font-face { font-family: "TT"; src: url("assets/fonts/Gilroy-XBold.otf"); font-weight: 700 900; }\n')


def prepare_assets(job):
    """Chép font Gilroy, logo và outro (đổi về 1080×1920, tách tiếng) vào assets/ của job."""
    for sub in ("fonts", "logo", "media"):
        os.makedirs(os.path.join(job, "assets", sub), exist_ok=True)
    for dst, src in FONT_FILES.items():
        shutil.copyfile(os.path.join(ROOT, "tu-lieu", "font", src), os.path.join(job, "assets", "fonts", dst))
    for dst, src in LOGO_FILES.items():
        shutil.copyfile(os.path.join(ROOT, "tu-lieu", "chung", src), os.path.join(job, "assets", "logo", dst))
    media = os.path.join(job, "assets", "media")
    if not os.path.exists(os.path.join(media, "outro.m4a")):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", OUTRO_SRC, "-vf", "scale=1080:1920,fps=30", "-an",
                        "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", os.path.join(media, "outro.mp4")],
                       check=True)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", OUTRO_SRC, "-vn", "-c:a", "aac", "-b:a", "192k",
                        os.path.join(media, "outro.m4a")], check=True)


def outro_end(vo_end):
    """Thời điểm kết video: outro chạy ngay sau câu cuối (từ vo_end - 0.2)."""
    return round(vo_end - 0.2 + OUTRO_DUR, 2)

BASE_CSS = """
#root { position: absolute; inset: 0; overflow: hidden; font-family: "TT", sans-serif; }
.big { display: block; font-weight: 900; color: #E81E37; -webkit-text-stroke: 10px #fff; paint-order: stroke fill;
       text-shadow: 0 6px 18px rgba(0,0,0,.28); line-height: 1.12; letter-spacing: -0.01em; white-space: nowrap; }
.wbig { display: block; font-weight: 900; color: #fff; -webkit-text-stroke: 9px #263E8B; paint-order: stroke fill;
        text-shadow: 0 6px 18px rgba(0,0,0,.28); line-height: 1.12; white-space: nowrap; }
.pill { display: inline-block; font-weight: 700; font-size: 46px; padding: 12px 34px 16px; border-radius: 60px;
        background: #1E6FE8; color: #fff; box-shadow: 0 8px 22px rgba(10,30,90,.28); white-space: nowrap; }
.pill.red { background: #E81E37; }
.pill.white { background: #fff; color: #1E6FE8; }
.pill.yellow { background: #FFE360; color: #263E8B; }
.pill.sm { font-size: 38px; padding: 10px 28px 13px; }
.center { position: absolute; left: 50px; right: 50px; text-align: center; }
.stack > * { margin: 0 auto 22px; }
.blue-bg { position: absolute; inset: 0; background: linear-gradient(180deg, #1E6FE8 0%, #3f8ff0 58%, #6fbcf5 100%); }
.scrim-b { position: absolute; left: 0; right: 0; bottom: 0; height: 1150px;
           background: linear-gradient(180deg, rgba(8,20,60,0) 0%, rgba(8,20,60,.55) 45%, rgba(8,20,60,.82) 100%); }
.scrim-t { position: absolute; left: 0; right: 0; top: 0; height: 900px;
           background: linear-gradient(0deg, rgba(8,20,60,0) 0%, rgba(8,20,60,.6) 45%, rgba(8,20,60,.85) 100%); }
.scrim-all { position: absolute; inset: 0; background: rgba(8,20,60,.58); }
.window { position: absolute; left: 40px; top: 1000px; width: 1000px; height: 667px; border-radius: 34px; overflow: hidden;
          border: 8px solid #fff; box-shadow: 0 18px 40px rgba(10,30,90,.35); }
.window video { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
.credit { position: absolute; left: 40px; right: 40px; top: 1690px; text-align: center; font-weight: 500; font-size: 28px;
          color: rgba(255,255,255,.9); }
.full { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; }
.logo { position: absolute; top: 100px; left: 50%; width: 120px; height: 120px; margin-left: -60px; }
.note { font-weight: 500; font-size: 30px; color: rgba(255,255,255,.9); white-space: normal; }
.card { position: absolute; left: 60px; right: 60px; background: #fff; border-radius: 40px; padding: 120px 50px 46px;
        box-shadow: 0 24px 60px rgba(5,15,50,.4); }
.card-h { position: absolute; left: 50%; top: -52px; transform: translateX(-50%); }
.row { display: flex; align-items: center; gap: 26px; margin-bottom: 34px; }
.ic { flex: none; width: 74px; height: 74px; border-radius: 50%; color: #fff; font-weight: 900; font-size: 44px;
      display: flex; align-items: center; justify-content: center; }
.rt { font-weight: 700; font-size: 48px; color: #263E8B; line-height: 1.22; }
.rt small { display: block; font-weight: 500; font-size: 32px; color: #5d6890; }
.fine { font-weight: 500; font-size: 28px; color: #6b7598; text-align: center; margin-top: 6px; }
"""


def scene(cid, body, js, root_css="", extra_css=""):
    return f"""<template>
  <style>
{FONTS}{BASE_CSS}
#root {{ {root_css} }}
{extra_css}
  </style>
  <div id="root" data-composition-id="{cid}" data-width="1080" data-height="1920">
{body}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{js}
    window.__timelines["{cid}"] = tl;
  </script>
</template>
"""


def pop(sel, t, d=0.3):
    return f'    tl.fromTo("{sel}", {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: {d}, ease: "back.out(2)" }}, {t:.2f});\n'


def rise(sel, t, d=0.32):
    return f'    tl.fromTo("{sel}", {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: {d}, ease: "power3.out" }}, {t:.2f});\n'


def out(sel, t, d=0.2):
    return (f'    tl.fromTo("{sel}", {{ opacity: 1 }}, {{ opacity: 0, duration: {d}, ease: "power2.in", '
            f'immediateRender: false }}, {t:.2f});\n')


def rows(prefix, items):
    """items: [(icon '✓' | '!' | '★', 'chữ', 'chữ nhỏ' hoặc '')]"""
    html = ""
    for i, (icon, text, small) in enumerate(items, 1):
        color = {"!": "#E81E37", "★": "#E8A400"}.get(icon, "#1E6FE8")
        sm = f"<small>{small}</small>" if small else ""
        html += (f'      <div id="{prefix}-r{i}" class="row"><span class="ic" style="background:{color}">{icon}</span>'
                 f'<span class="rt">{text}{sm}</span></div>\n')
    return html


def video(vid, src, start, dur, cls="full"):
    return (f'    <video id="{vid}" class="clip {cls}" src="assets/media/{src}" data-start="{start:.2f}" '
            f'data-duration="{dur:.2f}" muted playsinline></video>\n')


def outro_scene(cid="end"):
    """Outro chính thức (video). Tiếng outro do write_project đặt ở index (assets/media/outro.m4a)."""
    body = (f'    <video id="end-v" class="clip full" src="assets/media/outro.mp4" data-start="0" '
            f'data-duration="{OUTRO_DUR}" muted playsinline></video>')
    return scene(cid, body, "", root_css="background:#1E6FE8")


endcard_scene = outro_scene  # tên cũ, build.py cũ vẫn chạy


def linh_segments(job, scenes, linh_scenes, scene_lines):
    """Cảnh Linh → đoạn trong avatar.mp4 (HeyGen chỉ dựng câu lipsync). scene_lines: {cảnh: [id câu]}.
    Trả [(start, dur, media_start)] để đặt avatar đúng chỗ, khớp miệng."""
    m = {x["id"]: x for x in json.load(open(os.path.join(job, "linh_map.json"), encoding="utf-8"))}
    segs = []
    for cid, st, du, _ in scenes:
        if cid in linh_scenes:
            first = m[scene_lines[cid][0]]
            segs.append((st, du, max(0.0, first["linh_start"] - (first["main_start"] - st))))
    return segs


def write_project(job, title, scenes, vo_end, end, linh_scenes=(), music_vol=0.12, music_end_vol=0.45, avatar_segments=None, no_avatar=False):
    """no_avatar=True: video chỉ giọng + trám cảnh (không Linh/HeyGen); mọi cảnh phải có nền đặc."""
    """scenes: [(id, start, dur, html)]. Ghi compositions/*.html + index.html."""
    os.makedirs(os.path.join(job, "compositions"), exist_ok=True)
    for cid, _, _, html in scenes:
        open(os.path.join(job, "compositions", f"{cid}.html"), "w", encoding="utf-8").write(html)
    hosts = "".join(
        f'      <div id="{cid}" class="clip" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html" '
        f'data-start="{st:.2f}" data-duration="{du:.2f}" data-track-index="3" data-track-kind="graphics" '
        f'data-width="1080" data-height="1920" style="z-index:{i}"></div>\n'
        for i, (cid, st, du, _) in enumerate(scenes, 2))
    badges = "".join(
        f'      <div id="ai-{cid}" class="clip ai" data-start="{st:.2f}" data-duration="{du:.2f}" data-track-index="4">Hình ảnh AI</div>\n'
        for cid, st, du, _ in scenes if cid in linh_scenes)
    tail = round(end - vo_end, 2)
    outro = [(st, du) for cid, st, du, _ in scenes if cid == "end"] if os.path.exists(
        os.path.join(job, "assets", "media", "outro.m4a")) else []
    if outro:  # outro có tiếng riêng → nhạc nền nhỏ dần rồi tắt khi outro chạy
        music = (f'      <audio id="bgm" class="clip" src="assets/media/bgm.mp3" data-start="0" data-duration="{outro[0][0] + 0.6:.2f}" '
                 f'data-track-index="2" data-volume="{music_vol}" data-fade-in="0.8" data-fade-out="0.8"></audio>\n'
                 f'      <audio id="outro-a" class="clip" src="assets/media/outro.m4a" data-start="{outro[0][0]:.2f}" '
                 f'data-duration="{outro[0][1]:.2f}" data-track-index="5" data-volume="1"></audio>')
    else:
        music = (f'      <audio id="bgm" class="clip" src="assets/media/bgm.mp3" data-start="0" data-duration="{vo_end}" data-track-index="2" data-volume="{music_vol}" data-fade-in="0.8"></audio>\n'
                 f'      <audio id="bgm-end" class="clip" src="assets/media/bgm.mp3" data-start="{vo_end}" data-duration="{tail}" data-media-start="{vo_end}" data-track-index="2" data-volume="{music_end_vol}" data-fade-out="1.2"></audio>')
    if no_avatar:
        avatar = ""
    elif avatar_segments:
        avatar = "\n".join(
            f'      <video id="avatar-{i}" class="clip avatar" src="assets/media/avatar.mp4" data-start="{st:.2f}" '
            f'data-duration="{du:.2f}" data-media-start="{ms:.2f}" data-track-index="0" muted playsinline></video>'
            for i, (st, du, ms) in enumerate(avatar_segments, 1))
    else:
        avatar = (f'      <video id="avatar" class="clip avatar" src="assets/media/avatar.mp4" data-start="0" '
                  f'data-duration="{vo_end}" data-track-index="0" muted playsinline></video>')
    index = f"""<!doctype html>
<html lang="vi">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>{title}</title>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
{FONTS}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: #1e6fe8; }}
      #root {{ position: relative; width: 100%; height: 100%; }}
      .avatar {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; z-index: 1; }}
      .ai {{ position: absolute; top: 270px; left: 60px; z-index: 50; font-family: "TT", sans-serif; font-weight: 600;
             font-size: 30px; color: #fff; background: rgba(0,0,0,.45); padding: 8px 20px 10px; border-radius: 30px; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{end}" data-width="1080" data-height="1920">
{avatar}
      <audio id="vo" class="clip" src="assets/media/vo.mp3" data-start="0" data-duration="{vo_end}" data-track-index="1" data-volume="1"></audio>
{music}
{hosts}{badges}    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""
    open(os.path.join(job, "index.html"), "w", encoding="utf-8").write(index)
    print("ok", end, [(c, round(s, 2), round(d, 2)) for c, s, d, _ in scenes])


def timing(job):
    t = json.load(open(os.path.join(job, "timing.json"), encoding="utf-8"))
    return {l["id"]: l for l in t["lines"]}, t["total"]
