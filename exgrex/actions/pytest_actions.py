from pathlib import Path
from exgrex.default_config import DefaultConfig as config
import subprocess
from copy import copy
import xml.etree.ElementTree as ET

# todo добавить замечание в документацию
"""
Важное замечание в директории с тестами не должно быть файла __init__.py, 
иначе pytest будет валиться
"""

TITLE = 'Total tests: {}. Tests failed: {}, Errors: {}. Total time: {}.\n'
POSITIVE_MESSAGE = "All tests passed."


def xml_tree_to_dict(root, is_root=True):
    """создает словарь на основе xml дерева"""
    if is_root:
        return {root.tag: xml_tree_to_dict(root, is_root=False)}

    result_dict = copy(root.attrib)

    if root.text:
        result_dict["_text"] = root.text

    for x in root.findall("./*"):
        if x.tag not in result_dict:
            result_dict[x.tag] = []
        result_dict[x.tag].append(xml_tree_to_dict(x, is_root=False))

    return result_dict


def create_report(raw_data):
    """формирует отчет на основе словаря с результатами тестов"""

    data = raw_data.get('testsuites').get('testsuite').pop()
    test_cases = data['testcase']
    feedback = TITLE.format(data['tests'], data['failures'], data['errors'], data['time'])

    # ошибок грейдера и проваленых тестов нет
    if data['failures'] == '0' and data['errors'] == '0':
        return (feedback + POSITIVE_MESSAGE, 1)

    # есть ошибки грейдера
    if data['errors'] != '0':
        message = 'Grader error. Please check your solution for syntax errors.\n ' \
                  'Or contact your administrator.\n'
        for case in test_cases:
            if 'error' in case:
                traceback = case['error'][0]['_text']
                # todo добавить нормальный traceback
                return (feedback + message + traceback, 0)

    # есть проваленые тесты
    if data['failures'] != '0':

        for case in test_cases:

            if 'failure' in case:
                test_name = case['name']
                text = case['failure'][0]['_text']
                message = 'Failed test - {}.\n {}\n'.format(
                    test_name, text)
                return (feedback + message, 0)
        else:
            return (feedback + 'NotImplemented', 0)


def run_tests(failfast=None, traceback=None, pytest_command_template=None):
    """
    pytest_run_tests
    """

    def decorator(func):
        def wrapper(grader):
            nonlocal failfast
            nonlocal traceback
            nonlocal pytest_command_template
            # todo разобраться с выводом failfast, traceback
            grader.failfast = failfast or grader.failfast
            grader.traceback = traceback or grader.traceback

            if grader.tests_logfile_path is None:
                grader.tests_logfile_path = Path(grader.tests_path, 'tests_result.xml')

            if pytest_command_template is None:
                pytest_command_template = config.pytest_command_template

            command = pytest_command_template.format(
                grader.tests_logfile_path, grader.tests_path).split()

            subprocess.run(command,
                           stderr=subprocess.STDOUT,
                           stdout=subprocess.PIPE,
                           universal_newlines=True,
                           cwd=grader.cwd)
            return func(grader)

        return wrapper

    return decorator


def format_test_result():
    """
    pytest_format_test_result
    """

    def decorator(func):
        def wrapper(grader):
            xml_data = ET.parse(grader.tests_logfile_path).getroot()
            raw_data = xml_tree_to_dict(xml_data)
            grader.feedback, grader.score = create_report(raw_data)
            return func(grader)

        return wrapper

    return decorator
