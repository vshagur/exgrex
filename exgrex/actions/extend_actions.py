from pathlib import Path
import zipfile
from exgrex.exgrex_exceptions import GraderIOError


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
            if not zipfile.is_zipfile(
                    Path(grader.submission_path, grader.submission_filename)):
                raise GraderIOError('GraderIOError. Submission should be zip archive')

            return func(grader)

        return wrapper

    return decorator


def check_files_into_zip(filenames_list):
    """
    check_files_into_zip, проверяет наличие необходимых файлов в архиве решения, если
    архив содержит вложенные структуры, необходимо указывать путь + имя файла
    """

    def decorator(func):
        def wrapper(grader):
            nonlocal filenames_list
            zip_path = Path(grader.submission_path, grader.submission_filename)

            try:
                archive = zipfile.ZipFile(zip_path, 'r')
            except Exception as err:
                message = f'GraderIOError. An error occurred while processing the ' \
                          f'archive with the solution. Error - {err.__class__.__name__}'
                raise GraderIOError(message)

            for file_name in filenames_list:
                if file_name not in archive.namelist():
                    message = f'GraderIOError. The solution archive should contain ' \
                              f'the file: {file_name}.'
                    raise GraderIOError(message)

            return func(grader)

        return wrapper

    return decorator


def extract_files_from_zip(filenames):
    """
    extract_files_from_zip, пути указаны относительные для архива и директории грейдера
    """

    def decorator(func):
        def wrapper(grader):
            nonlocal filenames
            zip_path = Path(grader.submission_path, grader.submission_filename)

            try:
                archive = zipfile.ZipFile(zip_path, 'r')
                for file_name, path_to in filenames.items():
                    archive.extract(file_name, Path(grader.grader_path, path_to))
            except Exception as err:
                raise GraderIOError(
                    f'An error occurred while processing the archive with '
                    f'the solution. Error - {err.__class__.__name__}')

            return func(grader)

        return wrapper

    return decorator


def extract_all_from_zip(path_to=None):
    """
    extract_all_from_zip, может понадобиться в заданиях, на генерацию данных, когда
    решение в виде архива потом обрабатывается тестами, если переданный путь не
    существует, он будет создан
    """

    def decorator(func):
        def wrapper(grader):
            nonlocal path_to
            if path_to is None:
                path_to = grader.tests_path
            else:
                path_to = Path(grader.grader_path, path_to)

            zip_path = Path(grader.submission_path, grader.submission_filename)

            try:
                archive = zipfile.ZipFile(zip_path, 'r')
                archive.extractall(path_to)
            except Exception as err:
                message = f'GraderIOError. An error occurred while processing the ' \
                          f'archive with the solution. Error - {err.__class__.__name__}'
                raise GraderIOError(message)

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
            for parameter, value in new_parameters.items:
                setattr(grader, parameter, value)
            return func(grader)

        return wrapper

    return decorator



