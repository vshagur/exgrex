import exgrex.core as core
import pytest
from pathlib import Path
import os


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


def test_create_grader_default(config):
    cwd = Path(config.cwd)
    grader_path = Path('AAA')
    tests_path = Path(config.tests_path)
    submission_path = Path(config.submission_path)
    solution_filename = config.solution_filename
    grader = core.Grader(cwd, grader_path, tests_path, submission_path, solution_filename)
    # check type params
    assert isinstance(grader.cwd, Path)
    assert isinstance(grader.grader_path, Path)
    assert isinstance(grader.tests_path, Path)
    assert isinstance(grader.submission_path, Path)
    assert isinstance(grader.solution_filename, str)
    # check value params
    assert grader.cwd == Path(config.cwd)
    assert grader.grader_path == Path('AAA')
    assert grader.tests_path == Path(config.tests_path)
    assert grader.submission_path == Path(config.submission_path)
    assert grader.solution_filename == config.solution_filename
    # check type default params
    assert grader.submission_filename is None
    assert grader.score == 0
    assert grader.grader_is_failed == False
    assert grader.tests_result is None
    assert grader.tests_logfile_path is None
    assert grader.failfast == True
    assert grader.traceback == False
    assert grader.feedback == ''
    assert grader.solution_path is None
    assert grader.count_tests is None
    assert grader.debug == True


def test_create_grader(config):
    cwd = Path(config.cwd)
    grader_path = Path('AAA')
    tests_path = Path(config.tests_path)
    submission_path = Path(config.submission_path)
    solution_filename = config.solution_filename

    submission_filename = 'some_filename'
    score = 1
    grader_is_failed = True
    tests_result = 'some_tests_result'
    tests_logfile_path = 'some_tests_logfile_path'
    failfast = False
    traceback = True
    feedback = 'some_feedback'
    solution_path = 'some_solution_path'
    count_tests = 'some_count_tests'
    debug = False

    grader = core.Grader(
        cwd, grader_path, tests_path, submission_path, solution_filename,
        submission_filename=submission_filename, score=score,
        grader_is_failed=grader_is_failed, tests_result=tests_result,
        tests_logfile_path=tests_logfile_path, failfast=failfast, traceback=traceback,
        feedback=feedback, solution_path=solution_path, count_tests=count_tests,
        debug=debug)

    # check type params
    assert isinstance(grader.cwd, Path)
    assert isinstance(grader.grader_path, Path)
    assert isinstance(grader.tests_path, Path)
    assert isinstance(grader.submission_path, Path)
    assert isinstance(grader.solution_filename, str)
    # check value params
    assert grader.cwd == Path(config.cwd)
    assert grader.grader_path == Path('AAA')
    assert grader.tests_path == Path(config.tests_path)
    assert grader.submission_path == Path(config.submission_path)
    assert grader.solution_filename == config.solution_filename
    # check type default params
    assert grader.submission_filename == submission_filename
    assert grader.score == score
    assert grader.grader_is_failed == grader_is_failed
    assert grader.tests_result == tests_result
    assert grader.tests_logfile_path == tests_logfile_path
    assert grader.failfast == failfast
    assert grader.traceback == traceback
    assert grader.feedback == feedback
    assert grader.solution_path == solution_path
    assert grader.count_tests == count_tests
    assert grader.debug == debug


@pytest.mark.parametrize(
    'cli_parameters', [
        {'partId': 'AAA'},
        {'partId': 'BBB'},
    ])
def test_create_grader_from_create_grader_method(tmp_path, config, cli_parameters):
    config.cwd = tmp_path
    grader_path = Path(tmp_path, cli_parameters.get(config.cli_parameter_part_id))
    grader_path.mkdir()
    debug = False
    grader = core.Grader.create_grader(cli_parameters, debug, config)
    # check type params
    assert isinstance(grader.cwd, Path)
    assert isinstance(grader.grader_path, Path)
    assert isinstance(grader.tests_path, Path)
    assert isinstance(grader.submission_path, Path)
    assert isinstance(grader.solution_filename, str)
    # check value params
    assert grader.cwd == Path(config.cwd)
    assert grader.grader_path == grader_path
    assert grader.tests_path == Path(grader_path, config.tests_path)
    assert grader.submission_path == Path(config.submission_path)
    assert grader.solution_filename == config.solution_filename
    # check type default params
    assert grader.submission_filename is None
    assert grader.score == 0
    assert grader.grader_is_failed == False
    assert grader.tests_result is None
    assert grader.tests_logfile_path is None
    assert grader.failfast == True
    assert grader.traceback == False
    assert grader.feedback == ''
    assert grader.solution_path is None
    assert grader.count_tests is None
    assert grader.debug == False


@pytest.mark.parametrize(
    'cli_parameters', [
        {'partId': 'AAA'},
        {'partId': 'BBB'},
    ])
def test_create_grader_from_create_grader_method_debug(tmp_path, config, cli_parameters):
    os.chdir(tmp_path)
    config.cwd = tmp_path
    grader_path = Path(tmp_path, cli_parameters.get(config.cli_parameter_part_id))
    grader_path.mkdir()
    debug = True
    grader = core.Grader.create_grader(cli_parameters, debug, config)
    # check type params
    assert isinstance(grader.cwd, Path)
    assert isinstance(grader.grader_path, Path)
    assert isinstance(grader.tests_path, Path)
    assert isinstance(grader.submission_path, Path)
    assert isinstance(grader.solution_filename, str)
    # check value params
    assert grader.cwd == Path(config.cwd)
    assert grader.grader_path == grader_path
    assert grader.tests_path == Path(grader_path, config.tests_path)
    assert grader.submission_path == Path(tmp_path, config.submission_path_debug)
    assert grader.solution_filename == config.solution_filename
    # check type default params
    assert grader.submission_filename is None
    assert grader.score == 0
    assert grader.grader_is_failed == False
    assert grader.tests_result is None
    assert grader.tests_logfile_path is None
    assert grader.failfast == True
    assert grader.traceback == False
    assert grader.feedback == ''
    assert grader.solution_path is None
    assert grader.count_tests is None
    assert grader.debug == True
