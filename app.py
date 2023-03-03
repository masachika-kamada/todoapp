import PySimpleGUI as sg
import os


class TaskManager:
    def __init__(self):
        if not os.path.exists("tasks.txt"):
            with open("tasks.txt", "w") as f:
                f.write("")
        with open("tasks.txt", "r") as f:
            self.tasks = f.read().splitlines()

    def add_task(self, task):
        if task and task not in self.tasks:
            self.tasks.append(task)
            with open("tasks.txt", "a") as f:
                f.write(task + "\n")

    def remove_task(self, idx):
        if idx >= 0 and idx < len(self.tasks):
            self.tasks.pop(idx)
            with open("tasks.txt", "w") as f:
                f.writelines("\n".join(self.tasks))


def main():
    task_manager = TaskManager()
    font_text = ("Helvetica", 58)
    font_button = ("Helvetica", 20)
    text_button = "完了"
    max_tasks = 7
    sg.theme("Black")
    content = [
        [sg.Button(text_button, key=f"button_{i}", visible=True, font=font_button),
         sg.Text(task_text, key=f"text_{i}", visible=True, font=font_text)]
        for i, task_text in enumerate(task_manager.tasks[:min(max_tasks, len(task_manager.tasks))])
    ]
    if len(task_manager.tasks) < max_tasks:
        content += [
            [sg.Button(text_button, key=f"button_{i}", visible=False, font=font_button),
             sg.Text("", key=f"text_{i}", visible=False, font=font_text)]
            for i in range(len(task_manager.tasks), max_tasks)
        ]
    layout = [
        [sg.InputText("", size=(10, 1), key="input", font=font_text),
         sg.Button("追加", bind_return_key=True, font=font_button)],
        [sg.Column(content)],
    ]
    window = sg.Window("TODO App", layout, resizable=True, icon="icon.ico", no_titlebar=True, grab_anywhere=True)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break

        if event == "追加":
            task_text = values["input"]
            if task_text.strip():
                task_manager.add_task(task_text.strip())
                window["input"].update("")
                if len(task_manager.tasks) <= max_tasks:
                    window[f"button_{len(task_manager.tasks) - 1}"].update(visible=True)
                    window[f"text_{len(task_manager.tasks) - 1}"].update(task_text.strip(), visible=True)

        if event.startswith("button_"):
            task_index = int(event.split("_")[1])
            task_manager.remove_task(task_index)
            for i, task_text in enumerate(task_manager.tasks[:min(max_tasks, len(task_manager.tasks))]):
                window[f"button_{i}"].update(visible=True)
                window[f"text_{i}"].update(task_text, visible=True)
            for i in range(len(task_manager.tasks), max_tasks):
                window[f"button_{i}"].update(visible=False)
                window[f"text_{i}"].update("", visible=False)

    window.close()


if __name__ == "__main__":
    main()
