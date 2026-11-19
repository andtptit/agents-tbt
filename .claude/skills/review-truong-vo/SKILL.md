---
name: review-truong-vo
description: Làm video series "Review trường" cho kênh Du học Thầy Tư bản KHÔNG có KOL/HeyGen — chỉ giọng Vbee + trám cảnh (cảnh YouTube kênh chính thức của trường, footage kho TBT, thẻ D4-1/D2/học bổng, nhạc nền), dựng bằng HyperFrames, không tốn credit HeyGen. Dùng khi người dùng nói "review trường không KOL", "review trường không HeyGen", "chỉ voice và trám cảnh", "bản không Linh", hoặc muốn làm nhanh/rẻ một video giới thiệu trường Hàn Quốc.
---

# Review trường — bản chỉ giọng + trám cảnh (không Linh, không HeyGen)

Anh em với skill `/review-truong` (bản có KOL Linh AI). **Mọi quy tắc và các bước dữ liệu giống hệt** — đọc `.claude/skills/review-truong/SKILL.md` mục "Quy tắc bắt buộc" và các bước 1, 1b, 2, 3, 5, 6, 7, 9, 10, 11. Bản này chỉ khác những điểm dưới đây.
Mẫu: Keimyung (`video/jobs/DH-KEIMYUNG-VO/`, 18/11/2026) — cùng giọng, cùng dữ liệu với bản Linh để so sánh. Mã job: `DH-<TRUONG>-VO`.

## Khác bản có Linh

- Font SVN-Gilroy, outro chính thức, logo y 100–220 và chữ từ y ≥ 280: **giống bản có Linh** (khung chung `tools/truong_build.py`, `prepare_assets` + `outro_scene` + `outro_end`).

- **Bỏ bước 4 (HeyGen)**. Trong `kich-ban.json` mọi câu `"lipsync": false`. Không cần `linh.mp3`, `avatar.mp4`. Không có nhãn "Hình ảnh AI" (không có cảnh AI) — trừ khi dùng thêm cảnh AI minh họa thì phải gắn nhãn.
- **Hook phải tự kéo người xem bằng hình**: khung hình 0 đã có chữ to + cảnh campus đẹp nhất (khung ảnh YouTube) — không có gương mặt để giữ chân. Ưu tiên hook là điều bất ngờ/đẹp mắt về trường (phim trường, campus nổi tiếng, học bổng lớn).
- **Cảnh thay chỗ Linh** (không lặp clip đã dùng — `tools/footage_index.py find …`):
  - Hook (l01–l02): nền xanh + logo + chữ to + `.window` 2 cảnh YouTube (có thể `data-playback-rate="0.85–0.9"` để kéo dài clip 3 s cho vừa câu).
  - Lời khuyên giữa bài (l11/l12): footage học viên TBT (lớp học, viết bài) + `.scrim-t` + chữ ở top ~260.
  - Chốt + CTA (l13–l14): footage học viên → footage tư vấn viên (gọi điện, nhắn tin) + CTA "NHẮN TIN NGAY / Kiểm tra hồ sơ / Nhận bảng chi phí chi tiết".
  - Cảnh ngành học: sau khi hết clip YouTube thì ẩn khung ảnh (`out("#s2-w")`) và hiện lưới nhãn ngành cỡ lớn trên nền xanh — tránh dùng quá ~3 cảnh YouTube.
- **Mọi cảnh phải có nền đặc** (blue-bg hoặc footage): không có avatar chạy bên dưới.
- **Dựng**: chép `mau-build.py` (skill này), sửa chữ/cảnh, cuối file `write_project(HERE, "<tên>", S, VO_END, END, no_avatar=True)`.
- Agent ⑥ chấm như bản Linh (`--topic` kèm `doi-chieu.md`).

## Khi nào chọn bản nào

| | Bản có Linh (`/review-truong`) | Bản chỉ giọng (`/review-truong-vo`) |
|---|---|---|
| Credit HeyGen | ~20 s Linh nói/video | 0 |
| Thời gian | + ~2 phút chờ HeyGen | nhanh hơn |
| Giữ chân 3 s đầu | gương mặt + chữ | chỉ cảnh + chữ (hook phải mạnh) |
| Hợp với | video chủ lực, trường nổi bật | làm hàng loạt nhiều trường, trường ít tư liệu |
