import importlib.util
import os.path
import shutil
import sys
import unittest
from pathlib import Path
from exgrex.exgrex_exceptions import GraderIOError, GraderRunError


def check_solution_file_exist(ignore_list=None):
    """
    Проверяет наличие файла решения в переданной директории. Устанавливает значение
    grader.submission_filename. Иногда при отладке в debug режиме, в директории с
    решением создаются служебные файлы (например для python: '__pycache__').
    Список таких файлов может быть передан в параметре ignore_list.
    """

    def decorator(func):
        def wrapper(grader):
            nonlocal ignore_list
            ignore_list = ignore_list or []
            paths = [path for path in grader.submission_path.iterdir()
                     if path.is_file and path.name not in ignore_list]

            if not paths:
                raise GraderIOError('Solution file not found.')

            if len(paths) != 1:
                raise GraderIOError('Found several solution files.')

            grader.submission_filename = paths.pop().name

            return func(grader)

        return wrapper

    return decorator


def check_solution_file_name(solution_filename):
    """
    Проверяет правильность имени переданного файла решения. Проверка должна
    производиться после check_solution_file_exist.
    """

    def decorator(func):
        def wrapper(grader):
            if solution_filename != grader.submission_filename:
                raise GraderIOError(f'The solution file: {solution_filename} not found.')
            return func(grader)

        return wrapper

    return decorator


def copy_solution_file(path_to=None):
    """
    Копирует файл с решением в директорию path_to, по-умочанию берется значение
    из grader.tests_path. Устанавливает значение grader.solution_path.
    """

    def decorator(func):
        def wrapper(grader):
            nonlocal path_to

            if path_to is None:
                path_to = grader.tests_path
            else:
                path_to = Path(grader.grader_path, path_to)

            if not path_to.exists():
                path_to.mkdir()

            source = Path(grader.submission_path, grader.submission_filename)
            destination = Path(path_to, grader.solution_filename)

            shutil.copyfile(source, destination)
            grader.solution_path = path_to
            return func(grader)

        return wrapper

    return decorator


def add_solution_as_module(module_name=None):
    """
    Добавляет решение, как модуль (появляется возможность импортировать его в тестах
    через обычный import по имени module_name)
    """

    def decorator(func):
        def wrapper(grader):
            nonlocal module_name
            # todo обработать ошибки импорта решения как модуля
            module_name = module_name or Path(grader.solution_filename).stem
            module_path = Path(grader.cwd, grader.grader_path, grader.solution_filename)
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[spec.name] = module
            return func(grader)

        return wrapper

    return decorator


def run_tests(failfast=None, traceback=None):
    """Запуск unittest тестов. Устанавливает grader.tests_result и grader.count_tests"""

    def decorator(func):
        def wrapper(grader):
            # создание набора тестов, загрузчика
            suite = unittest.TestSuite()
            loader = unittest.TestLoader()
            # создание объекта result и установка настроек (останавливать тесты на
            # первом падении?, выводить traceback?)
            result = unittest.TestResult()
            result.failfast = failfast or grader.failfast
            result.tb_locals = traceback or grader.traceback
            # поиск тестов в директории и добавление их в набор
            tests_path = os.path.join(grader.cwd, grader.grader_path, grader.tests_path)
            tests = loader.discover(tests_path)
            # todo проверить на ошибки loader.error, нужно на время отладки тестов
            # проверить, что загрузчик тестов не будет ловить тесты из решения студента
            suite.addTests(tests)
            # запуск тестов и установка значения grader.tests_result
            try:
                grader.tests_result = suite.run(result)
                grader.count_tests = suite.countTestCases()
            except Exception as err:
                # todo добавить вывод нормального трейсбека
                raise GraderRunError(
                    f'The launch of the tests ended with the fall of the grader.\n {err}')
            return func(grader)

        return wrapper

    return decorator


def format_test_result():
    """
    Обработка результатов тестирования. Установка значений grader.feedback и
    grader.score
    """

    def decorator(func):
        def wrapper(grader):
            # === ошибок нет и все тесты пройдены ===
            if grader.tests_result.wasSuccessful() and not grader.tests_result.errors:
                grader.feedback = 'All tests passed!'
                grader.score = 1
                return func(grader)

            # === есть ошибки ===
            if grader.tests_result.errors:
                # todo написать реализацию
                return func(grader)

            # === не все тесты пройдены ===
            # создаем заголовок сообщения со статистикой:
            # "Test result: total - 5, passed - 2, failed - 1."
            total = grader.count_tests
            failed = len(grader.tests_result.failures)

            if grader.failfast:
                passed = grader.tests_result.testsRun - 1
            else:
                passed = grader.tests_result.count_tests - failed

            result = f'Test results: total - {total}, passed - {passed}, failed - {failed}.\n\n'

            # добавляем в вывод сообщения об упавших тестах
            for test_case_obj, traceback in grader.tests_result.failures:
                # получаем название теста и короткое описание теста (docstring)
                test_name = test_case_obj.id().split('.').pop()
                short_description = test_case_obj.shortDescription()
                # сбрасываем значение traceback, если вывод его не нужен
                traceback = traceback if grader.traceback else ' '
                result += f'FAILED: {test_name}.\nDescription: {short_description}\n{traceback}\n'
                # завершаем вывод сообщений, если требуется вывод только первого упавшего теста
                if grader.failfast:
                    break

            grader.feedback = result
            grader.score = 0
            return func(grader)

        return wrapper

    return decorator
