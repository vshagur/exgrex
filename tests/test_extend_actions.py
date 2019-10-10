from exgrex.actions import extend_actions
from exgrex.actions import base_actions
from pathlib import Path
from exgrex.core import Grader
import pytest
from exgrex.exgrex_exceptions import GraderIOError
import zipfile


def test_glue_code_default(create_structure, function):
    # test preparation
    cwd, grader_path, tests_path, submission_path, solution_filename = create_structure
    Path(grader_path, 'before.py').write_text('#file before text')
    Path(grader_path, 'after.py').write_text('#file after text')
    # create a grader object and apply function decorating
    grader = Grader(*create_structure)
    function = extend_actions.glue_code()(function)
    function = base_actions.check_solution_file_exist()(function)
    function(grader)
    # check
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


def test_check_files_into_zip_raises_graderioerror_then_file_not_found(create_structure,
                                                                       function):
    # todo вынести создание zip структуры в одтельную фикстуру
    cwd, grader_path, tests_path, submission_path, solution_filename = create_structure

    with zipfile.ZipFile(Path(submission_path, 'solution.zip'), 'w') as file:
        file.writestr('solution.py', Path(submission_path, 'solution.py').read_text())

    Path(submission_path, 'solution.py').unlink()
    grader = Grader(*create_structure)
    function = extend_actions.check_files_into_zip(['solution.py', 'other_file.txt'])(
        function)
    function = base_actions.check_solution_file_exist()(function)
    with pytest.raises(GraderIOError):
        function(grader)


def test_extract_files_from_zip(create_structure, function):
    cwd, grader_path, tests_path, submission_path, solution_filename = create_structure

    with zipfile.ZipFile(Path(submission_path, 'solution.zip'), 'w') as file:
        file.writestr('solution.py', 'print(100500)')
        file.writestr('newtests/solution1.py', 'print(42)')

    Path(submission_path, 'solution.py').unlink()
    filenames = {'solution.py': 'tests/', 'newtests/solution1.py': 'tests/'}
    grader = Grader(*create_structure)
    function = extend_actions.extract_files_from_zip(filenames)(function)
    function = base_actions.check_solution_file_exist()(function)
    function(grader)
    assert Path(tests_path, 'solution.py').exists()
    assert Path(tests_path, 'newtests/solution1.py').exists()
    assert Path(tests_path, 'solution.py').read_text() == 'print(100500)'
    assert Path(tests_path, 'newtests/solution1.py').read_text() == 'print(42)'


def test_extract_all_from_zip_default(create_structure, function):
    cwd, grader_path, tests_path, submission_path, solution_filename = create_structure

    with zipfile.ZipFile(Path(submission_path, 'solution.zip'), 'w') as file:
        file.writestr('solution.py', 'print(100500)')
        file.writestr('newtests/solution1.py', 'print(42)')

    Path(submission_path, 'solution.py').unlink()
    grader = Grader(*create_structure)
    function = extend_actions.extract_all_from_zip()(function)
    function = base_actions.check_solution_file_exist()(function)
    function(grader)
    assert Path(tests_path, 'solution.py').exists()
    assert Path(tests_path, 'newtests/solution1.py').exists()
    assert Path(tests_path, 'solution.py').read_text() == 'print(100500)'
    assert Path(tests_path, 'newtests/solution1.py').read_text() == 'print(42)'


def test_extract_all_from_zip(create_structure, function):
    cwd, grader_path, tests_path, submission_path, solution_filename = create_structure

    with zipfile.ZipFile(Path(submission_path, 'solution.zip'), 'w') as file:
        file.writestr('solution.py', 'print(100500)')
        file.writestr('newtests/solution1.py', 'print(42)')

    Path(submission_path, 'solution.py').unlink()
    grader = Grader(*create_structure)
    path_to = Path(grader_path, 'tests/dir_name').mkdir()
    function = extend_actions.extract_all_from_zip(path_to='tests/dir_name')(function)
    function = base_actions.check_solution_file_exist()(function)
    function(grader)
    assert Path(grader_path, 'tests/dir_name', 'solution.py').exists()
    assert Path(grader_path, 'tests/dir_name', 'newtests/solution1.py').exists()
    assert Path(grader_path, 'tests/dir_name', 'solution.py').read_text() == \
           'print(100500)'
    assert Path(tests_path, 'dir_name', 'newtests/solution1.py').read_text() == \
           'print(42)'


def test_configure_grader(create_structure, function):
    new_parameters = {'feedback': 'new_feedback',
                      'debug': False,
                      'count_tests': 100,
                      'tests_path': Path('some_path')}
    grader = Grader(*create_structure)
    function = extend_actions.configure_grader(new_parameters)(function)
    function = base_actions.check_solution_file_exist()(function)
    function(grader)
    for parameter, value in new_parameters.items():
        assert getattr(grader, parameter) == value


def test_check_files_into_zip_raises_graderioerror_then_bad_zip(create_structure,
                                                                function):
    # todo
    pass


def test_rename_solution_file(create_structure, function):
    # todo, подумать насколько необходима вообще эта функция (rename_solution_file)
    pass
