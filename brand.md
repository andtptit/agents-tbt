# BRAND BOOK — HỆ THƯƠNG HIỆU THẦY TƯ

> Tài liệu nền cho các AI Agent (Chiến lược nội dung, Biên kịch, Sản xuất, Dựng video, Kiểm duyệt).
> Phạm vi: **Tiếng Hàn Thầy Tư (PC02)** và **Du học Thầy Tư (PC01)**.
> Nguồn: fanpage, website chính thức, kế hoạch nội bộ, Bảng giá khóa học số 07/BG-TBT (07/11/2026), logo và màu do Marketing cung cấp, Bảng chi phí du học (bộ phận Du học). Cập nhật lần cuối 13/11/2026.
> Ký hiệu: ✅ đã xác minh (nguồn công khai hoặc đã được xác nhận nội bộ) · ⚠️ cần Giám đốc dự án xác nhận.
> **Người duyệt nội dung:** An (đại diện; số liên hệ trong `noi-bo/lien-he.md`; có người dự phòng, sẽ bổ sung tên)

---

## 0. Nhân vật trung tâm: Thầy Tư

| Mục | Nội dung |
|---|---|
| Họ tên | Thầy **Nguyễn Văn Tư** ✅ |
| Vai trò | Người sáng lập (cuối năm 2016), giáo viên đứng lớp, Giám đốc đào tạo Tiếng Hàn Thầy Tư ✅ |
| Học vấn | ĐH Ngoại ngữ – ĐHQG Hà Nội (Ngôn ngữ Anh); ĐH Hà Nội (Ngôn ngữ Hàn); ĐH Mở Hà Nội (Quản trị Kinh doanh) ✅ |
| Chuyên môn | Chuyên luyện thi TOPIK; tác giả bộ giáo trình ôn thi TOPIK ✅ |
| Sách đã xuất bản | Phương pháp học từ vựng tiếng Hàn qua âm Hán · Cẩm nang luyện thi TOPIK II 듣기 + 어휘 · Cẩm nang TOPIK II 읽기 + 문법 · Cẩm nang TOPIK II 쓰기 · Chiến lược làm câu 54 TOPIK II ✅ |
| Cách học viên gọi | "Thầy", xưng "em" (thân thiết, kính trọng) ✅ |

**Thầy Tư là tài sản thương hiệu chung của cả hai kênh.** Uy tín chuyên môn của Thầy (TOPIK, giáo trình) là nền để kênh Du học tạo niềm tin: *"Từ người đi trước đến người dẫn đường"*.

### 0.1 Bộ nhận diện chung ✅

**Logo:** biểu tượng **"TT"** gồm chữ T đỏ đội mũ tốt nghiệp xanh và chữ T xanh, một đường cong xanh cắt ngang (gợi đường bay hoặc sự bứt phá), vòng cung đỏ dạng địa cầu bao quanh. Ý nghĩa: học tập, tốt nghiệp, vươn ra thế giới. **Dùng chung cho cả 2 kênh.** ✅

| File | Kích thước | Nền | Dùng khi |
|---|---|---|---|
| `Icon TT ko nền.png` | 1843×1602 | Trong suốt | **Mặc định**: watermark góc video, intro/outro, trên nền sáng hoặc ảnh |
| `Logo TT tròn trắng.png` | 2049×2048 | Trong suốt, có vùng đệm | Ảnh đại diện, avatar, khung vuông hoặc tròn |
| `Logo TH va DH-ngang.png` | 1934×573 | Trong suốt | Logo ngang có chữ "TIẾNG HÀN VÀ DU HỌC THẦY TƯ": end card, banner, thumbnail |
| `Icon TT đen.png` | 1555×1359 | Trong suốt, đơn sắc đen | Bản đơn sắc; **đảo sang trắng** (CSS `filter: invert(1)`) khi đặt trên nền xanh hoặc đỏ đậm |
| `logo.jpg` | 2048×2047 | Trắng (không trong suốt) | Chỉ dùng tham khảo, **không chèn vào video** |

**Quy tắc dùng logo:** không kéo méo, không đổi màu (ngoài bản đơn sắc), không đặt bản màu trên nền xanh `#263E8B` hoặc đỏ `#E81E37` (chìm màu), khi đó dùng bản trắng. Chừa vùng an toàn ≥ 10% chiều rộng logo. Trên Reels, watermark đặt ở góc trên, tránh vùng UI của Facebook/TikTok (khoảng 15% dưới cùng và cột phải). **Trong video (chốt 13/11/2026):** logo tròn **nhỏ, khoảng 10% chiều ngang (108px trên khung 1080)**, sát **góc trên phải** (cách mép trên khoảng 70px, mép phải 48px). Không đặt logo to hay thấp xuống giữa khung.

| Màu | Mã | Vai trò gợi ý |
|---|---|---|
| 🔴 Đỏ | **`#E81E37`** | Màu nhấn, CTA, highlight từ khóa, con số |
| 🔵 Xanh đậm | **`#263E8B`** | Chữ, tiêu đề trên nền sáng, logo, khung |
| 🔷 Xanh tươi | **`#1E6FE8`** | **Nền chính** của video và banner (gradient sang xanh trời `#6FBCF5`), end card. Bổ sung 12/11/2026 theo phong cách kênh thực tế |
| 🟡 Vàng | **`#FFE360`** | Điểm nhấn phụ: sticker, gạch chân, badge "TOPIK 3+", giá |
| ⚪ Trắng | `#FFFFFF` | Nền sáng, chữ trên nền xanh hoặc đỏ |

**Cặp màu an toàn cho phụ đề Reels:** chữ trắng viền hoặc bóng xanh `#263E8B` · từ khóa nổi bật dùng vàng `#FFE360` trên nền xanh · chữ đỏ trên nền xanh chỉ dùng khi có viền trắng (kiểu hook của kênh).

