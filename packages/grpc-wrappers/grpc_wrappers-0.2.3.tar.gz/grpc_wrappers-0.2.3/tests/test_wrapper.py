from enum import Enum
from typing import Union

import pytest

from example_grpc.example_pb2 import ExampleMessage
from grpc_wrappers import GRPCMessageWrapper, GRPCRepeatedMessageWrapper


def test_direct_instantiation(message):
    with pytest.raises(RuntimeError):
        GRPCMessageWrapper(message)


def test_basic_types(wrapped):
    assert wrapped.bool_value is False
    assert wrapped.int_value == 0
    assert wrapped.string_value == ""

    wrapped.bool_value = True
    wrapped.int_value = 100
    wrapped.string_value = "Test String"
    assert wrapped.bool_value is True
    assert wrapped.int_value == 100
    assert wrapped.string_value == "Test String"

    with pytest.raises(TypeError):
        wrapped.bool_value = "INVALID"

    with pytest.raises(TypeError):
        wrapped.string_value = 10

    assert set(wrapped._compare()) == {
        "bool_value",
        "int_value",
        "string_value",
    }


def test_enum_types(wrapped):
    assert isinstance(wrapped.enum_value, Enum)
    assert wrapped.enum_value == wrapped.enum_value.A
    assert set(wrapped.enum_value.__class__.__members__) == set("ABCDE")

    wrapped.enum_value = "B"
    assert wrapped.enum_value == wrapped.enum_value.B

    wrapped.enum_value = 2
    assert wrapped.enum_value == wrapped.enum_value.C

    with pytest.raises(KeyError):
        wrapped.enum_value = "INVALID"

    assert set(wrapped._compare()) == {"enum_value"}


def test_submessage(wrapped):
    assert isinstance(wrapped.submessage, GRPCMessageWrapper)

    assert wrapped.submessage.bool_value is False

    wrapped.submessage.bool_value = True
    assert wrapped.submessage.bool_value is True

    changes = wrapped._compare()
    assert set(changes) == {"submessage"}
    assert isinstance(changes["submessage"], dict)
    assert set(changes["submessage"]) == {"bool_value"}


def test_nested_submessage(wrapped):
    assert isinstance(wrapped.nested_submessage, GRPCMessageWrapper)

    assert wrapped.nested_submessage.bool_value is False

    wrapped.nested_submessage.bool_value = True
    assert wrapped.nested_submessage.bool_value is True

    changes = wrapped._compare()
    assert set(changes) == {"nested_submessage"}
    assert isinstance(changes["nested_submessage"], dict)
    assert set(changes["nested_submessage"]) == {"bool_value"}


def test_repeated_scalar_types(wrapped):
    assert isinstance(wrapped.int_values, GRPCRepeatedMessageWrapper)

    assert len(wrapped.int_values) == 0

    wrapped.int_values.append(10)
    assert len(wrapped.int_values) == 1

    wrapped.int_values.extend([11, 12, 13])
    assert len(wrapped.int_values) == 4

    wrapped.int_values = [1, 2, 3, 4]
    assert list(wrapped.int_values) == [1, 2, 3, 4]

    with pytest.raises(TypeError):
        wrapped.int_values = "String"
    assert len(wrapped.int_values) == 4

    assert set(wrapped._compare()) == {"int_values"}


def test_repeated_enum_types(wrapped):
    assert isinstance(wrapped.enum_values, GRPCRepeatedMessageWrapper)

    assert len(wrapped.enum_values) == 0

    wrapped.enum_values.append(1)
    assert len(wrapped.enum_values) == 1

    wrapped.enum_values.extend([2, 3, 4])
    assert len(wrapped.enum_values) == 4

    wrapped.enum_values = [1, 2, 3, 4]
    assert [ev.value for ev in wrapped.enum_values] == [1, 2, 3, 4]

    with pytest.raises(Exception):
        # Could be a TypeError or ValueError depending on protobuf version
        wrapped.enum_values = "String"
    assert len(wrapped.enum_values) == 4

    assert set(wrapped._compare()) == {"enum_values"}


def test_repeated_message_types(wrapped):
    assert isinstance(wrapped.submessages, GRPCRepeatedMessageWrapper)

    assert len(wrapped.submessages) == 0

    wrapped.submessages.append(ExampleMessage())
    assert len(wrapped.submessages) == 1

    wrapped.submessages.extend([ExampleMessage(), ExampleMessage(), ExampleMessage()])
    assert len(wrapped.submessages) == 4

    wrapped.submessages = [ExampleMessage()] * 4
    assert len(wrapped.submessages) == 4

    with pytest.raises(TypeError):
        wrapped.submessages = "String"
    assert len(wrapped.submessages) == 4

    assert set(wrapped._compare()) == {"submessages"}
