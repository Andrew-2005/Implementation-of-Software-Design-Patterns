from model import TaskModel
from view import TaskView


class TaskController:
    def __init__(self, model: TaskModel, view: TaskView) -> None:
        self._model = model
        self._view = view
        view.bind_actions(self.add_task, self.toggle_task, self.delete_task)
        view.show_tasks(model.tasks())

    def add_task(self) -> None:
        try:
            task = self._model.add(self._view.title())
        except ValueError as error:
            self._view.show_message(str(error))
            return

        self._view.clear_title()
        self._view.show_message("")
        self._view.show_tasks(self._model.tasks(), selected_id=task.id)

    def toggle_task(self) -> None:
        task_id = self._view.selected_task_id()
        if task_id is not None:
            self._model.toggle(task_id)
            self._view.show_tasks(self._model.tasks(), selected_id=task_id)

    def delete_task(self) -> None:
        task_id = self._view.selected_task_id()
        if task_id is not None:
            self._model.delete(task_id)
            self._view.show_tasks(self._model.tasks())
