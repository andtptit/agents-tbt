"""Vbee TTS for video voiceovers: one request for the whole script, one clean clip per line.

Usage:
  python tools/vbee_tts.py ENV_FILE VOICE_KEY OUT_DIR SPEED name1 "line 1" [name2 "line 2" ...]

  -> OUT_DIR/name1.mp3, OUT_DIR/name2.mp3, ... and OUT_DIR/voice.json (durations)

Reads `id`, `token` and the voice code (VOICE_KEY, e.g. voice_id_dh) from the .env file;
never prints them.

Why it works this way: Vbee cuts off the last syllable of every file it returns, while
sentences *inside* a file end with a natural decay. So all lines go in one request, each as
its own paragraph with a long (1.2 s) paragraph pause, followed by a throwaway pad line. The
file is then split in the middle of those long pauses: every real line keeps its natural
ending and only the pad line (which we discard) is truncated. The spoken text is never altered.
"""
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request

import numpy as np

PAD_LINE = "Xin cảm ơn các bạn đã theo dõi."
PARAGRAPH_BREAK = 1.2  # seconds Vbee inserts between lines
SPLIT_MIN_GAP = 0.9    # a silence this long can only be a paragraph break
HEAD_KEEP = 0.05       # silence kept before a line
TAIL_KEEP = 0.30       # silence kept after a line (lets the last word ring out)
FADE_IN, FADE_OUT = 0.01, 0.04

env_file, voice_key, out_dir, speed = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4])
pairs = sys.argv[5:]
names, lines = pairs[0::2], pairs[1::2]
assert names and len(names) == len(lines), "give name/text pairs"
os.makedirs(out_dir, exist_ok=True)

env = {}
for row in open(env_file, encoding="utf-8"):
    row = row.strip()
    if row and not row.startswith("#") and "=" in row:
        k, v = row.split("=", 1)
        env[k.strip()] = v.strip().strip('"').strip("'")
H = {"Content-Type": "application/json", "Authorization": "Bearer " + env["token"], "App-Id": env["id"]}


def call(url, body=None):
    req = urllib.request.Request(url, data=json.dumps(body).encode() if body else None,
                                 method="POST" if body else "GET", headers=H)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        print("HTTP", e.code, e.read()[:400].decode("utf-8", "replace"))
        sys.exit(1)


def ensure_end_punct(s):
    s = s.strip()
    return s if s[-1] in ".!?…" else s + "."


script = "\n".join([ensure_end_punct(t) for t in lines] + [PAD_LINE])
res = call("https://api.vbee.vn/v1/tts", {
    "text": script, "voiceCode": env[voice_key], "mode": "async",
    "outputFormat": "mp3", "bitrate": 128, "speed": speed,
    "clientPause": {"paragraphBreak": PARAGRAPH_BREAK},
    # Required by the API; the result is polled below, so point it at an unused local address.
    "webhookUrl": "https://127.0.0.1/vbee-callback-unused"})
rid = res.get("requestId")
raw_path = os.path.join(out_dir, "_vbee_raw.mp3")
for _ in range(120):
    time.sleep(2)
    r = call(f"https://api.vbee.vn/v1/tts/requests/{rid}")
    if r.get("status") == "COMPLETED":
        urllib.request.urlretrieve(r["audioLink"], raw_path)
        break
    if r.get("status") not in ("PROCESSING", "QUEUED", "PENDING", None):
        print("STATUS", json.dumps(r)[:300])
        sys.exit(1)
else:
    print("TIMEOUT")
    sys.exit(1)

sr = 24000
pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", raw_path, "-ac", "1", "-ar", str(sr), "-f", "s16le", "-"],
                     capture_output=True, check=True).stdout
a = np.frombuffer(pcm, dtype=np.int16).astype(float) / 32768
step = 0.01
win = int(step * sr)
db = np.array([20 * np.log10(np.sqrt(np.mean(a[i:i + win] ** 2)) + 1e-9) for i in range(0, len(a) - win, win)])
loud = np.where(db > -60)[0]
speech_start = loud[0] * step if len(loud) else 0.0

gaps, i, quiet = [], 0, db < -60
while i < len(quiet):
    if quiet[i]:
        j = i
        while j < len(quiet) and quiet[j]:
            j += 1
        if (j - i) * step >= SPLIT_MIN_GAP and i > 0 and j < len(quiet):
            gaps.append((i * step, j * step))
        i = j
    else:
        i += 1

if len(gaps) != len(lines):
    print(f"ERROR expected {len(lines)} paragraph pauses, found {len(gaps)}: {gaps}")
    sys.exit(1)

bounds = [speech_start] + [g[1] for g in gaps[:-1]]
info = {}
for n, name in enumerate(names):
    start = max(0.0, bounds[n] - HEAD_KEEP)
    end = min(gaps[n][0] + TAIL_KEEP, gaps[n][1])
    dur = end - start
    out = os.path.join(out_dir, name + ".mp3")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{start:.3f}", "-t", f"{dur:.3f}", "-i", raw_path,
                    "-af", f"afade=t=in:d={FADE_IN},afade=t=out:st={dur - FADE_OUT:.3f}:d={FADE_OUT}",
                    "-b:a", "192k", out], check=True)
    info[name] = {"text": lines[n], "duration": round(dur, 3)}
    print(f"OK {out} {dur:.2f}s")
os.remove(raw_path)
json.dump(info, open(os.path.join(out_dir, "voice.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
