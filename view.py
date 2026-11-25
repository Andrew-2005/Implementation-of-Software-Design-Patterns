import tkinter as tk
from collections.abc import Callable
from tkinter import ttk

from model import Task


class TaskView(ttk.Frame):
    def __init__(self, parent: tk.Tk) -> None:
        super().__init__(parent, padding=16)
        self.pack(fill="both", expand=True)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(3, weight=1)

        ttk.Label(self, text="Нове завдання").grid(row=0, column=0, sticky="w")
        self._entry = ttk.Entry(self)
        self._entry.grid(row=1, column=0, sticky="ew", pady=(4, 0))
        self._entry.focus_set()

        self._add = ttk.Button(self, text="Додати")
        self._add.grid(row=1, column=1, padx=(8, 0), pady=(4, 0))

        self._message = tk.StringVar(master=self)
        ttk.Label(self, textvariable=self._message, foreground="#a02020").grid(
            row=2, column=0, columnspan=2, sticky="w", pady=(2, 6)
        )

        self._table = ttk.Treeview(
            self, columns=("title", "status"), show="headings", selectmode="browse"
        )
        self._table.heading("title", text="Завдання")
        self._table.heading("status", text="Статус")
        self._table.column("title", width=260)
        self._table.column("status", width=120, stretch=False)
        self._table.grid(row=3, column=0, columnspan=2, sticky="nsew")

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self._table.yview)
        scrollbar.grid(row=3, column=2, sticky="ns")
        self._table.configure(yscrollcommand=scrollbar.set)

        actions = ttk.Frame(self)
        actions.grid(row=4, column=0, columnspan=2, sticky="w", pady=(12, 0))
        self._toggle = ttk.Button(actions, text="Змінити статус")
        self._toggle.pack(side="left", padx=(0, 8))
        self._delete = ttk.Button(actions, text="Видалити")
        self._delete.pack(side="left")
        self._table.bind("<<TreeviewSelect>>", self._update_buttons)
        self._update_buttons()

    def bind_actions(
        self,
        add: Callable[[], None],
        toggle: Callable[[], None],
        delete: Callable[[], None],
    ) -> None:
        self._add.configure(command=add)
        self._toggle.configure(command=toggle)
        self._delete.configure(command=delete)
        self._entry.bind("<Return>", lambda _event: add())

    def title(self) -> str:
        return self._entry.get()

    def clear_title(self) -> None:
        self._entry.delete(0, tk.END)
        self._entry.focus_set()

    def show_message(self, message: str) -> None:
        self._message.set(message)

    def selected_task_id(self) -> int | None:
        selection = self._table.selection()
        return int(selection[0]) if selection else None

    def show_tasks(self, tasks: tuple[Task, ...], selected_id: int | None = None) -> None:
        self._table.delete(*self._table.get_children())
        for task in tasks:
            status = "Виконано" if task.completed else "До виконання"
            self._table.insert("", tk.END, iid=str(task.id), values=(task.title, status))

        if selected_id is not None:
            row = str(selected_id)
            self._table.selection_set(row)
            self._table.focus(row)
            self._table.see(row)

        self._update_buttons()

    def _update_buttons(self, _event: tk.Event | None = None) -> None:
        state = "normal" if self._table.selection() else "disabled"
        self._toggle.configure(state=state)
        self._delete.configure(state=state)
