# Nhà máy nội dung AI — Tiếng Hàn Thầy Tư & Du học Thầy Tư

Dự án của TBT Group: hệ thống AI Agent sản xuất và vận hành video ngắn (Reels/TikTok) cho **2 kênh**:
**Tiếng Hàn Thầy Tư (PC02)** và **Du học Thầy Tư (PC01)**. Mọi phiên Claude mở thư mục này đọc file này trước.

> Trả lời người dùng bằng **tiếng Việt**. Người dùng là quản lý dự án, không phải lập trình viên: giải thích ngắn, rõ, ít thuật ngữ.

## Đọc gì trước khi làm

| File | Nội dung |
|---|---|
| `brand.md` | **Nguồn sự thật**: định vị 2 kênh, bảng giá (07/BG-TBT), màu, font, logo, giọng Vbee + từ điển phát âm, quy tắc bắt buộc, quyết định vận hành |
| `phong-cach-tieng-han.md` | Ngôn ngữ hình ảnh kênh Tiếng Hàn (phân tích từ 11 video, 9 banner) |
| `huong-dan-kich-ban-tieng-han.md` | Công thức kịch bản kênh Tiếng Hàn + mẫu + điều cấm |
| `huong-dan-kich-ban-du-hoc.md` | Công thức kịch bản kênh Du học (4 dạng T/S/C/H) + mẫu + điều cấm |
| `PLAYBOOK.md` | Cách làm tổng quát (nguyên tắc, mẫu brand book, chia agent, vận hành) — dùng lại cho dự án khác |
| `nhat-ky-quyet-dinh.md` | Ai chốt gì, khi nào — **ghi thêm vào đây sau mỗi buổi làm việc** |
| `huong-dan-dao-tao/` | Đề bài cho các buổi bộ phận chuyên môn "dạy" hệ thống |

## Quy tắc không được vi phạm (chi tiết: brand.md mục 4)
1. **Không có người duyệt thì không đăng.** Mọi video qua người duyệt (hiện: An, qua Telegram).
2. **Giá, phí, visa, cam kết chỉ lấy từ dữ liệu đã xác nhận** trong brand.md. Mục ⚠️ chưa xác nhận thì không dùng.
3. **Không có khuyến mãi** → không viết "giảm giá / chỉ hôm nay / còn X suất". Không bịa số liệu (ví dụ "90% người học…").
4. Cam kết TOPIK 3+ luôn kèm "áp dụng theo điều khoản khóa học".
5. Cảnh AI chỉ để minh họa và gắn nhãn AI; học viên, lớp học, Thầy Tư phải là chất liệu thật.
6. Ảnh/tên học viên chỉ dùng khi An xác nhận học viên đồng ý.
7. **Không in, không chép giá trị trong `.env`** (token Vbee, Telegram) vào chat, file, log hay commit.

## Hệ thống đang có (sơ bộ — đã chạy trọn vòng 12/11/2026)

```
Telegram /tao <chủ đề> → Claude viết kịch bản (tools/script_writer.py) → An duyệt kịch bản
  → Vbee tạo giọng → HyperFrames dựng video khuôn K4 (tools/video_maker.py) → An duyệt video → Đăng Facebook (tools/meta_post.py: Đăng ngay / Lên lịch 20:00 / Nháp)
Trả về (kịch bản hoặc video) + lý do → Claude viết lại → chạy lại từ đầu.
```

- Bot **tự chạy cùng Windows**: file `ThayTu-Bot.vbs` trong thư mục Startup gọi `tools/giam_sat_bot.py` (ẩn cửa sổ, tự khởi động lại bot, một bản duy nhất). Nhật ký: `data/bot.log`. Sau khi sửa code bot phải khởi động lại: tắt tiến trình `python.exe … telegram_bot.py run` (trình giám sát tự bật lại sau 10 giây). **Không** chạy thêm `telegram_bot.py run` bằng tay khi giám sát đang chạy. Trạng thái đơn: `data/orders.json`.
- Báo cáo ngày gửi lúc 8h vào chủ đề 📊 Báo cáo (`/baocao` để gửi ngay).
- Nhóm Telegram "Nhà máy nội dung Thầy Tư" có 5 chủ đề (id trong `data/telegram_topics.json`): Đặt video, Duyệt kịch bản, Duyệt video, Báo cáo, Cảnh báo.
- Lệnh: `/tao <chủ đề>` (kênh Tiếng Hàn, mã TH-…), `/tao dh <chủ đề>` hoặc `/taodh <chủ đề>` (kênh Du học, mã DH-…, khuôn K4 nền trắng), `/cho`, `/ping` (bot + Claude đăng nhập chưa), `/lai <mã>` (viết lại kịch bản), `/dung <mã>` (dựng lại video).
- Viết kịch bản dùng Claude Code chạy dòng lệnh trên máy (bản đi kèm Claude desktop) — **phải đăng nhập**: `claude.exe auth login`.
- **Page Facebook để TEST đăng bài: "Allisagi là chân ái"** (META_PAGE_ID trong .env). Không đăng thử lên page thật. Đổi page: `python tools/meta_post.py setup "Tên page"`.
- Theo dõi trên máy: `python tools/theo_doi.py`. Video sinh theo đơn nằm ở `video/jobs/<mã>/` (không đưa lên Git).

