import csv
import turtle

class Person:
    def __init__(self, name, username, password, mobile_number):
        self.name = name
        self.username = username
        self.password = password
        self.mobile_number = mobile_number
        self.friends = []

    def __str__(self):
        return f"Name: {self.name}\nUsername: {self.username}\nMobile Number: {self.mobile_number}\n"

    def display_description(self):
        return f"Name: {self.name}\nUsername: {self.username}\n"


def load_data_from_csv(file_path):
    people = {}
    friends_graph = {}

    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            if len(row) == 5:  # Ensure each row has five values
                name, username, password, mobile_number, friends = row
                mobile_number = int(mobile_number)  # Convert mobile number to integer
                friends = friends.strip().split("|")  # Split friends string into a list
                person = Person(name, username, password, mobile_number)
                people[username] = person
                friends_graph[username] = friends
            else:
                print(f"Ignoring invalid row: {row}")

    for username, friends in friends_graph.items():
        person = people[username]
        person.friends = friends

    return people, friends_graph


def write_data_to_csv(people, friends_graph, file_path):
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Username", "Password", "Mobile_number", "Friends"])
        for username, person in people.items():
            friends = "|".join(person.friends)
            writer.writerow([person.name, person.username, person.password, person.mobile_number, friends])


def visualize_as_graph(graph, user_list):
    try:
        turtle.Screen().reset()  # Reset turtle graphics environment
    except turtle.Terminator:
        pass

    nodes = [node for node in graph if node]  # Filter out empty string keys
    n = len(nodes)
    turn_angle = 180 - (((n - 2) * 180) / n)

    t = turtle.Turtle()
    t.speed(5)
    t.penup()
    t.right(90)
    t.forward(200)
    t.left(90)
    t.pendown()

    circle_centers = {}

    for node in nodes:
        t.color("blue")  # Set circle color to light blue
        t.begin_fill()  # Begin filling the circle
        t.circle(20)
        t.end_fill()  # End filling the circle
        circle_centers[node] = t.pos()
        t.penup()
        t.left(turn_angle)
        t.forward(150)
        t.pendown()

    for person, friends in graph.items():
        if person not in circle_centers:  # Skip if person is an empty string
            continue
        center = circle_centers[person]
        name_of_person = user_list[person].name
        t.penup()
        t.goto(center[0] - 30, center[1] - 50)  # Adjust position for writing username
        t.pendown()
        t.write(name_of_person, font=("Arial", 12, "normal"))  # Write username near the circle
        for friend in friends:
            if friend and friend in circle_centers:  # Skip if friend is empty string or not in circle_centers
                friend_center = circle_centers[friend]
                t.penup()
                t.goto(center)
                t.pendown()
                t.goto(friend_center)

    turtle.done()


def view_users_as_admin(user_list, friends_graph):
    print("Do you want (1)detailed information or (2)just the usernames?")
    choice = get_int_input("Enter your choice: ")

    if choice == 1:
        for user in user_list.values():
            print(user)
            print()
    elif choice == 2:
        bfs(friends_graph, list(user_list.keys())[0])
    else:
        print("Invalid choice")


def bfs(graph, node):
    visited = []
    queue = []
    visited.append(node)
    queue.append(node)

    while queue:
        m = queue.pop(0)
        print(m)

        if m not in graph:
            continue

        for neighbour in graph[m]:
            if neighbour not in visited:
                visited.append(neighbour)
                queue.append(neighbour)


def delete_user(username, user_list, friends_graph):
    try:
        user_list.pop(username)
        friends_graph.pop(username)
        for key in friends_graph:
            if username in friends_graph[key]:
                friends_graph[key].remove(username)
        print(f"User '{username}' deleted")
    except KeyError:
        print(f"User '{username}' not found")


def get_int_input(prompt):
    while True:
        try:
            response = int(input(prompt))
            return response
        except ValueError:
            print("Please enter a number")


