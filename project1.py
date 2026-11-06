
# TO-DO LIST AND TASK MANAGER
# Basic Python: Lists, Loops, Conditions and Functions

users = []
tasks = []

sections = ["Personal", "Academic", "Projects"]

next_user_id = 1
next_task_id = 1


# ---------------- NAME VALIDATION ----------------

def validate_name(name):
    if name == "" or name != name.strip():
        return False

    if name.startswith(".") or name.endswith("."):
        return False

    if name.count(".") > 1:
        return False

    for ch in name:
        if not (ch.isalpha() or ch == " " or ch == "."):
            return False

    return True


# ---------------- PASSWORD VALIDATION ----------------

def validate_password(password):
    if len(password) != 10:
        return False

    upper = 0
    lower = 0
    digits = 0
    special = 0

    for ch in password:
        if ch.isupper() and ch.isalpha():
            upper += 1
        elif ch.islower() and ch.isalpha():
            lower += 1
        elif ch.isdigit():
            digits += 1
        else:
            special += 1

    return (
        upper == 1
        and lower == 4
        and digits == 4
        and special == 1
    )


# ---------------- REGISTRATION ----------------

def register_user():
    global next_user_id

    print("\n========== USER REGISTRATION ==========")

    while True:
        name = input("Enter your name: ").strip()

        if not validate_name(name):
            print("Invalid name!")
            print("Use letters and spaces, with at most one dot.")
            continue

        duplicate = False

        for user in users:
            if user[1].lower() == name.lower():
                duplicate = True
                break

        if duplicate:
            print("This name is already registered. Try another name.")
        else:
            break

    while True:
        password = input("Create your password: ")

        if validate_password(password):
            break

        print("Invalid password!")
        print("Requirements:")
        print("1 uppercase letter")
        print("4 lowercase letters")
        print("1 special character")
        print("4 digits")
        print("Exactly 10 characters, in any order.")

    user = [next_user_id, name, password]
    users.append(user)

    print("\nRegistration successful!")
    print("Your User ID is:", next_user_id)

    next_user_id += 1


# ---------------- LOGIN ----------------

def login():
    print("\n========== LOGIN ==========")

    name = input("Enter your name: ").strip()
    password = input("Enter your password: ")

    for user in users:
        if user[1].lower() == name.lower() and user[2] == password:
            print("\nLogin successful!")
            print("Welcome,", user[1])
            return user

    print("Invalid name or password.")
    return None


# ---------------- SELECT SECTION ----------------

def choose_section():
    print("\nAvailable Sections:")

    for i in range(len(sections)):
        print(i + 1, ".", sections[i])

    while True:
        section = input("Enter section name: ").strip()

        for available in sections:
            if section.lower() == available.lower():
                return available

        print("Invalid section. Please try again.")


# ---------------- TASK HELPER FUNCTIONS ----------------

def get_user_tasks(user_id):
    result = []

    for task in tasks:
        if task[1] == user_id:
            result.append(task)

    return result


def find_task(user_id, task_id):
    for task in tasks:
        if task[0] == task_id and task[1] == user_id:
            return task

    return None


def get_task_id():
    while True:
        value = input("Enter task ID: ").strip()

        if value.isdigit():
            return int(value)

        print("Enter a valid numeric ID.")


def generate_task_id():
    global next_task_id

    task_id = next_task_id
    next_task_id += 1

    return task_id


# ---------------- ADD TASK ----------------

def add_task(user):
    print("\n========== ADD TASK ==========")

    section = choose_section()

    title = input("Enter task title: ").strip()

    if title == "":
        print("Task title cannot be empty.")
        return

    description = input("Enter task description: ").strip()

    task = [
        generate_task_id(),
        user[0],
        section,
        title,
        description,
        "Pending"
    ]

    tasks.append(task)

    print("Task added successfully!")


# ---------------- VIEW TASKS ----------------

def view_tasks(user):
    print("\n========== YOUR TASKS ==========")

    found = False

    for task in tasks:
        if task[1] == user[0]:
            print("-----------------------------------")
            print("Task ID:", task[0])
            print("Section:", task[2])
            print("Title:", task[3])
            print("Description:", task[4])
            print("Status:", task[5])
            found = True

    if not found:
        print("No tasks found.")


# ---------------- VIEW TASKS BY SECTION ----------------

