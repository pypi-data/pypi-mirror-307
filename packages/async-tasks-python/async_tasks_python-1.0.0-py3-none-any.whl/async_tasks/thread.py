import ctypes
from threading import Thread
from typing import Callable, Optional

from .typing import TaskResultHandler, TaskReturn, ThreadStoppedException


class TaskThread(Thread):
    def __init__(
        self,
        task: Callable,
        name: Optional[str] = "TaskThread",
        on_completion: Optional[TaskResultHandler] = None,
    ) -> None:
        Thread.__init__(self, name=name)
        self.daemon = True
        self.task = task
        self.on_completion = on_completion
        self.result: TaskReturn = (None, None)

    def run(self) -> None:
        try:
            self.result = (self.task(), None)
        except BaseException as error:
            self.result = (None, error)
        if self.on_completion:
            self.on_completion(*self.result)

    def stop(self, exception=ThreadStoppedException):
        if not self.is_alive():
            return True
        c_tid = ctypes.c_ulong(self.ident)
        c_exception = ctypes.py_object(exception)
        try:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(c_tid, c_exception)
        except BaseException:
            pass
        return not self.is_alive()
