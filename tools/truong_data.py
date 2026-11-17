"""Dữ liệu trường từ Google Sheet của bộ phận du học (nguồn cho series review trường).

  python tools/truong_data.py update            # tải lại tất cả tab → noi-bo/truong-hoc/*.csv
  python tools/truong_data.py tim Catholic      # in mọi dòng có tên trường (mọi tab), kèm tên cột

Id sheet và danh sách tab ở data/truong_sheet.json (không lên Git vì sheet có học phí, cọc, ghi chú nội bộ).
Sheet phải để chế độ "ai có link đều xem được" thì mới tải được kiểu này.
"""
import csv
import glob
import json
import os
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONF = os.path.join(ROOT, "data", "truong_sheet.json")
OUT = os.path.join(ROOT, "noi-bo", "truong-hoc")


def update():
    c = json.load(open(CONF, encoding="utf-8"))
    os.makedirs(OUT, exist_ok=True)
    for name, gid in c["tabs"].items():
        url = f"https://docs.google.com/spreadsheets/d/{c['id']}/export?format=csv&gid={gid}"
        data = urllib.request.urlopen(url, timeout=60).read()
        open(os.path.join(OUT, f"{name}.csv"), "wb").write(data)
        print(f"{name}: {len(data) // 1024} KB")


def find(name):
    q = name.upper()
    for f in sorted(glob.glob(os.path.join(OUT, "*.csv"))):
        rows = list(csv.reader(open(f, encoding="utf-8")))
        hdr = next((r for r in rows if any("Tên trường" in x for x in r)), None)
        if not hdr:
            continue
        for r in rows:
            if q in " ".join(r).upper():
                print(f"===== {os.path.basename(f)}")
                for h, v in zip(hdr, r):
                    if v.strip():
                        print(f"[{h.replace(chr(10), ' ')[:30]}] {v.replace(chr(10), ' / ')}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    a = sys.argv[1:]
    if a[:1] == ["update"]:
        update()
    elif a[:1] == ["tim"] and len(a) > 1:
        find(" ".join(a[1:]))
    else:
        print(__doc__)
