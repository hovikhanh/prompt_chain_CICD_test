#!/usr/bin/env python3
"""
AI Auto Fix Script - Lab 5: A-SDLC
====================================

Script điều phối AI để tự động sửa lỗi mã nguồn Python.
Sử dụng Gemini API (Google Generative AI) với R.I.C.H. prompt framework.

Quy trình:
1. Đọc mã nguồn bị lỗi (calculator.py)
2. Đọc log lỗi từ pytest (test_results.log)
3. Xây dựng prompt theo framework R.I.C.H.
4. Gọi Gemini API để nhận mã đã sửa
5. Parse và làm sạch output
6. Ghi đè file calculator.py với mã đã sửa

Yêu cầu:
- Biến môi trường AI_API_KEY phải được thiết lập (Gemini API key)
"""

import os
import sys
import re
import json

# ---------------------------------------------------------------------------
# Cấu hình
# ---------------------------------------------------------------------------

SOURCE_FILE = "calculator.py"
TEST_LOG_FILE = "test_results.log"
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"


def read_file(filepath: str) -> str:
    """Đọc nội dung file.

    Args:
        filepath: Đường dẫn đến file cần đọc.

    Returns:
        Nội dung file dưới dạng chuỗi.

    Raises:
        FileNotFoundError: Nếu file không tồn tại.
    """
    if not os.path.exists(filepath):
        print(f"❌ Lỗi: Không tìm thấy file '{filepath}'")
        sys.exit(1)

    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def build_rich_prompt(source_code: str, error_log: str) -> str:
    """Xây dựng prompt theo framework R.I.C.H.

    Framework R.I.C.H. (Role, Instruction, Context, Hallmarks)
    giúp tạo ra các prompt có cấu trúc, rõ ràng và hiệu quả
    cho AI Agent.

    Args:
        source_code: Nội dung mã nguồn bị lỗi.
        error_log: Log lỗi từ pytest.

    Returns:
        Prompt đầy đủ theo chuẩn R.I.C.H.
    """
    prompt = f"""### ROLE
You are an expert Python developer and debugger with deep expertise
in writing clean, robust, and well-documented Python code. You follow
PEP 8 standards and best practices for error handling.

### INSTRUCTION
Analyze the provided source code and the pytest error log carefully.
Your task is to:
1. Identify ALL bugs in the source code that cause test failures.
2. Fix each bug while preserving the original function signatures,
   docstrings, and overall code structure.
3. Ensure proper error handling (e.g., division by zero should raise
   ValueError with message "Không thể chia cho 0").
4. Make sure all tests will pass after your fixes.

### CONTEXT
**Source Code (`calculator.py`):**
```python
{source_code}
```

**Pytest Error Log:**
```
{error_log}
```

### HALLMARKS
- Provide ONLY the complete, corrected Python code for calculator.py.
- Do NOT include any explanations, apologies, markdown formatting,
  or extra text outside of the code.
- Do NOT wrap the code in ```python``` code blocks.
- The output must be valid Python that can be directly saved to a file.
- Preserve all existing docstrings and comments (fix them if needed).
- Follow PEP 8 coding standards.
"""
    return prompt


def call_gemini_api(prompt: str, api_key: str) -> str:
    """Gọi Gemini API để nhận mã đã sửa.

    Args:
        prompt: Prompt đã xây dựng theo R.I.C.H. framework.
        api_key: API key cho Gemini.

    Returns:
        Response text từ Gemini API.

    Raises:
        SystemExit: Nếu API call thất bại.
    """
    import requests

    url = f"{GEMINI_API_URL}?key={api_key}"

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.1,
            "topP": 0.95,
            "maxOutputTokens": 4096,
        },
    }

    headers = {
        "Content-Type": "application/json",
    }

    print("🔄 Đang gửi request đến Gemini API...")

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        print("❌ Lỗi: Request đến Gemini API bị timeout (60s)")
        sys.exit(1)
    except requests.exceptions.HTTPError as e:
        print(f"❌ Lỗi HTTP từ Gemini API: {e}")
        print(f"   Response: {response.text}")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"❌ Lỗi kết nối đến Gemini API: {e}")
        sys.exit(1)

    # Parse response
    try:
        result = response.json()
        generated_text = result["candidates"][0]["content"]["parts"][0]["text"]
        return generated_text
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        print(f"❌ Lỗi khi parse response từ Gemini API: {e}")
        print(f"   Raw response: {response.text[:500]}")
        sys.exit(1)


