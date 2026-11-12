# PLAYBOOK — Xây "nhà máy nội dung" AI từ con số 0

> Tổng hợp **cách làm** đã dùng để dựng hệ thống video tự động (12/11/2026), viết ở dạng **dùng lại được** cho dự án khác
> (page affiliate, kênh YouTube video hoạt hình React/HTML…). Không chứa thông tin riêng của thương hiệu nào.
> Ví dụ cụ thể của dự án gốc nằm trong `brand.md`, `nhat-ky-quyet-dinh.md`.

---

## 1. Nguyên tắc cốt lõi

| # | Nguyên tắc | Vì sao |
|---|---|---|
| 1 | **Làm một vòng chạy được trước, đẹp sau** | Một dây chuyền thô nhưng chạy trọn (đặt → làm → duyệt → đăng) cho thấy chỗ nghẽn thật. Nâng chất lượng từng khâu sau |
| 2 | **Dữ liệu gốc là nguồn sự thật** | AI đoán chữ theo xác suất → thiếu dữ liệu thì bịa. Giá, cam kết, số liệu chỉ lấy từ văn bản đã xác nhận |
| 3 | **Đánh dấu mức độ chắc chắn** | Mỗi thông tin gắn ✅ đã xác nhận / ⚠️ chưa xác nhận. Agent chỉ dùng ✅ |
| 4 | **Không có người duyệt thì không đăng** | Con người giữ 2 cửa: duyệt kịch bản, duyệt thành phẩm. Tiền và khủng hoảng luôn do người quyết |
| 5 | **Học từ cái đang chạy tốt, không tự nghĩ phong cách** | Phân tích video/banner/lời thoại thật của kênh trước khi thiết kế khuôn |
| 6 | **Mỗi buổi làm việc kết thúc bằng file** | Trí nhớ trong chat mất khi sang chat khác; file trong dự án thì mọi phiên Claude và mọi người đều đọc được |
| 7 | **Quy trình trước, tự động hóa sau, skill sau cùng** | Mục tiêu + bối cảnh → làm thật → rút kinh nghiệm → quy trình → mới đóng gói thành skill |
| 8 | **Chọn công cụ theo chi phí giấy phép + khả năng cho AI điều khiển** | Ưu tiên mã nguồn mở, có API/dòng lệnh, chạy trên máy được |
| 9 | **Bí mật không bao giờ rời `.env`** | Không dán token vào chat, không commit, không in ra log |

---

## 2. Lộ trình triển khai (áp dụng cho dự án mới)

| Giai đoạn | Việc | Đầu ra |
|---|---|---|
| 0. Kế hoạch | Đọc kế hoạch/brief, khoanh **phạm vi nhỏ** (1–2 kênh) | Danh sách việc + câu hỏi còn thiếu |
| 1. Nền thương hiệu | Thu thập (page, website, tài liệu), đối chiếu, ghi brand book | `brand.md` |
| 2. Học từ cái đang có | Phân tích hình (trích khung hình), lời (Whisper), chỉ ra mâu thuẫn | `phong-cach-*.md`, `huong-dan-kich-ban-*.md` |
| 3. Chọn công cụ | Dựng video, giọng, nhận lời, kênh duyệt, kênh đăng | Quyết định ghi vào nhật ký |
| 4. Khuôn mẫu | 1–2 khuôn đầu tiên, render mẫu cho người duyệt xem | Khuôn có biến (đổi nội dung không đổi thiết kế) |
| 5. Dây chuyền | Nối: đặt việc → kịch bản → duyệt → giọng → dựng → duyệt → đăng | Một đơn chạy trọn vòng |
| 6. Vận hành | Bot tự chạy cùng máy, báo cáo định kỳ, cảnh báo, màn hình theo dõi | Hệ thống tự sống không cần mở chat |
| 7. Phân phối | Đăng qua API chính thức, test trên page riêng | Link bài đăng thật |
| 8. Đào tạo | Các bộ phận "dạy" (kịch bản, thiết kế, tiêu chí duyệt) → đóng gói skill | Skill + quy chuẩn từng bộ phận |

---

## 3. Cấu trúc Brand Book (mẫu dùng lại)

Mục tiêu: **hiểu chính xác thương hiệu muốn gì** để agent viết/dựng đúng mà không phải hỏi lại.

