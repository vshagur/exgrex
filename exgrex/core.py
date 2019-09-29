import os
from importlib import import_module
from pathlib import Path


class Grader:
    def __init__(
            self, cwd, grader_path, tests_path, submission_path, solution_filename,
            submission_type, submission_filename=None, score=0, grader_is_failed=False,
            tests_result=None, tests_log=None, failfast=True, traceback=False,
            feedback='', debug=True, solution_path=None, count_tests=None
    ):
        # общие параметры
        self.cwd = cwd  # рабочая директория
        self.grader_path = grader_path  # директория грейдера

        # параметры передачи файла с решением
        self.submission_path = submission_path  # директория с решением
        self.submission_filename = submission_filename  # имя файла с решением
        self.submission_type = submission_type  #

        self.tests_path = tests_path  # директория с тестами
        self.solution_filename = solution_filename  # имя файла с решением для тестов
        self.solution_path = solution_path

        # параметры выполнения
        self.feedback = feedback  # сообщение о результатах проверки
        self.score = score  # оценка по результатам проверки
        self.grader_is_failed = grader_is_failed  # флаг о непрохождении проверки
        self.tests_result = tests_result  # сырые результаты тестов
        self.tests_log = tests_log  # имя лог файла с результатами тестов
        self.failfast = failfast  # флаг остановки проверок на первом падении
        self.traceback = traceback  # флаг вывода traceback
        self.debug = debug  # флаг режима отладки
        self.count_tests = count_tests # количество тестов грейдера

    @classmethod
    def create_grader(cls, cli_parameters, debug, config):
        if debug:
            cwd = os.path.abspath(os.curdir)
            submission_path = config.submission_path_debug
        else:
            cwd = config.cwd
            submission_path = config.submission

        grader_path = cli_parameters[config.cli_parameter_part_id]
        tests_path = config.tests_path
        solution_filename = config.solution_filename
        submission_type = config.submission_type
        return Grader(cwd, grader_path, tests_path, submission_path, solution_filename,
                      submission_type)


def load_execute_module(grader_path, module_filename):
    module_name = '.'.join((grader_path, Path(module_filename).stem))
    return import_module(module_name)

# def execute_grader(grader):
#     return grader.score, grader.feedback
