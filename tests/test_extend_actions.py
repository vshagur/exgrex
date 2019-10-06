from exgrex.actions import extend_actions
from exgrex.actions import base_actions
from pathlib import Path
from exgrex.core import Grader
import pytest
from exgrex.exgrex_exceptions import GraderIOError


def test_glue_code_default(create_structure, function):
    cwd, grader_path, tests_path, submission_path, solution_filename = create_structure
    grader = Grader(*create_structure)
    Path(grader_path, 'before.py').write_text('#file before text')
    Path(grader_path, 'after.py').write_text('#file after text')
    function = extend_actions.glue_code()(function)
    function = base_actions.check_solution_file_exist()(function)
    function(grader)
    assert Path(tests_path, solution_filename).exists()
    assert grader.solution_path == Path(tests_path)
    assert Path(tests_path, solution_filename).read_text() == \
           Path(grader.submission_path, grader.submission_filename).read_text()


def test_glue_code_with_parameters(create_structure, function):
    cwd, grader_path, tests_path, submission_path, solution_filename = create_structure
    grader = Grader(*create_structure)
    Path(grader_path, 'before.py').write_text('#file before text')
    Path(grader_path, 'after.py').write_text('#file after text')
    function = extend_actions.glue_code(file_before_path='before.py',
                                        file_after_path='after.py')(function)
    function = base_actions.check_solution_file_exist()(function)
    function(grader)
    text = Path(grader.submission_path, grader.submission_filename).read_text()
    expected_text = '\n\n'.join(['#file before text', text, '#file after text'])
    assert Path(tests_path, solution_filename).exists()
    assert grader.solution_path == Path(tests_path)
    assert Path(tests_path, solution_filename).read_text() == expected_text


def test_check_zip_raises_graderioerror_then_file_not_zip(create_structure, function):
    grader = Grader(*create_structure)
    function = extend_actions.check_zip()(function)
    function = base_actions.check_solution_file_exist()(function)
    with pytest.raises(GraderIOError):
        function(grader)


def test_check_files_into_zip(create_structure, function):
    pass


def test_check_files_into_zip_raises_graderioerror_then_bad_zip(create_structure,
                                                                function):
    pass


def test_check_files_into_zip_raises_graderioerror_then_file_not_found(create_structure,
                                                                       function):
    pass


def test_extract_files_from_zip(create_structure, function):
    pass


def test_extract_all_from_zip(create_structure, function):
    pass


def test_rename_solution_file(create_structure, function):
    pass


def configure_grader(create_structure, function):
    pass