```
0. Tài sản dùng chung
   0.1 Nhận diện: logo (từng file + khi nào dùng), màu (mã + vai trò), font (độ đậm theo vai trò), quy tắc đặt logo
   0.2 Giọng đọc: công cụ TTS, giọng mặc định, TỪ ĐIỂN PHÁT ÂM (chữ trên màn hình → chữ viết cho TTS)
1. (Mỗi thương hiệu/kênh)
   1.1 Định danh: link kênh, website, liên hệ, quy mô hiện tại (mốc so sánh)
   1.2 Định vị: 1 câu mô tả, slogan đang dùng, tầm nhìn/sứ mệnh/giá trị
   1.3 Bằng chứng: con số kèm trạng thái ✅/⚠️ và nguồn
   1.4 Cam kết: nội dung + phạm vi áp dụng + điều khoản
   1.5 Sản phẩm & giá: chép từ VĂN BẢN có hiệu lực, ghi số hiệu/ngày; quy định cách nói giá
   1.6 Khách hàng: nhóm · mục tiêu · điểm đau
   1.7 Giọng thương hiệu: tính cách, xưng hô, từ nên dùng, từ cấm
   1.8 Trụ cột nội dung: 3 trục (sản phẩm · điểm đau · khác biệt) + CTA chuẩn
3. Quan hệ giữa các thương hiệu: phễu chéo, điểm phân biệt, cái gì KHÔNG được dùng chung
4. Quy tắc bắt buộc cho agent (đánh số, ngắn, kiểm được)
5. Quyết định vận hành (bảng: hạng mục → quyết định → ngày)
6. Thông tin còn thiếu (checklist)
```

**Cách thu thập:** đọc page/website (trình duyệt), lấy màu bằng CSS và đo màu banner, đọc tài liệu nội bộ (PDF/Word), hỏi người dùng phần còn thiếu.
**Cách xử lý mâu thuẫn:** khi 2–3 nguồn ghi khác nhau (ví dụ số buổi học, khuyến mãi) → **ghi rõ cả 3, đánh ⚠️, cấm agent dùng** tới khi người có thẩm quyền chốt.

**Hai tài liệu học từ thực tế đi kèm brand book:**
- *Phân tích phong cách hình ảnh*: trích khung hình mỗi 3 giây + 3 giây đầu của video cũ, ghép lưới để xem; đo màu chủ đạo của banner; ghi lại bố cục hook, kiểu chữ, sticker, end card, nhịp cắt.
- *Hướng dẫn kịch bản*: chuyển lời video cũ bằng Whisper → đo nhịp nói (âm tiết/giây, số chữ trong 3 giây đầu) → rút **công thức** (các bước của một kịch bản), **ngân hàng câu** (hook, chuyển, đúc kết, CTA), **điều cấm** (số liệu bịa, khan hiếm giả…), **định dạng đầu ra** cho agent, và 2 kịch bản mẫu để duyệt.

---

## 4. Phân chia agent

| Agent | Việc | Hiện thực trong dự án gốc | Trạng thái |
|---|---|---|---|
| ① Điều phối | Nhận việc, chuyển trạng thái, gọi agent khác, báo tiến độ | `tools/telegram_bot.py` (vòng lặp + hàng chờ đơn) | ✅ |
| ② Chiến lược | Lịch nội dung tháng theo trụ cột | Chưa (đang đặt tay bằng `/tao`) | ⏳ |
| ③ Biên kịch | Kịch bản JSON theo hướng dẫn + brand | `tools/script_writer.py` (Claude Code chạy dòng lệnh, chỉ được đọc file) | ✅ |
| ④ Sản xuất chất liệu | Giọng đọc, ảnh/clip | `tools/vbee_tts.py` (giọng) | ✅ giọng |
| ⑤ Dựng | Kịch bản + giọng → MP4 theo khuôn | `tools/video_maker.py` (sinh dự án HyperFrames, render) | ✅ |
| ⑥ Kiểm duyệt | Chấm điểm trước khi tới người duyệt | Hiện **người duyệt** qua Telegram; AI chấm điểm chưa làm | ⏳ |
| ⑦ Đăng | Đăng/lên lịch qua API | `tools/meta_post.py` (Facebook Reels) | ✅ |
| ⑧ Phân tích | Báo cáo, cảnh báo, số liệu | Báo cáo ngày trong bot; số liệu lượt xem chưa làm | ◐ |

