class BaseGraderError(Exception):
    """base class for grader exceptions"""


class GraderRunError(BaseGraderError):
    """ошибки возникающие при работе функций действий"""


class GraderIOError(BaseGraderError):
    """ошибки вызова гредера"""