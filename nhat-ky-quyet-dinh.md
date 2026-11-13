# Nhật ký quyết định

> Ghi mới ở **trên cùng**. Mỗi mục: ngày · ai · quyết định/thay đổi · vì sao · việc còn dở.

---

## 13/11/2026 (chiều) — Tách Notion theo kênh, làm trước Du học

- An: **2 kênh có 2 PM riêng** → mỗi kênh một trang Notion riêng, mời PM dạng khách vào đúng trang kênh mình.
- Đã tạo trang con **🎓 Du học Thầy Tư**: Đơn video Du học (bot tự đẩy đơn DH-…), Lịch nội dung Du học (5 ý tưởng chuyển từ bảng chung, thêm cột Người xem chính), Việc chờ PM Du học quyết (12 việc). Đã bỏ các mục Du học khỏi bảng chung (nằm trong thùng rác Notion, khôi phục được).

- An: **chỉ làm Du học, Tiếng Hàn tính sau** → kế hoạch 6 tháng viết lại chỉ cho Du học (đổi tên "Kế hoạch kênh Du học Thầy Tư"); 3 bảng chung ở trang gốc Notion (đơn Tiếng Hàn) đã cho vào thùng rác Notion (khôi phục được, id lưu ở `data/notion.json` mục `TH_archived`). Bot không đẩy đơn Tiếng Hàn lên Notion nữa.

**Còn dở:** tách trang Tiếng Hàn (khóa học) cho PM thứ hai; tách kế hoạch 6 tháng theo kênh nếu 2 PM cần; đơn TH-261113-01 (chủ đề du học nhưng đặt nhầm kênh) vẫn ở bảng chung.

---

## 13/11/2026 (trưa) — Kế hoạch 6 tháng + kết nối Notion

- Lập **kế hoạch 6 tháng 12/2026 – 05/2027** (tài liệu trên claude.ai để PM đọc, comment): 4 giai đoạn (Dạy và chạy thật → Đăng đều theo lịch → Tối ưu theo số liệu → Mở rộng), mục tiêu để PM điền.
- Quyết định: **dùng Notion bản Free** (đúng như chốt 12/11), An là thành viên duy nhất, PM và bộ phận vào dạng **khách** (tối đa 10) để không bị giới hạn block. Chưa xây site riêng.
- Đã kết nối: integration "Thay Tu Bot", trang "Nhà máy nội dung Thầy Tư" có 3 bảng: Đơn video (bot tự cập nhật mỗi phút), Lịch nội dung (9 ý tưởng tháng 12), Việc chờ PM quyết (9 việc). Notion chỉ để xem; duyệt vẫn trên Telegram.

**Còn dở:** PM trả lời 9 việc chờ quyết; điền ngày đăng cho lịch tháng 12; bot lấy chủ đề từ Lịch nội dung để tự đặt đơn (chưa làm).

---

## 13/11/2026 (sáng) — An góp ý video TH-261113-01

- **Logo** quá to, quá thấp → nhỏ lại (108px), sát góc trên phải.
- **Viền chữ** quá dày, xấu → viền mỏng (hook 9px, tiêu đề 7px, phụ 5px) + bóng đổ nhẹ, bỏ phát sáng hồng.
- **Kết hợp kiểu chữ trắng trên nhãn nền đỏ** (theo ảnh mẫu An gửi): dòng thứ 2 mỗi cảnh là nhãn đỏ.
- Áp dụng cho cả 2 kênh (khuôn K4 trong `tools/video_maker.py`), ghi vào brand.md mục 0.1. Bản dựng lại: `video/jobs/TH-261113-01/renders/TH-261113-01-v2.mp4`.
- Ghi nhận: đơn TH-261113-01 chủ đề du học nhưng gõ `/tao` thiếu `dh` → vào kênh Tiếng Hàn.

**Còn dở:** buổi dạy thiết kế (designer của An sẽ dạy sau, đề bài `huong-dan-dao-tao/thiet-ke.md`); bot hỏi lại kênh khi chủ đề có từ "du học" mà thiếu `dh` (chưa làm).

---

## 13/11/2026 — Mở kênh Du học Thầy Tư (Quản lý dự án + Claude)

- Phân tích `Bảng chi phí du học.pdf` + 2 ảnh "Giá trị nhận được" (D4-1/D2-1…4 và D2-6, nội dung giống nhau) và 6 kịch bản của bộ phận Du học.
- `brand.md`: thêm mục **2.3a** (dịch vụ trọn gói · khoản hồ sơ 9.500.000đ do bên thứ ba thu, đã cộng kiểm tra đúng · trượt code/visa: kỳ sau không đóng thêm, thanh lý nhận lại 5 triệu · khoản học viên tự trả), mục **2.3b** (số liệu 3 trường), điều kiện tối thiểu D4 TOPIK 2+ / D2 TOPIK 3+ hoặc IELTS 5.5, từ phát âm Du học, giao diện K4 bản Du học.
- Mới: `huong-dan-kich-ban-du-hoc.md` — xưng **mình – bạn**, 4 dạng: T giới thiệu trường, S hậu trường, C chi phí minh bạch (dạng mới, thế mạnh của kênh), H hỏi đáp.
- Bot: `/tao dh <chủ đề>` (hoặc `/taodh`) tạo đơn mã **DH-…**; Claude viết theo hướng dẫn Du học; video dựng khuôn K4 **nền trắng, mảng xanh/vàng, hook đỏ, con số trong nhãn vàng**, giọng chậm hơn (1.0).
- Quyết định: **không nêu phí dịch vụ / "gói 60 triệu"** cho tới khi có bảng chính thức; số liệu trường phải kèm "theo thông tin trường công bố".

