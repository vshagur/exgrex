import pytest
from pathlib import Path

TEXT_TEST_FILE = \
"""import unittest
import solution


class TestSumma(unittest.TestCase):
    def test_summa(self):
        self.assertEqual(solution.summa(3, 6), 9), 'add you comment here'

    def test_summa_zero(self):
        self.assertEqual(solution.summa(0, 0), 0)
"""

TEXT_SOLUTION_FILE = \
"""def summa(x, y):
    return x + y"""


@pytest.fixture(scope='function')
def config():
    class DefaultConfig:
        cli_parameter_part_id = 'partId'
        cwd = '/grader'
        env_parameter_debug = 'EXGREX_DEBUG'
        executor_filename = 'executor.py'
        submission_path = '/shared/submission'
        submission_path_debug = 'shared/submission'
        solution_filename = 'solution.py'
        tests_path = 'tests/'
        pytest_command_template = 'pytest --tb=line --junitxml={} {}'

    return DefaultConfig


@pytest.fixture()
def function():
    def execute_grader(grader):
        return grader.feedback, grader.score

    return execute_grader


@pytest.fixture()
def solution_file_text():
    return TEXT_SOLUTION_FILE


@pytest.fixture()
def test_file_text():
    return TEXT_TEST_FILE


@pytest.fixture()
def create_structure(tmp_path, solution_file_text, test_file_text):
    cwd = tmp_path
    grader_path = Path(tmp_path, 'XXX')
    grader_path.mkdir()
    tests_path = Path(grader_path, 'tests')
    tests_path.mkdir()
    submission_path = Path(tmp_path, 'shared')
    submission_path.mkdir()
    submission_path = Path(submission_path, 'submission')
    submission_path.mkdir()
    solution_filename = 'solution.py'
    Path(submission_path, solution_filename).write_text(solution_file_text)
    Path(tests_path, 'test_solution.py').write_text(test_file_text)
    return cwd, grader_path, tests_path, submission_path, solution_filename
