# async-tasks

<a href="https://pypi.python.org/pypi/async-tasks-python"><img src="http://img.shields.io/pypi/v/async-tasks-python.svg" alt="Latest version on PyPI"></a> <a href="https://pypi.python.org/pypi/async-tasks-python"><img src="https://img.shields.io/pypi/pyversions/async-tasks-python.svg" alt="Compatible Python versions."></a>

A Python library for managing asynchronous tasks—supporting multi-threading, task cancellation, and timeout handling.

## Key Features

- **Timeout Handling**: Automatically stops tasks that exceed a specified time limit.
- **Task Cancellation**: Provides the ability to stop or cancel tasks at any point during execution.
- **Multi-threading**: Runs tasks asynchronously in separate threads to avoid blocking the main thread.

## Installation

To install `async-tasks`, simply run:

```bash
pip install async-tasks-python
```

## Usage Example

### Basic Example: Running and Stopping a Task

```python
import time
from async_tasks import AsyncTask

# Define a long-running task
def long_running_task():
    for i in range(10):
        time.sleep(1)  # Simulate work with a 1-second delay
        print(f"Task running... {i + 1}")
    return "Task completed successfully"

# Run the task asynchronously in a separate thread
task = AsyncTask.run_async(long_running_task, task_id="task1")

# Stop the task after 3 seconds
time.sleep(3)
task.stop()

# Alternatively, cancel the task using its task ID
AsyncTask.cancel("task1")
```

### Example: Timeout and Callback

```python
import time
from async_tasks import AsyncTask

# Define a long-running task
def long_running_task():
    for i in range(10):
        time.sleep(1)  # Simulate work with a 1-second delay
        print(f"Task running... {i + 1}")
    return "Task completed successfully"

# Define a callback function to handle task completion
def on_completion(result, error):
    print("\n✅ Task finished")
    if error:
        print(f"Error: {error}")
    else:
        print(f"Result: {result}")

# Run the task with a timeout (3 seconds)
# If the task exceeds this time, it will be automatically stopped
AsyncTask.run_async(
    long_running_task,
    timeout=3,  # Task will stop if it takes longer than 3 seconds
    on_completion=on_completion,  # Callback function on task completion
)

# Allow some time for the task to run and timeout
time.sleep(5)
```

### Example: Managing a Thread Pool with `AsyncTasksExecutor`

You can manage a pool of asynchronous tasks in a manner similar to using `ThreadPoolExecutor`. This allows you to control the number of concurrent tasks and efficiently manage resources. In this example, we will submit multiple tasks to the executor, track their progress, and handle task completion.

```python
from queue import Queue
from time import sleep

import tqdm

from async_tasks.executor import AsyncTasksExecutor

# Number of concurrent workers
max_workers = 5

# Initialize result storage and result queue
results = []
result_queue = Queue()


def process_task(idx: int) -> None:
    try:
        sleep(1)  # Simulate work with a 1-second delay
        if idx % 2:  # Simulate failure for tasks with odd indices
            raise Exception(f"Task {idx + 1} failed")

        # If the task succeeds, put the result in the queue
        result_queue.put((None, f"Task {idx + 1} completed successfully"))
    except Exception as err:
        result_queue.put((err, None))  # In case of failure, put the error in the queue


# Create an AsyncTasksExecutor to manage a pool of concurrent threads
with AsyncTasksExecutor(max_workers=max_workers) as executor:
    # Submit tasks to the executor
    for idx in range(10):
        executor.submit(process_task, idx)

    # Track and display progress using tqdm for a progress bar
    completed = 0
    with tqdm.tqdm(total=10, desc="Processing Tasks") as process_bar:
        try:
            while completed < 10:
                # Retrieve the result of a completed task from the queue
                res = result_queue.get()
                results.append(res)
                completed += 1
                process_bar.update(1)  # Update the progress bar
        except KeyboardInterrupt:
            # Gracefully handle KeyboardInterrupt and shut down the executor
            print("\nProcess interrupted. Shutting down executor...")
            executor.shutdown()

# Optionally, print the results
print("\nAll tasks completed:")
for result in results:
    print(result)
```

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.
