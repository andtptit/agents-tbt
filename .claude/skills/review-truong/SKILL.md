---
name: review-truong
description: Làm video series "Review trường" cho kênh Du học Thầy Tư — KOL Linh AI (HeyGen) nói bằng giọng Vbee, xen footage kho TBT, cảnh YouTube kênh chính thức của trường, thẻ D4-1/D2/học bổng, nhạc nền, dựng bằng HyperFrames. Dùng khi người dùng nhắc "review trường", "series trường", "video về trường <tên>", "/taodh truong <tên>", hoặc muốn làm video giới thiệu một trường Hàn Quốc kiểu video Konkuk/Catholic.
---

# Series review trường — Du học Thầy Tư

Mẫu đã duyệt: video Konkuk (17/11/2026, An: "rất tốt, đây là 1 dạng video tôi muốn làm") và Catholic.
Một video = một trường, 55–65 giây, dọc 1080×1920. Trả lời người dùng bằng tiếng Việt, ít thuật ngữ.

## Quy tắc bắt buộc (đọc trước khi viết)

- **Không nêu số tiền** nào: học phí, KTX, phí apply, phí nhập học, cọc, sổ ngân hàng, "won"/"triệu". Muốn nói chi phí → CTA "nhận bảng chi phí chi tiết". (brand.md 2.3, chốt 17/11/2026)
- Chỉ dùng dữ liệu trong sheet trường (`noi-bo/truong-hoc/`) hoặc brand.md ✅. Không dùng cột ghi chú nội bộ: cọc chống trốn, sổ Kstudy/STK, "đi qua VPĐD", "phỏng vấn 100% đậu", phí thư mời.
- Được dùng: khu vực, nhóm TOP (ghi rõ "nhóm TOP 1/2/3" — đây là phân loại visa, KHÔNG phải xếp hạng chất lượng), điều kiện (GPA, năm trống, vùng miền, TOPIK/IELTS), kỳ tuyển và hạn nộp, % học bổng theo TOPIK, ngành. Luôn kèm chữ nhỏ "Theo thông tin trường công bố" (+ kỳ, ví dụ 03/2027).
- Vùng miền bị hạn chế: nói "một số khu vực có giới hạn", không nêu tên miền.
- "Trường đối tác / MOU / kết nối với trường": chỉ nói khi PM xác nhận (sheet LIST MOU có ghi đơn vị ký — nếu không phải TBT thì không nói). Mặc định nói "Du học Thầy Tư đồng hành…".
- Không cam kết visa/đỗ, không khuyến mãi, không "top 1" trơn, không bịa số liệu.
- Linh AI: mọi cảnh có Linh gắn nhãn **"Hình ảnh AI"**. Giọng luôn là **Vbee** (`voice_id_dh`), không dùng giọng HeyGen.
- YouTube (An chốt 17/11/2026): chỉ **kênh chính thức của trường**, mỗi cảnh 3–5 s, tối đa ~3 cảnh/video, bỏ tiếng gốc, cắt tránh logo/chữ của video gốc, dòng nguồn trên hình "Hình ảnh: kênh YouTube chính thức Đại học X (tên Hàn)", ghi `nguon-youtube.json`. Video chạy quảng cáo → thay bằng footage xin từ trường.
- Footage kho TBT: chọn đa dạng, **không lặp** clip đã dùng ở video khác (`data/footage_usage.json`). Bỏ nhóm kế toán, lập trình, họp nội bộ.
- Không đăng thật khi chưa qua An duyệt; đăng thử chỉ lên page test.

## Quy trình (mã job: `DH-<TRUONG>-LINH`, thư mục `video/jobs/<mã>/`)

Thứ tự chuẩn: **sheet → đối chiếu internet → kịch bản (+ chấm điểm) → giọng Vbee → Linh HeyGen → cảnh YouTube kênh chính thức → footage TBT → nhạc nền → dựng → kiểm → xuất → An duyệt → đăng page test** (page thật chỉ khi An cho phép).

