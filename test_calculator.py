"""
Test Calculator Module - Lab 5: A-SDLC Auto Fix CI/CD Demo
===========================================================

Bộ kiểm thử (unit test) cho module calculator.py sử dụng pytest.
Các test case này sẽ THẤT BẠI khi chạy với calculator.py gốc (có lỗi),
đóng vai trò kích hoạt quy trình tự động sửa lỗi bằng AI.

Bao gồm các kịch bản kiểm thử:
- Trường hợp cơ bản (positive numbers)
- Số âm (negative numbers)
- Số thập phân (floating point)
- Giá trị 0
- Edge case: chia cho 0
"""

import pytest
from calculator import add, subtract, multiply, divide


# ============================================================
# Test hàm add()
# ============================================================

class TestAdd:
    """Kiểm thử hàm cộng hai số."""

    def test_add_positive_numbers(self):
        """Kiểm tra cộng hai số dương."""
        assert add(2, 3) == 5

    def test_add_negative_numbers(self):
        """Kiểm tra cộng hai số âm."""
        assert add(-1, -1) == -2

    def test_add_mixed_numbers(self):
        """Kiểm tra cộng số dương và số âm."""
        assert add(-1, 1) == 0

    def test_add_with_zero(self):
        """Kiểm tra cộng với số 0."""
        assert add(5, 0) == 5

    def test_add_floating_point(self):
        """Kiểm tra cộng số thập phân."""
        assert add(1.5, 2.5) == pytest.approx(4.0)

    def test_add_large_numbers(self):
        """Kiểm tra cộng số lớn."""
        assert add(1000000, 2000000) == 3000000


# ============================================================
# Test hàm subtract()
# ============================================================

class TestSubtract:
    """Kiểm thử hàm trừ hai số."""

    def test_subtract_positive_numbers(self):
        """Kiểm tra trừ hai số dương."""
        assert subtract(5, 3) == 2

    def test_subtract_negative_result(self):
        """Kiểm tra trừ cho kết quả âm."""
        assert subtract(3, 5) == -2

    def test_subtract_negative_numbers(self):
        """Kiểm tra trừ hai số âm."""
        assert subtract(-5, -3) == -2

    def test_subtract_with_zero(self):
        """Kiểm tra trừ với số 0."""
        assert subtract(5, 0) == 5

    def test_subtract_same_numbers(self):
        """Kiểm tra trừ hai số bằng nhau."""
        assert subtract(7, 7) == 0

    def test_subtract_floating_point(self):
        """Kiểm tra trừ số thập phân."""
        assert subtract(5.5, 2.5) == pytest.approx(3.0)


# ============================================================
# Test hàm multiply()
# ============================================================

class TestMultiply:
    """Kiểm thử hàm nhân hai số."""

    def test_multiply_positive_numbers(self):
        """Kiểm tra nhân hai số dương."""
        assert multiply(3, 4) == 12

    def test_multiply_negative_numbers(self):
        """Kiểm tra nhân hai số âm."""
        assert multiply(-3, -4) == 12

    def test_multiply_mixed_numbers(self):
        """Kiểm tra nhân số dương với số âm."""
        assert multiply(-3, 4) == -12

    def test_multiply_with_zero(self):
        """Kiểm tra nhân với số 0."""
        assert multiply(5, 0) == 0

    def test_multiply_with_one(self):
        """Kiểm tra nhân với số 1."""
        assert multiply(7, 1) == 7

    def test_multiply_floating_point(self):
        """Kiểm tra nhân số thập phân."""
        assert multiply(2.5, 4.0) == pytest.approx(10.0)


# ============================================================
# Test hàm divide()
# ============================================================

class TestDivide:
    """Kiểm thử hàm chia hai số."""

    def test_divide_positive_numbers(self):
        """Kiểm tra chia hai số dương."""
        assert divide(10, 2) == pytest.approx(5.0)

    def test_divide_negative_numbers(self):
        """Kiểm tra chia hai số âm."""
        assert divide(-10, -2) == pytest.approx(5.0)

    def test_divide_mixed_numbers(self):
        """Kiểm tra chia số dương cho số âm."""
        assert divide(-10, 2) == pytest.approx(-5.0)

    def test_divide_result_with_decimals(self):
        """Kiểm tra chia cho kết quả thập phân."""
        assert divide(7, 2) == pytest.approx(3.5)

    def test_divide_by_zero(self):
        """Kiểm tra chia cho 0 phải raise ValueError."""
        with pytest.raises(ValueError, match="Không thể chia cho 0"):
            divide(10, 0)

    def test_divide_zero_by_number(self):
        """Kiểm tra 0 chia cho một số."""
        assert divide(0, 5) == pytest.approx(0.0)

    def test_divide_floating_point(self):
        """Kiểm tra chia số thập phân."""
        assert divide(7.5, 2.5) == pytest.approx(3.0)
