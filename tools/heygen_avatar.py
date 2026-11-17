"""Video avatar HeyGen nói bằng giọng Vbee có sẵn (gọi thẳng HeyGen API, không qua HyperFrames).

Cần dòng HEYGEN_API_KEY=... trong .env (lấy ở app.heygen.com → Settings → API). Không bao giờ in khóa.

  python tools/heygen_avatar.py list [tên]                      # tìm avatar theo tên, in id
  python tools/heygen_avatar.py make "Linh Du Học" vo.mp3 out.mp4  # avatar (tên hoặc id) + file giọng → video 9:16

Lưu ý quy tắc: cảnh AI phải gắn nhãn AI (CLAUDE.md quy tắc 5). Video avatar hiện chỉ để thử, chưa dùng đăng thật.
"""
import json
import os
import sys
import time
import unicodedata
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API = "https://api.heygen.com"
UPLOAD = "https://upload.heygen.com/v1/asset"


def api_key():
    for row in open(os.path.join(ROOT, ".env"), encoding="utf-8"):
        k, _, v = row.strip().partition("=")
        if k.strip() == "HEYGEN_API_KEY" and v.strip():
            return v.strip().strip('"').strip("'")
    sys.exit("Chưa có HEYGEN_API_KEY trong .env")


def call(url, body=None, data=None, ctype="application/json", method=None):
    headers = {"X-Api-Key": api_key(), "Accept": "application/json"}
    if body is not None:
        data = json.dumps(body).encode()
    if data is not None:
        headers["Content-Type"] = ctype
    req = urllib.request.Request(url, data=data, headers=headers, method=method or ("POST" if data else "GET"))
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HeyGen lỗi {e.code}: {e.read().decode()[:400]}")


def norm(s):
    s = unicodedata.normalize("NFD", (s or "").lower().replace("đ", "d"))
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


def all_avatars():
    """[(kind, id, tên)] gồm avatar thường và talking photo (photo avatar)."""
    d = call(f"{API}/v2/avatars").get("data", {})
    out = [("avatar", a["avatar_id"], a.get("avatar_name", "")) for a in d.get("avatars", [])]
    out += [("talking_photo", t["talking_photo_id"], t.get("talking_photo_name", "")) for t in d.get("talking_photos", [])]
    return out


def find(name_or_id):
    av = all_avatars()
    for a in av:
        if a[1] == name_or_id:
            return a
    hits = [a for a in av if norm(name_or_id) in norm(a[2])]
    if not hits:
        sys.exit(f"Không thấy avatar «{name_or_id}». Chạy: python tools/heygen_avatar.py list")
    return hits[0]


def make(who, audio, out):
    kind, aid, name = find(who)
    print(f"Avatar: {name} ({kind})")
    with open(audio, "rb") as f:
        up = call(UPLOAD, data=f.read(), ctype="audio/mpeg")
    asset = up["data"]["id"]
    character = ({"type": "avatar", "avatar_id": aid, "avatar_style": "normal"} if kind == "avatar"
                 else {"type": "talking_photo", "talking_photo_id": aid})
    job = call(f"{API}/v2/video/generate", {
        "video_inputs": [{"character": character, "voice": {"type": "audio", "audio_asset_id": asset}}],
        "dimension": {"width": 1080, "height": 1920}})
    vid = job["data"]["video_id"]
    print(f"Đã gửi HeyGen, video_id {vid}. Đang chờ dựng…")
    for _ in range(120):  # tối đa ~20 phút
        time.sleep(10)
        st = call(f"{API}/v1/video_status.get?video_id={vid}")["data"]
        if st.get("status") == "completed":
            urllib.request.urlretrieve(st["video_url"], out)
            print(f"Xong: {out}")
            return out
        if st.get("status") == "failed":
            raise RuntimeError(f"HeyGen dựng lỗi: {st.get('error')}")
    raise RuntimeError("Quá 20 phút HeyGen chưa dựng xong")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    a = sys.argv[1:]
    if a[:1] == ["list"]:
        q = norm(a[1]) if len(a) > 1 else ""
        for kind, aid, name in all_avatars():
            if q in norm(name):
                print(f"{kind:14} {aid}  {name}")
    elif a[:1] == ["make"] and len(a) == 4:
        make(a[1], a[2], a[3])
    else:
        print(__doc__)