1. **Dữ liệu**: `python tools/truong_data.py update` (tải lại sheet), rồi `python tools/truong_data.py tim <tên>` → đọc mọi tab có trường đó (D4-1-TOPx, D2-2, D2-3, LIST-MOU…). Ghi lại các ý dùng được và kỳ tuyển.
1b. **Đối chiếu internet (bắt buộc, trước khi viết)**: tìm thông tin mới nhất trên **nguồn chính thức** — web tuyển sinh quốc tế của trường (국제처 / International admissions, guideline kỳ gần nhất), viện tiếng Hàn của trường (hệ D4-1), trang Study in Korea / NIIED, Bộ Tư pháp Hàn (nhóm trường chứng nhận). Kiểm từng ý sẽ đưa vào video: kỳ tuyển + hạn nộp, điều kiện (GPA, năm trống, TOPIK/IELTS), % học bổng, ngành, vị trí, nhóm TOP, và câu hook (ví dụ "không phân biệt tôn giáo").
   - Khớp sheet → dùng. Internet chính thức mới hơn và **lệch** sheet → không đưa con số đó vào video, ghi lại để PM xác nhận (hoặc nói chung, không nêu số). Chỉ có trên blog/trung tâm khác → không dùng.
   - Ghi kết quả vào `video/jobs/<mã>/doi-chieu.md`: mỗi ý một dòng — nội dung · sheet · nguồn internet (link, ngày xem) · khớp/lệch/không thấy. Báo người dùng các chỗ lệch.
2. **Kịch bản** 13–15 câu, ~140–170 âm tiết/60 s, xưng mình – bạn. Khung (theo mẫu):
   - l01–l02 **Linh – hook phá lời đồn/câu hỏi** về trường (Konkuk: "con nhà giàu mới đi được?"; Catholic: "phải theo đạo mới được học?") → "Không hề / Khoan đã!".
   - l03–l04 **Campus** (khung ảnh YouTube): vị trí, điểm mạnh, ngành.
   - l05–l07 **Thẻ D4-1** (nền footage hồ sơ/tư vấn TBT): THPT, GPA, năm trống, vùng miền, kỳ + hạn nộp.
   - l08–l09 **Thẻ D2**: TOPIK/IELTS, ngoại lệ.
   - l10–l11 **Bảng học bổng** % theo TOPIK.
   - l12 **Linh**: lời khuyên (học tiếng chắc / chuẩn bị sớm…).
   - l13 **Footage TBT**: Du học Thầy Tư đồng hành (chọn ngành, học tiếng, hồ sơ).
   - l14–l15 **Linh – chốt + CTA** "nhắn tin kiểm tra hồ sơ và nhận bảng chi phí chi tiết".
   Phát âm Vbee: brand.md 0.2 (TOPIK → Tốp pích, D4-1 → đê bốn một, IELTS 5.5 → ai en năm phẩy năm, Seoul → Xơ-un, Gyeonggi → Kiơng-ki); tên trường viết theo cách đọc Việt (Konkuk → Côn Cúc, Catholic → Ca tô lích); số viết bằng chữ.
   Chấm thử: lưu kịch bản dạng JSON của script_writer rồi `python tools/script_judge.py file.json --dh` (đạt ≥ 7,5, không lỗi).
