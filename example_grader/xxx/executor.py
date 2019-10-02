import exgrex.actions.base_actions as actions


@actions.check_solution_file_exist()
@actions.copy_solution_file()
@actions.run_tests(failfast=False, traceback=False)
@actions.format_test_result()
def execute_grader(grader):
    return grader.feedback, grader.score
