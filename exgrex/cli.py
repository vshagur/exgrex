#!/usr/bin/env python
import sys
import json
from exgrex.core import execute_grader
from exgrex.default_config import DEFAULT_CONFIG


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


def main():
    required_setting_name = DEFAULT_CONFIG['cli_parameter_part_id']
    try:
        # распарсим cli, получим параметры
        parameters = parse(required_setting_name)
        # вызовем исполнитель с параметрами
        feedback, score = execute_grader(parameters)
    except Exception as err:
        feedback = 'Grader Error.\n' + str(err)
        score = 0

    # отправим отчет
    send_report(feedback, score)


if __name__ == "__main__":
    main()
