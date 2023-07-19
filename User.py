import sqlite3
from Hostname import Hostname
from Log import Log
import threading
import time

DB_URL = "monitoring.db"


class User:
    @classmethod
    def create_table(cls):
        query = """
                    CREATE TABLE IF NOT EXISTS users(
                        id INTEGER PRIMARY KEY,
                        fullname TEXT NOT NULL,
                        email TEXT NOT NULL UNIQUE,
                        username TEXT NOT NULL UNIQUE,
                        password TEXT NOT NULL
                    );
                """
        conn = sqlite3.connect(DB_URL)
        cursor = conn.cursor()
        cursor.execute(query)
        conn.close()

    def __init__(self, fullname, email, username, password, id=None):
        self.fullname = fullname
        self.email = email
        self.username = username
        self.password = password
        self.id = id

    @classmethod
    def login(cls, username, password):
        query = f"""
                    SELECT * FROM users WHERE username == ? and password == ?;
                """
        conn = sqlite3.connect(DB_URL)
        cursor = conn.cursor()
        result = cursor.execute(query, (username, password)).fetchone()
        user = User(result[1], result[2], result[3], result[4], result[0])
        print(user.fullname)
        if result == None:
            print("Wrong Username or Password!!!")
        else:
            print(result)
            return user
        conn.close()

    def register(self):
        query = """
                    INSERT INTO users(fullname,email,username,password) values(?,?,?,?);
                """
        conn = sqlite3.connect(DB_URL)
        cursor = conn.cursor()
        cursor.execute(query, (self.fullname, self.email, self.username, self.password))
        self.id = cursor.lastrowid
        conn.commit()
        conn.close

    def add_hostname(self):
        pass

    def del_hostname(self):
        pass

    def get_hostnames(self):
        pass


User.create_table()
Hostname.create_table()
Log.create_table()
Hostname.start_ping_check()

while True:
    choice = input("Enter your choice (1 for Log In, 2 for Register): ")
    print(choice)
    if choice == "2":
        fullname = input("Enter your Full Name: ")
        email = input("Enter your email: ")
        username = input("Enter your Username: ")
        password = input("Enter your Password: ")
        print(fullname, email, username, password)
        user = User(fullname, email, username, password)
        user.register()
        print("Succesfull Registration!")
    else:
        username = input("Username: ")
        password = input("Password: ")
        user = User.login(username, password)

        if isinstance(user, User):
            # print("match")
            while True:
                option = input(
                    "1. Display Hosts\n"
                    "2. Add Host\n"
                    "3. Remove Host\n"
                    "4. Back\n"
                    "5. Display Host's Logs\n"
                    "6. Display Current Alarms\n"
                    "Enter your choice: "
                )

                if option == "1":
                    Hostname.display_hosts(user)
                    print("")
                    # Perform action to display hosts
                    # Fetch and display the hosts for the user

                elif option == "2":
                    # Perform action to add host
                    name = input("Enter the name of the host: ")
                    hostname = input("Enter the hostname: ")
                    type = input("Enter the type of the host: ")
                    host = Hostname(name, hostname, type)
                    host.add_host(user)
                    # Call the add_host method of the Hostname class with the provided details

                elif option == "3":
                    name = input("Enter the name of the host: ")
                    Hostname.remove_host(user, name)

                elif option == "4":
                    # Quit and go back
                    # Hostname.running_thread = False
                    # Hostname.kill_thread()
                    # import os
                    # quit()
                    break

                elif option == "5":
                    while True:
                        host_name = input("Enter Host's Name: ")
                        history_log_range = input("Display Log History: ")
                        Hostname.select_host(user, host_name)
                        break
                elif option == "6":
                    Log.display_current_alarms(user)
                    pass

                else:
                    print("Invalid choice. Please try again.")