3. **Giọng**: `python tools/vbee_tts.py .env voice_id_dh video/jobs/<mã>/audio 1.05 l01 "…" l02 "…" …` → `python tools/truong_media.py vo video/jobs/<mã>` (ra `vo.mp3` + `timing.json`).
4. **Linh AI**: `python tools/truong_media.py linh video/jobs/<mã> "<tiêu đề>"` (HeyGen qua MCP `heygen`, trừ credit gói Creator, ~2–4 phút; avatar look "Linh Du Học"). Ra `assets/media/avatar.mp4`.
5. **YouTube**: `python -m yt_dlp --flat-playlist --print "%(channel)s | %(title)s | %(duration)s | %(id)s" "ytsearch15:<tên Hàn> 캠퍼스"` → chỉ chọn video của **kênh chính thức** (ưu tiên flycam/campus tour) → tải về `noi-bo/youtube/<truong>/` bằng `-f "bv*[height<=1080][ext=mp4]"` → xem tờ ảnh `fps=1/6,tile` → cắt 3 cảnh sạch: `ffmpeg -ss <t> -t 3-4.5 -i src -vf "crop=…,scale=1200:800" -an …` vào `assets/media/yt-*.mp4` (crop bỏ logo/chữ góc). Ghi `nguon-youtube.json` (mẫu: `mau-nguon-youtube.json`).
6. **Footage TBT**: `python tools/footage_index.py find tu-van ho-so lop-hoc …` → chọn 4–5 clip chưa dùng → `python tools/truong_media.py footage video/jobs/<mã> "<đường dẫn>" …` (ra `assets/media/tbt-*.mp4`, 1080×1920). Sau khi xuất: `footage_index.mark_used("<mã>", [...])`.
7. **Nhạc nền**: kho nhạc HeyGen (`search_audio_sounds` qua MCP, không lời, tươi sáng, ≥ 60 s), đổi sang mp3 thật → `assets/media/bgm.mp3`. Khung dựng tự để nhỏ (0,12) khi có giọng, to lên ở cảnh kết.
8. **Dựng**: chép `mau-build.py` (skill này) thành `video/jobs/<mã>/build.py`, sửa chữ/cảnh theo kịch bản (giữ id cảnh, thời điểm lấy từ `timing.json`); chép font/logo/hyperframes.json/package.json từ `video/th-k4-chu-dong/`; `python build.py`.
9. **Kiểm**: `npx hyperframes check --json` (không lỗi; cảnh báo vùng an toàn TikTok là chấp nhận được), `npx hyperframes snapshot --at …` xem tờ ảnh: chữ không đè mặt Linh/người trong footage (cảnh Linh đặt chữ ở top ~1050), nhãn AI có, dòng nguồn YouTube có.
10. **Xuất**: `npx hyperframes render -o renders/<mã>.mp4`, kiểm âm lượng (`volumedetect`, mean ≈ −17 dB), chép bản gửi duyệt vào `noi-bo/heygen-thu/`, ghi nhật ký quyết định.
11. **Đăng (sau khi An duyệt)**: `python tools/meta_post.py check` phải ra page test "Allisagi là chân ái" → `python tools/meta_post.py post renders/<mã>.mp4 "<caption>" PUBLISHED`. Caption: hook, điều kiện, % học bổng, CTA nhận bảng chi phí, hotline 0967 593 548, dòng nhỏ "(Theo thông tin trường công bố, kỳ … Video có sử dụng hình ảnh AI. Hình ảnh campus: kênh YouTube chính thức Đại học X.)", hashtag `#DuHocThayTu #DuHocHanQuoc #DaiHoc<Ten> #ReviewTruong`. Không số tiền. Xem `matches_found` trong kết quả (kiểm bản quyền của Facebook).

## Khung dựng (tools/truong_build.py)

Hàm có sẵn: `scene`, `pop`, `rise`, `out`, `rows` (thẻ ✓ / ! / ★ + chữ nhỏ), `video`, `endcard_scene`, `write_project(job, title, scenes, vo_end, end, linh_scenes=(…))`. Lớp CSS: `.big` (đỏ viền trắng), `.wbig` (trắng viền xanh đậm), `.pill` (`red|white|yellow|sm`), `.window` + `.credit` (khung ảnh YouTube 1000×667 ở y=1000), `.card`, `.blue-bg`, `.scrim-t|b|all`, `.full`. Avatar Linh chạy suốt dưới cùng; cảnh không có Linh phải có nền đặc (blue-bg hoặc footage).

## Còn chờ xác nhận (xem nhat-ky-quyet-dinh.md)

Quy tắc 5 (người dẫn AI) chưa sửa chính thức · Linh có tạo từ ảnh người thật không (cần văn bản đồng ý) · được nói MOU/đối tác không · điều khoản nhạc HeyGen · sheet đang để "ai có link đều xem".
