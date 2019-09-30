from exgrex.actions.default_actions import check_solution_file_exist
from exgrex.actions.default_actions import check_solution_file_name
from exgrex.actions.default_actions import copy_solution_file
from exgrex.actions.default_actions import add_solution_as_module
from exgrex.actions.default_actions import run_tests
from exgrex.actions.default_actions import format_test_result

@check_solution_file_exist()
@check_solution_file_name('solution.py')
@copy_solution_file()
@add_solution_as_module()
@run_tests(failfast=True,traceback=True)
@format_test_result()
def execute_grader(grader):
    print('call execute_grader')
    return grader.score, grader.feedback
