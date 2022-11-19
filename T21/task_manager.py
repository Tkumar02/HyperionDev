import os
from datetime import date, datetime

DATETIME_STRING_FORMAT = "%Y-%m-%d"


class Task:
    def __init__(self, username=None, title=None, description=None, due_date=None, assigned_date=None, completed=None, number=None):
        '''
        Inputs:
        username: String
        title: String
        description: String
        due_date: DateTime
        assigned_date: DateTime
        completed: Boolean
        number: Int
        '''
        self.username = username
        self.title = title
        self.description = description
        self.due_date = due_date
        self.assigned_date = assigned_date
        self.completed = completed
        self.number = number  # added new parameter

    def from_string(self, task_str):
        '''
        Convert from string in tasks.txt to object
        '''
        tasks = task_str.split(";")
        username = tasks[0]
        title = tasks[1]
        description = tasks[2]
        due_date = datetime.strptime(tasks[3], DATETIME_STRING_FORMAT)
        assigned_date = datetime.strptime(tasks[4], DATETIME_STRING_FORMAT)
        completed = True if tasks[5] == 'Yes' else False
        number = tasks[6]
        self.__init__(username, title, description,
                      due_date, assigned_date, completed, number)

    def to_string(self):
        '''
        Convert to string for storage in tasks.txt
        '''
        str_attrs = [
            self.username,
            self.title,
            self.description,
            self.due_date.strftime(DATETIME_STRING_FORMAT),
            self.assigned_date.strftime(DATETIME_STRING_FORMAT),
            'Yes' if self.completed else 'No',
            self.number  # added new parameter
        ]
        return ";".join(str_attrs)

    def display(self):
        '''
        Display object in readable format
        '''
        if self.completed == True:
            completed = 'Yes'
        else:
            completed = 'No'
        disp_str = f"Task: \t\t {self.title}\n"
        disp_str += f"Assigned to: \t {self.username}\n"
        disp_str += f"Date Assigned: \t {self.assigned_date.strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {self.due_date.strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {self.description}\n"
        disp_str += f"Task Number: \t {self.number}\n"
        disp_str += f"Task Completed: {completed}\n"
        return disp_str


# Read and parse tasks.txt
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]


task_list = []
for t_str in task_data:
    curr_t = Task()
    curr_t.from_string(t_str)
    task_list.append(curr_t)

# Read and parse user.txt

# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

# Keep trying until a successful login
logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True


def validate_string(input_str):
    '''
    Function for ensuring that string is safe to store
    '''
    if ";" in input_str:
        print("Your input cannot contain a ';' character")
        return False
    return True


def check_username_and_password(username, password):
    '''
    Ensures that usernames and passwords can't break the system
    '''
    # ';' character cannot be in the username or password
    if ";" in username or ";" in password:
        print("Username or password cannot contain ';'.")
        return False
    return True


def write_usernames_to_file(username_dict):
    '''
    Function to write username to file

    Input: dictionary of username-password key-value pairs
    '''
    with open("user.txt", "w") as out_file:
        user_data = []
        for k in username_dict:
            user_data.append(f"{k};{username_dict[k]}")
        out_file.write("\n".join(user_data))


#########################
# Main Program
#########################

#############
# Functions
#############

# defining a function when user selects 'r' to register a new user
def reg_user():
    # check user is admin before registering a user
    if curr_user != 'admin':
        print("Registering new users requires admin privileges")
        return

    # ask user to enter new username
    new_username = input('New username: ')

    # check whether username is already in user.txt
    with open('user.txt', 'r+') as f:
        users = f.readlines()
        for user in users:
            names = user.split(';')
            while names[0] == new_username:
                new_username = input(
                    'That username is already taken, please enter another username: ')

    # get new password from user
    new_password = input('New password: ')
    if not check_username_and_password(new_username, new_password):
        # Username or password is not safe for storage - break

        return

    # Request input of password confirmation.
    confirm_password = input("Confirm Password: ")

    # Check if the new password and confirmed password are the same.
    if new_password == confirm_password:
        # If they are the same, add them to the user.txt file,
        print("New user added")

        # Add to dictionary and write to file
        username_password[new_username] = new_password
        write_usernames_to_file(username_password)

    # Otherwise you present a relevant message.
    else:
        print("Passwords do no match")


