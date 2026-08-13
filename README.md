# Lab 5: Xây dựng Quy trình Tự động - AI Auto Fix CI/CD

**Ngày thực hiện:** 13-08-2026
**Giáo trình:** A-SDLC (Chương 8.03 - Lab 5)
**Kỹ thuật áp dụng:** Prompt Chaining (Chuỗi Lặp lại / Iterative Chaining)

---

## 🎯 Mục tiêu

Áp dụng kỹ thuật **Prompt Chaining** để xây dựng quy trình CI/CD trên **GitHub Actions** có khả năng **tự động phát hiện và sửa lỗi kiểm thử** bằng AI (Gemini API).

---

## 📋 Kịch bản

Một lập trình viên push một đoạn mã gây ra lỗi unit test. GitHub Actions sẽ tự động:

1. 🧪 **Chạy** các bài test và phát hiện lỗi
2. 📤 **Gửi** mã nguồn bị lỗi và log lỗi đến AI (Gemini API)
3. 📥 **Nhận** lại mã đã sửa từ AI
4. 🔧 **Áp dụng** bản vá và chạy lại các bài test
5. 📊 **Báo cáo** kết quả

```
┌─────────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│  Push Code  │────▶│  Pytest  │────▶│  AI Fix  │────▶│  Re-test │
│  (có lỗi)   │     │  (FAIL)  │     │ (Gemini) │     │  (PASS?) │
└─────────────┘     └──────────┘     └──────────┘     └──────────┘
```

---

## 📁 Cấu trúc Project

```
lab05/
├── calculator.py              # 🐛 Module Python có lỗi (cố ý)
├── test_calculator.py         # ✅ Bộ test pytest (sẽ fail với code gốc)
├── requirements.txt           # 📦 Dependencies
├── README.md                  # 📖 Hướng dẫn (file này)
├── LAB_REPORT.md              # 📝 Báo cáo thực hành
└── .github/
    ├── workflows/
    │   └── auto_fix.yml       # ⚙️ GitHub Actions workflow
    └── scripts/
        └── fix_code.py        # 🤖 Script điều phối AI (R.I.C.H. prompt)
```

---

## 🚀 Hướng dẫn Setup

### Bước 1: Cài đặt Dependencies

```bash
cd lab05
pip install -r requirements.txt
```

### Bước 2: Kiểm tra Tests (sẽ FAIL)

```bash
pytest test_calculator.py -v
```

Bạn sẽ thấy các test thất bại do `calculator.py` có lỗi cố ý:
- `add()` sử dụng phép trừ thay vì phép cộng
- `subtract()` sử dụng phép cộng thay vì phép trừ
- `divide()` thiếu xử lý chia cho 0

### Bước 3: Thiết lập AI API Key

**Chạy local:**
```bash
export AI_API_KEY='your-gemini-api-key'
```

**Trên GitHub:**
1. Vào repository Settings → Secrets and variables → Actions
2. Tạo secret mới: `AI_API_KEY` = Gemini API key của bạn

> 💡 **Lấy API key:** Truy cập [Google AI Studio](https://aistudio.google.com/) → Get API key

### Bước 4: Chạy Script AI Fix (Local)

```bash
# Chạy pytest và lưu log
pytest test_calculator.py -v > test_results.log 2>&1

# Chạy script AI fix
python .github/scripts/fix_code.py

# Kiểm tra lại
pytest test_calculator.py -v
```

### Bước 5: Chạy trên GitHub Actions

1. Push code lên GitHub repository
2. Đảm bảo đã add `AI_API_KEY` vào GitHub Secrets
3. GitHub Actions sẽ tự động chạy workflow `AI Auto Fix CI`
4. Xem kết quả tại tab **Actions** của repository

---

## 🔑 Kỹ thuật áp dụng

### R.I.C.H. Prompt Framework

Script `fix_code.py` sử dụng framework R.I.C.H. để xây dựng prompt:

| Thành phần | Mô tả | Ví dụ trong project |
|---|---|---|
| **[R]ole** | Gán vai trò chuyên gia | "Expert Python developer and debugger" |
| **[I]nstruction** | Chỉ dẫn cụ thể | Phân tích, sửa lỗi, xử lý edge case |
| **[C]ontext** | Bối cảnh đầy đủ | Source code + pytest error log |
| **[H]allmarks** | Định dạng output | Chỉ code Python, không giải thích |

### Prompt Chaining - Chuỗi Lặp lại (Iterative)

```
Prompt A (Pytest)  →  Script (Kiểm tra)  →  Prompt B (AI Fix)
        ↑                                          │
        └──────── Lặp lại nếu vẫn fail ────────────┘
```

---

## 📊 Các lỗi cài cắm trong calculator.py

| Hàm | Lỗi | Mô tả |
|---|---|---|
| `add(a, b)` | `return a - b` | Sử dụng phép trừ thay vì cộng |
| `subtract(a, b)` | `return a + b` | Sử dụng phép cộng thay vì trừ |
| `divide(a, b)` | Thiếu check `b == 0` | Không raise ValueError khi chia cho 0 |

---

## 📝 Tiêu chí đánh giá

- ✅ Quy trình CI/CD hoạt động đúng như mô tả
- ✅ Chất lượng prompt trong script `fix_code.py` (theo R.I.C.H.)
- ✅ Khả năng xử lý và làm sạch output từ AI
- ✅ Báo cáo và minh họa rõ ràng, chuyên nghiệp

---

## 📚 Tài liệu tham khảo

- **Giáo trình:** A-SDLC (Chương 8.03 - Lab 5: Xây dựng Quy trình Tự động)
- **API:** [Google Gemini API](https://ai.google.dev/gemini-api/docs)
- **CI/CD:** [GitHub Actions Documentation](https://docs.github.com/en/actions)
- **Testing:** [Pytest Documentation](https://docs.pytest.org/)
