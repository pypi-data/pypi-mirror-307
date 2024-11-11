import pytest
import file_picker_py


def test_sum_as_string():
    assert file_picker_py.sum_as_string(1, 1) == "2"
