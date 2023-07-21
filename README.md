# phase-3-project
# Monitoring Tool

This repository contains a simple monitoring tool implemented in Python that allows users to monitor the status of various hosts using ICMP ping and HTTP(S) requests.

## Features

- User Registration and Login: Users can register their account and log in to the monitoring tool.
- Host Management: Users can add, remove, and view the list of hosts they want to monitor.
- Ping Check: The tool periodically checks the status of the hosts using ICMP ping and records the response time.
- HTTPS Check: The tool can also check the status of hosts using HTTP(S) requests and records the response time.
- Log History: Users can view the log history of each host, showing when it was online or offline along with response times.
- Current Alarms: The tool displays the current alarms for hosts that are offline.

## Requirements

- Python 3.x
- SQLite3

## Setup

1. Clone the repository to your local machine.
2. Make sure you have Python 3.x installed.
3. Create a virtual environment (optional but recommended).
4. Install the required dependencies.
5. Run the `User.py` script to start the monitoring tool.

## Usage

1. When you run the `User.py` script, you will be prompted to choose between login or registration.
2. If you are a new user, select "Register" and provide your full name, email, username, and password.
3. If you are an existing user, select "Log In" and enter your username and password.
4. After logging in, you will be presented with options to manage your hosts and view logs.
5. Use the provided options to add hosts, remove hosts, view hosts, and view log history.
6. The tool will automatically start monitoring your hosts and displaying current alarms.

## Note

- For HTTPS checks, make sure the hostname starts with "https://" (e.g., https://www.example.com).
- For ICMP checks, only provide the hostname or IP address (e.g., www.example.com or 192.168.1.1).

Enjoy monitoring your hosts with this simple Python tool!
