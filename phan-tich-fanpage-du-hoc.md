# PHÂN TÍCH FANPAGE DU HỌC THẦY TƯ (6 tháng: 05–11/2026)

> Nguồn: Meta Graph API, kéo ngày 13/11/2026 bằng `python tools/meta_research.py duhoc 6` (chỉ đọc).
> Dữ liệu thô (có caption, có thể có tên học viên): `noi-bo/research/duhoc_20261113.json/.csv`, **không đưa lên Git**.
> Page: **13.639 người theo dõi**. 211 bài đăng (98 video, 73 album, 34 ảnh) + 84 Reels.
> ⚠️ Số liệu Meta trả về **gộp cả lượt xem từ quảng cáo**: bài được chạy quảng cáo sẽ có lượt xem cao bất thường.
> Vì vậy dùng thêm **thời gian xem trung bình** (người xem có ở lại không) để đánh giá chất lượng nội dung.

## 1. Bức tranh chung

| Chỉ số | Giá trị |
|---|---|
| Nhịp đăng | 9 bài (05/2026) → 35–45 bài/tháng (07–10/2026); Reels 13–18/tháng |
| Lượt phát Reels (trung vị) | khoảng 1.600 |
| Thời gian xem trung bình (trung vị) | **6,4 giây** — đa số người xem rời đi trong vài giây đầu → **hook 3 giây quyết định tất cả** |
| Độ dài Reels (trung vị) | 68 giây; Reels ≤ 45 giây có lượt phát trung vị nhỉnh hơn Reels > 75 giây (1.711 so với 1.189) |

## 2. Nhóm nội dung: cái gì hiệu quả

| Nhóm | Số Reels | Lượt phát (trung vị) | Xem TB (trung vị) | Nhận xét |
|---|---:|---:|---:|---|
| **Học viên thật, khoảnh khắc lên đường** | 7 | 5.748 | **11,9 s** | Mạnh nhất về giữ chân. Bài cao nhất kênh (≈580K lượt phát, 12,6 s) là học viên chia sẻ cảm xúc trước giờ bay; album "Tháng 9 này, chúng mình cùng bay" ≈654K lượt xem |
| **Giới thiệu trường (series "Đúng ngành, trúng trường")** | 23 | 3.490 | 6,1 s | Tập 8 Catholic ≈329K lượt phát, **11,3 s**; Inha, Konkuk cũng giữ chân tốt (11–12 s). Tập mở đầu chung chung (Top 5 trường) giữ chân kém (2,7–4,4 s) |
| **Phá lời đồn / hiểu lầm** | — | — | — | "Có sổ đóng băng là chắc chắn đỗ visa?" ≈116K, **12,9 s**; "Đi du học phải cần vài tỷ?" 14K |
| Visa, tài chính (giải thích) | 18 | 1.200 | 6,7 s | Ổn khi hook là một câu hỏi/hiểu lầm cụ thể |
| Khuyến mại, quỹ học bổng 250 triệu | 5 | 15.383 | **3,4 s** | Lượt phát cao nhưng người xem bỏ đi rất nhanh → nhiều khả năng do chạy quảng cáo, nội dung không giữ chân |
| Sách TOPIK, luyện thi (đăng chéo từ kênh Tiếng Hàn) | 8 | 614 | 6,8 s | Kém trên page Du học → để ở kênh Tiếng Hàn |
| Ảnh tỷ giá won ("Won vượt 17 rồi các mom ơi") | ảnh | ≈87K xem | — | Nói thẳng với **phụ huynh**, ngắn, đúng thời sự → hiệu quả với chi phí rất thấp |

## 3. Series đang chạy — để viết TIẾP

**"Đúng ngành, trúng trường – Du học không lạc đường"** (giới thiệu từng trường):
Tập 1 (Changwon – TOPIK 2 học bổng 100%) · Tập 2 (Ajou) · Tập 3 (Nữ sinh Seoul) · Tập 4 (Pyeongtaek, học bổng kỳ 12/2026) · Tập 5 (Konyang) · Tập 6 (Konkuk) · Tập 7 (Inha – Logistics) · Tập 8 (Catholic – TOPIK 3 học bổng 70%).
- Tập tiếp theo là **Tập 9**. Công thức thắng (Tập 6–8): **tên trường + một "nghịch lý"/biệt danh dạng câu hỏi** ("Trường con nhà giàu?", "Chân ái cho team Logistics?", "TOPIK 3, học bổng 70%?").
- ⚠️ Đánh số đang lệch: tháng 8 có một chuỗi "Tập 1–3" khác (Top 5 trường, trường Kỹ thuật, trường học phí "hạt dẻ"); Tập 5–8 đăng cùng một ngày 09/10. Nên giữ một chuỗi số duy nhất và đăng cách nhau.
- Số liệu trường dùng trong video vẫn phải có trong `brand.md` mục 2.3b (hiện mới có Catholic, Pyeongtaek, Woosong).

## 4. Bài học cho Agent Biên kịch (đã đưa vào huong-dan-kich-ban-du-hoc.md)

1. **Hook là câu hỏi về một hiểu lầm hoặc nghịch lý cụ thể** ("Có sổ đóng băng là chắc chắn đỗ visa?"), không phải lời rao ("ĐỪNG BỎ LỠ CHƯƠNG TRÌNH…").
2. **Chất liệu thật thắng lớn:** học viên, sân bay, lớp học. Khuôn chữ động chỉ là phương án khi chưa có cảnh quay.
3. **Ngắn hơn:** nhắm 40–60 giây; đưa ý chính lên trước giây thứ 6.
4. **Nói với phụ huynh** bằng chủ đề tiền bạc thực tế (tỷ giá won, chi phí, sổ tiết kiệm), giọng gần gũi.
5. **Không đăng nội dung luyện thi TOPIK trên page Du học.**

## 5. Cần PM xác nhận (phát hiện khi phân tích)

- Page đã chạy **"chương trình khuyến mại quý III"** và **"Quỹ Học Bổng Xanh lên tới 250 triệu"**. `brand.md` ghi "hiện không có khuyến mãi" → Agent **không** nhắc các chương trình này cho đến khi PM xác nhận còn hiệu lực và điều kiện cụ thể.
- Bài nào trong top được **chạy quảng cáo**? (để tách lượt xem tự nhiên khỏi lượt xem trả tiền khi đánh giá nội dung).
- Học viên trong các video "trước khi bay" đã đồng ý cho dùng lại hình ảnh chưa (quy tắc 6)?
