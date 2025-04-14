from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from datetime import datetime
import calendar
from widgets.popups import show_task_popup
from kivy.lang import Builder

Builder.load_file("kv/home.kv")
Builder.load_file("kv/add_tasks.kv")
Builder.load_file("kv/calendar.kv")

class HomeScreen(Screen):
    pass
    class HomeScreenCanvas(FloatLayout):
        pass


class AddTasksScreen(Screen):
    pass
    class AddTasksScreenCanvas(FloatLayout):
        pass


class CalendarScreen(Screen):
    pass
    class CalendarScreenCanvas(FloatLayout):
        pass

    def update_calendar(self, task_manager, year, month):
        calendar_grid = self.ids.calendar_grid
        month_label = self.ids.month_label

        calendar_grid.clear_widgets()
        month_label.text = f"{calendar.month_name[month]} {year}"

        tasks = task_manager.view_tasks()
        day_tasks = self.map_tasks_to_calendar(tasks, year, month)

        _, last_day = calendar.monthrange(year, month)
        start_day = datetime(year, month, 1).weekday()

        for _ in range((start_day + 1) % 7):
            calendar_grid.add_widget(Label())

        for day in range(1, last_day + 1):
            layout = BoxLayout(orientation='vertical', padding=4, spacing=4)
            layout.add_widget(Label(text=str(day), font_name="CustomFont", color=(0.184, 0.282, 0.345, 1)))

            if day in day_tasks:
                for task in day_tasks[day]:
                    btn = Button(
                        text=task['task_name'],
                        size_hint_y=None,
                        height="30dp",
                        font_name="CustomFont",
                        font_size="12sp",
                        background_color=(0.57, 0.87, 0.88, 1)
                    )
                    btn.bind(on_release=lambda instance, t=task: show_task_popup(t))
                    layout.add_widget(btn)

            calendar_grid.add_widget(layout)

    def map_tasks_to_calendar(self, tasks, year, month):
        result = {i: [] for i in range(1, calendar.monthrange(year, month)[1] + 1)}
        for task in tasks:
            try:
                due = datetime.strptime(task['due_date'], "%Y/%m/%d")
                if due.year == year and due.month == month:
                    result[due.day].append(task)
            except Exception as e:
                print(f"Error processing task: {e}")
        return result