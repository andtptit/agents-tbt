"""Màn hình theo dõi hệ thống (chạy trong cửa sổ terminal, Ctrl+C để thoát).

  python tools/theo_doi.py

Mỗi 3 giây: in ra mỗi khi trạng thái một đơn/video thay đổi, và cho biết Claude có đang chạy
(viết kịch bản) hay không.
"""
import json
import os
import subprocess
import sys
import time
from datetime import datetime

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILES = {"Đơn": os.path.join(ROOT, "data", "orders.json"), "Video": os.path.join(ROOT, "data", "review_queue.json")}


def read(path):
    try:
        return json.load(open(path, encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return {}


def claude_running():
    try:
        out = subprocess.run(["tasklist", "/FI", "IMAGENAME eq claude.exe", "/FO", "CSV", "/NH"],
                             capture_output=True, text=True, timeout=10).stdout
        return out.lower().count("claude.exe")
    except Exception:  # noqa: BLE001
        return 0


print("=== THEO DÕI NHÀ MÁY NỘI DUNG THẦY TƯ === (Ctrl+C để thoát)\n")
last = {}
last_claude = None
while True:
    t = datetime.now().strftime("%H:%M:%S")
    for kind, path in FILES.items():
        for code, item in read(path).items():
            st = item.get("status", "")
            key = (kind, code)
            if last.get(key) != st:
                extra = f" — {item.get('topic')}" if item.get("topic") else ""
                err = f"  ⚠ {item['error']}" if item.get("error") else ""
                print(f"[{t}] {kind} {code}: {st}{extra}{err}", flush=True)
                last[key] = st
    n = claude_running()
    busy = n > 0
    if busy != last_claude:
        print(f"[{t}] {'🤖 Claude ĐANG CHẠY (viết kịch bản)…' if busy else '💤 Claude đang nghỉ'}", flush=True)
        last_claude = busy
    time.sleep(3)