**Quy tắc chữ trên video (chốt 13/11/2026 theo góp ý của An):**
- **Viền chữ mỏng**, không dùng viền dày: hook viền trắng khoảng 9px, tiêu đề viền xanh đậm khoảng 7px, dòng phụ khoảng 5px (tính trên khung 1080×1920). Thay quầng phát sáng bằng **bóng đổ nhẹ**.
- **Kết hợp linh hoạt 2 kiểu chữ:** dòng tiêu đề là chữ viền; dòng ngay dưới là **chữ trắng trên nhãn nền đỏ `#E81E37`** (bo góc, ôm sát chữ, ưu tiên 1 dòng). Ví dụ: tiêu đề "2K9" + nhãn đỏ "TỐT NGHIỆP XONG LÀ ĐI HÀN?".
- Dòng chữ trên nhãn nên ngắn (khoảng 25 ký tự) để không phải xuống dòng.

**Phân biệt 2 kênh trong cùng bộ màu (đề xuất):**
- Tiếng Hàn Thầy Tư → **nền xanh tươi `#1E6FE8`** (gradient xanh trời), chữ đỏ viền trắng cho hook, vàng làm điểm nhấn
- Du học Thầy Tư → **nền trắng hoặc ảnh thật, đỏ `#E81E37` làm nhấn**, gợi cờ Hàn (cảm hứng, hành trình)

**Font ✅: Be Vietnam Pro** (Google Fonts, hỗ trợ đầy đủ dấu tiếng Việt) cho mọi chữ trong video và hình ảnh.

| Vai trò | Độ đậm | Ghi chú |
|---|---|---|
| Hook / tiêu đề lớn | ExtraBold 800 / Black 900 | Câu mở đầu 3 giây. Chữ đỏ `#E81E37`, **viền trắng mỏng** + bóng đổ nhẹ (chốt 13/11/2026; video cũ của kênh dùng viền dày + phát sáng, nay bỏ) |
| Phụ đề | Bold 700 | Chữ trắng viền mỏng xanh `#263E8B`, hoặc **chữ trắng trên nhãn nền đỏ** `#E81E37` |
| Nội dung, chú thích | Medium 500 / Regular 400 | |
| Giá, con số | ExtraBold 800 | Vàng `#FFE360` hoặc đỏ `#E81E37` |
| Chữ Hàn (한국어) | Noto Sans KR | Be Vietnam Pro không có glyph Hangul |

### 0.2 Giọng đọc (voice) ✅

- **Giai đoạn hiện tại: dùng Vbee TTS** (tạm thời). Sau này chuyển sang ElevenLabs API.
- **Giọng mặc định: `voice_id_dh`**, áp dụng cho cả 2 kênh cho đến khi có chỉ định khác.
- Thông tin xác thực Vbee (`id`, `token`) và các voice ID nằm trong file **`.env`** ở thư mục dự án. **Không chép giá trị vào kịch bản, brand.md, log hay commit**; code đọc qua biến môi trường.
  - Biến có sẵn: `id`, `token`, `voice_id`, `voice_id_2`, `voice_id_dh`
- Không dùng TTS hay nhân bản giọng khác (HeyGen voice…) ngoài Vbee hoặc ElevenLabs.
- Không mô phỏng giọng Thầy Tư khi chưa có văn bản đồng ý.
- Kịch bản cho TTS: viết số và từ viết tắt thành chữ để đọc đúng ("18.000.000đ" → "mười tám triệu đồng").
- **Từ điển phát âm Vbee (đã nghe kiểm tra):**

  | Chữ trên màn hình | Viết trong lời đọc | Ghi chú |
  |---|---|---|
  | TOPIK | **Tốp pích** | ✅ Xác nhận đọc đúng 12/11/2026. Viết "TOPIK" thì Vbee đánh vần T-O-P-I-K |
  | TOPIK 6 | Tốp pích sáu | Số viết bằng chữ |
  | 1900 4403 | một chín không không, bốn bốn không ba | Đọc từng số |
  | **Kênh Du học** (thêm 13/11/2026, ⚠️ chưa nghe kiểm tra — nghe ở video Du học đầu tiên rồi sửa bảng này) | | |
  | D4-1 | đê bốn một | Hệ tiếng |
  | D2 | đê hai | Hệ chuyên ngành |
  | GPA 6.9 | điểm trung bình sáu phẩy chín | Không đọc chữ "GPA" |
  | IELTS 5.5 | ai en năm phẩy năm | |
  | 5,4 triệu won | năm phẩy bốn triệu uôn | "won" dễ bị đọc kiểu tiếng Anh |
  | KTX | ký túc xá | |
  | Seoul / Busan / Daejeon / Gyeonggi | Xơ-un / Bu-xan / Đê-chon / Kiơng-ki | Tên địa danh Hàn |

- **Cách gọi API:** script `tools/vbee_tts.py` (gói hiện tại chỉ hỗ trợ chế độ async: gửi yêu cầu rồi chờ lấy file; webhook điền địa chỉ nội bộ không dùng).
  - ⚠️ Vbee **cắt cụt âm cuối của mỗi file trả về** và không giữ nghỉ đoạn. Vì vậy script gửi **mỗi câu một yêu cầu song song, thêm câu đệm phía sau**, rồi cắt ở chỗ nghỉ trước câu đệm. Script đã làm sẵn việc này. ✅ Đã nghe kiểm tra (12/11/2026).
  - Cú pháp: `python tools/vbee_tts.py .env voice_id_dh <thư mục ra> <tốc độ> s1 "câu 1" s2 "câu 2" ...` → mỗi câu một file mp3 + `voice.json` (thời lượng).

---

## 1. TIẾNG HÀN THẦY TƯ (PC02)

### 1.1 Thông tin định danh ✅

