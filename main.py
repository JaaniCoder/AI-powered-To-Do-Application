# main.py
import flet as ft
from flet import Checkbox, Column, Row, Text, TextField, ElevatedButton, Page, IconButton, icons
from model import categorize_task, get_related_words  # Import AI functions from model.py


class TodoApp:
    def __init__(self, page: Page):
        self.page = page
        self.page.title = "To-Do List Application"
        self.page.bgcolor = "teal"
        self.page.scroll = "adaptive"
        self.page.update()

        # Data storage for tasks
        self.tasks = {'Work': [], 'Personal': []}

        # Input box for new tasks
        self.task_input = TextField(label="Add a Task", expand=True, on_change=self.update_suggestions)

        # Suggestion label
        self.suggestion_label = Text("Related suggestions: ", size=16)

        # Work and Personal Columns
        self.work_column = Column(controls=[Text("Work Category", size=20, weight="bold")])
        self.personal_column = Column(controls=[Text("Personal Category", size=20, weight="bold")])

        # Main layout with buttons for adding to specific categories
        self.main_layout = Column(
            controls=[
                Row([self.task_input, ElevatedButton(text="Add to Work", on_click=self.add_task_to_work),
                     ElevatedButton(text="Add to Personal", on_click=self.add_task_to_personal)]),
                self.suggestion_label,
                Row([self.work_column, self.personal_column]),
            ]
        )

        # Adding the main layout to the page
        self.page.add(self.main_layout)

    # Function to update suggestions based on input
    def update_suggestions(self, e):
        input_text = e.control.value.strip()
        if input_text:
            suggestions = get_related_words(input_text)
            self.suggestion_label.value = f"Related suggestions: {', '.join(suggestions)}"
        else:
            self.suggestion_label.value = "Related suggestions: "
        self.page.update()

    # Function to add a new task to Work category
    def add_task_to_work(self, e):
        task_text = self.task_input.value.strip()
        if task_text:
            self.add_task(task_text, 'Work')

    # Function to add a new task to Personal category
    def add_task_to_personal(self, e):
        task_text = self.task_input.value.strip()
        if task_text:
            self.add_task(task_text, 'Personal')

    # Generic function to add a task to a specified category
    def add_task(self, task_text, category):
        # Creating the task item with editing and deletion options
        task_item = TaskItem(task_text, category, self.remove_task, self.mark_completed)

        # Add to appropriate column based on the category
        if category == 'Work':
            self.tasks['Work'].append(task_text)
            self.work_column.controls.append(task_item)
        else:
            self.tasks['Personal'].append(task_text)
            self.personal_column.controls.append(task_item)

        # Clear input and update the page
        self.task_input.value = ""
        self.page.update()

    # Function to remove a task
    def remove_task(self, task_item, category):
        if category == 'Work':
            self.work_column.controls.remove(task_item)
            self.tasks['Work'].remove(task_item.task_text)
        else:
            self.personal_column.controls.remove(task_item)
            self.tasks['Personal'].remove(task_item.task_text)
        self.page.update()

    # Function to mark a task as completed
    def mark_completed(self, checkbox, task_item):
        if checkbox.value:
            task_item.task_label.color = "gray"
            task_item.task_label.value = f"[Completed] {task_item.task_text}"
        else:
            task_item.task_label.color = "black"
            task_item.task_label.value = task_item.task_text
        self.page.update()


class TaskItem(Row):
    def __init__(self, task_text, category, remove_callback, complete_callback):
        super().__init__()
        self.task_text = task_text
        self.category = category
        self.remove_callback = remove_callback
        self.complete_callback = complete_callback

        # Task completion checkbox
        self.checkbox = Checkbox(on_change=lambda e: complete_callback(e, self))

        # Task label
        self.task_label = Text(task_text)

        # Edit button
        self.edit_button = IconButton(icon=icons.EDIT, on_click=self.edit_task)

        # Remove button
        self.remove_button = IconButton(icon=icons.DELETE, on_click=self.remove_task)

        # Adding controls to the row
        self.controls.extend([self.checkbox, self.task_label, self.edit_button, self.remove_button])

    # Function to edit a task
    def edit_task(self, e):
        new_text = self.task_label.value.replace("[Completed] ", "")  # Remove 'Completed' tag if present
        edit_field = TextField(value=new_text, on_submit=self.save_edit)
        self.controls[1] = edit_field  # Replace task label with edit field
        self.page.update()

    # Function to save the edited task
    def save_edit(self, e):
        new_text = e.control.value.strip()
        if new_text:
            self.task_text = new_text
            self.task_label.value = new_text
            self.controls[1] = self.task_label  # Replace edit field with updated task label
        self.page.update()

    # Function to remove the task
    def remove_task(self, e):
        self.remove_callback(self, self.category)


# Main function to run the application
def main(page: Page):
    TodoApp(page)


if __name__ == "__main__":
    ft.app(target=main)
