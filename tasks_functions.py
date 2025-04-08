import json

class TaskFunctions():

    def __init__(self):
        """Initialize the tasks dictionary and load tasks from file."""
        self.tasks = {}  # Instance-specific dictionary
        self.load_tasks_from_file()  # Load tasks when an instance is created

    # add a new task
    '''This function will add a task by taking the user input for name date and descriptio of the task that 
    will then be used and stored in the tasks dictionary using each task name as a key for the task to then be retrieved. 
    Once filled the dictionary is initialized globally to ensure its use accross all functions, in the final product this will be a local 
    variable of a class timeManager. '''

    def add_task(self, task_name, due_date, priority, description):
        # Store task details in the dictionary
        self.tasks[task_name] = {'due_date': due_date, 'priority': priority, 'description': description}

        #Saves the tasks dictionary to a JSON file
        try:
            with open("tasks.json", "w") as file:
                json.dump(self.tasks, file, indent=4)
            print("Tasks saved successfully.")
            return True
        except Exception as e:
            print(f"Error saving tasks: {e}")
            return False


    # view all tasks
    '''The view tasks function is primary use will be used ot view the tasks in order of what they were inputed in at its most basic use case 
    Once fully implemented this funciton will be able to sort the tasks by low high or medium priority and display them in a list and then on 
    a TKINTER calendar GUI'''


    def view_tasks(self):
        # Check if there are no tasks
        if not self.tasks:
            print("No tasks available.")
            return [] # Return empty list if no tasks exist
        else:
            tasks_list = ""
            # Loop through the tasks and print the details of each
            for name, info in self.tasks.items():
                tasks_list += (f"- {name}: Due {info['due_date']}, {info['description']}\n")

            return tasks_list


    def load_tasks_from_file(self):
        """
        Loads tasks from a JSON file into the tasks dictionary.
        """
        try:
            with open("tasks.json", "r") as file:
                self.tasks = json.load(file)
            print("Tasks loaded successfully.")
            print(self.tasks)
        except (FileNotFoundError, json.JSONDecodeError):
            self.tasks = {}
        except Exception as e:
            print(f"Error loading tasks: {e}")


if __name__ == "__main__":
    # loop to ask user for input everytime
    while True:
        # Display options
        '''The three main options that will be implemented in out GUI function that will be the end product are
        Add task, View task and exit. '''
        print("\n1. Add Task\n2. View Tasks\n3. Exit")

        # Get user's choice
        choice = input("Choose an option: ")

        if choice == "1":
            add_task()
        elif choice == "2":
            view_tasks()
        elif choice == "3":
            print("Have a good day!")
            break
        else:
            print("Please enter 1, 2, or 3")