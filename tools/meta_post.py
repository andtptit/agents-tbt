"""Đăng Reels lên Facebook Page qua Meta Graph API.

Lệnh:
  python tools/meta_post.py setup ["Tên page" | page_id]
      Đổi META_USER_TOKEN (ngắn hạn, lấy ở Graph API Explorer) sang token dài hạn, lấy token của
      Page và ghi vào .env (META_PAGE_ID, META_PAGE_NAME, META_PAGE_TOKEN). Không in token ra.
  python tools/meta_post.py check
      Kiểm tra token Page: quyền, hạn dùng.
  python tools/meta_post.py post VIDEO.mp4 "Mô tả" [DRAFT|PUBLISHED|SCHEDULED] [unix_time]
      Đăng Reels. DRAFT = chưa công khai (để thử).

Cần trong .env: META_APP_ID, META_APP_SECRET, META_USER_TOKEN (cho setup).
"""
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(ROOT, ".env")
GRAPH = "https://graph.facebook.com/v23.0"


def load_env():
    env = {}
    for row in open(ENV_PATH, encoding="utf-8"):
        row = row.strip()
        if row and not row.startswith("#") and "=" in row:
            k, v = row.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def set_env(key, value):
    rows = open(ENV_PATH, encoding="utf-8").read().splitlines()
    rows = [r for r in rows if not r.strip().startswith(key + "=")]
    rows.append(f"{key}={value}")
    open(ENV_PATH, "w", encoding="utf-8").write("\n".join(rows) + "\n")


def http(method, url, params=None, data=None, headers=None, timeout=120):
    if params:
        url += ("&" if "?" in url else "?") + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, data=data, method=method, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        body = e.read()
        try:
            err = json.loads(body).get("error", {})
            raise RuntimeError(f"Meta lỗi {e.code}: {err.get('message')} (code {err.get('code')}, "
                               f"subcode {err.get('error_subcode')})")
        except json.JSONDecodeError:
            raise RuntimeError(f"Meta lỗi {e.code}: {body[:300]!r}")


def setup():
    env = load_env()
    if env.get("META_APP_SECRET") and env.get("META_APP_ID"):
        long = http("GET", f"{GRAPH}/oauth/access_token", {
            "grant_type": "fb_exchange_token", "client_id": env["META_APP_ID"],
            "client_secret": env["META_APP_SECRET"], "fb_exchange_token": env["META_USER_TOKEN"]})["access_token"]
    else:
        print("⚠ Chưa có META_APP_SECRET: dùng tạm token ngắn hạn (hết hạn sau vài giờ).")
        long = env["META_USER_TOKEN"]
    pages = http("GET", f"{GRAPH}/me/accounts", {"fields": "id,name,access_token,tasks", "access_token": long})
    items = pages.get("data", [])
    if not items:
        sys.exit("Không thấy Page nào. Khi tạo token, nhớ tick chọn page test trong cửa sổ xin quyền.")
    for i, p in enumerate(items):
        print(f"[{i}] {p['name']} (id {p['id']}) — quyền: {', '.join(p.get('tasks', []))}")
    want = (sys.argv[2] if len(sys.argv) > 2 else load_env().get("META_PAGE_ID", "")).strip().lower()
    p = next((x for x in items if want and (x["id"] == want or x["name"].lower() == want)), items[0])
    set_env("META_USER_TOKEN_LONG", long)
    set_env("META_PAGE_ID", p["id"])
    set_env("META_PAGE_NAME", p["name"].replace("\n", " "))
    set_env("META_PAGE_TOKEN", p["access_token"])
    print(f"Đã lưu token Page «{p['name']}» vào .env.")


def check():
    env = load_env()
    app_tok = (f"{env['META_APP_ID']}|{env['META_APP_SECRET']}" if env.get("META_APP_SECRET")
               else env["META_PAGE_TOKEN"])
    info = http("GET", f"{GRAPH}/debug_token", {"input_token": env["META_PAGE_TOKEN"], "access_token": app_tok})["data"]
    exp = info.get("expires_at")
    print("Page:", env.get("META_PAGE_NAME"), env.get("META_PAGE_ID"))
    print("Hợp lệ:", info.get("is_valid"), "| Loại:", info.get("type"))
    print("Hết hạn:", "không hết hạn" if not exp else time.strftime("%Y-%m-%d %H:%M", time.localtime(exp)))
    print("Quyền:", ", ".join(info.get("scopes", [])))


def post_reel(video_path, description, state="DRAFT", scheduled=None, page_id=None, token=None):
    env = load_env()
    page_id = page_id or env["META_PAGE_ID"]
    token = token or env["META_PAGE_TOKEN"]
    start = http("POST", f"{GRAPH}/{page_id}/video_reels", {"upload_phase": "start", "access_token": token})
    vid, upload_url = start["video_id"], start["upload_url"]
    data = open(video_path, "rb").read()
    up = http("POST", upload_url, data=data, headers={"Authorization": f"OAuth {token}", "offset": "0",
                                                       "file_size": str(len(data))}, timeout=600)
    if not up.get("success"):
        raise RuntimeError(f"Tải video lên lỗi: {up}")
    params = {"upload_phase": "finish", "video_id": vid, "video_state": state,
              "description": description, "access_token": token}
    if state == "SCHEDULED":
        params["scheduled_publish_time"] = str(int(scheduled))
    fin = http("POST", f"{GRAPH}/{page_id}/video_reels", params)
    if not fin.get("success"):
        raise RuntimeError(f"Hoàn tất đăng lỗi: {fin}")
    # Chờ Meta xử lý video để lấy trạng thái và đường link
    status, link = {}, None
    for _ in range(30):
        time.sleep(5)
        st = http("GET", f"{GRAPH}/{vid}", {"fields": "status,permalink_url", "access_token": token})
        status, link = st.get("status", {}), st.get("permalink_url")
        if status.get("video_status") in ("ready", "error") or status.get("publishing_phase", {}).get("status") in (
                "complete", "error"):
            break
    return {"video_id": vid, "state": state, "status": status, "link": ("https://www.facebook.com" + link)
            if link and link.startswith("/") else link}


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "setup":
        setup()
    elif cmd == "check":
        check()
    elif cmd == "post":
        r = post_reel(sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else "DRAFT",
                      sys.argv[5] if len(sys.argv) > 5 else None)
        print(json.dumps(r, ensure_ascii=False, indent=1))
    else:
        sys.exit(__doc__)