| Mục | Nội dung |
|---|---|
| Fanpage | facebook.com/tienghanthaytuofficial · khoảng **49K người theo dõi** · 90% đề xuất (39 đánh giá) |
| Website | tienghanthaytu.com · khóa học online tại online.tbtgroup.com.vn |
| Mạng xã hội | Instagram `tienghanthaytuofficial` · TikTok `tienghanthaytu` · YouTube `TiengHanThayTu` |
| Địa chỉ | Tòa C, Số 79 Ngụy Như Kon Tum, phường Thanh Xuân, Hà Nội |
| Hotline | 0967 593 548 · 1900 4403 (phím 1: tư vấn, phím 0: CSKH) |
| Email | tienghanthaytu2020@gmail.com |
| Thành lập | Cuối năm 2016 |

### 1.2 Định vị

- **Mô tả 1 câu:** Tổ chức chuyên đào tạo tiếng Hàn **từ sơ cấp đến TOPIK 6**, có giáo trình chuyên biệt và lộ trình rõ ràng.
- **Slogan / tagline đang dùng:** "**Chinh phục TOPIK cùng Tiếng Hàn Thầy Tư**" · "Học chuyên sâu, không học tủ, học lướt"
- **Tầm nhìn:** Trở thành hệ sinh thái tiếng Hàn hàng đầu, được nhiều người theo học nhất Việt Nam.
- **Sứ mệnh:** Nâng cao năng lực tiếng Hàn, giúp cải thiện thu nhập cho người lao động biết tiếng Hàn tại Việt Nam.
- **Giá trị cốt lõi:** **Đức – Tâm – Tín – Trí**

### 1.3 Con số bằng chứng

| Chỉ số | Giá trị | Trạng thái |
|---|---|---|
| Kinh nghiệm giảng dạy và phát triển | **10 năm** | ✅ đã xác nhận |
| Học viên | **12.000+ học viên** | ✅ đã xác nhận |
| Hài lòng về cách giảng dạy | 99% | ⚠️ website ghi, chưa xác nhận |
| Đảm bảo chất lượng | 100% | ⚠️ website ghi, chưa xác nhận |

### 1.4 Cam kết đầu ra ✅

- **Cam kết đạt TOPIK 3 trở lên** cho các khóa học **từ số 0 lên TOPIK 3–4**: Chinh phục TOPIK 4 từ số 0, từ SC2, từ TC1 (`KHCBA_TP4_*`).
- ⚠️ Cần làm rõ trước khi đưa vào quảng cáo: điều kiện kèm theo (chuyên cần, bài tập) và quyền lợi nếu chưa đạt (học lại miễn phí hay hoàn phí). Khi đăng, luôn viết "cam kết đầu ra TOPIK 3+" kèm "áp dụng cho khóa…", không viết "đỗ 100%".

### 1.5 Bảng giá khóa học ✅ (Bảng giá 07/BG-TBT, hiệu lực từ 07/11/2026)

> **Quy định:** "Học phí ưu đãi" là **mức học viên thực đóng** tại thời điểm đăng ký. **Hiện không có chương trình khuyến mãi nào.**
> ⚠️ **Lưu ý khi làm nội dung:** không trình bày dạng "giảm từ X còn Y" hay "giảm 40% chỉ hôm nay", vì đây là giá thường xuyên chứ không phải khuyến mãi, dễ bị coi là giảm giá ảo (rủi ro pháp lý và chính sách Meta). Chỉ nêu "Học phí: Y đồng". Muốn nêu giá niêm yết thì cần Marketing Manager duyệt.
> Viết tắt: SC1, SC2 = Sơ cấp 1, 2 · TC1 = Trung cấp 1.

**Bảng 1. Khóa lẻ ONLINE (`KHKL_`):** khóa cấp tốc kèm tài liệu mềm, không có giáo trình in. Các khóa còn lại đã gồm giáo trình và miễn phí vận chuyển.

| Khóa học | Mã | Niêm yết | **Thực đóng** |
|---|---|---:|---:|
| Tiếng Hàn Sơ cấp 1 (40 buổi) | KHKL_THSC1 | 6.000.000 | **3.500.000** |
| Tiếng Hàn Sơ cấp 2 + Ôn thi TOPIK 2 (40 buổi) | KHKL_THSC2 | 6.000.000 | **4.500.000** |
| Tiếng Hàn Trung cấp 1 (40 buổi) | KHKL_THTC1 | 8.000.000 | **5.000.000** |
| Luyện thi TOPIK 3–4 (50 buổi) | KHKL_LTTP34 | 8.000.000 | **5.000.000** |
| Luyện thi TOPIK 5–6 (30 buổi) | KHKL_LTTP56 | 6.000.000 | **3.000.000** |
| Luyện thi TOPIK 2 cấp tốc (15 buổi) | KHKL_TP2_CTOL | 5.000.000 | **2.000.000** |
| Luyện thi TOPIK 3–4 cấp tốc (15 buổi) | KHKL_TP34_CTOL | 5.000.000 | **2.000.000** |
| Luyện thi TOPIK 5–6 cấp tốc (15 buổi) | KHKL_TP56_CTOL | 5.000.000 | **2.000.000** |
| Ôn luyện phỏng vấn trường và Đại sứ quán (20 buổi) | KHKL_OLPVTVDSQ | 6.000.000 | **2.500.000** |

**Bảng 2. Combo ONLINE (`KHCBA_`):** đã gồm giáo trình và miễn phí vận chuyển.

| Khóa học | Mã | Gồm | Niêm yết | **Thực đóng** |
|---|---|---|---:|---:|
| Chinh phục TOPIK 2 từ số 0 | KHCBA_TP2_SC1 | SC1 + SC2 | 12.000.000 | **8.000.000** |
| Chinh phục TOPIK 4 từ số 0 ⭐ | KHCBA_TP4_SC1 | SC1 + SC2 + TC1 + TOPIK 3–4 | 28.000.000 | **18.000.000** |
| Chinh phục TOPIK 4 từ SC2 ⭐ | KHCBA_TP4_SC2 | SC2 + TC1 + TOPIK 3–4 | 22.000.000 | **14.500.000** |
| Chinh phục TOPIK 4 từ TC1 ⭐ | KHCBA_TP4_TC1 | TC1 + TOPIK 3–4 | 16.000.000 | **10.000.000** |
| Chinh phục TOPIK 5–6 từ số 0 | KHCBA_TP56_SC1 | SC1 + SC2 + TC1 + TOPIK 3–4 + TOPIK 5–6 | 34.000.000 | **19.500.000** |
| Combo Luyện thi TOPIK 3–6 | KHCBA_LTTP3_6 | TOPIK 3–4 + TOPIK 5–6 | 14.000.000 | **6.500.000** |

