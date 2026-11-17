# Nhật ký quyết định

> Ghi mới ở **trên cùng**. Mỗi mục: ngày · ai · quyết định/thay đổi · vì sao · việc còn dở.

---

## 17/11/2026 — Series review trường: thử Đại học Catholic (An)

- Nguồn dữ liệu trường: Google Sheet của bộ phận du học (14 tab: D4-1 TOP1–3, D2-x, LIST MOU, ghi chú) → tải về `noi-bo/truong-hoc/` (không lên Git). Video **không nêu số tiền**, không dùng ghi chú nội bộ (cọc, sổ, VPĐD, "phỏng vấn 100% đậu").
- An chốt: được dùng cảnh tải từ **YouTube kênh chính thức của trường**, mỗi cảnh 3–5 giây, tối đa ~3 cảnh/video, bỏ tiếng gốc, tránh logo/chữ, ghi nguồn trên hình + file `nguon-youtube.json` trong job. (Claude đã nói rõ: không có quy định "dưới 3–5 giây thì không vi phạm"; rủi ro thấp, công ty quyết.) Video chạy quảng cáo nên thay bằng footage xin từ trường.
- Công cụ mới: `tools/footage_index.py` (danh mục 292 clip kho TBT, chọn clip ít dùng, ghi `data/footage_usage.json`), `tools/truong_media.py` (ghép giọng Vbee, dựng Linh trên HeyGen, chuẩn hóa footage), `tools/truong_build.py` (khung dựng HyperFrames chung). Nhạc nền: kho nhạc HeyGen (nhạc AI, không lời), tự nhỏ khi Linh nói.
- Quy trình chuẩn (An chốt): sheet → **đối chiếu internet nguồn chính thức** (ghi `doi-chieu.md`, lệch thì báo PM, không đưa số lệch vào video) → kịch bản → Vbee → Linh → YouTube → footage → nhạc → dựng → An duyệt → đăng page test. Konkuk và Catholic đã đăng page test (17/11) nhưng **chưa** qua bước đối chiếu internet.
- Lưu thành skill dự án `/review-truong` (`.claude/skills/review-truong/SKILL.md` + `mau-build.py`), thêm `tools/truong_data.py` (tải sheet, tìm trường; id sheet ở `data/truong_sheet.json`).
- Kết quả: `video/jobs/DH-CATHOLIC-LINH/` 65 s. Việc còn dở: nối lệnh `/taodh truong <tên>` vào bot (Claude tự viết build từ sheet); PM xác nhận câu "không phân biệt tôn giáo" và có được nói MOU; nghe kiểm tra phát âm "Ca tô lích"; kiểm tra điều khoản nhạc HeyGen; đổi chế độ chia sẻ sheet (đang ai có link cũng xem).

---

## 17/11/2026 — Thử video KOL Linh AI (HeyGen) + giọng Vbee (An)

- Nối HeyGen qua cầu nối MCP (tài khoản Creator, trừ credit gói, không cần API key). Avatar "Linh Du Học" (photo avatar) nói khớp miệng theo **file giọng Vbee** (`create_video_from_avatar` + `audioAssetId`), không dùng giọng HeyGen.
- Làm lại video mẫu `tu-lieu/du-hoc/video/Konkuk.mp4` → `video/jobs/DH-KONKUK-LINH/` (61 s): Linh AI + footage trung tâm (`Video-Trám cảnh-TBT/`, đã chặn khỏi Git) + dải không chữ của B-roll Konkuk trong video gốc + thẻ D4-1/D2 dựng bằng HyperFrames. Bỏ mọi số tiền học phí, bỏ "top 1", bỏ câu hứa "bóc giá"; giữ điều kiện tuyển sinh + học bổng 30–100% kèm "theo thông tin trường công bố". Gắn nhãn "Hình ảnh AI" khi Linh xuất hiện.
- ⚠️ Cần chốt trước khi đăng thật: (1) sửa quy tắc 5 (hiện cấm người dẫn AI); (2) Linh có được tạo từ ảnh người thật (KOL trong video Konkuk gốc rất giống) → cần văn bản đồng ý; (3) PM xác nhận số liệu Konkuk; (4) phát âm "Côn Cúc"; (5) chưa có nhạc nền.

---

## 17/11/2026 — Agent ⑥ chấm điểm kịch bản (An)

