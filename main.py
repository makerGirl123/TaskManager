# MUST INSTALL PYTHON PACKAGES kivy AND kivymd2 AND python-dateutil


# used for most MD apps
from kivymd.app import MDApp
#Used to reference the widgets in .kv and keep the positions
from kivy.uix.floatlayout import FloatLayout
#Used for changing screens
from kivy.uix.screenmanager import ScreenManager, Screen
#used to set screen size
from kivy.core.window import Window

#used to create a popup window
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

from kivy.core.text import LabelBase

from datetime import datetime, timedelta
import calendar

# Register your custom font
LabelBase.register(name='CustomFont', fn_regular='assets\InknutAntiqua-Regular.ttf')


#import functions from other python file
from tasks_functions import TaskFunctions
task_manager = TaskFunctions()  # Create an instance

#example Android screen size
Window.size = (750, 750)

#class for each screen and its canvas
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




class TasksApp(MDApp):
    def build(self):
        self.current_month = datetime.today().month
        self.current_year = datetime.today().year

        self.theme_cls.primary_palette = "Silver"
        self.theme_cls.theme_style = "Light"

        self.sm = ScreenManager()
        self.sm.add_widget(HomeScreen(name='home'))
        self.sm.add_widget(AddTasksScreen(name='tasks'))
        self.sm.add_widget(CalendarScreen(name='calendar'))
        return self.sm

    def go_home(self):
        self.sm.current = 'home'

    def save_task(self):
        """Fetches input values and saves them to a file."""
        task_screen = self.sm.get_screen('tasks')  # Get the AddTasksScreen

        task_name = task_screen.ids.task_name.text
        due_date = task_screen.ids.due_date.text
        priority = task_screen.ids.priority.text
        description = task_screen.ids.description.text

        if not task_name or not due_date or not priority or not description:
            print("Error: All fields must be filled!")  # You can replace with a popup message
            return

        success = task_manager.add_task(task_name, due_date, priority, description)

        if success:
            self.show_popup("Success", "Task saved successfully!")
        else:
            self.show_popup("Error", "Failed to save task.")

        # Clear the input fields after saving
        task_screen.ids.task_name.text = ""
        task_screen.ids.due_date.text = ""
        task_screen.ids.priority.text = ""
        task_screen.ids.description.text = ""

    def show_popup(self, title, message):
        """Displays a popup message."""
        layout = BoxLayout(orientation='vertical', padding=10)
        label = Label(text=message, size_hint_y=None, height=40)
        close_button = Button(text="OK", size_hint_y=None, height=40)

        layout.add_widget(label)
        layout.add_widget(close_button)

        popup = Popup(title=title, content=layout, size_hint=(None, None), size=(300, 200))
        close_button.bind(on_release=popup.dismiss)
        popup.open()

    def go_calendar(self):
        self.update_calendar()
        self.sm.current = 'calendar'

    def update_calendar(self):
        screen = self.sm.get_screen('calendar')
        calendar_grid = screen.ids.calendar_grid
        month_label = screen.ids.month_label

        # Clear previous calendar
        calendar_grid.clear_widgets()

        # Update label
        month_name = calendar.month_name[self.current_month]
        month_label.text = f"{month_name} {self.current_year}"

        # Build mapping
        tasks = task_manager.view_tasks()
        #print("Tasks loaded:", tasks)  # Print loaded tasks to verify they are being fetched correctly

        day_tasks = self.map_tasks_to_calendar(tasks, self.current_year, self.current_month)
        #print("Mapped tasks to days:", day_tasks)  # Print the mapped tasks to verify correct mapping

        _, last_day = calendar.monthrange(self.current_year, self.current_month)

        # Add blank labels for days of the week if the month doesn't start on Sunday
        start_day = datetime(self.current_year, self.current_month, 1).weekday()
        for _ in range((start_day + 1) % 7):
            calendar_grid.add_widget(Label())

        for day in range(1, last_day + 1):
            layout = BoxLayout(orientation='vertical', padding=4, spacing=4)

            # Add Label for the day number
            day_label = Label(
                text=str(day),
                font_name="CustomFont",
                color=(0.184, 0.282, 0.345, 1)
            )
            layout.add_widget(day_label)

            # Add buttons for each task due on this day
            if day in day_tasks:
                #print(f"Adding tasks for day {day}: {day_tasks[day]}")  # Debug: Check if tasks are due on this day
                for thisTask in day_tasks[day]:
                    task_button = Button(
                        text=thisTask['task_name'],
                        color=(1, 1, 1, 1),
                        font_name="CustomFont",
                        font_size="12sp",
                        size_hint_y=None,
                        height="30dp",
                        background_color=(0.572549, 0.870588, 0.882352, 1)
                    )
                    task_button.bind(on_release=lambda instance, task=thisTask: self.show_task_popup(task))
                    layout.add_widget(task_button)
            #else:
                #print(f"No tasks for day {day}")  # Debug: No tasks for this day

            calendar_grid.add_widget(layout)

    def change_month(self, direction):
        self.current_month += direction
        if self.current_month > 12:
            self.current_month = 1
            self.current_year += 1
        elif self.current_month < 1:
            self.current_month = 12
            self.current_year -= 1
        self.update_calendar()

    def map_tasks_to_calendar(self, tasks, year, month):
        result = {i: [] for i in range(1, calendar.monthrange(year, month)[1] + 1)}
        #print("Initial result structure:", result)  # Debug: Check initial structure of the result
        for task in tasks:
            try:
                # Parse the due date
                due = datetime.strptime(task['due_date'], "%Y/%m/%d")
                #print(f"Task '{task['task_name']}' due date parsed as: {due}")  # Debug: Print the parsed date

                # Ensure that the task is in the correct year and month
                if due.year == year and due.month == month:
                    result[due.day].append(task)
                    #print(f"Task '{task['task_name']}' mapped to day {due.day}")  # Debug: Check each task mapping
            except Exception as e:
                print(f"Error processing task {task}: {e}")  # Debug: Catch and log any errors
        #print("Final mapped tasks:", result)  # Debug: Verify the final mapping
        return result

    def show_task_popup(self, task):
        layout = BoxLayout(orientation='vertical', padding=10)

        # Display task name and due date
        layout.add_widget(Label(text=f"Task: {task['task_name']}"))
        layout.add_widget(Label(text=f"Due: {task['due_date']}"))
        layout.add_widget(Label(text=f"Priority: {task['priority']}"))

        # Display description with wrapping
        description_label = Label(
            text=f"Description: {task['description']}",
            size_hint_y=None,
            height=200,  # Adjust the height of the description box
            text_size=(300, None),  # Allow the text to wrap within a fixed width
            halign='left',
            valign='top'
        )

        layout.add_widget(description_label)

        # Create the popup with a taller size
        popup = Popup(title="Task Details", content=layout, size_hint=(None, None),
                      size=(400, 500))  # Increase height here

        # Close button
        close_btn = Button(text="Close", size_hint_y=None, height=40)
        close_btn.bind(on_release=popup.dismiss)
        layout.add_widget(close_btn)

        popup.open()


if __name__ == '__main__':
    TasksApp().run()