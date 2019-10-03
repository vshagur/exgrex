import exgrex.actions.base_actions as actions
import exgrex.actions.extend_actions as extend_actions

@actions.check_solution_file_exist()
# @extend_actions.check_zip()
@actions.copy_solution_file()
# @extend_actions.glue_code(file_before_path='code_before.txt',
#                           file_after_path='code_after.txt')
@actions.run_tests(failfast=False, traceback=False)
@actions.format_test_result()
def execute_grader(grader):
    return grader.feedback, grader.score
