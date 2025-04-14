from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager
from datetime import datetime

from screens import HomeScreen, AddTasksScreen, CalendarScreen
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
        self.sm.add_widget(CalendarScreen(name='calendar'))

        return self.sm

    def save_task(self):
        screen = self.sm.get_screen('tasks')

        task_name = screen.ids.task_name.text
        due_date = screen.ids.due_date.text
        priority = screen.ids.priority.text
        description = screen.ids.description.text

        if not task_name or not due_date or not priority or not description:
            show_popup("Error", "All fields must be filled!")
            return

        success = self.task_manager.add_task(task_name, due_date, priority, description)

        if success:
            show_popup("Success", "Task saved successfully!")
        else:
            show_popup("Error", "Failed to save task.")

        screen.ids.task_name.text = ""
        screen.ids.due_date.text = ""
        screen.ids.priority.text = ""
        screen.ids.description.text = ""

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

if __name__ == '__main__':
    TasksApp().run()