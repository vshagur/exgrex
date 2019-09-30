def pytest_run_tests(failfast=None, traceback=None):
    """
    pytest_run_tests
    """

    def decorator(func):
        def wrapper(grader):
            nonlocal failfast
            nonlocal traceback

            return func(grader)

        return wrapper

    return decorator

def pytest_format_test_result(b):
    """
    pytest_format_test_result
    """

    def decorator(func):
        def wrapper(grader):
            nonlocal b

            return func(grader)

        return wrapper

    return decorator