- Mỗi kịch bản Claude viết xong được **chấm trước khi gửi An**: (1) luật cứng bằng Python: khuyến mãi, khan hiếm giả, "giá rẻ", cam kết visa/đỗ, % bịa; kênh Du học thêm số tiền, hứa thu nhập, HB Xanh; kênh Tiếng Hàn thêm số buổi học, cam kết TOPIK thiếu điều khoản; thời lượng 30–90s, tốc độ đọc, hook dài, chữ số trong lời đọc. (2) Claude chấm 6 tiêu chí (hook, cấu trúc, dữ liệu, lời đọc, giữ chân, CTA).
- **Đạt** = không có lỗi + điểm ≥ 7,5. Chưa đạt thì bot tự cho viết lại theo hướng dẫn sửa, **tối đa 2 lần**; vẫn chưa đạt thì vẫn gửi An nhưng ghi "⚠️ CHƯA ĐẠT".
- Thử: DH-261117-01 được 8,0/10 (đạt), bắt được câu hứa việc riêng với học viên, đọc ngày quá dài, clip tư liệu dễ bị hiểu là của Hùng. Luật cứng bắt được "5,2 triệu", "1,4 triệu" ở đơn DH-261113-01 (làm trước ngày chốt không nêu số tiền).
- Đổi lại: mỗi kịch bản lâu thêm khoảng 1–2 phút (thêm 2–4 phút mỗi lần tự viết lại).
- Việc còn dở: chưa có lịch sử An trả về để chỉnh tiêu chí; sau 2–3 tuần xem lại `judge` trong orders.json so với lần An trả về, chỉnh mức đạt 7,5 nếu cần.

---

## 17/11/2026 — Thử làm banner bằng HTML (An)

- Sửa thử banner cũ "Hệ tiếng D4-1": bỏ khối ưu đãi (HB GPA 10–20 triệu, HB Xanh 250 triệu, quà ngày hội) → "Thầy Tư đồng hành"; nút "Nhận tư vấn ngay". Còn chờ PM: kỳ tuyển hiện tại (banner ghi kỳ 12/2026).
- Dựng **khuôn banner B1 "Thẻ"** (`banner/b1-the/`) + `tools/banner_maker.py`: Claude viết nội dung theo brand.md → ghép HTML → Chrome chụp ảnh. Chạy thử 2 banner: "Lộ trình 5 bước", "Cần TOPIK mấy?" (ảnh ở `noi-bo/banner-thu/`).
- Đã cân nhắc Canva (có cầu nối chính thức cho Claude, cần mẫu do người thiết kế làm + gói Canva phù hợp) và ChatGPT/Gemini vẽ ảnh (hay sai dấu tiếng Việt; chỉ hợp làm hình minh họa, gắn nhãn AI).
- Việc còn dở: ảnh campus đang cắt từ banner cũ (mờ) → cần ảnh gốc chất lượng cao; người thiết kế duyệt khuôn; chưa nối Telegram (`/banner`), chưa đăng.

---

## 17/11/2026 — Số liệu fanpage vào báo cáo Telegram

- Đã thử Meta API trên 2 page chính: dùng được lượt xem (page_media_view), người xem, lượt vào trang, theo dõi mới/bỏ, lượt xem video, followers; Reels: lượt phát + thời gian xem TB. Meta đã bỏ page_impressions / page_fans / page_fan_adds_unique; page_post_engagements của page Tiếng Hàn luôn = 0 nên không dùng.
- Báo cáo 8h thêm phần 📈 FANPAGE (hôm qua, so TB 7 ngày, top 3 Reels, video hệ thống đã đăng); giảm >30% → cảnh báo. Gửi thử thành công 17/11.
- Chưa có: số lead (cần quyền leads_retrieval + hộp thư). Quyền đọc token hết hạn 11/02/2027.

---

## 17/11/2026 — Tư liệu kênh Du học (5 video, 8 banner)
**Ai:** PM Du học gửi tư liệu, Claude phân tích.
- Chuyển lời 5 video bằng Whisper → `tu-lieu/loi-thoai/du-hoc/`. Phân tích hình ảnh, lời thoại → **`phong-cach-du-hoc.md`** (mới).
- Hướng dẫn kịch bản Du học: thêm bài học từ video cũ (giữ hook điểm danh, câu đảo lời đồn; bỏ "siêu rẻ", hứa thu nhập, đọc học phí, ưu đãi), thêm **dạng V (chúc mừng visa)** và **dạng D (tuyển đối tác B2B, chỉ khi PM đặt)**. Bot nhận 2 dạng mới.
- brand.md 2.3: ghi các hệ mới thấy trên banner (cao đẳng, thạc sĩ, hệ tiếng Anh, TOEIC/IELTS, kỹ sư) và chương trình B2B ở trạng thái ⚠️ chờ xác nhận; ưu đãi trên tư liệu cũ coi như không còn.
- Notion: việc "video/banner cũ" → xong; thêm 4 câu hỏi (ưu đãi cũ đã hết chưa, các hệ còn tuyển không, Pyeongtaek lệch số, có làm tiếp video B2B không); thêm ý tưởng lịch "Chúc mừng visa Gachon".
- Ghi lại cho buổi dạy thiết kế: kênh thật dùng nền xanh nhiều hơn khuôn K4 Du học (nền trắng). Chưa đổi khuôn.