def add_task():
    # Prompt a user for the following:
    #     A username of the person whom the task is assigned to,
    #     A title of a task,
    #     A description of the task and
    #     the due date of the task.

    # Ask for username
    task_username = input("Name of person assigned to task: ")
    if task_username not in username_password.keys():
        print("User does not exist. Please enter a valid username")
        return

    # Get title of task and ensure safe for storage
    while True:
        task_title = input("Title of Task: ")
        if validate_string(task_title):
            break

    # Get description of task and ensure safe for storage
    while True:
        task_description = input("Description of Task: ")
        if validate_string(task_description):
            break

    # Obtain and parse due date
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(
                task_due_date, DATETIME_STRING_FORMAT)
            break
        except ValueError:
            print("Invalid datetime format. Please use the format specified")

    # Obtain and parse current date
    curr_date = date.today()

    # enter task_number
    number = 1
    for t in task_list:
        number += 1
    task_number = str(number)

    # Create a new Task object and append to list of tasks - also added task number as a new view on tasks
    new_task = Task(task_username, task_title,
                    task_description, due_date_time, curr_date, False, task_number)
    task_list.append(new_task)

    # Write to tasks.txt
    with open("tasks.txt", "w") as task_file:
        task_file.write("\n".join([t.to_string() for t in task_list]))
    print("Task successfully added.")


def view_all():
    print("-----------------------------------")

    if len(task_list) == 0:
        print("There are no tasks.")
        print("-----------------------------------")

    for t in task_list:
        print(t.display())
        print("-----------------------------------")

# editing tasks


def edit_task(number):
    # select what to edit
    edit = input(
        'Would you like to edit or complete the task(enter "complete" or "edit"): ').lower()
    # marking task as completed
    if edit == 'complete':
        for task in task_list:
            if task.number == number:
                task.completed = True
        with open("tasks.txt", "w") as task_file:
            task_file.write("\n".join([t.to_string() for t in task_list]))
        print('\nYour task has been successfully marked as completed')

    elif edit == 'edit':
        topic = input('Would you like to change date or owner? ')

        # change due date of task
        if topic == 'date':
            new_date = input('Enter date in format YYYY-MM-DD: ')
            new_date_formatted = datetime.strptime(
                new_date, DATETIME_STRING_FORMAT)
            for task in task_list:
                if task.number == number:
                    task.due_date = new_date_formatted
            print('\n The date has successfully been updated')

        # change owner of task
        elif topic == 'owner':
            new_owner = input('Enter name of owner: ').lower()
            with open('user.txt', 'r') as f:
                users = f.readlines()
                for user in users:
                    name_index = user.index(';')
                    name = user[0:name_index]
                    if name == new_owner:
                        for task in task_list:
                            if task.number == number:
                                task.username = new_owner
                                print(
                                    f'\n The owner has successfully been changed to {new_owner}')
                                return
                print('\nUnknown user')
        with open("tasks.txt", "w") as task_file:
            task_file.write("\n".join([t.to_string() for t in task_list]))
    else:
        print('Unknown command')
        return


def view_mine():
    print("-----------------------------------")
    has_task = False
    for t in task_list:
        if t.username == curr_user:
            has_task = True
            print(t.display())
            print("-----------------------------------")

    if not has_task:
        print("You have no tasks.")
        print("-----------------------------------")

    # select task
    selection = int(input('Select task number to edit or enter -1 to exit: '))
    if selection == -1:
        return
    # available task is selected
    else:
        for task in task_list:
            if task.username == curr_user and task.number == str(selection):
                with open('tasks.txt', 'r') as f:
                    tasks = f.readlines()
                    # select correct task
                    for task in tasks:
                        t = task.split(';')
                        task_num = t[-1].strip('\n')
                        # ensure task is not completed
                        if task_num == str(selection):
                            if t[-2] == 'Yes':
                                print('Cannot edit a completed task')
                                return
                            elif t[-2] == 'No':
                                edit_task(str(selection))
                                return
        print('Incorrect selection')
        return


####################
# End of functions
####################

while True:
    # Get input from user
    print()
    if curr_user == 'admin':
        menu = input('''Select one of the following Options below:
    r - Registering a user
    a - Adding a task
    va - View all tasks
    vm - view my task
    ds - display statistics
    e - Exit
    : ''').lower()
    else:
        menu = input('''Select one of the following Options below:
    r - Registering a user
    a - Adding a task
    va - View all tasks
    vm - view my task
    e - Exit
    : ''').lower()

    if menu == 'r':  # Register new user (if admin)
        reg_user()

    elif menu == 'a':  # Add a new task
        add_task()

    elif menu == 'va':  # View all tasks
        view_all()

    elif menu == 'vm':  # View my tasks
        view_mine()

    elif menu == 'ds' and curr_user == 'admin':  # If admin, display statistics
        num_users = len(username_password.keys())
        num_tasks = len(task_list)

        print("-----------------------------------")
        print(f"Number of users: \t\t {num_users}")
        print(f"Number of tasks: \t\t {num_tasks}")
        print("-----------------------------------")

    elif menu == 'e':  # Exit program
        print('Goodbye!!!')
        exit()

    else:  # Default case
        print("You have made a wrong choice, Please Try again")