⭐ = khóa áp dụng cam kết TOPIK 3+ (⚠️ xác nhận lại danh sách chính xác)

**Bảng 3. Combo OFFLINE (`KHCBA_`, `KHĐH_`):** đã gồm giáo trình và miễn phí vận chuyển.

| Khóa học | Mã | Gồm | Niêm yết | **Thực đóng** |
|---|---|---|---:|---:|
| Chinh phục TOPIK 2 từ số 0 | KHCBA_TP2_SC1 | SC1 + SC2 | 20.000.000 | **10.500.000** |
| Tiếng Hàn định hướng TOPIK 2 cho du học sinh từ số 0 | KHĐH_TP2_SC1 | SC1 + SC2 + Ôn luyện phỏng vấn | 30.000.000 | **13.000.000** |

> ⚠️ Mã `KHCBA_TP2_SC1` đang dùng cho cả combo online lẫn offline, cần đội Sale kiểm tra lại.

**Sản phẩm khác (website, chưa có trong bảng giá):** Giao tiếp nâng cao, Từ vựng tiếng Hàn (qua âm Hán), Luyện thi EPS từ số 0. ⚠️ Chưa nêu giá các khóa này trong nội dung.

**Hình thức học:** offline tại Hà Nội, online, livestream (ví dụ "Bộ sách TOPIK II – 8 cuốn"). Sản phẩm phụ: giáo trình TOPIK của Thầy, thi thử online.

### 1.6 Chân dung khách hàng

| Nhóm | Mục tiêu | Điểm đau |
|---|---|---|
| Sinh viên, người đi làm ôn TOPIK II | Đạt TOPIK 4–6 để du học, đi làm, lên lương | Phần Viết (câu 53, 54) điểm thấp; học lan man, không có chiến lược; thi nhiều lần chưa lên cấp |
| Người mới học | Có nền tảng vững | Không biết bắt đầu từ đâu; từ vựng khó nhớ |
| Người chuẩn bị du học | Đạt TOPIK 3 để làm visa | Áp lực thời gian, cần đạt nhanh và chắc |
| Lao động EPS | Thi EPS-TOPIK để sang Hàn làm việc | Học từ số 0, ít thời gian |

### 1.7 Giọng thương hiệu

- **Tính cách:** người thầy giỏi chuyên môn, nghiêm túc nhưng gần gũi, đáng tin.
- **Giọng văn:** rõ ràng, có phương pháp, đưa mẹo cụ thể và dùng được ngay. Tránh hô hào sáo rỗng.
- **Xưng hô:** Thầy – các em / các bạn.
- **Từ khóa nên dùng:** chinh phục TOPIK, lộ trình rõ ràng, học chuyên sâu, chiến lược, câu 54, từ vựng qua âm Hán, đậu cấp, giáo trình của Thầy, cam kết đầu ra TOPIK 3+.
- **Tránh:** "học tủ", "đỗ 100%", "giảm giá sốc / chỉ hôm nay" (không có khuyến mãi), so sánh hay chê trung tâm khác.

### 1.8 Nhận diện hình ảnh → xem **mục 0.1** (dùng chung bộ nhận diện Thầy Tư)

### 1.9 Trụ cột nội dung Reels (gợi ý theo 3 trục của kế hoạch)

| Trục | Ý tưởng |
|---|---|
| Câu chuyện sản phẩm | Học viên đạt TOPIK 5–6 kể lại hành trình; một buổi học của Thầy; bộ sách TOPIK II |
| Điểm đau khách hàng | "Vì sao Viết chỉ được 30 điểm?"; mẹo câu 54 trong 60 giây; nhớ 10 từ Hán Hàn trong 1 phút |
| Điểm khác biệt | Thầy là tác giả giáo trình; học chuyên sâu, không học tủ; lộ trình từ sơ cấp đến TOPIK 6 |

**CTA chuẩn:** "Nhắn tin cho trang để nhận lộ trình học miễn phí" · "Gọi 1900 4403" · "Thi thử online miễn phí tại tienghanthaytu.com"

---

## 2. DU HỌC THẦY TƯ (PC01)

### 2.1 Thông tin định danh ✅

| Mục | Nội dung |
|---|---|
| Fanpage | facebook.com/duhocthaytu · khoảng **13K người theo dõi** · 100% đề xuất (22 đánh giá) |
| Website | duhocthaytu.com |
| Mạng xã hội | `duhocthaytu` (Instagram, TikTok, YouTube) |
| Địa chỉ | Tòa C, Số 79 Ngụy Như Kon Tum, phường Thanh Xuân, Hà Nội *(trùng trụ sở Tiếng Hàn Thầy Tư)* |
| Hotline | 0967 593 548 |
| Email | duhocthaytu@gmail.com |

### 2.2 Định vị

- **Mô tả 1 câu:** Người cố vấn du học Hàn Quốc, không chỉ là đơn vị xử lý hồ sơ. Đồng hành từ chọn lộ trình đến khi ổn định cuộc sống tại Hàn.
- **Câu chuyện ra đời:** Từ các lớp ôn TOPIK II, Thầy Tư thấy nhiều học sinh loay hoay khi tự chuẩn bị du học, nên lập Du Học Thầy Tư → *"Từ người đi trước đến người dẫn đường"*.
- **Tagline đang dùng:**
  - Fanpage: "**Có TOPIK 3 – Có ngay VISA**" · "Nơi gửi trọn niềm tin" · "Chắp cánh ước mơ du học Hàn Quốc"
  - Website: "**Chi phí rõ ràng, hành trình vững vàng.**" · "Hiểu rõ mục tiêu. Chọn đúng lộ trình." · "Giấc mơ lớn, bắt đầu từ từng bước nhỏ."
