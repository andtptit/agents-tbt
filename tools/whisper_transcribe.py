"""Transcribe videos/audio to Vietnamese text with word timestamps (faster-whisper, GPU if available).

Usage:
  python tools/whisper_transcribe.py OUT_DIR file1.mp4 [file2.mp4 ...]

For each input writes OUT_DIR/<name>.txt (readable, one segment per line with [mm:ss])
and OUT_DIR/<name>.json (segments + words with start/end seconds).
"""
import glob
import json
import os
import site
import sys

sys.stdout.reconfigure(encoding="utf-8")

# CUDA libraries installed by pip (nvidia-cublas-cu12, nvidia-cudnn-cu12) must be on PATH on Windows.
for base in site.getsitepackages():
    dirs = glob.glob(os.path.join(base, "nvidia", "*", "bin"))
    if dirs:
        os.environ["PATH"] = os.pathsep.join(dirs) + os.pathsep + os.environ["PATH"]
        for d in dirs:
            os.add_dll_directory(d)

from faster_whisper import WhisperModel  # noqa: E402

# Domain words help Whisper spell what the channel actually says.
PROMPT = ("Tiếng Hàn Thầy Tư. TOPIK, TOPIK I, TOPIK II, TOPIK 3, TOPIK 4, TOPIK 5, TOPIK 6, sơ cấp, trung cấp, "
          "từ vựng Hán Hàn, ngữ pháp, Nghe, Đọc, Viết, câu 51, câu 52, câu 53, câu 54, giáo trình, lộ trình, "
          "du học Hàn Quốc, visa, EPS, E-learning, inbox, Thầy Tư.")

out_dir = sys.argv[1]
files = sys.argv[2:]
os.makedirs(out_dir, exist_ok=True)
try:
    model = WhisperModel("large-v3", device="cuda", compute_type="float16")
except Exception as e:  # no GPU: slower but works
    print("GPU unavailable, using CPU:", e)
    model = WhisperModel("medium", device="cpu", compute_type="int8")

for f in files:
    name = os.path.splitext(os.path.basename(f))[0]
    segs, info = model.transcribe(f, language="vi", word_timestamps=True, initial_prompt=PROMPT,
                                  vad_filter=True, beam_size=5)
    seg_list = []
    lines = []
    for s in segs:
        seg_list.append({"start": round(s.start, 2), "end": round(s.end, 2), "text": s.text.strip(),
                         "words": [{"w": w.word.strip(), "s": round(w.start, 2), "e": round(w.end, 2)}
                                   for w in (s.words or [])]})
        lines.append(f"[{int(s.start // 60):02d}:{s.start % 60:05.2f}] {s.text.strip()}")
    with open(os.path.join(out_dir, name + ".json"), "w", encoding="utf-8") as fh:
        json.dump({"file": os.path.basename(f), "duration": round(info.duration, 2), "segments": seg_list},
                  fh, ensure_ascii=False, indent=1)
    with open(os.path.join(out_dir, name + ".txt"), "w", encoding="utf-8") as fh:
        fh.write(f"# {os.path.basename(f)} ({info.duration:.1f}s)\n\n" + "\n".join(lines) + "\n")
    print(f"OK {name}: {len(seg_list)} segments, {info.duration:.1f}s")
