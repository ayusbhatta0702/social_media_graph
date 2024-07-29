import math
import sys
import csv
import turtle
import random

class Person:
    def __init__(self, name, username, password, mobile_number):
        self.name = name
        self.username = username
        self.password = password
        self.mobile_number = mobile_number
        
    friends = []
    sent_requests = []
    recieved_requests = []
    
    def _str_(self):
        info = f"""Name: {self.name}
        Username: {self.username}
        Password: {self.password}
        Mobile Number: {self.mobile_number}                
                """
        return info
    
    def display_description(self):
        info = f"""Name: {self.name}
        Username: {self.username}"""
        return info
    
password_list = ["12345", "54321", "11111"]
filename = "file_path"

    
def main():
    user_list, connection_graph = load_data(filename)

    print("Welcome to BhattaBook\n")
    print("What are you?\n1.Admin     2. User")
    try:
        role = int(input("Enter your response: "))
    except ValueError:
        print("Invalid input")
        sys.exit(0)

    if role==1:
        password = input("Please enter your password: ")
        if password in password_list:
            print("Access granted.")
            user_list, connection_graph = manipulate_as_admin(user_list, connection_graph)
        else:
            print("Access Denied")
            sys.exit(0)
    elif role==2:
        while(True):
            print("What do you want to do?\n1. Login        2. Create new Account")
            choice = int(input("Enter your response: "))
            if choice==1:                                                                   # Login
                while(True):
                    mobile_number = input("Please enter your mobile number: ")
                    user_password = input("Please enter your password: ")
                    person = find_person(mobile_number, user_password, user_list)
                    if person:
                        connection_graph = use_account(person, user_list, connection_graph)
                    else:
                        print("Either mobile number or password is incorrect.\nPlease try again.")
                        continue

            elif choice==2:                                                                 # Register
                name = input("Please enter your name: ")
                username = input("Please enter your username: ")
                mobile_number = int(input("Please enter your mobile number: "))
                user_password = 'TEMP'
                while(True):
                    temp_password = input("Please enter a password: ")
                    if (temp_password == input("Please enter your password again: ")):
                        user_password = temp_password
                        break
                    else:
                        print("Passwords do not match")
                        continue

                user_list, person = create_account(name, username, user_password, mobile_number, user_list, connection_graph)                              # Account created
                use_account(person, user_list, connection_graph)
            else:
                print("Invalid input")
                continue
    
    else:
        print("Invalid input")
        sys.exit(0)

    return





def create_account(name, username, password, mobile_number, old_list, connection_graph):
    person = Person(name, username, password, mobile_number)
    old_list.append(person)
    user_list = sorted(old_list, key=lambda x: int(x.mobile_number))
    connection_graph[username] = {}
    return user_list, person


def find_person(mobile_number, user_password, user_list):
    low = 0
    high = len(user_list) - 1

    while low <= high:
        mid = (low + high) // 2
        mid_person = user_list[mid]
        if mid_person.mobile_number == mobile_number:
            if mid_person.password == user_password:
                return mid_person
            else:
                return None
        elif mid_person.mobile_number < mobile_number:
            low = mid + 1
        else:
            high = mid - 1
    return None

def find_person_by_mobile_number(mobile_number_of_friend, user_list):
    low = 0
    high = len(user_list) - 1

    while low <= high:
        mid = (low + high) // 2
        mid_person = user_list[mid]
        if mid_person.mobile_number == mobile_number_of_friend:
            return mid_person
        elif mid_person.mobile_number < mobile_number_of_friend:
            low = mid + 1
        else:
            high = mid - 1
    return user_list[0]

def load_data(account_filename):
    temp_user_list = []
    connection_graph = {}
    with open(account_filename, 'r') as file1:
        csv_file = csv.DictReader(file1)
        for row in csv_file:
            name = row['Name']
            username = row['Username']
            password = row['Password']
            mobile_number = row['Mobile_number']
            person = Person(name, username, password, mobile_number)
            temp_user_list.append(person)

    user_list = sorted(temp_user_list, key=lambda x: x.mobile_number)

    with open(account_filename, 'r') as file1:
        csv_file = csv.DictReader(file1)
        for row in csv_file:
            username = row['Username']
            connection_graph[username] = {}

            received_requests = row['Received_requests'].split(',')
            connection_graph[username]['Received_requests'] = []
            for received_username in received_requests:
                for person in user_list:
                    if received_username == person.username:
                        connection_graph[username]['Received_requests'].append({'Username': person.username, 'Mobile_number': person.mobile_number})

            sent_requests = row['Sent_requests'].split(',')
            connection_graph[username]['Sent_requests'] = []
            for sent_username in sent_requests:
                for person in user_list:
                    if sent_username == person.username:
                        connection_graph[username]['Sent_requests'].append({'Username': person.username, 'Mobile_number': person.mobile_number})

            friends = row['Friends'].split(',')
            connection_graph[username]['Friends'] = []
            for friend_username in friends:
                for person in user_list:
                    if friend_username == person.username: 
                        connection_graph[username]['Friends'].append({'Username': person.username, 'Mobile_number': person.mobile_number})

    print(connection_graph)
    return user_list, connection_graph