- **4 tôn chỉ hoạt động:**
  1. **Học tiếng, rèn bản lĩnh.** Tiếng Hàn là nền tảng để sống tự lập, không chỉ để qua kỳ thi.
  2. **Lộ trình riêng cho từng bạn.** Xây từ học lực, thế mạnh, mục tiêu thực tế.
  3. **Minh bạch từng khoản phí.** Rõ trước khi ký, hạn chế phát sinh.
  4. **Đồng hành cả sau khi bay.** Từ chọn ngành, phỏng vấn đến ổn định tại Hàn.

> ⚠️ **Lưu ý mâu thuẫn giọng điệu:** tagline fanpage "Có TOPIK 3 – Có ngay VISA" mang tính cam kết mạnh, trong khi website nhấn "không hứa hẹn viển vông". Cần thống nhất. Khuyến nghị: video dùng giọng minh bạch như website. Câu "Có ngay VISA" chỉ dùng khi có điều kiện cụ thể đã được xác nhận (rủi ro chính sách Meta về quảng cáo cam kết kết quả).

### 2.3 Sản phẩm, dịch vụ

- **Hệ:** Hệ tiếng (D4-1) · Hệ Đại học · Hệ Thạc sĩ ✅
- **Gói trọn gói:** khoảng **60 triệu đồng** *(theo kế hoạch nội bộ, chưa thấy trên website)* ⚠️ **chưa dùng**: bảng chi phí chính thức (mục 2.3a) không ghi phí dịch vụ. Không dùng từ "giá rẻ".
- **Khóa tiếng chuẩn bị du học** (Bảng giá 07/BG-TBT) ✅, bán qua Tiếng Hàn Thầy Tư, kênh Du học có thể giới thiệu:
  - Tiếng Hàn định hướng TOPIK 2 cho du học sinh từ số 0 (offline): SC1 + SC2 + Ôn luyện phỏng vấn, **13.000.000đ**
  - Ôn luyện phỏng vấn trường và Đại sứ quán (online, 20 buổi): **2.500.000đ**
  - Luyện thi TOPIK 3–4 / Chinh phục TOPIK 4 (xem mục 1.5) để đạt TOPIK 3, nền cho hồ sơ visa
- **Lộ trình 5 bước** ✅
  1. Tư vấn và chọn hướng đi (học lực, ngân sách → ngành, trường)
  2. Học tiếng, chuẩn bị kỹ năng
  3. Hoàn thiện hồ sơ, xin thư mời
  4. Chuẩn bị phỏng vấn, làm visa
  5. Cất cánh, rồi tiếp tục đồng hành
- **Cấu trúc chi phí công bố** ✅: Đóng cho trường (học phí, nhập học, KTX) · Chuẩn bị trước khi đi (hồ sơ, dịch thuật, vé máy bay; phí dịch vụ tách riêng) · Sinh hoạt dự kiến.
- **Điều kiện tối thiểu của trung tâm** ✅ (phiếu dự tuyển học bổng nội bộ): hệ tiếng D4 cần **TOPIK 2 trở lên**; hệ chuyên ngành D2 cần **TOPIK 3 trở lên hoặc IELTS 5.5**. Trung tâm định hướng trường theo năng lực học tập và năng lực hồ sơ; khuyến khích đăng ký trường tuyển sinh sớm.

### 2.3a Quyền lợi du học sinh và chi phí hồ sơ ✅
> Nguồn: `Bảng chi phí du học.pdf` + ảnh `Giá trị nhận được 1-08.jpg` (hệ D4-1, D2-1, D2-2, D2-3, D2-4) và `1-09.jpg` (hệ D2-6) do bộ phận Du học cung cấp, 12/11/2026. Hai bảng **giống hệt nhau** về nội dung.
> Bắt buộc khi nhắc số tiền: kèm câu "**mức chi phí mang tính tham khảo, có thể thay đổi tùy trường hợp**" (đúng như ghi chú trên ảnh gốc). Luôn dùng dấu "khoảng".

**A. Trọn gói dịch vụ (không tính tiền riêng):** định hướng nghề nghiệp, chọn ngành · tư vấn chọn trường theo năng lực hồ sơ · tư vấn hồ sơ cá nhân hóa · sắp xếp lịch phỏng vấn với trường Hàn · hướng dẫn đóng tiền invoice **trực tiếp sang trường** · hướng dẫn chuẩn bị, nộp hồ sơ visa tại Đại sứ quán/Lãnh sự quán · **lệ phí xét hồ sơ của trường** · hướng dẫn hội nhập, liên lạc sau khi nhập học · hỗ trợ thủ tục nhận học bổng (hệ D2).

**B. Khoản 9.500.000đ chi phí hồ sơ do bên thứ ba thu** (không phải phí dịch vụ của công ty):

| Khoản | Khoảng |
|---|---:|
| Công chứng, dịch thuật hồ sơ | 1.000.000đ |
| Tem xác nhận dịch thuật ("tem vàng") | 500.000đ |
| Hướng dẫn thủ tục chứng minh tài chính (xác nhận số dư sổ tiết kiệm) | 2.500.000đ |
| Gửi hồ sơ bản cứng sang trường + hỗ trợ đăng ký KTX/tìm phòng | 1.500.000đ (⚠️ PDF và ảnh ghi đảo 500k/1 triệu giữa hai dòng — chỉ nêu tổng) |
| Phối hợp với trường đón tại sân bay Hàn Quốc về KTX | 2.000.000đ |
| Hỗ trợ hồ sơ lên chuyên ngành cho hệ D4-1 | 2.000.000đ |
| **Cộng** | **9.500.000đ** (đã kiểm tra, cộng đúng) |

