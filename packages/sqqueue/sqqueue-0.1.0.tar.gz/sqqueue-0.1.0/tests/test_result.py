# tests/test_result.py

from sqqueue.result import Err, Ok, Result


def test_ok_initialization():
    """
    Test that Ok can be initialized with a value and that its methods behave as expected.
    """
    result = Ok(10)

    assert result.is_ok() is True, "Ok instance should return True for is_ok."
    assert result.is_err() is False, "Ok instance should return False for is_err."
    assert result.value == 10, "Ok instance should store the correct value."


def test_err_initialization():
    """
    Test that Err can be initialized with an error and that its methods behave as expected.
    """
    result = Err("An error occurred")

    assert result.is_ok() is False, "Err instance should return False for is_ok."
    assert result.is_err() is True, "Err instance should return True for is_err."
    assert (
        result.error == "An error occurred"
    ), "Err instance should store the correct error message."


def test_ok_type():
    """
    Test that Ok is an instance of Result and behaves generically.
    """
    result: Result[int, str] = Ok(5)

    assert isinstance(result, Result), "Ok should be an instance of Result."
    assert result.is_ok(), "Ok instance should be considered a successful Result."
    assert result.value == 5, "Ok instance should store the correct integer value."


def test_err_type():
    """
    Test that Err is an instance of Result and behaves generically.
    """
    result: Result[int, str] = Err("Error message")

    assert isinstance(result, Result), "Err should be an instance of Result."
    assert result.is_err(), "Err instance should be considered an erroneous Result."
    assert (
        result.error == "Error message"
    ), "Err instance should store the correct error message."


def test_ok_with_different_types():
    """
    Test that Ok can handle different types as values.
    """
    result_str = Ok("Success")
    result_list = Ok([1, 2, 3])

    assert (
        result_str.is_ok() is True
    ), "Ok instance should return True for is_ok with a string."
    assert (
        result_str.value == "Success"
    ), "Ok instance should store the correct string value."

    assert (
        result_list.is_ok() is True
    ), "Ok instance should return True for is_ok with a list."
    assert result_list.value == [
        1,
        2,
        3,
    ], "Ok instance should store the correct list value."


def test_err_with_different_types():
    """
    Test that Err can handle different types as errors.
    """
    result_int = Err(404)
    result_dict = Err({"error": "Not found"})

    assert (
        result_int.is_err() is True
    ), "Err instance should return True for is_err with an integer."
    assert (
        result_int.error == 404
    ), "Err instance should store the correct integer error code."

    assert (
        result_dict.is_err() is True
    ), "Err instance should return True for is_err with a dictionary."
    assert result_dict.error == {
        "error": "Not found"
    }, "Err instance should store the correct dictionary error message."
