"""
Calculator Module - Lab 5: A-SDLC Auto Fix CI/CD Demo
=====================================================

Module chứa các hàm tính toán cơ bản.
CỐ Ý CÓ LỖI để minh họa quy trình CI/CD tự động sửa lỗi bằng AI.

Các lỗi được cài cắm:
- Hàm add(): Sử dụng phép trừ thay vì phép cộng
- Hàm subtract(): Sử dụng phép cộng thay vì phép trừ
- Hàm divide(): Thiếu xử lý trường hợp chia cho 0
"""


def add(a, b):
    """Cộng hai số.

    Args:
        a: Số thứ nhất.
        b: Số thứ hai.

    Returns:
        Tổng của a và b.
    """
    # BUG: Sử dụng phép trừ thay vì phép cộng
    return a - b


def subtract(a, b):
    """Trừ hai số.

    Args:
        a: Số bị trừ.
        b: Số trừ.

    Returns:
        Hiệu của a và b.
    """
    # BUG: Sử dụng phép cộng thay vì phép trừ
    return a + b


def multiply(a, b):
    """Nhân hai số.

    Args:
        a: Số thứ nhất.
        b: Số thứ hai.

    Returns:
        Tích của a và b.
    """
    return a * b


def divide(a, b):
    """Chia hai số.

    Args:
        a: Số bị chia (tử số).
        b: Số chia (mẫu số).

    Returns:
        Thương của a và b.

    Raises:
        ValueError: Nếu b bằng 0.
    """
    # BUG: Thiếu xử lý trường hợp b == 0
    return a / b
