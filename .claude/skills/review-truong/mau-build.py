"""Series review trường – Đại học Keimyung (계명대학교). Dữ liệu: sheet + guideline 2027 Spring (doi-chieu.md).
Linh chỉ có ở s1, s6, s8 (câu lipsync); HeyGen chỉ dựng các câu đó (linh.mp3 → avatar.mp4, linh_map.json).
Chạy: python build.py"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "tools"))
from truong_build import (outro_end, outro_scene, prepare_assets, linh_segments, out, pop, rise, rows, scene, timing, video,  # noqa: E402
                          write_project)

L, VO_END = timing(HERE)
END = outro_end(VO_END)
prepare_assets(HERE)
st = lambda k: L[k]["start"]  # noqa: E731
S = []
SCENE_LINES = {"s1": ["l01", "l02"], "s6": ["l11"], "s8": ["l13", "l14"]}

# S1 Linh – hook phim trường
s, e = 0.0, st("l03") - 0.14
t2 = st("l02") - s
body = """    <div id="s1-a" class="center stack" style="top:1050px">
      <span id="s1-big" class="big" style="font-size:76px">TRƯỜNG TRONG PHIM</span>
      <span id="s1-pill" class="pill red">có thật đấy!</span>
    </div>
    <div id="s1-b" class="center stack" style="top:1050px">
      <span id="s1-big2" class="wbig" style="font-size:96px">VƯỜN SAO BĂNG</span>
      <span id="s1-pill2" class="pill">Quý ngài Ánh dương</span>
    </div>"""
js = (f'    tl.fromTo("#s1-big", {{ scale: 1.15 }}, {{ scale: 1, duration: 0.3, ease: "power3.out" }}, 0);\n'
      + pop("#s1-pill", 0.8) + out("#s1-a", t2 - 0.2) + pop("#s1-big2", t2 + 1.6) + rise("#s1-pill2", t2 + 2.6))
S.append(("s1", s, e - s, scene("s1", body, js)))

# S2 Campus gạch đỏ (YouTube chính thức)
s = st("l03") - 0.14; e = st("l05") - 0.1; d = e - s; t4 = st("l04") - s; c = d / 3
body = f"""    <div class="blue-bg"></div>
    <img class="logo" src="assets/logo/tt-tron.png" alt="Logo" />
    <div class="center" style="top:300px">
      <span id="s2-k" class="wbig" style="font-size:58px">ĐẠI HỌC</span>
      <span id="s2-t" class="big" style="font-size:132px">KEIMYUNG</span>
      <span id="s2-pin" class="pill yellow" style="margin-top:14px">● DAEGU · NHÓM TOP 1</span>
    </div>
    <div id="s2-a" class="center" style="top:720px">
      <span id="s2-p1" class="pill red sm">Tòa nhà gạch đỏ như phim</span>
    </div>
    <div id="s2-b" class="center" style="top:700px">
      <span id="s2-q1" class="pill white sm">Kinh doanh</span>
      <span id="s2-q2" class="pill white sm" style="margin-left:8px">Du lịch</span>
      <span id="s2-q3" class="pill white sm" style="margin-left:8px">Truyền thông</span><br>
      <span id="s2-q4" class="pill white sm" style="margin-top:16px">Kỹ thuật</span>
      <span id="s2-q5" class="pill white sm" style="margin-left:8px;margin-top:16px">Game</span>
      <span id="s2-q6" class="pill white sm" style="margin-left:8px;margin-top:16px">Thời trang</span>
    </div>
    <div class="window">
{video("s2-v1", "yt-1.mp4", 0, c, "")}{video("s2-v2", "yt-2.mp4", c, c, "")}{video("s2-v3", "yt-3.mp4", 2 * c, d - 2 * c, "")}    </div>
    <div class="credit">Hình ảnh: kênh YouTube chính thức Đại học Keimyung (계명대학교)</div>"""
js = (pop("#s2-t", 0.05) + rise("#s2-k", 0.15) + pop("#s2-pin", 0.5) + pop("#s2-p1", 1.3) + out("#s2-a", t4 - 0.2)
      + "".join(pop(f"#s2-q{i}", t4 + 1.6 + 0.55 * (i - 1)) for i in range(1, 7)))
S.append(("s2", s, d, scene("s2", body, js)))

# S3 D4-1 (footage hồ sơ + tư vấn TBT)
s = st("l05") - 0.1; e = st("l07") - 0.1; d = e - s; t6 = st("l06") - s; cut = 3.4
items = rows("s3", [("✓", "Tốt nghiệp THPT", ""), ("✓", "Điểm trung bình từ 7.0", ""),
                    ("✓", "Trống không quá 2 năm", ""), ("!", "Một số khu vực có giới hạn", "Kiểm tra hồ sơ trước")])
body = (video("s3-v1", "tbt-hoso-chung-toan-02.mp4", 0, cut) + video("s3-v2", "tbt-tuyensinh-chung-trung-03.mp4", cut, d - cut)
        + f"""    <div class="scrim-all"></div>
    <div id="s3-card" class="card" style="top:560px">
      <span id="s3-h" class="card-h pill red" style="font-size:56px;padding:16px 46px 20px">HỆ TIẾNG D4-1</span>
{items}      <div id="s3-f" class="fine">Theo thông tin trường công bố</div>
    </div>""")
js = (rise("#s3-card", 0) + pop("#s3-h", 0.2) + rise("#s3-r1", 0.8) + rise("#s3-r2", 2.0) + rise("#s3-r3", 3.2)
      + rise("#s3-r4", t6 + 0.1) + rise("#s3-f", t6 + 0.9))
S.append(("s3", s, d, scene("s3", body, js, root_css="background:#000")))

# S4 D2 điều kiện
s = st("l07") - 0.1; e = st("l09") - 0.1; d = e - s
items = rows("s4", [("✓", "TOPIK 3", "hầu hết các ngành"), ("✓", "Hoặc hoàn thành cấp độ 3", "viện tiếng Hàn của trường")])
body = f"""    <div class="blue-bg"></div>
    <img class="logo" src="assets/logo/tt-tron.png" alt="Logo" />
    <div id="s4-card" class="card" style="top:560px">
      <span id="s4-h" class="card-h pill red" style="font-size:52px;padding:16px 40px 20px">HỆ ĐẠI HỌC D2</span>
{items}      <div id="s4-f" class="fine">Theo thông tin trường công bố</div>
    </div>"""
js = rise("#s4-card", 0) + pop("#s4-h", 0.2) + rise("#s4-r1", 1.2) + rise("#s4-r2", 2.6) + rise("#s4-f", 3.4)
S.append(("s4", s, d, scene("s4", body, js)))

# S4b hạn nộp
s = st("l09") - 0.1; e = st("l10") - 0.1; d = e - s
body = """    <div class="blue-bg"></div>
    <img class="logo" src="assets/logo/tt-tron.png" alt="Logo" />
    <div class="center" style="top:520px">
      <span id="s4b-k" class="wbig" style="font-size:70px">KỲ 03/2027</span>
      <span id="s4b-p" class="pill red" style="margin-top:24px">Đợt 2 nhận hồ sơ</span>
      <div id="s4b-d" class="dates"><span>30/11/2026</span><span class="ar">→</span><span>04/01/2027</span></div>
      <div id="s4b-f" class="note" style="margin-top:30px">Theo thông tin trường công bố</div>
    </div>"""
css = """
.dates { margin-top: 40px; display: flex; justify-content: center; align-items: center; gap: 16px; }
.dates span { font-weight: 900; font-size: 58px; color: #FFE360; -webkit-text-stroke: 8px #263E8B; paint-order: stroke fill; }
.dates .ar { color: #fff; font-size: 70px; }
"""
js = pop("#s4b-k", 0.05) + rise("#s4b-p", 0.5) + pop("#s4b-d", 1.6) + rise("#s4b-f", 2.4)
S.append(("s4b", s, d, scene("s4b", body, js, extra_css=css)))

# S5 Học bổng kỳ đầu
s = st("l10") - 0.1; e = st("l11") - 0.14; d = e - s
body = """    <div class="blue-bg"></div>
    <img class="logo" src="assets/logo/tt-tron.png" alt="Logo" />
    <div class="center" style="top:380px">
      <span id="s5-t" class="big" style="font-size:118px">HỌC BỔNG</span>
      <span id="s5-t2" class="wbig" style="font-size:64px">KỲ ĐẦU · HỆ D2</span>
    </div>
    <div id="s5-tb" class="center" style="top:720px">
      <div id="s5-r1" class="hb"><span class="lv">TOPIK 3</span><span class="pc">50%</span></div>
      <div id="s5-r2" class="hb"><span class="lv">TOPIK 4</span><span class="pc">70%</span></div>
      <div id="s5-r3" class="hb top"><span class="lv">TOPIK 5+</span><span class="pc">100%</span></div>
      <div id="s5-f" class="note" style="margin-top:26px">học phí kỳ đầu · theo thông tin trường công bố, kỳ 03/2027</div>
    </div>"""
css = """
.hb { display: flex; justify-content: space-between; align-items: center; background: #fff; border-radius: 30px;
      padding: 18px 50px; margin: 0 70px 22px; box-shadow: 0 12px 30px rgba(10,30,90,.3); }
.hb .lv { font-weight: 800; font-size: 56px; color: #263E8B; }
.hb .pc { font-weight: 900; font-size: 84px; color: #E81E37; }
.hb.top { background: #FFE360; }
"""
js = pop("#s5-t", 0.05) + rise("#s5-t2", 0.3) + rise("#s5-r1", 1.3) + rise("#s5-r2", 2.6) + pop("#s5-r3", 3.8) + rise("#s5-f", 4.4)
S.append(("s5", s, d, scene("s5", body, js, extra_css=css)))

# S6 Linh – học bổng khi đang học
s = st("l11") - 0.14; e = st("l12") - 0.1; d = e - s
body = """    <div id="s6-a" class="center stack" style="top:1050px">
      <span id="s6-big" class="big" style="font-size:104px">HỌC TỐT</span>
      <span id="s6-pill" class="pill">vẫn có học bổng, tới 100%</span>
      <span id="s6-f" class="note">(Theo thông tin trường công bố)</span>
    </div>"""
js = pop("#s6-big", 0.15) + rise("#s6-pill", 1.0) + rise("#s6-f", 1.6)
S.append(("s6", s, d, scene("s6", body, js)))

# S7 Du học Thầy Tư đồng hành (footage tư vấn + lớp học TBT)
s = st("l12") - 0.1; e = st("l13") - 0.1; d = e - s; cut = 2.2
body = (video("s7-v1", "tbt-tuyensinh-chung-toan-02.mp4", 0, cut) + video("s7-v2", "tbt-daotao-chung-toan-04.mp4", cut, d - cut)
        + """    <div class="scrim-t"></div>
    <div class="center stack" style="top:260px">
      <span id="s7-t" class="wbig" style="font-size:74px">DU HỌC THẦY TƯ</span>
      <span id="s7-p0" class="pill red">Đồng hành từ đầu</span>
      <div><span id="s7-p1" class="pill white sm">Học tiếng</span>
      <span id="s7-p2" class="pill white sm" style="margin-left:8px">Chọn ngành</span>
      <span id="s7-p3" class="pill white sm" style="margin-left:8px">Hồ sơ</span></div>
    </div>""")
js = pop("#s7-t", 0.05) + rise("#s7-p0", 0.5) + pop("#s7-p1", 1.2) + pop("#s7-p2", 2.0) + pop("#s7-p3", 2.8)
S.append(("s7", s, d, scene("s7", body, js, root_css="background:#000")))

# S8 Linh – chốt + CTA
s = st("l13") - 0.1; e = VO_END - 0.2; d = e - s; t14 = st("l14") - s
body = """    <div id="s8-a" class="center stack" style="top:1050px">
      <span id="s8-big" class="big" style="font-size:96px">PHIM HÀN</span>
      <span id="s8-pill" class="pill">+ học bổng tốt</span>
    </div>
    <div id="s8-b" class="center stack" style="top:1010px">
      <span id="s8-cta" class="pill red" style="font-size:62px;padding:22px 56px 26px">NHẮN TIN NGAY</span>
      <span id="s8-c1" class="pill white">Kiểm tra hồ sơ</span>
      <span id="s8-c2" class="pill yellow">Nhận bảng chi phí chi tiết</span>
    </div>"""
js = (pop("#s8-big", 0.1) + rise("#s8-pill", 0.9) + out("#s8-a", t14 - 0.2) + pop("#s8-cta", t14)
      + rise("#s8-c1", t14 + 1.0) + rise("#s8-c2", t14 + 2.0))
S.append(("s8", s, d, scene("s8", body, js)))

s = VO_END - 0.2
S.append(("end", s, END - s, outro_scene()))

LINH = ("s1", "s6", "s8")
write_project(HERE, "Đại học Keimyung – KOL Linh AI – Du học Thầy Tư", S, VO_END, END, linh_scenes=LINH,
              avatar_segments=linh_segments(HERE, S, LINH, SCENE_LINES))
