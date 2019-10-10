from exgrex.actions import base_actions
from pathlib import Path
from exgrex.exgrex_exceptions import GraderIOError
from exgrex.core import Grader
import pytest
import sys


def test_check_solution_file_exist_raises_graderioerror_then_many_solution_files(
        create_structure, function):
    _, _, _, submission_path, _ = create_structure
    path = Path(submission_path, 'other_filename.py')
    path.write_text('print(42)')
    grader = Grader(*create_structure)
    function = base_actions.check_solution_file_exist()(function)
    with pytest.raises(GraderIOError):
        function(grader)


def test_check_solution_file_exist_raises_graderioerror_then_path_not_exist(
        create_structure, function):
    cwd, grader_path, tests_path, submission_path, solution_filename = create_structure
    grader = Grader(*create_structure)
    Path(submission_path, solution_filename).unlink()
    function = base_actions.check_solution_file_exist()(function)
    with pytest.raises(GraderIOError):
        function(grader)


def test_check_solution_file_exist_with_ignore_list(create_structure, function):
    _, _, _, submission_path, _ = create_structure
    path = Path(submission_path, 'other_filename.py')
    path.write_text('print(42)')
    grader = Grader(*create_structure)
    function = base_actions.check_solution_file_exist(['solution.py', ])(function)
    function(grader)
    assert grader.submission_filename == 'other_filename.py'


def test_check_solution_file_exist_set_submission_filename(create_structure, function):
    grader = Grader(*create_structure)
    cwd, grader_path, tests_path, submission_path, solution_filename = create_structure
    Path(submission_path, solution_filename).unlink()
    Path(submission_path, 'other_filename.py').write_text('print(42)')
    function = base_actions.check_solution_file_exist()(function)
    function(grader)
    assert grader.submission_filename == 'other_filename.py'


def test_check_solution_file_name_raises_graderioerror_then_other_filename(
        create_structure, function):
    grader = Grader(*create_structure)
    function = base_actions.check_solution_file_name('other_filename.py')(function)
    with pytest.raises(GraderIOError):
        function(grader)


def test_copy_solution_file_default(create_structure, function):
    cwd, grader_path, tests_path, submission_path, solution_filename = create_structure
    grader = Grader(*create_structure)
    function = base_actions.copy_solution_file()(function)
    function = base_actions.check_solution_file_exist()(function)
    function(grader)
    assert Path(tests_path, solution_filename).exists()
    assert Path(tests_path, solution_filename).read_text() == \
           Path(submission_path, 'solution.py').read_text()
    assert grader.solution_path == Path(tests_path)


def test_copy_solution_file_with_parameter(create_structure, function):
    cwd, grader_path, tests_path, submission_path, solution_filename = create_structure
    Path(grader_path, 'new_path').mkdir()
    grader = Grader(*create_structure)
    function = base_actions.copy_solution_file(
        path_to='new_path', filename='new_filename')(function)
    function = base_actions.check_solution_file_exist()(function)
    function(grader)
    assert grader.solution_filename == 'new_filename'
    assert Path(grader_path, 'new_path', grader.solution_filename).exists()
    assert Path(grader.submission_path, grader.submission_filename).read_text() == \
           Path(grader_path, 'new_path', grader.solution_filename).read_text()
    assert grader.solution_path == Path(grader_path, 'new_path')


def test_add_solution_as_module_default(create_structure, function):
    grader = Grader(*create_structure)
    function = base_actions.add_solution_as_module()(function)
    function = base_actions.copy_solution_file()(function)
    function = base_actions.check_solution_file_exist()(function)
    function(grader)
    assert 'solution' in sys.modules


def test_add_solution_as_module_with_parameter(create_structure, function):
    grader = Grader(*create_structure)
    function = base_actions.add_solution_as_module('some_module_name')(function)
    function = base_actions.copy_solution_file()(function)
    function = base_actions.check_solution_file_exist()(function)
    function(grader)
    assert 'some_module_name' in sys.modules


def test_run_tests_default_set_tests_result_and_count_tests(create_structure, function):
    grader = Grader(*create_structure)
    function = base_actions.run_tests()(function)
    function = base_actions.add_solution_as_module('some_module_name')(function)
    function = base_actions.copy_solution_file()(function)
    function = base_actions.check_solution_file_exist()(function)
    function(grader)
    assert grader.count_tests == 2
    assert grader.tests_result is not None


def test_run_tests_with_parameter(create_structure, function):
    # todo
    pass


def test_format_test_result_set_feedback_and_score(create_structure, function):
    # todo
    pass