**Còn dở:** mức phí dịch vụ; PDF và ảnh ghi đảo 500k/1 triệu giữa "gửi hồ sơ" và "KTX"; xác nhận số liệu 3 trường còn hiệu lực; nghe kiểm tra phát âm D4-1, won, IELTS; video/banner cũ kênh Du học; page Facebook thật của kênh Du học (hiện vẫn đăng lên page test).

---

## 12/11/2026 (chiều) — Hệ thống sơ bộ chạy trọn vòng

- Telegram: nhóm "Nhà máy nội dung Thầy Tư" chia 5 chủ đề; bot tự chạy cùng Windows (trình giám sát), báo cáo 8h sáng.
- Dây chuyền: `/tao` → Claude viết kịch bản → An duyệt → Vbee giọng → HyperFrames dựng (K4) → An duyệt → **đăng Facebook** (đăng ngay / lên lịch 20:00 / nháp).
- Đơn đầu tiên TH-261112-03 «chào hỏi tiếng Hàn» đã **đăng thật lên page thử nghiệm "Calio test"** lúc 16:57.
- Vbee: không giữ được nghỉ đoạn → chuyển sang mỗi câu một yêu cầu, cắt trước câu đệm.
- Meta: đang dùng token người dùng (app n8n-api) cho page test. **Chưa có App Secret** → token hết hạn trong ngày.

**Còn dở:** thêm META_APP_SECRET để token không hết hạn; chuyển sang System User + 2 fanpage thật (cần quyền Admin Business Portfolio); thu hẹp quyền token (đang cấp 16 page); Notion; kênh Du học; buổi dạy thiết kế.

---

## 12/11/2026 — Buổi làm việc đầu tiên (Quản lý dự án + Claude)

**Phạm vi:** chỉ tập trung 2 kênh Tiếng Hàn Thầy Tư (PC02) và Du học Thầy Tư (PC01).

**Dữ liệu gốc đã xác nhận**
- Bảng giá khóa học 07/BG-TBT (07/11/2026): "học phí ưu đãi" = mức học viên thực đóng. **Không có khuyến mãi** đang chạy.
- Cam kết TOPIK 3+ cho các khóa từ số 0 lên TOPIK 3–4.
- 10 năm giảng dạy, 12.000+ học viên.
- Người duyệt: An (đại diện), sẽ có người dự phòng. Nhân sự riêng chăm sóc bình luận/inbox.
- Mốc ban đầu: Tiếng Hàn 49K người theo dõi, Du học 13K.
- Pháp lý (cam kết, dữ liệu cá nhân, giấy phép tư vấn du học, quyền hình ảnh): đã đầy đủ.

**Nhận diện**
- Logo "TT" dùng chung 2 kênh (4 file PNG). Màu đỏ `#E81E37`, xanh `#263E8B`, vàng `#FFE360`; **thêm xanh tươi `#1E6FE8` làm nền chính** (theo banner/video thực tế).
- Font **Be Vietnam Pro** cho mọi chữ, kể cả hook (giữ cảm giác kênh cũ: chữ đỏ viền trắng dày).
- Video 9:16, **30–90 giây**.

**Kiến trúc hệ thống**
- 8 AI Agent theo kế hoạch 24/10/2026; lịch khởi động linh hoạt.
- Duyệt/thông báo qua **Telegram** (thay Zalo vì API Zalo phức tạp). Dashboard: **Notion** (thay web app nội bộ vì cần dùng khi ra ngoài). Đăng Facebook qua **Meta Graph API**; TikTok tạm qua TikTok Studio.
- Dựng video bằng **HyperFrames** (miễn phí) thay Remotion (Remotion cần Company License ~100 USD/tháng vì công ty >3 người).
- Dạy hệ thống / lập kế hoạch: chat trực tiếp với Claude; vận hành hằng ngày: Telegram.
- Quy tắc cảnh AI: chỉ minh họa, luôn gắn nhãn AI.

**Đã làm được**
- `brand.md`, `phong-cach-tieng-han.md`, `huong-dan-kich-ban-tieng-han.md`.
- Khuôn K4 (Chữ động) và K5 (Kết quả học viên, có giọng) — K5 đã duyệt.
- Giọng Vbee: phát hiện Vbee cắt cụt cuối mỗi file → gửi cả kịch bản 1 lần rồi tách. "TOPIK" đọc là "Tốp pích" (đã nghe xác nhận).
- Whisper chạy GPU; chuyển lời 11 video Tiếng Hàn.
- Bot Telegram `@thaytu_duyet_bot`: gửi video, nút Duyệt/Trả về, ghi trạng thái — đã thử duyệt thành công.

**Còn dở / chờ**
- ⚠️ Chốt số buổi học (3 nguồn lệch nhau).
- Xác nhận ưu đãi 10% (video/banner cũ) và điều kiện "Có TOPIK 3 – Có ngay VISA".
- Bật Topics nhóm Telegram; viết lệnh `/tao` chạy cả dây chuyền.
- Notion, Meta App, TikTok Developer App.
- Kênh Du học: phân tích tư liệu (`Bảng chi phí du học.pdf`, `Giá trị nhận được 1-08/1-09.jpg`).
- Buổi dạy thiết kế: xem `huong-dan-dao-tao/thiet-ke.md`.
