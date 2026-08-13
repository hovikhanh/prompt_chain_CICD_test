# 📝 Báo cáo Thực hành Lab 5: Xây dựng Quy trình Tự động

**Học viên:** [Điền tên]
**Ngày thực hiện:** 13-08-2026
**Giáo trình:** A-SDLC - Chương 8.03 Lab 5

---

## 1. Mô tả Dự án

### 1.1 Mục tiêu

Xây dựng quy trình CI/CD trên GitHub Actions có khả năng **tự động phát hiện và sửa lỗi kiểm thử** bằng AI, áp dụng kỹ thuật **Prompt Chaining** (Chuỗi Lặp lại - Iterative Chaining).

### 1.2 Kịch bản

1. Developer push code có lỗi → GitHub Actions tự động chạy pytest
2. Pytest phát hiện lỗi → Script đọc mã nguồn + log lỗi
3. Script gửi prompt R.I.C.H. đến Gemini API → Nhận mã đã sửa
4. Ghi đè file → Chạy lại pytest → Báo cáo kết quả

### 1.3 Công nghệ sử dụng

| Công nghệ | Vai trò |
|---|---|
| Python 3.11 | Ngôn ngữ lập trình |
| Pytest | Framework kiểm thử |
| GitHub Actions | CI/CD platform |
| Gemini API | AI model để sửa lỗi |
| R.I.C.H. Framework | Cấu trúc prompt |

---

## 2. Nhật ký Prompt (Top 5 Prompt quan trọng nhất)

### Prompt 1: R.I.C.H. Prompt chính trong fix_code.py

**Mục đích:** Đây là prompt cốt lõi, được gửi đến Gemini API để yêu cầu AI phân tích và sửa lỗi mã nguồn.

**Lý do thiết kế:** Áp dụng đầy đủ 4 thành phần R.I.C.H. để đảm bảo AI hiểu rõ vai trò, biết chính xác phải làm gì, có đủ bối cảnh, và trả về đúng định dạng mong muốn.

```
### ROLE
You are an expert Python developer and debugger with deep expertise
in writing clean, robust, and well-documented Python code.

### INSTRUCTION
1. Identify ALL bugs in the source code that cause test failures.
2. Fix each bug while preserving the original function signatures.
3. Ensure proper error handling (division by zero → ValueError).
4. Make sure all tests will pass after your fixes.

### CONTEXT
**Source Code (`calculator.py`):** [source code]
**Pytest Error Log:** [error log]

### HALLMARKS
- Provide ONLY the complete, corrected Python code.
- Do NOT include any explanations or markdown formatting.
- Follow PEP 8 coding standards.
```

**Ghi chú:** Phần HALLMARKS rất quan trọng - nếu thiếu, AI sẽ trả về cả giải thích lẫn code, gây khó khăn cho việc parse tự động.

---

### Prompt 2: Yêu cầu tạo calculator.py có lỗi

**Mục đích:** Tạo file mã nguồn mẫu có các lỗi cố ý để demo workflow.

```
Tạo một file calculator.py với 4 hàm: add, subtract, multiply, divide.
Cố ý cài 3 lỗi:
- add() dùng phép trừ thay vì cộng
- subtract() dùng phép cộng thay vì trừ
- divide() thiếu xử lý chia cho 0
Mỗi hàm cần có docstring theo chuẩn Google.
```

**Lý do thiết kế:** Các lỗi đủ đơn giản để AI có thể sửa trong 1 lần, nhưng đủ đa dạng (lỗi logic + thiếu error handling) để minh họa khả năng phân tích.

---

### Prompt 3: Yêu cầu tạo test suite

**Mục đích:** Tạo bộ test toàn diện bao phủ các trường hợp biên.

```
Viết bộ unit test bằng pytest cho calculator.py. Bao gồm:
- Test cơ bản với số dương
- Test với số âm
- Test với số 0
- Test với số thập phân
- Test edge case: chia cho 0 phải raise ValueError
Tổ chức test theo class cho mỗi hàm.
```

**Lý do thiết kế:** Bộ test phải đủ chi tiết để phát hiện được TẤT CẢ các lỗi, đồng thời test các edge case mà AI cần xử lý.

---

### Prompt 4: Thiết kế GitHub Actions workflow

