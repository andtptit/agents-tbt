# Đề bài buổi dạy: THIẾT KẾ (dành cho bộ phận Design)

> Người dạy: designer của team. Người học: Claude (mở thư mục dự án này).
> Mục tiêu: sau buổi dạy, Claude dựng video/khuôn **đúng mắt thẩm mỹ của team**, không chỉ đúng màu và font.

## 1. Claude đã biết gì (designer không cần dạy lại)
- Màu, font, logo, quy tắc dùng logo: `brand.md` mục 0.1.
- Phong cách kênh Tiếng Hàn rút từ 11 video + 9 banner: `phong-cach-tieng-han.md`.
- 2 khuôn đã dựng: `video/th-k4-chu-dong/` (Chữ động) và `video/th-k5-ket-qua/` (Kết quả học viên). Xem bản render trong thư mục `renders/` của từng khuôn.

## 2. Designer nên dạy những gì

| # | Chủ đề | Cách dạy hiệu quả nhất |
|---|---|---|
| 1 | **Nhận xét K4 và K5**: chỗ nào đạt, chỗ nào chưa | Nói theo giây: "giây 5: chữ quá to", "giây 12: thiếu khoảng thở". Claude sửa ngay trong buổi |
| 2 | **Bố cục chuẩn** của kênh: vùng đặt hook, chữ khóa, logo, CTA | Đưa 2–3 video/banner "chuẩn nhất" và chỉ rõ vì sao chuẩn |
| 3 | **Kiểu chữ trên video**: cỡ, độ đậm, viền, bóng, hiệu ứng xuất hiện | Đưa ví dụ đúng và sai |
| 4 | **Chuyển động**: tốc độ, kiểu chuyển cảnh, hiệu ứng được/không được dùng | Có thể gửi link video tham khảo |
| 5 | **Thư viện thành phần**: sticker, icon, khung ảnh, end card | Gửi file gốc (PNG nền trong, SVG) nếu có |
| 6 | **Điều cấm về thiết kế** | Ví dụ: không dùng màu X, không đặt chữ trên mặt người… |
| 7 | **Khuôn mới cần có** (ví dụ K1 Series sách, K6 Lịch khai giảng) | Mô tả hoặc phác thảo |

Tài liệu gửi kèm: bỏ vào `tu-lieu/` (banner, video, file gốc) và nói cho Claude biết đường dẫn.

## 3. Đầu ra bắt buộc sau buổi dạy
Claude phải tạo/cập nhật trước khi kết thúc:
1. **`huong-dan-dao-tao/ket-qua/thiet-ke-quy-chuan.md`**: quy chuẩn thiết kế viết lại từ những gì designer dạy (bố cục, chữ, chuyển động, điều cấm), kèm ví dụ.
2. **Khuôn K4/K5 đã chỉnh** theo nhận xét (render lại để designer xem).
3. Một mục mới trong **`nhat-ky-quyet-dinh.md`**: ngày, người dạy, thay đổi gì, việc còn dở.

Designer xác nhận "đạt" thì buổi dạy mới kết thúc. Sau này quy chuẩn này sẽ được đóng gói thành **skill thiết kế** để agent tự dùng.

## 4. Cách bắt đầu (designer)
1. Mở Claude (desktop) → chọn thư mục `D:\AN\SOURCECODE\CLAUDE_DH` (hoặc bản đã tải từ GitHub).
2. Gõ câu mở đầu:
   > *"Tôi là designer của team. Hãy đọc CLAUDE.md và huong-dan-dao-tao/thiet-ke.md, rồi bắt đầu buổi dạy thiết kế. Đầu tiên cho tôi xem K4 và K5."*
3. Dạy theo bảng mục 2; cuối buổi kiểm tra đầu ra mục 3.

## 5. Lưu ý
- Không cần biết code: chỉ cần nói bằng lời, gửi ảnh/video mẫu.
- Không sửa `brand.md` mục màu/font nếu chưa có Quản lý dự án đồng ý — ghi đề xuất vào nhật ký.
- Không cần và không được xem file `.env`.