## 17/11/2026 — PM Du học trả lời "Việc chờ quyết" (qua Notion)
**Ai:** PM Du học (trả lời trên Notion), An chuyển cho Claude cập nhật.
- **Video không nói mức giá:** không phí dịch vụ, không 9,5 triệu và từng khoản, không "hoàn 5 triệu". Video chỉ nói chính sách. **An xác nhận 17/11: giữ nghĩa chặt, bỏ mọi con số tiền của công ty trong video.**
- **Video trường:** PM tự đặt đơn kèm số liệu mới nhất. Agent không tự làm video trường, không tự lấy số ở brand.md 2.3b.
- **"Có TOPIK 3 – Có ngay VISA":** không nói, chỉ được hiện chữ ở outro.
- **Học viên Du học:** tất cả đã đồng ý dùng hình ảnh (xin phép trước khi chụp, quay), kể cả video "trước khi bay".
- **Đo lường:** đo chung lượt xem tự nhiên và quảng cáo.
- **Tần suất:** 3 bài/ngày (video + ảnh).
- Đã sửa: `brand.md` (2.2, 2.3, 2.3a, 2.3b, mục 5, mục 6), `huong-dan-kich-ban-du-hoc.md` (mục 0, dạng T/C, mục 4, mẫu mục 8), quy tắc kênh DH trong `tools/script_writer.py`. Notion: 9 việc chuyển "Đã đưa vào brand.md"; ghi chú vào 6 ý tưởng lịch dạng T/C.
- **Còn chờ PM Du học:** video/banner cũ, quyền đăng fanpage thật, người dạy kịch bản, kỳ nhập học và hạn hồ sơ, **mới:** 3 bài/ngày thì mấy video mấy ảnh, ảnh có cần hệ thống làm không.
- PM Tiếng Hàn: chưa trả lời việc nào.

## 13/11/2026 (chiều) — Research fanpage Tiếng Hàn + Notion riêng

- Kéo **4 tháng** page Tiếng Hàn Thầy Tư (An yêu cầu giảm để tiết kiệm): 198 bài + 66 Reels → `phan-tich-fanpage-tieng-han.md`. Dạng A (Thầy Tư giải thích nghịch lý) giữ chân tốt nhất (10–27 s); bài ưu đãi lượt cao nhưng ~3 s; series review 8 cuốn sách đã xong; album "lưu về" tương tác cao nhất. Đã thêm mục 0 vào huong-dan-kich-ban-tieng-han.md.
- Notion: trang 📘 **Tiếng Hàn Thầy Tư** riêng (Đơn video Tiếng Hàn, Lịch nội dung Tiếng Hàn – 6 ý tưởng, Việc chờ PM Tiếng Hàn quyết – 11 việc). **Tách hoàn toàn** với trang Du học: 2 PM, 2 chiến lược. Đơn TH-… đồng bộ lại vào trang này.
- Thử 2 đơn: TH-261113-02 (dạng A: học chăm mà điểm không nhúc nhích), TH-261113-03 (lưu về: gốc 학).

**Còn dở:** ⚠️ PM Tiếng Hàn xác nhận các ưu đãi đang chạy trên page (giảm 10%, giảm 60%, voucher sách) — brand.md vẫn ghi không có khuyến mãi nên hiện cấm viết; giáo viên livestream đồng ý cắt clip chưa.

---

## 13/11/2026 (chiều) — An chốt sau research + thử 2 kịch bản

- "Khuyến mại quý III" và "Quỹ Học Bổng Xanh 250 triệu" **đã dừng**, không nhắc lại (brand.md 2.3, Notion đã cập nhật).
- **Chỉ đăng lên page test** cho đến khi An cho phép đăng 2 page chính.
- Nhiều Reels cũ có KOL (người đại diện, không phải Thầy Tư) nói trước máy quay: hệ thống không thay thế dạng này, mà **chuyển sang chữ động K4** (ghi vào huong-dan-kich-ban-du-hoc.md mục 0).
- Thử 2 đơn: DH-261113-01 (Tập 9 Woosong, ~70s) và DH-261113-02 (Phá lời đồn: chưa biết tiếng Hàn, ~50s) — đang chờ An duyệt trên Telegram.

---

## 13/11/2026 (chiều) — Research fanpage Du học bằng Meta API

- Không dùng Apify: đọc trực tiếp bằng Meta Graph API. An cấp quyền 2 page chính cho app n8n-api; lưu token đọc dài hạn `META_READ_TOKEN` (không hết hạn). Token đăng bài vẫn chỉ trỏ page test. Nhân tiện app giờ chỉ còn quyền trên page test + 2 page chính (đã thu hẹp từ 16 page).
- Kéo 6 tháng page Du Học Thầy Tư: 211 bài + 84 Reels → `phan-tich-fanpage-du-hoc.md`. Kết luận chính: hook = câu hỏi về hiểu lầm/nghịch lý; học viên thật giữ chân tốt nhất; series "Đúng ngành, trúng trường" đã tới Tập 8 → viết tiếp Tập 9; thêm dạng P (phá lời đồn); không đăng nội dung TOPIK trên page Du học.

**Còn dở:** PM xác nhận "khuyến mại quý III" và "Quỹ Học Bổng Xanh 250 triệu" (đang mâu thuẫn với brand.md "không có khuyến mãi"); bài nào đã chạy quảng cáo; học viên trong video "trước khi bay" đồng ý chưa; research page Tiếng Hàn (để sau).

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