def main():
    filename = "E:/VIT/VScode/ADS Project/trial6/Accounts.csv"

    password_list = ["12345", "54321", "11111"]

    user_list, friends_graph = load_data_from_csv(filename)

    print("Welcome to Bhatta Book\n")
    print("What are you?\n1.Admin     2.User")
    role = get_int_input("Enter your response: ")

    if role == 1:
        password = input("Please enter your password: ")
        if password in password_list:
            print("Access granted\n")
            admin_menu(password_list, user_list, friends_graph)
        else:
            print("Access denied")
    
    elif role == 2:
        user_menu(user_list, friends_graph)

    else:
        print("Invalid input.")

    write_data_to_csv(user_list, friends_graph, filename)


def admin_menu(password_list, user_list, friends_graph):
    while True:
        print("What would you like to do?")
        print("1. View users as admin")
        print("2. See visuals as graph")
        print("3. Delete a user")
        print("0. Exit")
        
        choice = get_int_input("Enter your choice: ")
        if choice == 0:
            print("Logging out...")
            break
        elif choice == 1:
            view_users_as_admin(user_list, friends_graph)
        elif choice == 2:
            visualize_as_graph(friends_graph, user_list)
        elif choice == 3:
            username = input("Enter username of the person:")
            delete_user(username, user_list, friends_graph)
        else:
            print("Invalid input. Please enter correct options.")


def user_menu(user_list, friends_graph):
    print("What do you want to do?")
    print("1. Login     2. Create new account")
    choice = get_int_input("Enter your choice: ")
    if choice == 1:
        login(user_list, friends_graph)
    elif choice == 2:
        create_new_account(user_list)
    else:
        print("Invalid choice")


def login(user_list, friends_graph):
    mobnum = int(input("Enter mobile number: "))
    password = input("Enter your password: ")
    flag = 0
    for user in user_list.values():
        if user.mobile_number == mobnum:
            flag = 1
            if password == user.password:
                print("Access granted\n")
                user_actions(user_list, friends_graph, user)
            else:
                print("Password does not match")
    if flag == 0:
        print(f"User with mobile number '{mobnum}' not found")


def user_actions(user_list, friends_graph, user):
    while True:
        print("What do you want to do?")
        print("1. Connect with a person")
        print("2. Delete a connection")
        print("3. See your friends")
        print("0. Exit")

        choice = get_int_input("Enter your choice: ")
        if choice == 0:
            print("Logging out...")
            break
        elif choice == 1:
            connect_with_person(user_list, friends_graph, user)
        elif choice == 2:
            delete_connection(user_list, friends_graph, user)
        elif choice == 3:
            see_friends(user_list, user)
        else:
            print("Invalid input. Please enter correct options.")


def connect_with_person(user_list, friends_graph, user):
    person_name = input("Enter the person's username: ").strip()
    try:
        friend = user_list[person_name]
        if friend.username not in friends_graph[user.username]:
            friends_graph[user.username].append(friend.username)
            friends_graph[friend.username].append(user.username)
            print(f"User '{friend.username}' added to your friend list")
        else:
            print(f"User '{friend.username}' is already your friend")
    except KeyError:
        print(f"User '{person_name}' not found")


def delete_connection(user_list, friends_graph, user):
    person_name = input("Enter the person's username: ").strip()
    try:
        friend = user_list[person_name]
        if friend.username in friends_graph[user.username]:
            friends_graph[user.username].remove(friend.username)
            friends_graph[friend.username].remove(user.username)
            print(f"User '{friend.username}' removed from your friend list")
        else:
            print(f"User '{friend.username}' is not your friend")
    except KeyError:
        print(f"User '{person_name}' not found")


def see_friends(user_list, user):
    for person in user_list.values():
        if person.username in user.friends:
            print(person.display_description())


def create_new_account(user_list):
    name = input("Enter name: ")
    mobile_number = input("Enter mobile number: ")
    username = input("Enter username: ")
    while True:
        password = input("Enter password: ")
        again_password = input("Enter again password: ")
        if password == again_password:
            user = Person(name, username, password, mobile_number)
            user_list[user.username] = user
            print("Account has been created. Login again to continue.\n")
            break
        else:
            print("Passwords do not match")


if __name__ == "__main__":
    main()