def display_menu():
    print("\nWhat do you want to do?\n")
    print("1. View details of your account")
    print("2. View my friends")
    print("3. View my sent requests")
    print("4. View any received requests")
    print("5. Send friend request")
    print("6. View suggested friends")
    print("0. Exit")


def view_friends(user_list, connection_graph, my_username):
    if connection_graph[my_username]['Friends']:
        for friend in connection_graph[my_username]['Friends']:
            mobile_number_of_friend = friend['Mobile_number']
            person = find_person_by_mobile_number(mobile_number_of_friend, user_list)
            print(person.display_description())

    else:
        print("You have no friends.\n")
    print("\nDo you want to see visuals?     1. Yes       2. No")


def view_sent_requests(user_list, connection_graph, my_username):
    if connection_graph[my_username]['Sent_requests']:
        for friend in connection_graph[my_username]['Sent_requests']:
            mobile_number_of_friend = friend['Mobile_number']
            person = find_person_by_mobile_number(mobile_number_of_friend, user_list)
            print(person.display_description())

    else:
        print("You have no sent requests.\n")
    print("\nDo you want to see visuals?     1. Yes       2. No")


def view_received_requests(user_list, connection_graph, my_username):
    if connection_graph[my_username]['Received_requests']:
        for friend in connection_graph[my_username]['Received_requests']:
            mobile_number_of_friend = friend['Mobile_number']
            person = find_person_by_mobile_number(mobile_number_of_friend, user_list)
            print(person.display_description())

    else:
        print("You have no received requests\n")
    return connection_graph

