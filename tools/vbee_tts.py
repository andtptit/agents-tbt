"""Vbee TTS for video voiceovers: one clean clip per line, natural endings.

Usage:
  python tools/vbee_tts.py ENV_FILE VOICE_KEY OUT_DIR SPEED name1 "line 1" [name2 "line 2" ...]

  -> OUT_DIR/name1.mp3, OUT_DIR/name2.mp3, ... and OUT_DIR/voice.json (durations)

Reads `id`, `token` and the voice code (VOICE_KEY, e.g. voice_id_dh) from the .env file;
never prints them.

Why it works this way: Vbee cuts off the last syllable of every file it returns (the audio
stops dead), while sentences *inside* a file end with a natural decay. Vbee also does not
reliably honour paragraph pauses, so lines cannot be split out of one long file.
So each line is requested on its own (in parallel), followed by a short pad sentence with no
commas. The cut is made inside the LAST sentence pause of the file — the pause between the
real line and the pad — so the real line keeps its natural ending and only the pad (discarded)
is truncated. Comma pauses are much shorter than sentence pauses and are never chosen.
The spoken text is never altered.
"""
import json
import os
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.request

import numpy as np

PAD_LINE = "Xin cảm ơn các bạn đã theo dõi."
SENTENCE_BREAK = 0.5   # seconds Vbee pauses at "." (we set it explicitly)
COMMA_BREAK = 0.2      # seconds Vbee pauses at ","
MIN_SENTENCE_GAP = 0.36  # a silence at least this long is a sentence pause, never a comma
PAD_MAX = 3.5          # the pad sentence never lasts longer than this
HEAD_KEEP = 0.05
TAIL_KEEP = 0.30
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
        raise RuntimeError(f"HTTP {e.code} {e.read()[:300].decode('utf-8', 'replace')}")


def ensure_end_punct(s):
    s = s.strip()
    return s if s[-1] in ".!?…" else s + "."


def synth(text, raw_path):
    res = call("https://api.vbee.vn/v1/tts", {
        "text": ensure_end_punct(text) + " " + PAD_LINE, "voiceCode": env[voice_key], "mode": "async",
        "outputFormat": "mp3", "bitrate": 128, "speed": speed,
        "clientPause": {"sentenceBreak": SENTENCE_BREAK, "mediumBreak": COMMA_BREAK},
        # Required by the API; the result is polled below, so point it at an unused local address.
        "webhookUrl": "https://127.0.0.1/vbee-callback-unused"})
    rid = res.get("requestId")
    for _ in range(150):
        time.sleep(2)
        r = call(f"https://api.vbee.vn/v1/tts/requests/{rid}")
        if r.get("status") == "COMPLETED":
            urllib.request.urlretrieve(r["audioLink"], raw_path)
            return
        if r.get("status") not in ("PROCESSING", "QUEUED", "PENDING", None):
            raise RuntimeError(f"Vbee status {json.dumps(r)[:200]}")
    raise RuntimeError("Vbee timeout")


def cut_line(raw_path, out_path):
    sr, step = 24000, 0.01
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", raw_path, "-ac", "1", "-ar", str(sr), "-f", "s16le", "-"],
                         capture_output=True, check=True).stdout
    a = np.frombuffer(pcm, dtype=np.int16).astype(float) / 32768
    win = int(step * sr)
    db = np.array([20 * np.log10(np.sqrt(np.mean(a[i:i + win] ** 2)) + 1e-9) for i in range(0, len(a) - win, win)])
    total = len(a) / sr
    loud = np.where(db > -55)[0]
    start = max(0.0, (loud[0] * step if len(loud) else 0.0) - HEAD_KEEP)
    gaps, i, quiet = [], 0, db < -50
    while i < len(quiet):
        if quiet[i]:
            j = i
            while j < len(quiet) and quiet[j]:
                j += 1
            if (j - i) * step >= MIN_SENTENCE_GAP and i > 0 and j < len(quiet):
                gaps.append((i * step, j * step))
            i = j
        else:
            i += 1
    if not gaps or total - gaps[-1][1] > PAD_MAX:
        raise RuntimeError(f"không tìm thấy chỗ nghỉ trước câu đệm (gaps={gaps}, total={total:.2f})")
    g0, g1 = gaps[-1]
    end = min(g0 + TAIL_KEEP, g1)
    dur = end - start
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{start:.3f}", "-t", f"{dur:.3f}", "-i", raw_path,
                    "-af", f"afade=t=in:d={FADE_IN},afade=t=out:st={dur - FADE_OUT:.3f}:d={FADE_OUT}",
                    "-b:a", "192k", out_path], check=True)
    return dur


results, errors = {}, {}


def work(name, text):
    raw = os.path.join(out_dir, f"_raw_{name}.mp3")
    for attempt in range(2):
        try:
            synth(text, raw)
            results[name] = round(cut_line(raw, os.path.join(out_dir, name + ".mp3")), 3)
            os.remove(raw)
            return
        except Exception as e:  # noqa: BLE001
            errors[name] = str(e)
    # keep raw for debugging if both attempts failed


threads = [threading.Thread(target=work, args=(n, t)) for n, t in zip(names, lines)]
for th in threads:
    th.start()
    time.sleep(0.3)  # be gentle with the API
for th in threads:
    th.join()

failed = [n for n in names if n not in results]
if failed:
    print("ERROR " + "; ".join(f"{n}: {errors.get(n)}" for n in failed))
    sys.exit(1)
info = {n: {"text": t, "duration": results[n]} for n, t in zip(names, lines)}
json.dump(info, open(os.path.join(out_dir, "voice.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
for n in names:
    print(f"OK {os.path.join(out_dir, n + '.mp3')} {results[n]:.2f}s")
