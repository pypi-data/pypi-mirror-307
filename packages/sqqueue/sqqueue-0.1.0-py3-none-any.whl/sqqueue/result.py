# sqqueue/result.py

from typing import Generic, TypeVar, Union

T = TypeVar("T")
E = TypeVar("E")


class Result(Generic[T, E]):
    pass


class Ok(Result, Generic[T, E]):
    def __init__(self, value: T):
        self.value = value

    def is_ok(self) -> bool:
        return True

    def is_err(self) -> bool:
        return False


class Err(Result, Generic[T, E]):
    def __init__(self, error: E):
        self.error = error

    def is_ok(self) -> bool:
        return False

    def is_err(self) -> bool:
        return True
