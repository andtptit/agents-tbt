"""Research fanpage: kéo bài đăng + Reels + số liệu của một page (CHỈ ĐỌC, không đăng gì).

  python tools/meta_research.py duhoc [số_tháng=6]
  python tools/meta_research.py tienghan [số_tháng=6]

Dùng META_READ_TOKEN trong .env (token người dùng dài hạn, có quyền đọc 2 page chính).
KHÔNG dùng/đổi META_PAGE_* (token đăng bài lên page test).
Kết quả lưu ở noi-bo/research/<page>_<ngày>.json và .csv (noi-bo/ không đưa lên Git: bài đăng có thể có
tên/ảnh học viên, bình luận khách).
"""
import csv
import json
import os
import sys
import time
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import meta_post as m  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "noi-bo", "research")
PAGES = {"duhoc": ("111519684743413", "Du Học Thầy Tư"), "tienghan": ("892203107517134", "Tiếng Hàn Thầy Tư")}
REEL_METRICS = ["blue_reels_play_count", "fb_reels_total_plays", "post_video_avg_time_watched",
                "post_impressions_unique", "post_video_followers"]
POST_METRICS = ["post_impressions_unique", "post_clicks", "post_media_view"]


def get(path, params, token):
    params = dict(params, access_token=token)
    return m.http("GET", f"{m.GRAPH}/{path}", params)


def paged(path, params, token, since_ts, time_key="created_time", cap=500):
    out, url_params = [], dict(params)
    while True:
        r = get(path, url_params, token)
        batch = r.get("data", [])
        for x in batch:
            t = x.get(time_key) or x.get("updated_time")
            if t and datetime.fromisoformat(t.replace("+0000", "+00:00")).timestamp() < since_ts:
                return out
            out.append(x)
        nxt = (r.get("paging") or {}).get("cursors", {}).get("after")
        if not batch or not nxt or len(out) >= cap or not (r.get("paging") or {}).get("next"):
            return out
        url_params["after"] = nxt


def insights(obj_id, metrics, token, edge="insights"):
    vals = {}
    for metric in metrics:  # từng chỉ số một: chỉ số nào Meta đã bỏ thì bỏ qua, không làm hỏng cả lượt
        try:
            for d in get(f"{obj_id}/{edge}", {"metric": metric}, token).get("data", []):
                v = (d.get("values") or [{}])[0].get("value")
                vals[d["name"]] = v
        except Exception:  # noqa: BLE001
            pass
    return vals


def run(key, months=6):
    page_id, page_name = PAGES[key]
    env = m.load_env()
    user_tok = env.get("META_READ_TOKEN")
    if not user_tok:
        sys.exit("Thiếu META_READ_TOKEN trong .env")
    tok = get(page_id, {"fields": "access_token"}, user_tok)["access_token"]
    since = (datetime.now() - timedelta(days=30 * months)).timestamp()
    info = get(page_id, {"fields": "name,followers_count,fan_count"}, tok)

    print(f"Đang kéo {page_name} ({months} tháng)…")
    posts = paged(f"{page_id}/published_posts", {
        "fields": "id,created_time,message,status_type,permalink_url,attachments{media_type,type,title},"
                  "shares,reactions.summary(total_count).limit(0),comments.summary(total_count).limit(0)",
        "limit": 50}, tok, since)
    reels = paged(f"{page_id}/video_reels", {"fields": "id,description,created_time,length,permalink_url", "limit": 50},
                  tok, since)
    print(f"  {len(posts)} bài đăng, {len(reels)} Reels. Đang lấy số liệu…")

    rows = []
    for p in posts:
        att = ((p.get("attachments") or {}).get("data") or [{}])[0]
        rows.append({
            "kind": "post", "id": p["id"], "date": p["created_time"][:10], "type": att.get("media_type") or p.get("status_type"),
            "text": (p.get("message") or "").strip(), "link": p.get("permalink_url"),
            "reactions": (p.get("reactions") or {}).get("summary", {}).get("total_count", 0),
            "comments": (p.get("comments") or {}).get("summary", {}).get("total_count", 0),
            "shares": (p.get("shares") or {}).get("count", 0),
            **insights(p["id"], POST_METRICS, tok)})
        time.sleep(0.05)
    for r in reels:
        rows.append({
            "kind": "reel", "id": r["id"], "date": r["created_time"][:10], "type": "reel",
            "text": (r.get("description") or "").strip(), "link": r.get("permalink_url"), "length_s": r.get("length"),
            **insights(r["id"], REEL_METRICS, tok, edge="video_insights")})
        time.sleep(0.05)

    os.makedirs(OUT, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d")
    base = os.path.join(OUT, f"{key}_{stamp}")
    json.dump({"page": info, "months": months, "fetched_at": datetime.now().isoformat(timespec="minutes"), "rows": rows},
              open(base + ".json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    cols = sorted({k for r in rows for k in r}, key=lambda k: ["kind", "date", "type", "text"].index(k)
                  if k in ("kind", "date", "type", "text") else 9)
    with open(base + ".csv", "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow({k: (json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else v) for k, v in r.items()})
    print(f"Đã lưu {base}.json và .csv ({len(rows)} dòng). Theo dõi: {info.get('followers_count')}")
    return base + ".json"


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) < 2 or sys.argv[1] not in PAGES:
        sys.exit(__doc__)
    run(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 6)