def view_section_tasks(user):
    section = choose_section()

    print("\nTasks in", section)

    found = False

    for task in tasks:
        if task[1] == user[0] and task[2] == section:
            print(
                "ID:", task[0],
                "| Title:", task[3],
                "| Status:", task[5]
            )
            found = True

    if not found:
        print("No tasks found in this section.")


# ---------------- MARK COMPLETED ----------------

def mark_completed(user):
    view_tasks(user)

    task_id = get_task_id()
    task = find_task(user[0], task_id)

    if task is None:
        print("Task not found.")
    elif task[5] == "Completed":
        print("Task is already completed.")
    else:
        task[5] = "Completed"
        print("Task marked as completed!")


# ---------------- EDIT TASK ----------------

def edit_task(user):
    view_tasks(user)

    task_id = get_task_id()
    task = find_task(user[0], task_id)

    if task is None:
        print("Task not found.")
        return

    title = input(
        "Enter new title (press Enter to keep current): "
    ).strip()

    if title != "":
        task[3] = title

    description = input(
        "Enter new description (press Enter to keep current): "
    ).strip()

    if description != "":
        task[4] = description

    change = input("Change section? (yes/no): ").strip().lower()

    if change == "yes":
        task[2] = choose_section()

    print("Task updated successfully!")


# ---------------- DELETE TASK ----------------

def delete_task(user):
    view_tasks(user)

    task_id = get_task_id()
    task = find_task(user[0], task_id)

    if task is None:
        print("Task not found.")
        return

    confirm = input(
        "Are you sure you want to delete this task? (yes/no): "
    ).strip().lower()

    if confirm == "yes":
        tasks.remove(task)
        print("Task deleted successfully!")
    else:
        print("Deletion cancelled.")


# ---------------- SEARCH TASKS ----------------

def search_tasks(user):
    keyword = input("Enter search keyword: ").strip().lower()

    if keyword == "":
        print("Search keyword cannot be empty.")
        return

    found = False

    for task in tasks:
        if task[1] == user[0]:
            if (keyword in task[3].lower()
                    or keyword in task[4].lower()):
                print(
                    "ID:", task[0],
                    "| Section:", task[2],
                    "| Title:", task[3],
                    "| Status:", task[5]
                )
                found = True

    if not found:
        print("No matching tasks found.")


# ---------------- COMPLETION SUMMARY ----------------

def completion_summary(user):
    total = 0
    completed = 0
    pending = 0

    for task in tasks:
        if task[1] == user[0]:
            total += 1

            if task[5] == "Completed":
                completed += 1
            else:
                pending += 1

    percentage = 0

    if total > 0:
        percentage = completed * 100 / total

    print("\n========== COMPLETION SUMMARY ==========")
    print("Total tasks:", total)
    print("Completed tasks:", completed)
    print("Pending tasks:", pending)
    print("Completion rate: {:.2f}%".format(percentage))

    print("\nSection-wise summary:")

    for section in sections:
        section_total = 0
        section_completed = 0

        for task in tasks:
            if task[1] == user[0] and task[2] == section:
                section_total += 1

                if task[5] == "Completed":
                    section_completed += 1

        print(
            section + ":",
            section_completed,
            "completed out of",
            section_total
        )


# ---------------- TASK MANAGER MENU ----------------

def task_manager(user):
    while True:
        print("\n========== TASK MANAGER ==========")
        print("1. Add task")
        print("2. View all tasks")
        print("3. View tasks by section")
        print("4. Mark task completed")
        print("5. Edit task")
        print("6. Delete task")
        print("7. Search tasks")
        print("8. Completion summary")
        print("9. Logout")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_task(user)

        elif choice == "2":
            view_tasks(user)

        elif choice == "3":
            view_section_tasks(user)

        elif choice == "4":
            mark_completed(user)

        elif choice == "5":
            edit_task(user)

        elif choice == "6":
            delete_task(user)

        elif choice == "7":
            search_tasks(user)

        elif choice == "8":
            completion_summary(user)

        elif choice == "9":
            print("Logged out successfully.")
            break

        else:
            print("Invalid choice. Enter a number from 1 to 9.")


# ---------------- MAIN PROGRAM ----------------

def main():
    while True:
        print("\n===================================")
        print("   TO-DO LIST AND TASK MANAGER")
        print("===================================")
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            register_user()

        elif choice == "2":
            if len(users) == 0:
                print("No registered users. Please register first.")
            else:
                user = login()

                if user is not None:
                    task_manager(user)

        elif choice == "3":
            print("Thank you for using the application!")
            break

        else:
            print("Invalid choice. Enter 1, 2, or 3.")


main()
