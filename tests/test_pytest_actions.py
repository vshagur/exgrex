from exgrex.actions import base_actions
from exgrex.actions import pytest_actions
from pathlib import Path
from exgrex.core import Grader
import pytest
from exgrex.exgrex_exceptions import GraderIOError


def test_run_tests_create_logfile(create_structure_for_pytest, function):
    # cwd, grader_path, tests_path, submission_path, solution_filename = create_structure_for_pytest
    # grader = Grader(*create_structure_for_pytest)
    # function = pytest_actions.run_tests(function)
    # function = base_actions.copy_solution_file()(function)
    # function = base_actions.check_solution_file_exist()(function)
    # function(grader)
    #
    # assert grader.tests_logfile_path is None
    pass
    # assert grader.tests_logfile_path is not None
    # assert grader.tests_logfile_path.exist()



def test_run_tests_write_logfile(create_structure_for_pytest, function):
    pass


def test_create_report_case_failures(create_structure_for_pytest, function):
    pass


def test_create_report_case_errors(create_structure_for_pytest, function):
    pass


def test_create_report_case_positive(create_structure_for_pytest, function):
    pass


def test_format_test_result_positive(create_structure_for_pytest, function):
    pass


def test_format_test_result_errors(create_structure_for_pytest, function):
    pass


def test_format_test_result_case_failures(create_structure_for_pytest, function):
    pass
