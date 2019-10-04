from exgrex.default_config import DefaultConfig


def test_default_config():
    assert DefaultConfig.cli_parameter_part_id == 'partId'
    assert DefaultConfig.cwd == '/grader'
    assert DefaultConfig.env_parameter_debug == 'EXGREX_DEBUG'
    assert DefaultConfig.executor_filename == 'executor.py'
    assert DefaultConfig.submission_path == '/shared/submission'
    assert DefaultConfig.submission_path_debug == 'shared/submission'
    assert DefaultConfig.solution_filename == 'solution.py'
    assert DefaultConfig.tests_path == 'tests/'
    assert DefaultConfig.pytest_command_template == 'pytest --tb=line --junitxml={} {}'
