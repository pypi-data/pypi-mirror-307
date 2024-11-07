from typing import Any, Callable, Optional, Tuple

TaskResult = Any
TaskError = Optional[BaseException]
TaskReturn = Tuple[TaskResult, TaskError]
TaskResultHandler = Callable[[TaskResult, TaskError], Any]


class ThreadStoppedException(BaseException):
    def __str__(self):
        return self.__class__.__name__


class AsyncTaskException(BaseException):
    def __str__(self):
        return self.__class__.__name__


class AsyncTaskTimeoutException(AsyncTaskException):
    def __str__(self):
        return self.__class__.__name__


class AsyncTaskCanceledException(AsyncTaskException):
    def __str__(self):
        return self.__class__.__name__
