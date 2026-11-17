"""Danh mục footage trám cảnh của trung tâm (thư mục `Video-Trám cảnh-TBT/`) + chọn clip không lặp.

Tên file đã mô tả cảnh: QT-<NHÓM>-<GIAI ĐOẠN>-<CỠ CẢNH>-<số>_<mo-ta-khong-dau>.mp4
  python tools/footage_index.py build            # quét thư mục → data/footage_index.json (thời lượng, khổ)
  python tools/footage_index.py find tu-van ho-so # tìm clip theo từ khóa, ưu tiên clip ít dùng
Lịch sử dùng: data/footage_usage.json ({file: [mã video, ...]}) để các video trong series không lặp cảnh.
"""
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIB = os.path.join(ROOT, "Video-Trám cảnh-TBT")
INDEX = os.path.join(ROOT, "data", "footage_index.json")
USAGE = os.path.join(ROOT, "data", "footage_usage.json")
# Nhóm hợp với video du học (tư vấn, hồ sơ, lớp học, không gian trung tâm). Bỏ kế toán, lập trình, họp nội bộ.
GOOD_GROUPS = {"TUYENSINH", "HOSO", "DAOTAO", "CHUNG", "NEN", "DOINGU"}
SKIP_WORDS = ("code", "lap-trinh", "ke-toan", "excel")


def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                          "stream=width,height:format=duration", "-of", "json", path],
                         capture_output=True, text=True).stdout
    d = json.loads(out or "{}")
    st = (d.get("streams") or [{}])[0]
    return float(d.get("format", {}).get("duration", 0)), st.get("width", 0), st.get("height", 0)


def build():
    items = []
    for folder, _, files in os.walk(LIB):
        for f in sorted(files):
            if not f.lower().endswith(".mp4"):
                continue
            m = re.match(r"QT-([A-Z]+)-([A-Z]+)-([A-Z]+)-(\d+)_(.+)\.mp4$", f)
            group, phase, size, _, desc = m.groups() if m else ("?", "?", "?", "0", f[:-4])
            path = os.path.join(folder, f)
            dur, w, h = probe(path)
            items.append({"file": os.path.relpath(path, ROOT).replace("\\", "/"), "group": group, "phase": phase,
                          "size": size, "desc": desc.replace("-", " "), "duration": round(dur, 2),
                          "vertical": h > w, "w": w, "h": h,
                          "ok_du_hoc": group in GOOD_GROUPS and not any(s in desc for s in SKIP_WORDS)})
    os.makedirs(os.path.dirname(INDEX), exist_ok=True)
    json.dump(items, open(INDEX, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{len(items)} clip, {sum(i['ok_du_hoc'] for i in items)} hợp video du học → {INDEX}")


def usage():
    return json.load(open(USAGE, encoding="utf-8")) if os.path.exists(USAGE) else {}


def find(words, n=5, exclude=()):
    """Clip khớp nhiều từ khóa nhất, ít được dùng nhất, chưa nằm trong exclude."""
    idx = json.load(open(INDEX, encoding="utf-8"))
    use = usage()
    scored = []
    for it in idx:
        if not it["ok_du_hoc"] or it["file"] in exclude:
            continue
        text = f"{it['group']} {it['desc']}".lower()
        hit = sum(w.replace("-", " ") in text for w in words)
        if hit:
            scored.append((-hit, len(use.get(it["file"], [])), it["file"], it))
    scored.sort(key=lambda x: x[:3])
    return [s[3] for s in scored[:n]]


def mark_used(code, files):
    use = usage()
    for f in files:
        use.setdefault(f, [])
        if code not in use[f]:
            use[f].append(code)
    json.dump(use, open(USAGE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    a = sys.argv[1:]
    if a[:1] == ["build"]:
        build()
    elif a[:1] == ["find"]:
        for it in find(a[1:], 10):
            print(f"{it['duration']:5.1f}s {'dọc' if it['vertical'] else 'ngang'}  {it['file']}")
    else:
        print(__doc__)
