#!/usr/bin/env python3
import sys
import os
import json
from exgrex.core import Grader, load_execute_module
from exgrex.default_config import DefaultConfig


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


def main(config=DefaultConfig):
    try:
        cli_parameters = parse(config.cli_parameter_part_id)
        debug = os.environ.get(config.env_parameter_debug, True)
        grader = Grader.create_grader(cli_parameters, debug, config)
        executor = load_execute_module(grader.grader_path, config.executor_filename)
        feedback, score = executor.execute_grader(grader)
    except Exception as err:
        feedback = 'Grader Error.\n' + str(err)
        score = 0

    # отправим отчет
    send_report(feedback, score)


if __name__ == "__main__":
    main()
