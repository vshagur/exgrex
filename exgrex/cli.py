#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
    sys.stdout.write(json.dumps({'fractionalScore': score, 'feedback': feedback}))
    sys.exit(0)


def load_executor_module(module_name, module_path):
    """загружает модуль executor, определенный пользователем"""
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    executor = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(executor)
    return executor


def is_debug(config):
    """возвращает True, если грейдер запущен в debug режиме, иначе False"""
    # todo добавить возможность установить значение debug, передачей параметра cli или
    # определением переменной debug в файле executor.py
    return os.environ.get(config.env_parameter_debug, '0') != '0'


def main(config=DefaultConfig):
    try:
        cli_parameters = parse(config.cli_parameter_part_id)
        debug = is_debug(config)
        grader = Grader.create_grader(cli_parameters, debug, config)
        module_path = os.path.join(
            grader.cwd, grader.grader_path, config.executor_filename)
        # todo сделать загрузку по умолчанию для случая, когда файл executor.py не найден
        module_name = Path(config.executor_filename).stem
        executor = load_executor_module(module_name, module_path)
        feedback, score = executor.execute_grader(grader)
    except Exception as err:
        tb = sys.exc_info()[2]
        feedback = 'Grader Error.\n' + str(err.with_traceback(tb))  # todo доделать вывод
        score = 0

    # отправим отчет
    send_report(feedback, score)


if __name__ == "__main__":
    main()
