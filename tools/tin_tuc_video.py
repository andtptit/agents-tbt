"""Agent Dựng – khuôn BT "Bản tin du học Hàn": kịch bản của tools/tin_tuc.py → video MP4.

  python tools/tin_tuc_video.py <mã> <file kịch bản.json>

Bố cục (dùng khung chung tools/truong_build.py: font SVN-Gilroy, logo, outro chính thức):
  Hook  : nền xanh + logo + "BẢN TIN DU HỌC HÀN" + ngày
  Tin N : footage kho TBT (mờ tối) + thẻ trắng: nhãn đỏ (VISA/HỌC BỔNG…), tiêu đề, 2–3 ý, dòng NGUỒN + ngày (bắt buộc)
  CTA   : footage TBT + "DU HỌC THẦY TƯ" + NHẮN TIN NGAY
  Outro : tu-lieu/chung/Outro THDHTT-Dọc.mp4
Nhạc nền: noi-bo/am-thanh/nhac-ban-tin.mp3 (không có thì bỏ nhạc).
"""
import html
import math
import re
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import footage_index  # noqa: E402
import truong_media  # noqa: E402
from script_writer import ROOT  # noqa: E402
from truong_build import (outro_end, outro_scene, pop, prepare_assets, rise, scene, video,  # noqa: E402
                          write_project)

K4 = os.path.join(ROOT, "video", "th-k4-chu-dong")
MUSIC = os.path.join(ROOT, "noi-bo", "am-thanh", "nhac-ban-tin.mp3")
NPX = shutil.which("npx") or "npx"
HF = "hyperframes@0.9.37"  # cùng bản với tools/video_maker.py
FOOT_WORDS = ["tuyensinh", "hoso", "daotao", "doingu", "chung", "nen"]

CSS = """
.num { font-weight: 800; font-size: 34px; color: #fff; background: rgba(0,0,0,.4); padding: 8px 22px 10px; border-radius: 30px;
       display: inline-block; }
.hl { font-weight: 800; font-size: 58px; color: #263E8B; line-height: 1.16; text-align: center; margin-bottom: 34px; }
.pt { display: flex; gap: 22px; align-items: flex-start; margin-bottom: 24px; }
.pt b { flex: none; width: 20px; height: 20px; border-radius: 50%; background: #E81E37; margin-top: 18px; }
.pt span { font-weight: 600; font-size: 44px; color: #26305c; line-height: 1.25; }
.src { margin-top: 30px; padding-top: 24px; border-top: 3px dashed #d5dbef; text-align: center; font-weight: 600; font-size: 32px;
       color: #5d6890; }
.src strong { color: #1E6FE8; font-weight: 800; }
"""


def esc(t):
    return html.escape(str(t or ""))


def fmt_date(d):
    try:
        return datetime.strptime(d, "%Y-%m-%d").strftime("%d/%m/%Y")
    except (TypeError, ValueError):
        return str(d or "")


def pick_footage(job, code, n):
    """n clip kho TBT ít dùng nhất (khác nhau) → assets/media/tbt-*.mp4."""
    clips = footage_index.find(FOOT_WORDS, n=n)
    files = [c["file"] for c in clips]
    names = truong_media.footage(job, files)
    footage_index.mark_used(code, files)
    return [names[f] for f in files]


