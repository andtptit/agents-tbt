"""Trình giám sát: giữ bot Telegram luôn chạy (tự khởi động lại nếu bot dừng).

Được Windows tự chạy khi đăng nhập (file .vbs trong thư mục Startup), không hiện cửa sổ.
Chạy tay:  pythonw tools/giam_sat_bot.py
Nhật ký:   data/bot.log
Chỉ cho phép MỘT bản chạy cùng lúc (khóa cổng nội bộ 47821), tránh hai bot cùng nhận tin.
"""
import os
import socket
import subprocess
import sys
import time
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG = os.path.join(ROOT, "data", "bot.log")
os.makedirs(os.path.dirname(LOG), exist_ok=True)


def log(msg):
    with open(LOG, "a", encoding="utf-8") as fh:
        fh.write(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] [giám sát] {msg}\n")


# Một bản duy nhất
lock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    lock.bind(("127.0.0.1", 47821))
except OSError:
    sys.exit(0)  # đã có bản khác đang chạy

python = sys.executable.replace("pythonw.exe", "python.exe")
flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
log("Bắt đầu giám sát bot.")
while True:
    # Cắt log khi quá 5 MB
    if os.path.exists(LOG) and os.path.getsize(LOG) > 5_000_000:
        os.replace(LOG, LOG + ".old")
    with open(LOG, "a", encoding="utf-8") as out:
        p = subprocess.Popen([python, "-I", "-u", os.path.join(ROOT, "tools", "telegram_bot.py"), "run"],
                             cwd=ROOT, stdout=out, stderr=subprocess.STDOUT, creationflags=flags)
        code = p.wait()
    log(f"Bot dừng (mã {code}). Khởi động lại sau 10 giây.")
    time.sleep(10)