| Thành phần | Ở đâu | Ghi chú |
|---|---|---|
| Giọng đọc | `tools/vbee_tts.py` | **Mỗi câu một yêu cầu song song** + câu đệm, cắt ở chỗ nghỉ trước câu đệm (Vbee cắt cụt cuối mỗi file và KHÔNG giữ nghỉ đoạn). Giọng `voice_id_dh` |
| Chuyển lời video | `tools/whisper_transcribe.py` | faster-whisper large-v3 trên GPU RTX 3060 |
| Dựng video | `video/<khuôn>/` | HyperFrames (miễn phí, Apache 2.0). Khuôn **K4 Chữ động** (`th-k4-chu-dong`), **K5 Kết quả học viên** (`th-k5-ket-qua`). Font Be Vietnam Pro, 1080×1920 |
| Duyệt | `tools/telegram_bot.py` | Bot `@thaytu_duyet_bot`, nhóm "Nhà máy nội dung Thầy Tư" (5 Topics). `whoami` / `send` / `run`. Trạng thái: `data/orders.json`, `data/review_queue.json` |
| Notion (chỉ xem) | `tools/notion_sync.py` | Trang "Nhà máy nội dung Thầy Tư" (bản Free, PM vào dạng khách). **Mỗi kênh một trang con riêng cho PM của kênh đó**: đã có trang 🎓 **Du học Thầy Tư** (đơn DH-… vào bảng "Đơn video Du học"); kênh Tiếng Hàn **tạm chưa có trên Notion** (bảng cũ đã vào thùng rác 13/11, bot bỏ qua đơn TH), sẽ làm trang riêng sau. Mỗi trang 3 bảng: **Đơn video** (bot tự đẩy mỗi phút, đừng sửa tay), **Lịch nội dung**, **Việc chờ PM quyết** (PM sửa). Token `NOTION_TOKEN` trong `.env`, id bảng trong `data/notion.json`. Duyệt vẫn trên Telegram |
| Lời thoại 11 video cũ | `tu-lieu/loi-thoai/tieng-han/` | `.txt` đọc, `.json` có thời điểm từng từ |

Lệnh HyperFrames trong mỗi thư mục khuôn: `npx hyperframes check`, `npx hyperframes snapshot --at 1,3`, `npx hyperframes render -o renders/<tên>.mp4`. Đọc skill `/hyperframes` trước khi sửa khuôn.

## Đã chốt (tóm tắt — đầy đủ trong nhat-ky-quyet-dinh.md)
- Công cụ dựng: **HyperFrames** (không dùng Remotion vì phí giấy phép 100 USD/tháng cho công ty >3 người).
- Duyệt và thông báo: **Telegram** (không dùng Zalo). Dashboard: **Notion** (chưa dựng). Đăng Facebook: **Meta Graph API** qua app `n8n-api` (token Page không hết hạn, đang dùng page test). Chạy thật với 2 fanpage cần System User trong Business Portfolio (người dùng chưa có quyền Admin Business). TikTok: tạm qua TikTok Studio.
- Màu: xanh tươi `#1E6FE8` (nền), xanh đậm `#263E8B`, đỏ `#E81E37`, vàng `#FFE360`. Font: **Be Vietnam Pro** cho mọi chữ.
- Video 9:16, **30–90 giây**. Dạy hệ thống và lập kế hoạch: **chat trực tiếp với Claude**; vận hành hằng ngày: Telegram.

## Đang chờ người dùng
- Chốt **số buổi học** (bảng giá 40 buổi/khóa, banner 89/43, video 28/27 — 3 nguồn lệch).
- Xác nhận: ưu đãi 10% còn chạy không; điều kiện câu "Có TOPIK 3 – Có ngay VISA".
- Kênh Du học: mức **phí dịch vụ** (gói 60 triệu?), xác nhận số liệu 3 trường Catholic/Pyeongtaek/Woosong (brand.md 2.3b), video/banner cũ của kênh, nghe kiểm tra phát âm D4-1 / won / IELTS.
- Trả lời các việc trong bảng Notion "Việc chờ PM quyết"; kế hoạch 6 tháng (tài liệu claude.ai/artifact/CeUguQTWg2DBzFshqmvhXW) chờ PM góp ý.
- TikTok Developer App; quyền Admin Business Portfolio để chuyển Meta sang System User + 2 fanpage thật.
- Token Meta đang có quyền trên 16 page (cấp thừa) → nên thu hẹp.
- Các hướng tiếp theo người dùng có thể chọn: kênh Du học, Notion, buổi dạy thiết kế, AI chấm điểm kịch bản (Agent ⑥), Agent Chiến lược (lịch tháng).

## Trạng thái gần nhất (13/11/2026)
- Đơn TH-261112-03 đã chạy trọn vòng và **đã đăng** lên page test. Bot tự chạy cùng Windows, không cần mở app Claude; chỉ cần máy bật, đã đăng nhập Windows, Claude Code còn đăng nhập.
- Remote Control (chat với Claude từ xa) người dùng phải tự bật công tắc trên thanh công cụ app Claude (auto mode chặn Claude tự bật).

## Cách làm việc chung (nhiều người cùng dạy hệ thống)
- Mỗi bộ phận dạy trong **một cuộc chat riêng**, mở **cùng thư mục** này.
- **Mỗi buổi phải kết thúc bằng file**: cập nhật file quy chuẩn/khuôn tương ứng + ghi một mục vào `nhat-ky-quyet-dinh.md` (ngày, người dạy, thay đổi gì, việc còn dở).
- Không để hai người cùng lúc cho Claude sửa cùng một file.
- Lưu thay đổi bằng Git (kho `github.com/andtptit/agents-tbt`). **Không commit**: `.env`, `noi-bo/`, `data/`, video gốc, bản render, file PDF/Word nội bộ (đã chặn trong `.gitignore`). Ảnh (banner, ảnh thật) **được phép** đưa lên (chốt 12/11/2026).
