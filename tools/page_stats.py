"""Số liệu fanpage cho báo cáo Telegram (CHỈ ĐỌC qua Meta Graph API).

  python tools/page_stats.py          -> in thử phần báo cáo fanpage

Dùng META_READ_TOKEN (token đọc, thấy 2 page chính) — chỉ gọi GET, không đăng gì.
Video do hệ thống đăng (đơn có fb_video_id) đọc bằng META_PAGE_TOKEN của page test.

Chỉ số dùng được (đã thử 17/11/2026): page_media_view (lượt xem), page_total_media_view_unique (người xem),
page_views_total (lượt vào trang), page_daily_follows_unique / page_daily_unfollows_unique, page_video_views,
followers_count; Reels: blue_reels_play_count, post_video_avg_time_watched (mili giây).
Meta đã bỏ: page_impressions, page_fans, page_fan_adds_unique. page_post_engagements của page Tiếng Hàn luôn = 0
nên không dùng.
"""
import json
import os
import sys
import time
import unicodedata
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import meta_post as m  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = [("tienghan", "892203107517134", "Tiếng Hàn Thầy Tư"), ("duhoc", "111519684743413", "Du học Thầy Tư")]
DAY_METRICS = ["page_media_view", "page_total_media_view_unique", "page_views_total",
               "page_daily_follows_unique", "page_daily_unfollows_unique", "page_video_views"]
DROP_ALERT = 0.30  # lượt xem giảm hơn 30% so với trung bình 7 ngày trước -> cảnh báo


def get(path, params, token):
    return m.http("GET", f"{m.GRAPH}/{path}", dict(params, access_token=token), timeout=60)


def fmt(n):
    return f"{int(round(n)):,}".replace(",", ".")


def sec(x):
    return f"{x:.1f}".replace(".", ",") + "s"


def daily(pid, tok):
    """{metric: [(ngày, giá trị), …]} cho 8 ngày gần nhất (ngày cuối = hôm qua)."""
    since = int((datetime.now() - timedelta(days=9)).timestamp())
    until = int(datetime.now().timestamp())
    out = {}
    for met in DAY_METRICS:
        try:
            data = get(f"{pid}/insights", {"metric": met, "period": "day", "since": since, "until": until}, tok)["data"]
            vals = data[0]["values"] if data else []
            # end_time là mốc kết thúc của ngày -> ngày của số liệu = end_time - 1 ngày
            out[met] = [((datetime.fromisoformat(v["end_time"].replace("+0000", "+00:00")) - timedelta(days=1)).date(),
                         v.get("value") or 0) for v in vals]
        except Exception:  # noqa: BLE001  — chỉ số lỗi thì bỏ qua, không làm hỏng cả báo cáo
            out[met] = []
    return out


def top_reels(pid, tok, days=7, n=3):
    since = (datetime.now() - timedelta(days=days)).timestamp()
    reels = get(f"{pid}/video_reels", {"fields": "id,description,created_time", "limit": 40}, tok).get("data", [])
    rows = []
    for r in reels:
        if datetime.fromisoformat(r["created_time"].replace("+0000", "+00:00")).timestamp() < since:
            continue
        try:
            ins = {d["name"]: (d.get("values") or [{}])[0].get("value") for d in get(
                f"{r['id']}/video_insights", {"metric": "blue_reels_play_count,post_video_avg_time_watched"}, tok)["data"]}
        except Exception:  # noqa: BLE001
            continue
        # Chữ "in đậm" kiểu 𝐁𝐢́ 𝐦𝐚̣̂𝐭 trên Facebook -> chữ thường để đọc được
        title = " ".join(unicodedata.normalize("NFKC", r.get("description") or "(không mô tả)").split())
        rows.append((ins.get("blue_reels_play_count") or 0, (ins.get("post_video_avg_time_watched") or 0) / 1000, title))
        time.sleep(0.05)
    return sorted(rows, reverse=True)[:n], len(rows)


def short(text, n=45):
    """Cắt ở chỗ hết từ, thêm dấu … (không cắt giữa chữ)."""
    text = " ".join(text.split())
    if len(text) <= n:
        return text
    cut = text[:n].rsplit(" ", 1)[0]
    return cut.rstrip(",.;:-–— ") + "…"


def page_data(key, pid, name, user_tok):
    """Số liệu có cấu trúc của một page (dùng cho cả chữ và thẻ ảnh)."""
    tok = get(pid, {"fields": "access_token"}, user_tok)["access_token"]
    d = daily(pid, tok)
    views = d.get("page_media_view") or []
    out = {"key": key, "name": name, "followers": get(pid, {"fields": "followers_count"}, tok).get("followers_count") or 0,
           "views_series": views[-8:], "ok": bool(views)}
    if not views:
        return out

    def last(met):
        s = d.get(met) or []
        return s[-1][1] if s else 0

    day, v = views[-1]
    prev = [x for _, x in views[-8:-1]]
    avg = sum(prev) / len(prev) if prev else 0
    out.update(day=day, views=v, avg=avg, change=(v - avg) / avg if avg else 0,
               reach=last("page_total_media_view_unique"), visits=last("page_views_total"),
               follows=last("page_daily_follows_unique"), unfollows=last("page_daily_unfollows_unique"))
    try:
        out["top"], out["reel_count"] = top_reels(pid, tok)
    except Exception:  # noqa: BLE001
        out["top"], out["reel_count"] = [], 0
    return out