def clean_code_output(raw_output: str) -> str:
    """Làm sạch output từ AI, loại bỏ code block markers.

    AI đôi khi trả về mã trong các code block markdown (```python ... ```).
    Hàm này loại bỏ các markers đó để chỉ giữ lại mã Python thuần.

    Args:
        raw_output: Output thô từ AI.

    Returns:
        Mã Python đã được làm sạch.
    """
    cleaned = raw_output.strip()

    # Loại bỏ code block markers nếu có
    # Pattern: ```python ... ``` hoặc ``` ... ```
    code_block_pattern = r"^```(?:python)?\s*\n(.*?)```\s*$"
    match = re.match(code_block_pattern, cleaned, re.DOTALL)
    if match:
        cleaned = match.group(1).strip()

    # Loại bỏ bất kỳ text giải thích trước code block
    if "```python" in cleaned:
        start = cleaned.find("```python") + len("```python")
        end = cleaned.find("```", start)
        if end != -1:
            cleaned = cleaned[start:end].strip()

    # Loại bỏ ``` đơn ở đầu/cuối nếu còn sót
    if cleaned.startswith("```"):
        cleaned = cleaned[3:]
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]

    return cleaned.strip()


def write_fixed_code(filepath: str, code: str) -> None:
    """Ghi mã đã sửa vào file.

    Args:
        filepath: Đường dẫn file đích.
        code: Mã nguồn đã được sửa.
    """
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(code)
        if not code.endswith("\n"):
            f.write("\n")

    print(f"✅ Đã ghi mã đã sửa vào '{filepath}'")


def main():
    """Hàm chính - điều phối quy trình sửa lỗi bằng AI."""
    print("=" * 60)
    print("🤖 AI Auto Fix Script - Lab 5: A-SDLC")
    print("=" * 60)

    # 1. Kiểm tra API key
    api_key = os.environ.get("AI_API_KEY")
    if not api_key:
        print("❌ Lỗi: Biến môi trường AI_API_KEY chưa được thiết lập!")
        print("   Hướng dẫn:")
        print("   - Local: export AI_API_KEY='your-gemini-api-key'")
        print("   - GitHub: Settings → Secrets → AI_API_KEY")
        sys.exit(1)

    print(f"✅ Đã tìm thấy API key (***{api_key[-4:]})")

    # 2. Đọc mã nguồn bị lỗi
    print(f"\n📖 Đọc mã nguồn từ '{SOURCE_FILE}'...")
    source_code = read_file(SOURCE_FILE)
    print(f"   → Đã đọc {len(source_code.splitlines())} dòng code")

    # 3. Đọc log lỗi từ pytest
    print(f"📖 Đọc log lỗi từ '{TEST_LOG_FILE}'...")
    error_log = read_file(TEST_LOG_FILE)
    print(f"   → Đã đọc {len(error_log.splitlines())} dòng log")

    # 4. Xây dựng prompt theo R.I.C.H. framework
    print("\n📝 Xây dựng prompt theo framework R.I.C.H....")
    prompt = build_rich_prompt(source_code, error_log)
    print(f"   → Prompt gồm {len(prompt)} ký tự")

    # 5. Gọi AI API
    print("\n🚀 Gọi Gemini API...")
    raw_response = call_gemini_api(prompt, api_key)
    print(f"   → Nhận được response ({len(raw_response)} ký tự)")

    # 6. Làm sạch output
    print("\n🧹 Làm sạch output từ AI...")
    fixed_code = clean_code_output(raw_response)
    print(f"   → Mã đã sửa gồm {len(fixed_code.splitlines())} dòng")

    # 7. Ghi file đã sửa
    print(f"\n💾 Ghi mã đã sửa vào '{SOURCE_FILE}'...")
    write_fixed_code(SOURCE_FILE, fixed_code)

    # 8. Hiển thị diff tóm tắt
    print("\n📋 Nội dung calculator.py sau khi AI sửa:")
    print("-" * 50)
    print(fixed_code)
    print("-" * 50)

    print("\n✅ Hoàn tất! Đang chờ pytest chạy lại...")


if __name__ == "__main__":
    main()