def accept_friend_requests(user_list, connection_graph, my_username):
    received_requests = connection_graph[my_username]['Received_requests']
    if received_requests:
        print("Received Friend Requests:")
        for i, request in enumerate(received_requests, start=1):
            print(f"{i}. {request['Username']}")

        try:
            request_index = int(input("Enter the number of the friend request you want to accept (or 0 to cancel): "))
            if request_index == 0:
                return connection_graph
            elif 1 <= request_index <= len(received_requests):
                request = received_requests[request_index - 1]
                friend_username = request['Username']
                friend_mobile_number = request['Mobile_number']

                # Add friend to the friends list
                connection_graph[my_username]['Friends'].append({'Username': friend_username, 'Mobile_number': friend_mobile_number})

                # Remove friend request from received requests
                del received_requests[request_index - 1]

                # Update the corresponding sent requests for the friend
                sent_requests = connection_graph[friend_username]['Sent_requests']
                for sent_request in sent_requests:
                    if sent_request['Username'] == my_username:
                        sent_requests.remove(sent_request)
                        break

                print(f"{friend_username} has been added to your friends list.")
            else:
                print("Invalid request number.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    else:
        print("You have no friend requests.")
    return connection_graph



def send_friend_request(user_list, connection_graph, my_username):
    friend_username = input("Please enter friend's username: ").strip()
    flag = 0
    friend_mobile_number = 0
    for person in user_list:
        if friend_username == person.username:
            flag = 1
            friend_mobile_number = person.mobile_number
            break
    if flag == 1:
        inner_flag = 0
        for people in connection_graph[my_username]['Sent_requests']:
            if people['Username'] == friend_username:
                print(f"You have already sent a friend request to {friend_username}")
                inner_flag = 1
                break
        for people in connection_graph[my_username]['Friends']:
            if people['Username'] == friend_username:
                print(f"You are already friends with {friend_username}")
                inner_flag = 1
                break
        if inner_flag == 0:
            connection_graph[my_username]['Sent_requests'].append({'Username': friend_username, 'Mobile_number': friend_mobile_number})
            connection_graph[friend_username]['Received_requests'].append({'Username': my_username, 'Mobile_number': friend_mobile_number})
    else:
        print(f"{friend_username} does not exist")


def handle_user_input(user_list, connection_graph, my_username, choice, person):
    if choice == 0:
        print("Logging out...")
        return
    elif choice == 1:
        print(person)
    elif choice == 2:
        view_friends(user_list, connection_graph, my_username)
    elif choice == 3:
        accept_friend_requests(user_list, connection_graph, my_username)
    elif choice == 4:
        connection_graph = view_received_requests(user_list, connection_graph, my_username)
    elif choice == 5:
        connection_graph = send_friend_request(user_list, connection_graph, my_username)
    else:
        print("Invalid input")


def use_account(person, user_list, connection_graph):
    my_username = person.username
    while True:
        display_menu()
        choice = int(input("Enter your choice: "))
        connection_graph = handle_user_input(user_list, connection_graph, my_username, choice, person)
        if choice == 0:
            break
    return connection_graph

def manipulate_as_admin(user_list, connection_graph):
    while True:
        print("1. View users as admin")
        print("2. Visuals as graph")
        print("3. Delete users as admin")
        print("0. Exit")

        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid input. Please enter a number.")

        match choice:
            case 0:
                print("Logging out...")
                break
            case 1:
                view_users_as_admin(user_list)
            case 2:
                visualize_as_graph(user_list, connection_graph)
            case 3:
                username = input("Enter the username you want to delete: ")
                user_list, connection_graph = delete_user(username, user_list, connection_graph)
            case _:
                print("Invalid input. Please enter a number.")

    return user_list, connection_graph


def view_users_as_admin(user_list):
    for i, person in enumerate(user_list, start=1):
        print(f"{i}.", end=" ")
        print(person)
    
def delete_user(username, user_list, connection_graph):
    # Check if the user exists
    user_exists = False
    for user in user_list:
        if user.username == username:
            user_exists = True
            break

    if user_exists:
        # Remove user from user_list
        user_list = [user for user in user_list if user.username != username]

        # Remove user from connection_graph
        if username in connection_graph:
            del connection_graph[username]

        # Remove user from friends lists of other users
        for user, connections in connection_graph.items():
            for category in connections:
                for friend in connections[category]:
                    if friend['Username'] == username:
                        connections[category].remove(friend)

        print(f"User '{username}' has been successfully deleted.")
    else:
        print(f"User '{username}' does not exist.")

    return user_list, connection_graph


def visualize_as_graph(user_list, connection_graph):
  # Screen setup
  screen = turtle.Screen()
  screen.setup(width=800, height=600)
  screen.bgcolor("lightblue")  # Set background color

  # Function to draw a user node
  def draw_user(user, x, y):
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.fillcolor("white")
    t.begin_fill()
    t.circle(20)  # Adjust circle size as needed
    t.end_fill()
    t.penup()
    t.goto(x, y + 25)  # Adjust label position
    t.write(user.username, align="center", font=("Arial", 12, "bold"))

  # Function to draw a connection between two users
  def draw_connection(username1, username2):
    person1 = next((person for person in user_list if person.username == username1), None)
    person2 = next((person for person in user_list if person.username == username2), None)
    if person1 and person2:
      t.penup()
      # Randomize user position within adjusted boundaries
      max_radius = min(screen.window_width() // 2 - 50, screen.window_height() // 2 - 50)
      x1 = random.randint(-max_radius + 50, max_radius - 50) + screen.window_width() // 2
      y1 = random.randint(-max_radius + 50, max_radius - 50) + screen.window_height() // 2
      t.goto(x1, y1)
      t.pendown()
      x2 = random.randint(-max_radius + 50, max_radius - 50) + screen.window_width() // 2
      y2 = random.randint(-max_radius + 50, max_radius - 50) + screen.window_height() // 2
      t.goto(x2, y2)
      t.pencolor("black")
      t.hideturtle()

  # Draw user nodes and connections
  t = turtle.Turtle()
  t.speed(3)  # Set drawing speed to fastest

  # Distribute user nodes evenly on the screen (modify as needed)
  num_users = len(user_list)
  circle_radius = 50  # Adjust based on circle size and screen size
  angle = 360 / num_users
  for i, user in enumerate(user_list):
    x = circle_radius * math.cos(math.radians(angle * i)) + screen.window_width() // 2
    y = circle_radius * math.sin(math.radians(angle * i)) + screen.window_height() // 2
    draw_user(user, x, y)

  # Draw connections between friends
  for username, connections in connection_graph.items():
    if 'Friends' in connections:
      for friend in connections['Friends']:
        friend_username = friend['Username']
        draw_connection(username, friend_username)

  # Hide the turtle and display the graph (centered)
  t.hideturtle()
#   screen.setposition(0) # Move the canvas to (0, 0) for centering
  turtle.done()



if __name__=="__main__":
    main()
