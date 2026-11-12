# Nhật ký quyết định

> Ghi mới ở **trên cùng**. Mỗi mục: ngày · ai · quyết định/thay đổi · vì sao · việc còn dở.

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