def page_section(key, pid, name, user_tok, data=None):
    p = data or page_data(key, pid, name, user_tok)
    alerts = []
    if not p["ok"]:
        return [f"━ {name}", "  (Chưa lấy được số liệu hôm qua)"], alerts
    ch, net = p["change"], p["follows"] - p["unfollows"]
    trend = f"{'+' if ch >= 0 else '−'}{abs(ch) * 100:.0f}% so với TB 7 ngày" if p["avg"] else ""
    lines = [f"━ {name} ({p['day']:%d/%m})",
             f"  👁 {fmt(p['views'])} lượt xem ({trend}) · {fmt(p['reach'])} người",
             f"  👥 +{p['follows']} / −{p['unfollows']} → {'+' if net >= 0 else ''}{net} · tổng {fmt(p['followers'])}"
             f" · {fmt(p['visits'])} lượt vào trang"]
    if p.get("top"):
        lines.append(f"  🏆 Top Reels 7 ngày ({p['reel_count']} video):")
        for plays, avg_s, title in p["top"]:
            lines.append(f"     • {fmt(plays)} lượt phát · xem TB {sec(avg_s)} — {short(title)}")
    if p["avg"] and ch <= -DROP_ALERT:
        alerts.append(f"⚠️ {name}: lượt xem ngày {p['day']:%d/%m} giảm {abs(ch) * 100:.0f}% so với trung bình 7 ngày "
                      f"({fmt(p['views'])} so với {fmt(p['avg'])}).")
    return lines, alerts


def system_videos(orders, env):
    """Hiệu quả các video do hệ thống đăng (đang đăng lên page test)."""
    tok = env.get("META_PAGE_TOKEN")
    rows = []
    for code, o in orders.items():
        vid = o.get("fb_video_id")
        if not vid or o.get("status") != "Đã đăng" or not tok:
            continue
        try:
            ins = {d["name"]: (d.get("values") or [{}])[0].get("value") for d in get(
                f"{vid}/video_insights", {"metric": "blue_reels_play_count,post_video_avg_time_watched"}, tok)["data"]}
            rows.append(f"     • {code}: {fmt(ins.get('blue_reels_play_count') or 0)} lượt phát · "
                        f"xem TB {sec((ins.get('post_video_avg_time_watched') or 0) / 1000)}")
        except Exception:  # noqa: BLE001
            continue
    return rows[-5:]


def token_warning(env):
    try:
        info = get("debug_token", {"input_token": env["META_READ_TOKEN"]},
                   f"{env['META_APP_ID']}|{env['META_APP_SECRET']}")["data"]
    except Exception:  # noqa: BLE001
        return "⚠️ Không kiểm tra được token đọc số liệu Meta."
    if not info.get("is_valid"):
        return "🔴 Token đọc số liệu Meta đã hết hiệu lực — cần lấy lại (Graph API Explorer)."
    exp = info.get("data_access_expires_at")
    if exp:
        days = (exp - time.time()) / 86400
        if days < 21:
            return (f"⚠️ Quyền đọc số liệu Meta hết hạn sau {days:.0f} ngày "
                    f"({datetime.fromtimestamp(exp):%d/%m/%Y}) — cần đăng nhập lại để gia hạn.")
    return None


def build(orders=None):
    """Trả về (danh sách dòng báo cáo, danh sách cảnh báo)."""
    env = m.load_env()
    if not env.get("META_READ_TOKEN"):
        return ["(Chưa có META_READ_TOKEN — bỏ qua số liệu fanpage)"], []
    lines, alerts = ["📈 FANPAGE (số liệu hôm qua)"], []
    for key, pid, name in PAGES:
        try:
            sec, al = page_section(key, pid, name, env["META_READ_TOKEN"])
        except Exception as e:  # noqa: BLE001
            sec, al = [f"━ {name}", f"  (Lỗi lấy số liệu: {str(e)[:80]})"], []
        lines += sec
        alerts += al
    sysv = system_videos(orders or {}, env)
    if sysv:
        lines.append(f"━ Video hệ thống đã đăng (page test «{env.get('META_PAGE_NAME', '')}»):")
        lines += sysv
    w = token_warning(env)
    if w:
        lines.append(w)
    return lines, alerts


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    orders = json.load(open(os.path.join(ROOT, "data", "orders.json"), encoding="utf-8"))
    t0 = time.time()
    lines, alerts = build(orders)
    print("\n".join(lines))
    print("\nCẢNH BÁO:", alerts or "không có")
    print(f"(mất {time.time() - t0:.0f} giây)")