def make_video(code, script, log=print):
    job = os.path.join(ROOT, "video", "jobs", code)
    shutil.rmtree(job, ignore_errors=True)
    os.makedirs(os.path.join(job, "assets", "media"))
    for f in ("hyperframes.json", "package.json"):
        shutil.copy(os.path.join(K4, f), job)
    json.dump({"id": code.lower(), "name": code.lower()}, open(os.path.join(job, "meta.json"), "w"))
    json.dump({"lines": [{"id": l["id"], "text": l["text"], "part": l["part"]} for l in script["lines"]]},
              open(os.path.join(job, "kich-ban.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(script, open(os.path.join(job, "kich-ban-day-du.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    prepare_assets(job)

    log("🎙 Đang tạo giọng Vbee…")
    truong_media.vbee(job)
    truong_media.join_vo(job)
    shutil.copy(os.path.join(job, "vo.mp3"), os.path.join(job, "assets", "media", "vo.mp3"))
    t = json.load(open(os.path.join(job, "timing.json"), encoding="utf-8"))
    vo_end, start = t["total"], {l["id"]: l["start"] for l in t["lines"]}
    end = outro_end(vo_end)
    if os.path.exists(MUSIC):
        shutil.copy(MUSIC, os.path.join(job, "assets", "media", "bgm.mp3"))
    else:  # không có nhạc → file im lặng để khung dựng không lỗi
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-t", str(end), "-i", "anullsrc=r=44100:cl=mono",
                        os.path.join(job, "assets", "media", "bgm.mp3")], check=True)

    # Mốc từng phần (hook, t1, t2, …, cta) = câu đầu tiên của phần đó
    parts, first = [], {}
    for l in script["lines"]:
        if l["part"] not in first:
            first[l["part"]] = start[l["id"]]
            parts.append(l["part"])
    bounds = [max(0.0, first[p] - 0.1) if i else 0.0 for i, p in enumerate(parts)] + [vo_end - 0.2]
    news = {n["part"]: n for n in script.get("news", [])}
    total_news = sum(1 for p in parts if p in news)

    log("🎬 Đang dựng video…")
    # Mỗi cảnh tin đổi footage khoảng 5 s một lần (cảnh 16 s một clip thì nhàm)
    cuts = {p: max(1, math.ceil((bounds[i + 1] - bounds[i]) / 5.5)) for i, p in enumerate(parts) if p in news}
    foot = pick_footage(job, code, sum(cuts.values()) + 1)
    fi = 0
    S, k = [], 0
    day = datetime.now().strftime("%d/%m/%Y")
    for i, p in enumerate(parts):
        s, d = bounds[i], bounds[i + 1] - bounds[i]
        cid = f"p{i:02d}"
        if p == "hook":
            sub = esc(re.sub(r"^dòng nhỏ[^:]*:\s*", "", script.get("hook_sub") or "").strip() or "Tin mới cho bạn")
            body = f"""    <div class="blue-bg"></div>
    <img class="logo" src="assets/logo/tt-tron.png" alt="Logo" />
    <div class="center" style="top:520px">
      <span id="{cid}-k" class="wbig" style="font-size:80px">BẢN TIN</span>
      <span id="{cid}-t" class="big" style="font-size:118px">DU HỌC HÀN</span>
      <span id="{cid}-d" class="pill yellow" style="margin-top:26px">{day}</span>
      <div id="{cid}-s" class="wbig" style="font-size:54px;margin-top:60px;white-space:normal">{sub}</div>
    </div>"""
            js = rise(f"#{cid}-k", 0.05) + pop(f"#{cid}-t", 0.25) + pop(f"#{cid}-d", 0.7) + rise(f"#{cid}-s", 1.1)
            S.append((cid, s, d, scene(cid, body, js)))
        elif p in news:
            k += 1
            n = news[p]
            pts = "".join(f'      <div id="{cid}-p{j}" class="pt"><b></b><span>{esc(x)}</span></div>\n'
                          for j, x in enumerate(n.get("points", [])[:3], 1))
            m = cuts[p]
            seg = d / m
            clips = "".join(video(f"{cid}-v{j}", foot[fi + j], seg * j, seg + (0.05 if j < m - 1 else 0)) for j in range(m))
            fi += m
            body = (clips + f"""    <div class="scrim-all"></div>
    <div class="center" style="top:300px"><span id="{cid}-n" class="num">TIN {k}/{total_news}</span></div>
    <div id="{cid}-card" class="card" style="top:520px">
      <span id="{cid}-h" class="card-h pill red" style="font-size:54px;padding:16px 46px 20px">{esc(n.get('kicker', 'TIN MỚI'))}</span>
      <div id="{cid}-hl" class="hl">{esc(n.get('headline'))}</div>
{pts}      <div id="{cid}-src" class="src">Nguồn: <strong>{esc(n.get('publisher'))}</strong> · {fmt_date(n.get('published'))}</div>
    </div>""")
            step = max(0.9, (d - 1.6) / max(1, len(n.get("points", [])[:3]) + 1))
            js = (rise(f"#{cid}-n", 0) + rise(f"#{cid}-card", 0.05) + pop(f"#{cid}-h", 0.25) + rise(f"#{cid}-hl", 0.45)
                  + "".join(rise(f"#{cid}-p{j}", 0.45 + step * j) for j in range(1, len(n.get("points", [])[:3]) + 1))
                  + rise(f"#{cid}-src", 0.6))
            S.append((cid, s, d, scene(cid, body, js, root_css="background:#000", extra_css=CSS)))
        else:  # cta
            body = (video(f"{cid}-v", foot[-1], 0, d) + f"""    <div class="scrim-t"></div>
    <div class="center stack" style="top:260px">
      <span id="{cid}-t" class="wbig" style="font-size:74px">DU HỌC THẦY TƯ</span>
      <span id="{cid}-p" class="pill white">Cập nhật tin du học mỗi ngày</span>
      <span id="{cid}-c" class="pill red" style="font-size:62px;padding:22px 56px 26px">NHẮN TIN NGAY</span>
    </div>""")
            js = pop(f"#{cid}-t", 0.05) + rise(f"#{cid}-p", 0.5) + pop(f"#{cid}-c", min(1.4, d * 0.4))
            S.append((cid, s, d, scene(cid, body, js, root_css="background:#000")))
    s = vo_end - 0.2
    S.append(("end", s, end - s, outro_scene()))
    write_project(job, f"{code} – {script.get('title', '')}", S, vo_end, end, no_avatar=True)

    out = os.path.join(job, "renders", f"{code}.mp4")
    p = subprocess.run([NPX, "--yes", HF, "render", "-o", out], capture_output=True, text=True,
                       encoding="utf-8", errors="replace", cwd=job, timeout=1500, shell=os.name == "nt")
    if p.returncode != 0 or not os.path.exists(out):
        raise RuntimeError("Render lỗi: " + (p.stdout + p.stderr)[-400:])
    log(f"✅ Đã dựng xong {end:.0f}s")
    return out, end


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    path, total = make_video(sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8")))
    print("OK", path, total)
