import time
from typing import Any, Callable, Dict, Optional
from uuid import uuid4

from .thread import TaskThread
from .typing import (
    AsyncTaskCanceledException,
    AsyncTaskTimeoutException,
    TaskResultHandler,
)


class AsyncTask:
    _running_tasks: Dict[str, TaskThread] = {}

    @classmethod
    def run(
        cls,
        task: Callable,
        task_id=uuid4(),
        task_name=None,
        timeout: Optional[float] = None,
    ):
        task_thread = cls.run_async(
            task=task, task_id=task_id, task_name=task_name, timeout=timeout
        )
        task_thread.join()
        if cls._running_tasks.get(task_id):
            cls._running_tasks.pop(task_id)
        return task_thread.result

    @classmethod
    def cancel(cls, task_id: str):
        task_thread = cls._running_tasks.get(task_id)
        if task_thread:
            cls._running_tasks.pop(task_id)
            task_thread.stop(AsyncTaskCanceledException)

    @classmethod
    def run_async(
        cls,
        task: Callable,
        task_id=uuid4(),
        task_name="AsyncTask",
        timeout: Optional[float] = None,
        on_completion: Optional[TaskResultHandler] = None,
    ):
        ref: Dict[str, Any] = {"timeout_thread": None}

        def _on_completion(res, err):
            timeout_thread = ref.get("timeout_thread")
            if timeout_thread:
                timeout_thread.stop()
            if on_completion:
                on_completion(res, err)

        task_thread = TaskThread(
            task=task, name=f"{task_name}_{task_id}", on_completion=_on_completion
        )
        cls._running_tasks[task_id] = task_thread

        def _timeout_thread():
            start = time.time()
            while (time.time() - start) < timeout:
                if not cls._running_tasks.get(task_id):
                    return
                time.sleep(0.01)
            task_thread.stop(AsyncTaskTimeoutException)

        if timeout:
            timeout_thread = TaskThread(
                task=_timeout_thread, name=f"{task_name}_{task_id}_timeout"
            )
            ref["timeout_thread"] = timeout_thread
            timeout_thread.start()

        task_thread.start()
        return task_thread
