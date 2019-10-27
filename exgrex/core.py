from pathlib import Path
from exgrex.exgrex_exceptions import GraderIOError


class Grader:
    def __init__(
            self, cwd, grader_path, tests_path, submission_path, solution_filename,
            score=0, grader_is_failed=False, failfast=True, debug=True, traceback=False,
            feedback='', submission_filename=None, tests_result=None,
            tests_logfile_path=None, solution_path=None, count_tests=None):
        # общие параметры
        self.cwd = cwd  # рабочая директория
        self.grader_path = grader_path  # директория грейдера
        self.tests_path = tests_path  # директория с тестами
        self.solution_path = solution_path  # директория назначения при копировании файла решения
        self.solution_filename = solution_filename  # имя файла с решением для тестов

        # параметры передачи файла с решением
        self.submission_path = submission_path  # директория с решением
        # assert submission_filename is None
        self.submission_filename = submission_filename  # имя файла с решением

        # параметры выполнения
        self.feedback = feedback  # сообщение о результатах проверки
        self.score = score  # оценка по результатам проверки
        self.grader_is_failed = grader_is_failed  # флаг о непрохождении проверки
        self.tests_result = tests_result  # сырые результаты тестов
        self.tests_logfile_path = tests_logfile_path  # имя лог файла с результатами тестов
        self.failfast = failfast  # флаг остановки проверок на первом падении
        self.traceback = traceback  # флаг вывода traceback
        self.debug = debug  # флаг режима отладки
        self.count_tests = count_tests  # количество тестов грейдера

    @classmethod
    def create_grader(cls, cli_parameters, debug, config):
        if debug == '0':
            cwd = Path(config.cwd)
            submission_path = Path(config.submission_path)
        else:
            cwd = Path.cwd()
            submission_path = Path(cwd, config.submission_path_debug)

        grader_path = Path(cwd, cli_parameters[config.cli_parameter_part_id])

        if not grader_path.exists():
            raise GraderIOError(f'Grader with id: {grader_path.name} not found.')

        tests_path = Path(grader_path, config.tests_path)
        solution_filename = config.solution_filename

        return Grader(
            cwd, grader_path, tests_path, submission_path, solution_filename, debug=debug)
