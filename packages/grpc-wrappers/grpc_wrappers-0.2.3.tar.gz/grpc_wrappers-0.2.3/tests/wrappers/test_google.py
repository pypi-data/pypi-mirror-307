import time

import arrow
import pytest


def test_google_wrappers_get(wrapped):
    assert wrapped.wrapped_bool_value is None
    assert wrapped.wrapped_float_value is None
    assert wrapped.wrapped_string_value is None
    assert wrapped.wrapped_timestamp is None


def test_google_wrappers_set(wrapped):
    timestamp = time.time()

    wrapped.wrapped_bool_value = True
    wrapped.wrapped_float_value = 1000
    wrapped.wrapped_string_value = "Test String"
    wrapped.wrapped_timestamp = timestamp

    assert wrapped.wrapped_bool_value is True
    assert wrapped.wrapped_float_value == 1000
    assert wrapped.wrapped_string_value == "Test String"
    assert arrow.get(wrapped.wrapped_timestamp).timestamp() == pytest.approx(timestamp)

    assert set(wrapped._compare()) == {
        "wrapped_bool_value",
        "wrapped_float_value",
        "wrapped_string_value",
        "wrapped_timestamp",
    }
