import pytest
from simple_math_pip.number import Integer

def test_integer_creation():
    num = Integer(5)
    assert num.value == 5

def test_integer_invalid_type():
    with pytest.raises(TypeError):
        Integer(5.5)

def test_integer_add():
    num1 = Integer(5)
    num2 = Integer(3)
    result = num1.add(num2)
    assert result.value == 8

def test_integer_subtract():
    num1 = Integer(5)
    num2 = Integer(3)
    result = num1.subtract(num2)
    assert result.value == 2

def test_integer_invalid_operation():
    num = Integer(5)
    with pytest.raises(TypeError):
        num.add(5)