- **Nếu trượt code hoặc visa:** đăng ký kỳ tiếp theo thì **không đóng thêm** khoản này; thanh lý hợp đồng thì **được nhận lại 5.000.000đ**. ✅ Đây là điểm "minh bạch" rất mạnh để làm video.

**C. Học viên tự thanh toán trực tiếp** (ngoài 9,5 triệu): tem tư pháp "tem tím" khoảng 832.000đ (4 USD/tem, 4–8 tem) · lệ phí visa tại Đại sứ quán khoảng 1.800.000đ (50 USD + 390.000đ phí KVAC) · khám sức khỏe khoảng 310.000đ · vé máy bay (theo lịch nhập cảnh của trường) · chứng minh tài chính bằng sổ tiết kiệm hoặc K-Study (theo quy định của trường và Đại sứ quán; sổ phải **chính chủ, không kỳ hạn**).

⚠️ **Chưa có:** mức **phí dịch vụ** (bảng chỉ ghi "trọn gói dịch vụ", không ghi số tiền) → **không nêu** "gói 60 triệu" hay bất kỳ con số phí dịch vụ nào. Học phí trường đóng thẳng cho trường theo invoice.

### 2.3b Dữ liệu trường (theo kỳ tuyển sinh)
> Nguồn: kịch bản do bộ phận Du học soạn (`tu-lieu/kich-ban/du-hoc/kich_ban_dh.txt`, nhận 12/11/2026). Học phí, học bổng **thay đổi theo kỳ** → khi dùng phải ghi "theo thông tin trường công bố" và kỳ áp dụng (nếu có). ⚠️ An xác nhận lại số liệu còn hiệu lực trước khi duyệt video. Trường không có trong bảng này: **không nêu số liệu**, chỉ nói chung và mời nhắn tin kiểm tra hồ sơ.

| Trường | Vị trí, điểm nổi bật | Hệ tiếng D4-1 | Hệ chuyên ngành D2 · học bổng |
|---|---|---|---|
| **Catholic** (Đại học Công giáo) | Gần Seoul, giao thông thuận tiện, chi phí sinh hoạt dễ thở hơn trung tâm Seoul. 4 ngành riêng cho SV quốc tế: Quản trị kinh doanh, Âm nhạc, Tiếng Hàn, Truyền thông nghệ thuật. Phát triển AI, Công nghệ sinh học, Y sinh | GPA từ 6,9; tốt nghiệp THPT; trống không quá 2 năm (trên 2 năm cần TOPIK 2+). Học phí khoảng 5,4 triệu won/năm | TOPIK 3 hoặc IELTS 5.5 (TOPIK 2 được nếu đã học đủ 300 giờ tiếng Hàn). Học phí khoảng 4,39 triệu won/kỳ. HB kỳ đầu: TOPIK 3 → 70% · TOPIK 4 → 90% · TOPIK 5–6 → 100% |
| **Pyeongtaek** | Trường Top 2, tỉnh Gyeonggi; tuyển sinh toàn quốc. Ngành: IT, Logistics, Phúc lợi xã hội, Quảng cáo, Truyền thông, Phim và Kịch | Tốt nghiệp THPT hoặc GDTX; GPA từ 6,5; trống không quá 3 năm. Học phí khoảng 5 triệu won/năm; KTX khoảng 1,08 triệu won/6 tháng | Kỳ **tháng 12/2026**: TOPIK 2+ → 500.000 won · GPA 3 năm THPT từ 8,0 → 500.000 won · có anh chị em ruột đang học tại trường → 500.000 won |
| **Woosong** | Daejeon, môi trường quốc tế. Có chương trình **100% tiếng Anh** (IELTS từ 5.5 tùy chương trình). Mạnh: Quản trị khách sạn, Ẩm thực, AI, Logistics, CNTT | Tốt nghiệp THPT; GPA từ 6,7; trống không quá 2 năm. Học phí khoảng 5,2 triệu won/năm; KTX khoảng 1,4 triệu won/2 kỳ (gồm 1 bữa/ngày) | Chương trình tiếng Hàn: TOPIK 3; tiếng Anh: IELTS 5.5 tùy ngành. HB kỳ đầu: TOPIK 3 → 30% · TOPIK 4 → 50% · TOPIK 5 → 70% · TOPIK 6 → 100% học phí 4 năm (nếu duy trì kết quả học tập theo yêu cầu) |
- **Trường nổi bật trên web** ✅: ChungAng (Seoul, TOP 1), Inha (Incheon, TOP 1), Daegu, DongA (Busan), Pyeongtaek (TOP 2), Gimcheon (TOP 3).
- **Mạng lưới đối tác** ✅: Ajou, Keimyung, Konyang, Ngoại ngữ Busan, Sunmoon, Sejong, Hanyang, Inha, Joongbu, ChungAng, Nữ Sookmyung, Thần học Seoul, Chungnam, Nữ sinh Duksung, Sungkyunkwan, Sungkyul, Konkuk, Kyungsung, Nữ sinh Seoul.
  ⚠️ Cần xác nhận trường nào là đối tác chính thức trước khi nêu tên trong video.

### 2.4 Chân dung khách hàng

| Nhóm | Mục tiêu | Điểm đau / băn khoăn |
|---|---|---|
| Học sinh lớp 12, mới tốt nghiệp THPT | Du học hệ tiếng, rồi lên đại học | "Du học Hàn có hợp với mình?"; chưa biết tiếng Hàn |
| **Phụ huynh** (người quyết định tài chính) | Con đi an toàn, chi phí rõ ràng | Sợ phát sinh phí, sợ trung tâm "vẽ vời"; lo con sống tự lập |
| Sinh viên, người đã tốt nghiệp | Hệ đại học, thạc sĩ | Chọn trường Seoul hay tỉnh; điều kiện GPA, TOPIK |