**Nguyên tắc chia agent:** mỗi agent = một file công cụ làm **một việc**, đầu vào/đầu ra rõ (JSON, file mp3/mp4), chạy được độc lập bằng dòng lệnh để thử riêng. Điều phối chỉ gọi các công cụ và ghi trạng thái.

---

## 5. Quản lý và vận hành

**Trạng thái một đơn (state machine):**
```
Chờ viết kịch bản → Đang viết kịch bản → Chờ duyệt kịch bản → Kịch bản đã duyệt → Đang dựng video
→ Chờ duyệt video → Đã duyệt video → Đang đăng → Đã đăng | Đã lên lịch | Đã lưu nháp
Trả về (kịch bản/video) + lý do → Viết lại kịch bản → (lặp)     Lỗi … → /lai hoặc /dung để chạy lại
```
Lưu ở `data/orders.json` (sau này đồng bộ Notion). Mỗi đơn có mã `XX-YYMMDD-NN`, lịch sử ai làm gì lúc nào.

**Kênh giao tiếp:**
| Việc | Ở đâu |
|---|---|
| Đặt việc, duyệt, báo cáo, cảnh báo | **Telegram, 1 nhóm chia Topics** (Đặt video · Duyệt kịch bản · Duyệt video · Báo cáo · Cảnh báo) |
| Dạy hệ thống, lập kế hoạch, sửa hệ thống | **Chat trực tiếp với Claude** (mỗi bộ phận một cuộc chat, cùng thư mục) |
| Xem tổng thể, kéo thả lịch | Notion (dự kiến) |

**Bot Telegram:** long polling (không cần máy chủ công khai), nút bấm inline, trả lời "Reply" để ghi lý do, chỉ ID trong danh sách được bấm duyệt, **tin nhắn xác nhận đơn tự cập nhật tiến độ** (biết hệ thống đang chạy tới đâu), lệnh `/tao /cho /ping /lai /dung /baocao`.

**Tự vận hành:** trình giám sát giữ bot luôn chạy (tự khởi động lại, chỉ 1 bản), file `.vbs` trong thư mục Startup của Windows, nhật ký `data/bot.log`, báo cáo 8h sáng, màn hình theo dõi `tools/theo_doi.py`.

**Làm việc nhiều người:** `CLAUDE.md` (Claude tự đọc khi mở thư mục) + `nhat-ky-quyet-dinh.md` + đề bài dạy cho từng bộ phận (`huong-dan-dao-tao/`) + Git/GitHub (`.gitignore` chặn `.env`, dữ liệu vận hành, tài liệu nội bộ, video nặng).

---

## 6. Bộ công cụ và bài học kỹ thuật

| Khâu | Công cụ | Bài học |
|---|---|---|
| Dựng video | **HyperFrames** (HTML → MP4, Apache 2.0, miễn phí) | Remotion mạnh nhưng phải trả giấy phép khi công ty > 3 người (gói tự động ~100 USD/tháng). Luôn `check` + `snapshot` xem khung hình trước khi render. Khung 0 phải là hook (ảnh bìa) |
| Giọng | **Vbee** (tiếng Việt) | Vbee **cắt cụt âm cuối mỗi file** và **không giữ nghỉ đoạn** → mỗi câu một yêu cầu kèm câu đệm, cắt ở chỗ nghỉ trước câu đệm. Viết lời cho TTS theo từ điển phát âm (tên riêng, số) |
| Nhận lời | **faster-whisper large-v3** trên GPU | Cần cài `nvidia-cublas-cu12`, `nvidia-cudnn-cu12` và thêm DLL vào PATH trên Windows. Đưa từ chuyên ngành vào `initial_prompt` |
| Font | Be Vietnam Pro (Việt), Noto Sans KR (Hàn) | Chữ Hàn: `word-break: keep-all` để không ngắt giữa từ; dòng lẫn ngôn ngữ dùng font dự phòng |
| Viết kịch bản tự động | **Claude Code chạy dòng lệnh** (`claude -p`, chỉ cho đọc file) | Phải đăng nhập trên máy chạy; yêu cầu trả **JSON** theo mẫu, tự ghi nguồn đã dùng |
| Duyệt | **Telegram Bot API** | Bật Topics → nhóm đổi ID; bot phải được bật quyền "Manage topics" riêng |
| Đăng Facebook | **Meta Graph API** (`/{page}/video_reels`: start → upload → finish) | Test bằng `DRAFT`. Token: user ngắn hạn → dài hạn (cần App Secret) → token Page không hết hạn. Chạy thật nên dùng **System User** trong Business Portfolio. Có 1 page riêng để test |
| Lưu trữ | Git + GitHub | Code và "bộ não" lên Git; video/media nặng để Drive |

