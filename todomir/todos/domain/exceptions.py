class TodosException(Exception):
    pass


class TaskNotFound(TodosException):
    pass


class TaskAlreadyCompleted(TodosException):
    pass


class TaskNotCompletedYet(TodosException):
    pass