**FAQ thật trên website** (nguồn chủ đề Reels): Chưa biết tiếng Hàn có bắt đầu được không? · Cần dự trù những khoản nào? · Cần chuẩn bị giấy tờ gì? · Seoul hay thành phố khác? · Khi nào nên bắt đầu chuẩn bị? · Sang Hàn được hỗ trợ thế nào?

### 2.5 Giọng thương hiệu

- **Tính cách:** người anh, người thầy đi trước. Điềm tĩnh, thực tế, minh bạch, ấm áp.
- **Giọng văn:** câu ngắn, nhịp chậm, chân thành. *"Không cần vội. Chỉ cần đi đúng hướng."*
- **Nói với 2 đối tượng:** học sinh (truyền cảm hứng trưởng thành, tự lập) và phụ huynh (an tâm, rõ chi phí).
- **Từ khóa nên dùng:** minh bạch, lộ trình riêng, đồng hành, chi phí rõ ràng, sống tự lập, trưởng thành, người dẫn đường.
- **Tránh:** "giá rẻ", "bao đậu visa 100%", "vừa học vừa làm kiếm nhiều tiền" (dễ vi phạm chính sách và gây kỳ vọng sai), thông tin visa hay phí chưa có trong bộ dữ liệu gốc.

### 2.6 Nhận diện hình ảnh → xem **mục 0.1** (dùng chung bộ nhận diện Thầy Tư)

- **Phong cách hình:** lớp học thật, khoảnh khắc lên đường ở sân bay, lễ trao học bổng, học viên tốt nghiệp tại Hàn, khuôn viên trường Hàn Quốc.
- **Khuôn chữ động của kênh Du học (K4 bản Du học, chốt sơ bộ 13/11/2026):** nền **trắng**, góc có mảng màu xanh tươi `#1E6FE8` và vàng `#FFE360` (theo ảnh "Giá trị nhận được" của bộ phận Du học); hook **chữ đỏ `#E81E37`**, tiêu đề xanh đậm `#263E8B`, dòng thứ hai chữ trắng trên nhãn đỏ, số tiền và học bổng trong nhãn vàng. Logo và quy tắc chữ như mục 0.1. Khác hẳn nền xanh của kênh Tiếng Hàn để người xem phân biệt ngay. Giọng Vbee tốc độ 1.0 (chậm hơn kênh Tiếng Hàn 1.05).
- Chưa có video/banner cũ của kênh Du học trong `tu-lieu/du-hoc/` → khi có, phân tích bổ sung như `phong-cach-tieng-han.md`.

### 2.7 Trụ cột nội dung Reels

| Trục | Ý tưởng |
|---|---|
| Câu chuyện sản phẩm | Hành trình 5 bước của một bạn học viên; khoảnh khắc ở sân bay; học viên tốt nghiệp tại Hàn |
| Điểm đau khách hàng | "Du học Hàn cần chuẩn bị bao nhiêu tiền?" (tách 3 nhóm phí); "Chưa biết tiếng Hàn có đi được không?"; Seoul hay Busan? |
| Điểm khác biệt | Thầy Tư là chuyên gia TOPIK (học tiếng thật chứ không học để đối phó); minh bạch phí trước khi ký; đồng hành sau khi bay |

**CTA chuẩn:** "Để lại thông tin để Thầy Tư đánh giá hồ sơ miễn phí" · "Nhắn tin để nhận lộ trình du học riêng" · "Gọi 0967 593 548"

---

## 3. Quan hệ giữa hai thương hiệu

```
                 THẦY TƯ (uy tín chuyên môn TOPIK)
                 /                              \
   Tiếng Hàn Thầy Tư (PC02)  ──học viên──▶  Du học Thầy Tư (PC01)
   "Chinh phục TOPIK"            TOPIK 3      "Người dẫn đường"
```

- **Phễu chéo:** học viên ôn TOPIK → khách tiềm năng du học; khách du học → học tiếng tại Tiếng Hàn Thầy Tư.
- **Được phép:** nhắc chéo, livestream chung (đang làm), dùng hình ảnh Thầy Tư ở cả hai kênh.
- **Phân biệt khi làm video:**

| | Tiếng Hàn Thầy Tư | Du học Thầy Tư |
|---|---|---|
| Năng lượng | Nhanh, sắc, mẹo học, thử thách | Chậm, ấm, truyền cảm hứng, an tâm |
| Màu chủ đạo | Nền xanh `#263E8B` + nhấn vàng `#FFE360` | Nền trắng hoặc ảnh thật + nhấn đỏ `#E81E37` |
| Giọng đọc | Vbee `voice_id_dh`, tốc độ nhanh hơn một chút | Vbee `voice_id_dh`, tốc độ chậm, ấm |
| Người xem chính | Người học 18–30 tuổi | Học sinh 17–22 tuổi và phụ huynh |

- ⛔ **Tách biệt với B1, B2:** không nhắc, không chia sẻ chéo, không dùng chung tài sản (logo, giọng đọc, người dẫn AI, khuôn video) với B1, B2.

---

## 4. Quy tắc bắt buộc cho AI Agent

