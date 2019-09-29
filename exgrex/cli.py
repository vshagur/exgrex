#!/usr/bin/env python3
import sys
import os
import json
import importlib.util
from exgrex.core import Grader
from exgrex.default_config import DefaultConfig
from pathlib import Path


def parse(required_setting_name):
    """returns the dictionary with the cli parameters passed to the grader"""
    parameters = {key: value for key, value in zip(*(iter(sys.argv[1:]),) * 2)}
    if required_setting_name in parameters:
        return parameters
    raise KeyError(f'The required {required_setting_name} argument is not passed.')


def send_report(feedback, score):
    """sends a report with the result of the grader’s checks"""
    sys.stdout.write(json.dumps({'feedback': feedback, 'score': score}))
    sys.exit(0)


def load_executor_module(module_name, module_path):
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    executor = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(executor)
    return executor


def main(config=DefaultConfig):
    try:
        cli_parameters = parse(config.cli_parameter_part_id)
        debug = os.environ.get(config.env_parameter_debug, True)
        grader = Grader.create_grader(cli_parameters, debug, config)
        module_path = os.path.join(
            grader.cwd, grader.grader_path, config.executor_filename)
        module_name = Path(config.executor_filename).stem
        executor = load_executor_module(module_name, module_path)
        feedback, score = executor.execute_grader(grader)
    except Exception as err:
        tb = sys.exc_info()[2]
        feedback = 'Grader Error.\n' + str(err.with_traceback(tb)) # todo доделать вывод
        score = 0

    # отправим отчет
    send_report(feedback, score)


# def main(config=DefaultConfig):
# try:
#     cli_parameters = parse(config.cli_parameter_part_id)
#     debug = os.environ.get(config.env_parameter_debug, True)
#     grader = Grader.create_grader(cli_parameters, debug, config)
#     module_path = os.path.join(grader.cwd, grader.grader_path)
#     executor = load_execute_module(module_path, config.executor_filename)
#     feedback, score = executor.execute_grader(grader)
# except Exception as err:
#     feedback = 'Grader Error.\n' + str(err)
#     score = 0
#
# # отправим отчет
# send_report(feedback, score)


if __name__ == "__main__":
    main()
