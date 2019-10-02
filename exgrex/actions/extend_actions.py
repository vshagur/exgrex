def rename_solution_file(new_filename):
    """
    rename_solution_file
    """

    def decorator(func):
        def wrapper(grader):
            nonlocal new_filename

            return func(grader)

        return wrapper

    return decorator


def configure_grader(new_parameters):
    """
    configure_grader
    """

    def decorator(func):
        def wrapper(grader):
            nonlocal new_parameters

            return func(grader)

        return wrapper

    return decorator


def glue_code(file_before=None, file_after=None):
    """
    glue_code
    """

    def decorator(func):
        def wrapper(grader):
            nonlocal file_before
            nonlocal file_after

            return func(grader)

        return wrapper

    return decorator


def check_zip():
    """
    check_zip
    """

    def decorator(func):
        def wrapper(grader):
            return func(grader)

        return wrapper

    return decorator


def check_files_into_zip(filenames_list):
    """
    check_files_into_zip
    """

    def decorator(func):
        def wrapper(grader):
            nonlocal filenames_list

            return func(grader)

        return wrapper

    return decorator


def extract_files_from_zip(extract_parameters):
    """
    extract_files_from_zip
    """

    def decorator(func):
        def wrapper(grader):
            nonlocal extract_parameters

            return func(grader)

        return wrapper

    return decorator


def extract_all_from_zip(path_to=None):
    """
    extract_all_from_zip
    """

    def decorator(func):
        def wrapper(grader):
            nonlocal path_to

            return func(grader)

        return wrapper

    return decorator


def delete_files(filenames_list):
    """
    delete
    """

    def decorator(func):
        def wrapper(grader):
            nonlocal filenames_list

            return func(grader)

        return wrapper

    return decorator
