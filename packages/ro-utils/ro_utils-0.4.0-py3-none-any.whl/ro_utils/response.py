def response(
    success: bool, data, code: int, message: str, error: str, error_code: int = 0
):
    """
    return a dictionary containing the results of the request and the associated error message

    Parameters:
        success (bool): Indicates whether the request was successful
        data: The data returned by the request
        code (int): HTTP status code indicating the success or failure of the request
        message (str): Text message detailing the request outcome
        error (str): Error message indicating the reason for the request failure
        error_code (int): Error code associated with the error message

    Return:
        dict: A dictionary containing the response information

    Using case:
        >>> response(True, {"key": "value"}, 200, "success msg", "", 0)
        {'success': True, 'data': {'key': 'value'}, 'code': 200, 'message': 'success msg', 'error': '', 'error_code': 0}
    """  # noqa: E501
    return {
        "success": success,
        "data": data,
        "code": code,
        "message": message,
        "error": error,
        "error_code": error_code,
    }


def success(data, code: int = 200):
    """
    This function is used to return a dictionary containing the results of the request and the associated error message.

    Parameters:
        data: The data returned by the request
        code (int): HTTP status code indicating the success or failure of the request

    Return:
        dict: A dictionary containing the success status, data, and a success message

    Usage example:
        >>> success({"key": "value"}, 200)
        {'success': True, 'data': {'key': 'value'}, 'code': 200, 'message': 'success', 'error': '', 'error_code': 0}
    """  # noqa: E501
    return response(
        True,
        data,
        code,
        "success",
        "",
    )


def error(
    message,
    description: str,
    code: int,
    error_code: int = 0,
):
    """
    Generate a dictionary of error responses

    Parameters:
        message (str): Error message
        description (str): Error description
        code (int): Status code
        error_code (int): Error code

    Return:
        dict: Error response dictionary

    Usage example:
        >>> error("Request failed", "Server internal error", 500, 5000)
        {'success': False, 'data': None, 'code': 500, 'message': 'Request failed', 'error': 'Server internal error', 'error_code': 5000}
    """  # noqa: E501
    return response(False, None, code, message, description, error_code)


def client_error(message, description="", code: int = 400, error_code: int = 0):
    """
    Generate a dictionary of error responses

    Parameters:
        message (str): Error message
        description (str): Error description
        code (int): Status code
        error_code (int): Error code

    Return:
        dict: Error response dictionary

    Usage example:
        >>> client_error("Request failed", "Parameter error", 400, 1001)
        {'success': False, 'data': None, 'code': 400, 'message': 'Request failed', 'error': 'Parameter error', 'error_code': 1001}
    """  # noqa: E501
    return error(message, description, code, error_code)


def server_error(
    message: str, description: str = "", code: int = 500, error_code: int = 0
):
    """
    Generate a dictionary of error responses

    Parameters:
        message (str): Error message
        description (str): Error description
        code (int): Status code
        error_code (int): Error code

    Return:
        dict: Error response dictionary

    Usage example:
        >>> server_error("Request failed", "Server internal error", 500, 5000)
        {'success': False, 'data': None, 'code': 500, 'message': 'Request failed', 'error': 'Server internal error', 'error_code': 5000}
    """  # noqa: E501
    return error(message, description, code, error_code)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
