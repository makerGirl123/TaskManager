from ics import Calendar, Event
from datetime import datetime
import pytz
import os

class TaskFunctions():

    def __init__(self):
        """Initialize the tasks dictionary and load tasks from file."""
        self.tasks = {}  # Instance-specific dictionary


    # add a new task
    '''This function will add a task by taking the user input for name date and descriptio of the task that 
    will then be used and stored in the tasks dictionary using each task name as a key for the task to then be retrieved. 
    Once filled the dictionary is initialized globally to ensure its use accross all functions, in the final product this will be a local 
    variable of a class timeManager. '''

    def add_task(self, task_name, due_date, priority, description, start_time, end_time, start_ampm, end_ampm):

        event = Event()
        event.name = task_name
        try:
            # Example: set timezone to Eastern Time (US)
            timezone = pytz.timezone("US/Eastern")

            start_dt = datetime.strptime(f"{due_date} {start_time} {start_ampm}", "%Y/%m/%d %I:%M %p")
            end_dt = datetime.strptime(f"{due_date} {end_time} {end_ampm}", "%Y/%m/%d %I:%M %p")
            event.begin = timezone.localize(start_dt)
            event.end = timezone.localize(end_dt)

        except ValueError:
            print("Invalid date/time format.")
            return False

        event.description = f"Priority: {priority}\n{description}"

        cal = Calendar()

        # Load existing .ics data if the file exists
        if os.path.exists("tasks.ics"):
            try:
                with open("tasks.ics", "r") as f:
                    cal = Calendar(f.read())
            except Exception as e:
                print(f"Failed to load existing calendar: {e}")
                os.remove("tasks.ics")
                cal = Calendar()

        cal.events.add(event)

        try:
            with open("tasks.ics", "w", newline="\n") as f:
                f.write(str(cal))  # Use str(cal) instead of writelines
            print("Task added and saved to ICS.")
            return True
        except Exception as e:
            print(f"Error writing ICS file: {e}")
            return False

    # view all tasks
    '''The view tasks function is primary use will be used ot view the tasks in order of what they were inputed in at its most basic use case 
    Once fully implemented this funciton will be able to sort the tasks by low high or medium priority and display them in a list and then on 
    a TKINTER calendar GUI'''

    def view_tasks(self):
        tasks_list = []
        if not os.path.exists("tasks.ics"):
            return tasks_list

        try:
            with open("tasks.ics", "r") as f:
                cal = Calendar(f.read())
            for event in cal.events:
                desc_lines = event.description.split('\n', 1)
                priority_line = desc_lines[0].strip()
                actual_description = desc_lines[1] if len(desc_lines) > 1 else ""

                priority = priority_line.replace("Priority:", "").strip() if priority_line.startswith(
                    "Priority:") else "N/A"
                task = {
                    'task_name': event.name,
                    'due_date': event.begin.format('YYYY/MM/DD'),
                    'priority': priority,
                    'description': actual_description,
                    'time': f"{event.begin.format('hh:mm A')} - {event.end.format('hh:mm A')}"
                }
                tasks_list.append(task)
        except Exception as e:
            print(f"Error reading ICS file: {e}")
        return tasks_list

    def export_tasks_to_ics(self, filename="tasks.ics"):
        cal = Calendar()
        for name, info in self.tasks.items():
            event = Event()
            try:
                event.begin = datetime.strptime(info["due_date"], "%Y/%m/%d")
            except ValueError:
                print(f"Skipping invalid date: {info['due_date']}")
                continue
            event.name = name
            event.description = f"Priority: {info['priority']}\n{info['description']}"
            cal.events.add(event)

        try:
            with open(filename, "w") as f:
                f.writelines(cal)
            print(f"ICS file saved as {filename}")
            return True
        except Exception as e:
            print(f"Error writing ICS file: {e}")
            return False

    def delete_task(self, task_name, due_date):
        if not os.path.exists("tasks.ics"):
            return False

        try:
            with open("tasks.ics", "r") as f:
                cal = Calendar(f.read())

            to_delete = None
            for event in cal.events:
                if event.name == task_name and event.begin.format('YYYY/MM/DD') == due_date:
                    to_delete = event
                    break

            if to_delete:
                cal.events.remove(to_delete)
                with open("tasks.ics", "w", newline="\n") as f:
                    f.write(str(cal))
                return True
            else:
                print("Task not found for deletion.")
                return False
        except Exception as e:
            print(f"Error deleting task: {e}")
            return False