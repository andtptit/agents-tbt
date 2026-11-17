"""Series review trường – Đại học Catholic (가톨릭대학교). Dữ liệu: sheet trường học (D4-1 TOP 2, D2-2), kỳ 03/2027.
Chạy: python build.py → index.html + compositions/*.html"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "tools"))
from truong_build import (endcard_scene, out, pop, rise, rows, scene, timing, video,  # noqa: E402
                          write_project)

L, VO_END = timing(HERE)
END = round(VO_END + 3.5, 2)
st = lambda k: L[k]["start"]  # noqa: E731
S = []

# S1 Linh – hook phá lời đồn
s, e = 0.0, st("l03") - 0.14
t2 = st("l02") - s
body = """    <div id="s1-a" class="center stack" style="top:1050px">
      <span id="s1-big" class="big" style="font-size:96px">THEO ĐẠO</span>
      <span id="s1-pill" class="pill red">mới được học?</span>
    </div>
    <div id="s1-b" class="center stack" style="top:1050px">
      <span id="s1-big2" class="big" style="font-size:118px">KHÔNG HỀ!</span>
      <span id="s1-pill2" class="pill">Không phân biệt tôn giáo</span>
    </div>"""
js = (f'    tl.fromTo("#s1-big", {{ scale: 1.15 }}, {{ scale: 1, duration: 0.3, ease: "power3.out" }}, 0);\n'
      + pop("#s1-pill", 0.9) + out("#s1-a", t2 - 0.2) + pop("#s1-big2", t2) + rise("#s1-pill2", t2 + 1.4))
S.append(("s1", s, e - s, scene("s1", body, js)))

# S2 Campus (YouTube chính thức) – vị trí + thế mạnh
s = st("l03") - 0.14; e = st("l05") - 0.1; d = e - s; t4 = st("l04") - s; c = d / 3
body = f"""    <div class="blue-bg"></div>
    <img class="logo" src="assets/logo/tt-tron.png" alt="Logo" />
    <div class="center" style="top:300px">
      <span id="s2-k" class="wbig" style="font-size:58px">ĐẠI HỌC</span>
      <span id="s2-t" class="big" style="font-size:140px">CATHOLIC</span>
      <span id="s2-pin" class="pill yellow" style="margin-top:14px">● GYEONGGI · SÁT SEOUL</span>
    </div>
    <div id="s2-a" class="center" style="top:700px">
      <span id="s2-p1" class="pill white sm">Đi lại thuận tiện</span><br>
      <span id="s2-p2" class="pill red sm" style="margin-top:16px">Chi phí sinh hoạt dễ thở hơn</span>
    </div>
    <div id="s2-b" class="center" style="top:700px">
      <span id="s2-q1" class="pill white sm">Công nghệ sinh học</span>
      <span id="s2-q2" class="pill white sm" style="margin-left:8px">AI</span><br>
      <span id="s2-q3" class="pill white sm" style="margin-top:16px">Y sinh</span>
      <span id="s2-q4" class="pill white sm" style="margin-left:8px;margin-top:16px">Quản trị kinh doanh</span>
    </div>
    <div class="window">
{video("s2-v1", "yt-xuan.mp4", 0, c, "")}{video("s2-v2", "yt-sinhvien.mp4", c, c, "")}{video("s2-v3", "yt-thu.mp4", 2 * c, d - 2 * c, "")}    </div>
    <div class="credit">Hình ảnh: kênh YouTube chính thức Đại học Catholic (가톨릭대학교)</div>"""
js = (pop("#s2-t", 0.05) + rise("#s2-k", 0.15) + pop("#s2-pin", 0.5) + pop("#s2-p1", 1.6) + pop("#s2-p2", 2.6)
      + out("#s2-a", t4 - 0.2) + pop("#s2-q1", t4 + 0.6) + pop("#s2-q2", t4 + 1.3) + pop("#s2-q3", t4 + 1.9)
      + pop("#s2-q4", t4 + 2.6))
S.append(("s2", s, d, scene("s2", body, js)))

# S3 D4-1 (footage hồ sơ + tư vấn TBT)
s = st("l05") - 0.1; e = st("l08") - 0.1; d = e - s; t6 = st("l06") - s; t7 = st("l07") - s
cut = 3.6
items = rows("s3", [("✓", "Tốt nghiệp THPT", ""), ("✓", "Điểm trung bình từ 6.9", ""),
                    ("✓", "Trống không quá 2 năm", "Trống lâu hơn: cần TOPIK 2"),
                    ("★", "Kỳ 03/2027", "Nhận hồ sơ đến 24/12/2026")])
body = (video("s3-v1", "tbt-hoso-chung-toan-01.mp4", 0, cut) + video("s3-v2", "tbt-tuyensinh-chung-toan-03.mp4", cut, d - cut)
        + f"""    <div class="scrim-all"></div>
    <div id="s3-card" class="card" style="top:560px">
      <span id="s3-h" class="card-h pill red" style="font-size:56px;padding:16px 46px 20px">HỆ TIẾNG D4-1</span>
{items}      <div id="s3-f" class="fine">Theo thông tin trường công bố</div>
    </div>""")
js = (rise("#s3-card", 0) + pop("#s3-h", 0.2) + rise("#s3-r1", 0.9) + rise("#s3-r2", 2.2) + rise("#s3-r3", t6 + 0.1)
      + rise("#s3-r4", t7 + 0.1) + rise("#s3-f", t7 + 1.0))
S.append(("s3", s, d, scene("s3", body, js, root_css="background:#000")))

# S4 D2 điều kiện
s = st("l08") - 0.1; e = st("l10") - 0.1; d = e - s; t9 = st("l09") - s
items = rows("s4", [("✓", "Tốt nghiệp THPT", ""), ("✓", "TOPIK 3 hoặc IELTS 5.5", ""),
                    ("!", "Chỉ có TOPIK 2?", "Được, nếu hoàn thành 300 giờ tiếng Hàn")])
body = f"""    <div class="blue-bg"></div>
    <img class="logo" src="assets/logo/tt-tron.png" alt="Logo" />
    <div id="s4-card" class="card" style="top:560px">
      <span id="s4-h" class="card-h pill red" style="font-size:52px;padding:16px 40px 20px">HỆ ĐẠI HỌC D2</span>
{items}      <div id="s4-f" class="fine">Theo thông tin trường công bố</div>
    </div>"""
js = rise("#s4-card", 0) + pop("#s4-h", 0.2) + rise("#s4-r1", 0.7) + rise("#s4-r2", 1.5) + rise("#s4-r3", t9 + 0.1) + rise("#s4-f", t9 + 1.2)
S.append(("s4", s, d, scene("s4", body, js)))

# S5 Học bổng kỳ đầu
s = st("l10") - 0.1; e = st("l12") - 0.14; d = e - s; t11 = st("l11") - s
body = """    <div class="blue-bg"></div>
    <img class="logo" src="assets/logo/tt-tron.png" alt="Logo" />
    <div class="center" style="top:380px">
      <span id="s5-t" class="big" style="font-size:118px">HỌC BỔNG</span>
      <span id="s5-t2" class="wbig" style="font-size:64px">KỲ ĐẦU · HỆ D2</span>
    </div>
    <div id="s5-tb" class="center" style="top:720px">
      <div id="s5-r1" class="hb"><span class="lv">TOPIK 3</span><span class="pc">70%</span></div>
      <div id="s5-r2" class="hb"><span class="lv">TOPIK 4</span><span class="pc">90%</span></div>
      <div id="s5-r3" class="hb top"><span class="lv">TOPIK 5–6</span><span class="pc">100%</span></div>
      <div id="s5-f" class="note" style="margin-top:26px">học phí kỳ đầu · theo thông tin trường công bố, kỳ 03/2027</div>
    </div>"""
css = """
.hb { display: flex; justify-content: space-between; align-items: center; background: #fff; border-radius: 30px;
      padding: 18px 50px; margin: 0 70px 22px; box-shadow: 0 12px 30px rgba(10,30,90,.3); }
