import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from app.validator import validate_sql


def test_block_delete():
    with pytest.raises(ValueError):
        validate_sql("DELETE FROM students;")


def test_allow_select():
    assert validate_sql("SELECT * FROM students;") == True