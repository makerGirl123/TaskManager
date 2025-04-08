# MUST INSTALL PYTHON PACKAGES kivy AND kivymd2


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
from kivy.core.text import LabelBase, DEFAULT_FONT

#import functions from other python file
from tasks_functions import TaskFunctions
task_manager = TaskFunctions()  # Create an instance

#example Android screen size
Window.size = (750, 750)

#Set custom font
LabelBase.register(name='CustomFont', fn_regular='assets/InknutAntiqua-Regular.ttf')

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
        self.theme_cls.primary_palette = "Silver"
        self.theme_cls.theme_style = "Light"

        self.sm = ScreenManager()
        self.sm.add_widget(HomeScreen(name='home'))
        self.sm.add_widget(AddTasksScreen(name='tasks'))
        self.sm.add_widget(CalendarScreen(name='calendar'))
        return self.sm

    def go_home(self):
        self.sm.current = 'home'

    def go_calendar(self):
        """Fetches current tasks and updates the calendar screen."""
        tasks = task_manager.view_tasks()  # Retrieve tasks

        self.sm.current = 'calendar'

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

if __name__ == '__main__':
    TasksApp().run()
