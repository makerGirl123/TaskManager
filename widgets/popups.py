from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button


def show_popup(title, message):
    layout = BoxLayout(orientation='vertical', padding=10)
    layout.add_widget(Label(text=message))
    close = Button(text="OK", size_hint_y=None, height=40)
    layout.add_widget(close)
    popup = Popup(title=title, content=layout, size_hint=(None, None), size=(300, 200))
    close.bind(on_release=popup.dismiss)
    popup.open()


def show_task_popup(task):
    layout = BoxLayout(orientation='vertical', padding=10)
    layout.add_widget(Label(text=f"Task: {task['task_name']}"))
    layout.add_widget(Label(text=f"Due: {task['due_date']}"))
    layout.add_widget(Label(text=f"Priority: {task['priority']}"))
    layout.add_widget(Label(
        text=f"Description: {task['description']}",
        size_hint_y=None,
        height=200,
        text_size=(300, None),
        halign='left',
        valign='top'
    ))
    close = Button(text="Close", size_hint_y=None, height=40)
    layout.add_widget(close)
    popup = Popup(title="Task Details", content=layout, size_hint=(None, None), size=(400, 500))
    close.bind(on_release=popup.dismiss)
    popup.open()