**Mục đích:** Tạo workflow CI/CD tích hợp vòng lặp AI fix.

```
Tạo GitHub Actions workflow thực hiện:
1. Checkout & setup Python
2. Chạy pytest lần 1 (continue-on-error)
3. Nếu fail → gọi script fix_code.py
4. Chạy pytest lần 2
5. Báo cáo kết quả (pass lần 1 / AI sửa thành công / cần can thiệp)
Sử dụng GitHub Secrets cho AI_API_KEY.
```

**Lý do thiết kế:** Workflow cần `continue-on-error: true` ở bước test lần 1 để không dừng pipeline, và conditional steps để chỉ gọi AI khi thực sự cần.

---

### Prompt 5: Parse và làm sạch AI output

**Mục đích:** Xử lý output không nhất quán từ AI.

```
Viết hàm clean_code_output() để:
- Loại bỏ code block markers (```python ... ```)
- Xử lý trường hợp AI trả về giải thích trước/sau code
- Chỉ giữ lại mã Python thuần
- Xử lý nhiều format output khác nhau từ AI
```

**Lý do thiết kế:** AI không phải lúc nào cũng tuân thủ HALLMARKS 100%. Dù prompt yêu cầu "chỉ code", đôi khi AI vẫn wrap trong code blocks. Hàm này đảm bảo mã luôn sạch.

---

## 3. Phản hồi & Bài học Kinh nghiệm

### 3.1 Khó khăn lớn nhất khi làm việc với AI Agent

Thách thức lớn nhất là **kiểm soát định dạng output** từ AI. Dù prompt R.I.C.H. đã chỉ rõ trong phần HALLMARKS rằng AI chỉ cần trả về mã Python thuần, AI vẫn thường xuyên "quên" và thêm markdown code blocks, giải thích, hoặc lời xin lỗi. Điều này đòi hỏi phải xây dựng hàm `clean_code_output()` đủ mạnh để xử lý nhiều trường hợp. Bài học: **Không bao giờ tin tưởng tuyệt đối vào output của AI** - luôn cần lớp hậu xử lý.

### 3.2 Kỹ thuật hiệu quả nhất

**Prompt Chaining (Chuỗi Lặp lại)** là kỹ thuật hiệu quả nhất trong lab này. Thay vì cố gắng giải quyết mọi thứ trong một prompt, việc chia thành: (1) Pytest phát hiện lỗi → (2) AI phân tích & sửa → (3) Pytest xác minh, tạo ra một vòng phản hồi tự nhiên. Mỗi bước có input/output rõ ràng, dễ debug khi có vấn đề. Framework R.I.C.H. cũng cực kỳ hiệu quả - việc gán Role giúp AI tập trung vào lĩnh vực chuyên môn, và HALLMARKS giúp giảm thiểu việc parse output.

### 3.3 Bài học quan trọng về bối cảnh

**Bối cảnh (Context) là yếu tố quyết định chất lượng.** Khi chỉ gửi source code mà không kèm log lỗi pytest, AI phải "đoán" lỗi nằm ở đâu. Nhưng khi cung cấp cả hai (source code + error log), AI có thể chính xác pinpoint từng lỗi cụ thể. Điều này khẳng định nguyên tắc trong giáo trình: *"Chất lượng đầu ra của AI tỷ lệ thuận với chất lượng bối cảnh bạn cung cấp."* Trong thực tế, hãy luôn cung cấp càng nhiều context liên quan càng tốt: stack trace, log lỗi, mã nguồn liên quan, và cả test cases.

---

## 4. Kết luận

Lab 5 đã minh họa thành công việc tích hợp AI vào quy trình CI/CD thông qua kỹ thuật Prompt Chaining. Quy trình này có thể mở rộng cho các dự án thực tế, tuy nhiên cần lưu ý:

- **Giới hạn lặp lại:** Nên đặt giới hạn số lần thử (N lần) để tránh vòng lặp vô hạn
- **Review bởi con người:** AI có thể sửa lỗi sai cách (fix test thay vì fix code). Luôn cần human review
- **Chi phí API:** Mỗi lần gọi Gemini API tốn token. Cần cân nhắc chi phí trong production

---

*Báo cáo được tạo theo yêu cầu Lab 5 - Giáo trình A-SDLC*
