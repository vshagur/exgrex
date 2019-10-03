import exgrex.actions.base_actions as actions
import exgrex.actions.extend_actions as extend_actions


@actions.check_solution_file_exist()
# for zip
@extend_actions.check_zip()
@extend_actions.check_files_into_zip(['submission/solution.py'])
@extend_actions.extract_files_from_zip({'submission/solution.py':'tests'})
# for file
# @actions.copy_solution_file()
@actions.run_tests(failfast=False, traceback=False)
@actions.format_test_result()
def execute_grader(grader):
    return grader.feedback, grader.score
