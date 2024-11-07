from functools import partial
from typing import Callable, Dict, List, Optional
from uuid import uuid4

from . import AsyncTask
from .thread import TaskThread


class AsyncTasksExecutor:
    def __init__(self, max_workers: Optional[int]):
        self.is_shutdown = False
        self.max_workers = max_workers
        self._pending_tasks: List[Callable] = []
        self._running_tasks: Dict[str, TaskThread] = {}

    def shutdown(self):
        self.is_shutdown = True
        while self._running_tasks:
            task_id = list(self._running_tasks.keys())[0]
            del self._running_tasks[task_id]
            AsyncTask.cancel(task_id)

    def submit(self, task, /, *args, **keywords):
        if self.is_shutdown:
            raise RuntimeError("Cannot submit task - executor has been shut down")

        self._pending_tasks.append(partial(task, *args, **keywords))
        self._run_next()

    def _run_next(self):
        if (
            (not self._pending_tasks)
            or self.is_shutdown
            or (self.max_workers and (len(self._running_tasks) >= self.max_workers))
        ):
            return

        task_id = uuid4()
        next_task = self._pending_tasks.pop(0)

        def on_completion(_, __):
            if self._running_tasks.get(task_id):
                del self._running_tasks[task_id]
            self._run_next()

        self._running_tasks[task_id] = AsyncTask.run_async(
            next_task, task_id=task_id, on_completion=on_completion
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.shutdown()
