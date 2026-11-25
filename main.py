import tkinter as tk

from controller import TaskController
from model import TaskModel
from view import TaskView


def main() -> None:
    root = tk.Tk()
    root.title("Список завдань — MVC")
    root.minsize(440, 300)

    TaskController(TaskModel(), TaskView(root))
    root.mainloop()


if __name__ == "__main__":
    main()