---

## 7. Áp dụng cho dự án khác

### 7.1 Hệ thống page affiliate
- **Brand book rút gọn cho từng ngách/page**: định vị, khách hàng, giọng, trụ cột nội dung, CTA, **từ cấm**.
- **Dữ liệu gốc = nguồn sản phẩm**: giá, link, ưu đãi lấy từ feed/API của nền tảng affiliate tại thời điểm làm video; không để AI tự nhớ giá.
- **Quy tắc bắt buộc thêm**: luôn ghi rõ là **nội dung tiếp thị liên kết** theo quy định nền tảng; không cam kết hiệu quả sản phẩm; không dùng ảnh/video của người khác khi chưa có quyền.
- Dây chuyền giữ nguyên: đặt chủ đề → kịch bản → duyệt → giọng → dựng → duyệt → đăng; thêm agent "lấy dữ liệu sản phẩm".
- ⚠️ **Rủi ro cần cân nhắc trước**: Meta và TikTok cấm hành vi không xác thực (tạo hàng loạt tài khoản/page giả, nội dung trùng lặp hàng loạt) và có thể khóa cả mạng lưới. Không tự động **tạo** tài khoản/page; nên ít page hơn nhưng mỗi page có nội dung riêng, có người thật quản lý, dùng API chính thức.

### 7.2 Kênh YouTube video hoạt hình React/HTML
- Khuôn **16:9 (1920×1080)**, dài hơn → chia chương (mỗi chương một sub-composition), có phụ đề (Whisper xuất SRT).
- HyperFrames dùng HTML/CSS/GSAP; muốn React thì Remotion (lưu ý giấy phép) hoặc dựng React rồi xuất HTML tĩnh.
- Đăng: **YouTube Data API** (OAuth). Lưu ý hạn mức upload hằng ngày và app chưa xác minh thì video tải lên có thể bị để ở chế độ riêng tư → test bằng kênh phụ, xin xác minh app trước khi chạy thật.
- Thêm agent **ảnh bìa (thumbnail)** và **tiêu đề/mô tả/chương** theo SEO.

### 7.3 Checklist bắt đầu một dự án mới
- [ ] Phạm vi nhỏ nhất (1 kênh) và mục tiêu đo được
- [ ] `brand.md` theo mẫu mục 3, đánh ✅/⚠️
- [ ] Thu thập 5–10 nội dung đang chạy tốt → phân tích hình + lời
- [ ] Chọn công cụ (giấy phép, API, chạy trên máy)
- [ ] 1 khuôn + 1 video mẫu → người duyệt xác nhận
- [ ] Bot duyệt (Telegram topics) + 1 page/kênh **test riêng**
- [ ] Dây chuyền chạy trọn 1 đơn
- [ ] Tự khởi động, báo cáo, cảnh báo
- [ ] `CLAUDE.md` + nhật ký + Git (chặn bí mật)
- [ ] Buổi dạy của từng bộ phận → quy chuẩn → skill

---

## 8. Bản đồ file dùng lại

| File | Dùng lại thế nào |
|---|---|
| `tools/telegram_bot.py` | Đổi tên chủ đề, danh sách người duyệt, các bước trong `dispatch_jobs` |
| `tools/giam_sat_bot.py` | Giữ nguyên |
| `tools/script_writer.py` | Đổi đường dẫn file hướng dẫn và mẫu JSON |
| `tools/vbee_tts.py` | Giữ nguyên (đổi giọng trong `.env`) |
| `tools/video_maker.py` | Đổi khuôn cảnh (`scene_html`), kích thước khung |
| `tools/meta_post.py` | Giữ nguyên; đổi page bằng `setup "Tên page"` |
| `tools/whisper_transcribe.py` | Đổi `PROMPT` theo từ chuyên ngành |
| `tools/theo_doi.py` | Giữ nguyên |
| `CLAUDE.md`, `nhat-ky-quyet-dinh.md`, `huong-dan-dao-tao/` | Làm mẫu cho dự án mới |
