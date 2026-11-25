from dataclasses import dataclass, replace
from itertools import count


@dataclass(frozen=True)
class Task:
    id: int
    title: str
    completed: bool = False


class TaskModel:
    def __init__(self) -> None:
        self._tasks: dict[int, Task] = {}
        self._next_id = count(1)

    def tasks(self) -> tuple[Task, ...]:
        return tuple(self._tasks.values())

    def add(self, title: str) -> Task:
        title = title.strip()
        if not title:
            raise ValueError("Введіть назву завдання.")

        task = Task(id=next(self._next_id), title=title)
        self._tasks[task.id] = task
        return task

    def toggle(self, task_id: int) -> None:
        task = self._tasks[task_id]
        self._tasks[task_id] = replace(task, completed=not task.completed)

    def delete(self, task_id: int) -> None:
        del self._tasks[task_id]
