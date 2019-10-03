from pathlib import Path


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


def glue_code(file_before_path=None, file_after_path=None, path_to=None):
    # todo добавить в параметр - имя файла
    """
    glue_code, указанный в path_to путь должен существовать, путь указывается
    относительно директории грейдера. file_before_path - путь до файла, включая имя файла
    """

    def decorator(func):
        def wrapper(grader):
            nonlocal file_before_path
            nonlocal file_after_path
            nonlocal path_to
            file_paths = []

            if not file_before_path is None:
                file_paths.append(Path(grader.grader_path, Path(file_before_path)))

            file_paths.append(Path(grader.submission_path, grader.submission_filename))

            if not file_after_path is None:
                file_paths.append(Path(grader.grader_path, Path(file_after_path)))

            if path_to is None:
                path_to = grader.tests_path
            else:
                path_to = Path(grader.grader_path, path_to)

            destination_path = Path(path_to, grader.solution_filename)
            text = '\n\n'.join(path.read_text() for path in file_paths)
            destination_path.write_text(text)

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