.hb .lv { font-weight: 800; font-size: 56px; color: #263E8B; }
.hb .pc { font-weight: 900; font-size: 84px; color: #E81E37; }
.hb.top { background: #FFE360; }
"""
js = (pop("#s5-t", 0.05) + rise("#s5-t2", 0.3) + rise("#s5-r1", 1.6) + rise("#s5-r2", 3.0) + pop("#s5-r3", t11 + 0.1)
      + rise("#s5-f", t11 + 0.8))
S.append(("s5", s, d, scene("s5", body, js, extra_css=css)))

# S6 Linh – bí quyết học tiếng
s = st("l12") - 0.14; e = st("l13") - 0.1; d = e - s
body = """    <div id="s6-a" class="center stack" style="top:1050px">
      <span id="s6-big" class="big" style="font-size:88px">HỌC TIẾNG CHẮC</span>
      <span id="s6-pill" class="pill">TOPIK càng cao, học bổng càng lớn</span>
    </div>"""
js = pop("#s6-big", 0.15) + rise("#s6-pill", 1.9)
S.append(("s6", s, d, scene("s6", body, js)))

# S7 Du học Thầy Tư đồng hành (footage tư vấn + lớp học TBT)
s = st("l13") - 0.1; e = st("l14") - 0.1; d = e - s; cut = 2.2
body = (video("s7-v1", "tbt-tuyensinh-chung-toan-01.mp4", 0, cut) + video("s7-v2", "tbt-daotao-chung-toan-03.mp4", cut, d - cut)
        + """    <div class="scrim-t"></div>
    <div class="center stack" style="top:260px">
      <span id="s7-t" class="wbig" style="font-size:74px">DU HỌC THẦY TƯ</span>
      <span id="s7-p0" class="pill red">Đồng hành từ đầu</span>
      <div><span id="s7-p1" class="pill white sm">Chọn ngành</span>
      <span id="s7-p2" class="pill white sm" style="margin-left:8px">Học tiếng</span>
      <span id="s7-p3" class="pill white sm" style="margin-left:8px">Hồ sơ</span></div>
    </div>""")
js = pop("#s7-t", 0.05) + rise("#s7-p0", 0.5) + pop("#s7-p1", 1.2) + pop("#s7-p2", 2.0) + pop("#s7-p3", 2.9)
S.append(("s7", s, d, scene("s7", body, js, root_css="background:#000")))

# S8 Linh – chốt + CTA
s = st("l14") - 0.1; e = VO_END - 0.2; d = e - s; t15 = st("l15") - s
body = """    <div id="s8-a" class="center stack" style="top:1050px">
      <span id="s8-big" class="big" style="font-size:96px">GẦN SEOUL</span>
      <span id="s8-pill" class="pill">+ học bổng tốt</span>
    </div>
    <div id="s8-b" class="center stack" style="top:1010px">
      <span id="s8-cta" class="pill red" style="font-size:62px;padding:22px 56px 26px">NHẮN TIN NGAY</span>
      <span id="s8-c1" class="pill white">Kiểm tra hồ sơ</span>
      <span id="s8-c2" class="pill yellow">Nhận bảng chi phí chi tiết</span>
    </div>"""
js = (pop("#s8-big", 0.1) + rise("#s8-pill", 0.8) + out("#s8-a", t15 - 0.2) + pop("#s8-cta", t15)
      + rise("#s8-c1", t15 + 1.0) + rise("#s8-c2", t15 + 2.0))
S.append(("s8", s, d, scene("s8", body, js)))

# Cảnh kết
s = VO_END - 0.2
S.append(("end", s, END - s, endcard_scene()))

write_project(HERE, "Đại học Catholic – KOL Linh AI – Du học Thầy Tư", S, VO_END, END, linh_scenes=("s1", "s6", "s8"))
