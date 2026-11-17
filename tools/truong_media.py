"""Series review trường – phần âm thanh và KOL Linh AI.

  python tools/truong_media.py vo <thư mục job>       # ghép audio/lNN.mp3 (Vbee) → vo.mp3 + timing.json
  python tools/truong_media.py linh <thư mục job>     # tải vo.mp3 lên HeyGen, dựng avatar Linh → avatar.mp4
  python tools/truong_media.py footage <thư mục job> file1 file2 ...   # chuẩn hóa footage TBT về 1080×1920

HeyGen chạy qua cầu nối MCP "heygen" (tài khoản Creator, trừ credit gói), gọi bằng Claude Code chạy ngầm.
Avatar mặc định: look "Linh Du Học". Giọng giữ nguyên Vbee (không dùng giọng HeyGen).
"""
import hashlib
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from script_writer import ROOT, find_claude  # noqa: E402

LINH_LOOK = "cd88e36a43184863869a63e597591756"
GAP, LEAD, TAIL = 0.3, 0.25, 0.5
ENC = ["-c:v", "libx264", "-preset", "medium", "-crf", "18", "-g", "30", "-pix_fmt", "yuv420p", "-r", "30", "-an"]


def join_vo(job):
    v = json.load(open(os.path.join(job, "audio", "voice.json"), encoding="utf-8"))
    keys = sorted(v)
    inputs, lines, t = [], [], LEAD

    def sil(d):
        inputs.extend(["-f", "lavfi", "-t", f"{d:.3f}", "-i", "anullsrc=r=44100:cl=mono"])
    sil(LEAD)
    for i, k in enumerate(keys):
        d = v[k]["duration"]
        inputs.extend(["-i", os.path.join(job, "audio", f"{k}.mp3")])
        lines.append({"id": k, "start": round(t, 3), "end": round(t + d, 3), "text": v[k]["text"]})
        t += d
        g = GAP if i < len(keys) - 1 else TAIL
        sil(g)
        t += g
    n = inputs.count("-i")
    fc = "".join(f"[{i}]aresample=44100,aformat=sample_fmts=fltp:channel_layouts=mono[a{i}];" for i in range(n))
    fc += "".join(f"[a{i}]" for i in range(n)) + f"concat=n={n}:v=0:a=1[o]"
    out = os.path.join(job, "vo.mp3")
    subprocess.run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", fc, "-map", "[o]", "-b:a", "192k", out],
                   check=True)
    json.dump({"total": round(t, 3), "lines": lines}, open(os.path.join(job, "timing.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print(f"vo.mp3 {t:.2f}s, {len(lines)} câu")


def linh(job, title):
    vo = os.path.join(job, "vo.mp3")
    data = open(vo, "rb").read()
    size, sha = len(data), hashlib.sha256(data).hexdigest()
    prompt = f"""Thư mục hiện tại có file vo.mp3 ({size} byte, sha256 {sha}). Làm đúng các bước, chỉ tạo đúng MỘT video:
1) heygen create_asset_upload(filename='vo.mp3', contentType='audio/mpeg', sizeBytes={size}, checksumSha256 như trên).
2) Tải file lên upload_url bằng Bash: curl -sS -X PUT -H 'Content-Type: audio/mpeg' --data-binary @vo.mp3 '<upload_url>' (thêm header nếu bước 1 yêu cầu). Không in URL có chữ ký.
3) heygen complete_asset_upload(assetId).
4) heygen create_video_from_avatar: avatarId='{LINH_LOOK}', audioAssetId=<asset_id>, aspectRatio='9:16', resolution='1080p', title='{title}'. Không dùng script/voice.
5) Chờ: khoảng 30 giây gọi get_video một lần (chạy sleep 30 ở chế độ nền nếu sleep trực tiếp bị chặn), tối đa 20 phút.
6) Xong thì tải về avatar-raw.mp4 trong thư mục hiện tại bằng curl -sSL -o avatar-raw.mp4 '<video_url>'.
In ngắn: asset_id, video_id, trạng thái, thời lượng, đã lưu file chưa, lỗi nếu có."""
    r = subprocess.run([find_claude(), "-p", prompt, "--allowedTools", "mcp__heygen,Bash(curl:*),Bash(sleep:*),Bash(ls:*)",
                        "--output-format", "text"], capture_output=True, text=True, encoding="utf-8", cwd=job,
                       timeout=1800)
    open(os.path.join(job, "heygen.log"), "w", encoding="utf-8").write(r.stdout + r.stderr)
    raw = os.path.join(job, "avatar-raw.mp4")
    if not os.path.exists(raw):
        raise RuntimeError("HeyGen không trả video: xem heygen.log")
    os.makedirs(os.path.join(job, "assets", "media"), exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", raw, "-vf", "scale=1080:1920", *ENC,
                    os.path.join(job, "assets", "media", "avatar.mp4")], check=True)
    print("avatar.mp4 xong")


def footage(job, files):
    """Footage TBT → assets/media/<tên ngắn>.mp4, 1080×1920 (ngang thì cắt giữa)."""
    out = {}
    for f in files:
        src = os.path.join(ROOT, f)
        name = "tbt-" + os.path.basename(f).split("_", 1)[0].lower().replace("qt-", "") + ".mp4"
        dst = os.path.join(job, "assets", "media", name)
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", src, "-vf",
                        "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920", *ENC, dst], check=True)
        out[f] = name
        print(name, "←", f)
    return out


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    a = sys.argv[1:]
    if a[:1] == ["vo"]:
        join_vo(a[1])
    elif a[:1] == ["linh"]:
        linh(a[1], a[2] if len(a) > 2 else "Series trường – Linh AI")
    elif a[:1] == ["footage"]:
        footage(a[1], a[2:])
    else:
        print(__doc__)
