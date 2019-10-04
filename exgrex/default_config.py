class DefaultConfig:
    """Класс хранения пользовательских настроек."""
    cli_parameter_part_id = 'partId'
    cwd = '/grader'
    env_parameter_debug = 'EXGREX_DEBUG'
    executor_filename = 'executor.py'
    submission_path = '/shared/submission'
    submission_path_debug = 'shared/submission'
    solution_filename = 'solution.py'
    tests_path = 'tests/'
    pytest_command_template = 'pytest --tb=line --junitxml={} {}'