1. **Giá, phí, visa, cam kết:** chỉ dùng số liệu ✅ trong file này (học phí lấy từ mục 1.5, nêu mức thực đóng). Mục ⚠️ **chưa được dùng** trong nội dung đăng.
2. **Không có khuyến mãi:** không viết "giảm giá", "ưu đãi có hạn", "chỉ hôm nay", "flash sale".
3. **Lời chứng thực học viên:** chỉ dùng tên và kết quả học viên đã đồng ý công khai (website có mục "Cảm nhận học viên").
4. **Giọng đọc:** hiện dùng Vbee (`voice_id_dh`, thông tin trong `.env`), sau chuyển sang ElevenLabs. Người dẫn AI hoặc giọng mô phỏng Thầy Tư cần Thầy đồng ý bằng văn bản.
5. **Duyệt cuối:** mọi kịch bản và thành phẩm phải qua **An** hoặc người duyệt dự phòng trước khi đăng.
6. **Định dạng:** 9:16, 30–90 giây (chốt 12/11/2026), câu mở đầu giữ chân trong 3 giây đầu, luôn có phụ đề, logo đúng kênh, có CTA.
7. **Chính sách Meta:** không cam kết kết quả tuyệt đối, không nhắm vào đặc điểm cá nhân ("Bạn đang thất nghiệp?"), không trước/sau gây hiểu lầm.
8. **Cảnh quay AI chỉ để minh họa, luôn gắn nhãn AI:** bật nhãn "nội dung do AI tạo" trên Facebook và TikTok cho mọi video có cảnh Veo/Kling hoặc người dẫn HeyGen. Lời chứng thực, kết quả học viên, lớp học và Thầy Tư phải là chất liệu **thật**. Không dùng AI dựng "học viên", "lớp học" hay "bảng điểm" giả.

---

## 5. Quyết định vận hành (chốt ngày 12/11/2026)

| Hạng mục | Quyết định |
|---|---|
| Lịch khởi động | Linh hoạt, không cố định ngày 16/11. Chạy khi hệ thống sẵn sàng. |
| Người duyệt | An (đại diện) và một người dự phòng |
| Bình luận, tin nhắn khách | Có nhân sự riêng phụ trách; tự động hóa sau |
| Kênh duyệt và thông báo | **Telegram Bot** thay cho Zalo: duyệt bằng nút bấm, báo cáo, cảnh báo. Bot chạy trên máy Cowork (long polling, không cần máy chủ công khai). Chỉ nhận lệnh từ tài khoản được phép. **Không gửi số điện thoại hay họ tên khách hàng qua Telegram.** |
| Dashboard | **Notion** thay cho web app tự xây (giai đoạn đầu): lịch nội dung, hàng chờ duyệt, dữ liệu gốc, báo cáo. Mở được ở mọi nơi, trên máy tính và điện thoại. Agent đọc/ghi qua Notion API. File video lưu trên Google Drive, Notion chỉ giữ link. **Không lưu dữ liệu cá nhân khách hàng trong Notion** (lead nằm trong CRM). Từ 2027 cân nhắc chuyển sang EduHubs. |
| Đăng Facebook | Meta Graph API (System User token trong Business Manager) |
| Đăng TikTok | Cowork qua TikTok Studio, hoặc API đẩy vào nháp, cho đến khi app qua audit |
| Nội dung AI | Cảnh AI chỉ minh họa, luôn gắn nhãn AI (xem mục 4, quy tắc 8) |
| Pháp lý (cam kết, dữ liệu cá nhân, giấy phép tư vấn du học, quyền hình ảnh) | Đã đầy đủ |

**Mốc ban đầu (12/11/2026)** để so sánh hiệu quả:

| Kênh | Người theo dõi Facebook |
|---|---|
| Tiếng Hàn Thầy Tư | 49K |
| Du học Thầy Tư | 13K |

*Nên bổ sung thêm khi có: số lead/tháng, chi phí/lead và tỷ lệ chốt hiện tại, để đo được hiệu quả về doanh thu, không chỉ lượng người theo dõi.*

---

## 6. Thông tin còn thiếu (cần bổ sung)

- [ ] Tên và Telegram của người duyệt dự phòng
- [ ] Kiểm tra Telegram trên 4G của người duyệt
- [ ] Meta App + quyền admin 2 fanpage · TikTok Developer App (nộp audit sớm)
- [ ] Workspace Notion của công ty (gói đang dùng), tạo integration Notion API cho hệ thống
- [ ] Thư mục Google Drive chứa video thành phẩm

**Đã có:** ✅ Bảng giá khóa học Tiếng Hàn · ✅ Khuyến mãi (không có) · ✅ Cam kết TOPIK 3+ · ✅ 10 năm, 12.000+ học viên · ✅ Người duyệt (An) · ✅ Voice (Vbee tạm, `voice_id_dh`, `.env`) · ✅ Logo đủ bộ (PNG trong suốt, ngang, tròn, đơn sắc) · ✅ 3 màu chính · ✅ Font Be Vietnam Pro

**Còn thiếu:**
- [ ] ElevenLabs API key và voice ID (khi chuyển từ Vbee)
- [ ] Logo vector SVG/AI (không bắt buộc, PNG hiện tại đủ dùng cho video 1080×1920)
- [ ] Điều kiện và quyền lợi của cam kết TOPIK 3+ (học lại hay hoàn phí), danh sách khóa áp dụng chính xác
- [ ] Mã khóa trùng `KHCBA_TP2_SC1` (online và offline)
- [ ] Giá các khóa Giao tiếp nâng cao, Từ vựng, EPS (có trên website, không có trong bảng giá)
- [x] Bảng chi phí hồ sơ du học (mục 2.3a, nhận 12/11/2026) — [ ] còn thiếu **mức phí dịch vụ** (gói 60 triệu?) và lệch 500k/1 triệu giữa 2 dòng "gửi hồ sơ" và "KTX"
- [ ] Xác nhận số liệu 3 trường Catholic, Pyeongtaek, Woosong (mục 2.3b) còn hiệu lực; kỳ nhập học sắp tới
- [ ] Video/banner cũ của kênh Du học (thư mục `tu-lieu/du-hoc/` đang trống)
- [ ] Điều kiện cụ thể cho câu "Có TOPIK 3 – Có ngay VISA"
- [ ] Danh sách trường đối tác chính thức, học bổng, kỳ nhập học sắp tới
- [ ] Top 10 video hoặc bài đăng hiệu quả nhất của mỗi kênh (cần quyền quản trị trang; khi chưa đăng nhập, Facebook chỉ hiện thông tin giới thiệu)
- [ ] Danh sách học viên đồng ý xuất hiện trong video
- [ ] Người duyệt nội dung của từng kênh
