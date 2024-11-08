import pytest


@pytest.fixture
def message():
    from example_grpc.example_pb2 import ExampleMessage

    return ExampleMessage()


@pytest.fixture
def wrapped(message):
    from grpc_wrappers import GRPCMessageWrapper

    return GRPCMessageWrapper.for_message(message)
