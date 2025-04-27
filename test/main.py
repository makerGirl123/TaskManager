from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.menu import MDDropdownMenu
from kivy.clock import Clock
from datetime import datetime

from screens import HomeScreen, AddTasksScreen, CalendarScreen, ViewTasksScreen
from tasks_functions import TaskFunctions
from widgets.popups import show_popup
from kivy.lang import Builder

Builder.load_file("kv/home.kv")
Builder.load_file("kv/add_tasks.kv")
Builder.load_file("kv/calendar.kv")

# App Settings
Window.size = (750, 750)
LabelBase.register(name='CustomFont', fn_regular='assets/InknutAntiqua-Regular.ttf')


class TasksApp(MDApp):
    def build(self):
        self.current_month = datetime.today().month
        self.current_year = datetime.today().year

        self.task_manager = TaskFunctions()

        self.theme_cls.primary_palette = "Silver"
        self.theme_cls.theme_style = "Light"

        self.sm = ScreenManager()
        self.sm.add_widget(HomeScreen(name='home'))
        self.sm.add_widget(AddTasksScreen(name='tasks'))

        start_ampm_items = [
            {"text": "AM", "on_release": lambda x="AM": self.set_start_ampm(x)},
            {"text": "PM", "on_release": lambda x="PM": self.set_start_ampm(x)},
        ]

        self.start_ampm_menu = MDDropdownMenu(
            caller=self.sm.get_screen('tasks').ids.start_ampm,
            items=start_ampm_items,
            width_mult=2,
        )

        end_ampm_items = [
            {"text": "AM", "on_release": lambda x="AM": self.set_end_ampm(x)},
            {"text": "PM", "on_release": lambda x="PM": self.set_end_ampm(x)},
        ]

        self.end_ampm_menu = MDDropdownMenu(
            caller=self.sm.get_screen('tasks').ids.end_ampm,
            items=end_ampm_items,
            width_mult=2,
        )


        self.sm.add_widget(CalendarScreen(name='calendar'))
        self.sm.add_widget(ViewTasksScreen(name='view_tasks'))

        return self.sm

    def save_task(self):
        screen = self.sm.get_screen('tasks')

        task_name = screen.ids.task_name.text
        due_date = screen.ids.due_date.text
        priority = screen.ids.priority.text
        description = screen.ids.description.text
        start_time = screen.ids.start_time.text
        end_time = screen.ids.end_time.text
        start_ampm = screen.ids.start_ampm.text
        end_ampm = screen.ids.end_ampm.text

        screen.ids.time_display.text = f"{start_time} {start_ampm} - {end_time} {end_ampm}"

        if not task_name or not due_date or not priority or not description:
            show_popup("Error", "All fields must be filled!")
            return

        success = self.task_manager.add_task(task_name, due_date, priority, description, start_time, end_time, start_ampm, end_ampm)

        if success:
            show_popup("Success", "Task saved successfully!")
        else:
            show_popup("Error", "Failed to save task.")

        screen.ids.task_name.text = ""
        screen.ids.due_date.text = ""
        screen.ids.priority.text = ""
        screen.ids.description.text = ""
        screen.ids.start_time.text = ""
        screen.ids.end_time.text = ""
        screen.ids.start_ampm.text = "AM"
        screen.ids.end_ampm.text = "AM"
        screen.ids.time_display.text = ""

    def update_calendar(self):
        screen = self.sm.get_screen('calendar')
        screen.update_calendar(self.task_manager, self.current_year, self.current_month)

    def change_month(self, direction):
        self.current_month += direction
        if self.current_month > 12:
            self.current_month = 1
            self.current_year += 1
        elif self.current_month < 1:
            self.current_month = 12
            self.current_year -= 1
        self.update_calendar()

    def go_home(self):
        self.sm.current = 'home'

    def go_calendar(self):
        self.update_calendar()
        self.sm.current = 'calendar'

    def export_to_ics(self):
        if self.task_manager.export_tasks_to_ics():
            show_popup("Success", "Tasks exported to tasks.ics")
        else:
            show_popup("Error", "Failed to export tasks.")

    def show_saved_tasks(self):
        screen = self.sm.get_screen('view_tasks')
        tasks = self.task_manager.view_tasks()
        screen.display_tasks(tasks)
        self.sm.current = 'view_tasks'

    def delete_task(self, task_name, due_date):
        if self.task_manager.delete_task(task_name, due_date):
            show_popup("Success", "Task marked as complete.")
        else:
            show_popup("Error", "Task could not be removed.")

    def set_start_ampm(self, value):
        self.sm.get_screen('tasks').ids.start_ampm.text = value
        self.start_ampm_menu.dismiss()

    def set_end_ampm(self, value):
        self.sm.get_screen('tasks').ids.end_ampm.text = value
        self.end_ampm_menu.dismiss()

    def open_ampm_menu(self, which):
        def do_open(*_):
            if which == "start":
                self.end_ampm_menu.dismiss()  # close other
                self.start_ampm_menu.caller = self.sm.get_screen("tasks").ids.start_ampm
                self.start_ampm_menu.open()
            elif which == "end":
                self.start_ampm_menu.dismiss()  # close other
                self.end_ampm_menu.caller = self.sm.get_screen("tasks").ids.end_ampm
                self.end_ampm_menu.open()

        Clock.schedule_once(do_open, 0.05)

if __name__ == '__main__':
    TasksApp().run()
