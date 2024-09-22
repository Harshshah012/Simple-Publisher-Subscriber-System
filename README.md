# Advance Operating Systems CS 550 
# Programming Assignment 1
# Name: Harsh Shah
# Publisher-Subscriber System

## Overview.
This Python project implements a Publisher-Subscriber model, which allows publishers to send messages to topics and subscribers to retrieve messages from them. The system is intended to promote communication among numerous clients (publishers and subscribers) via a server.

## Features.
Publisher functionality:
  1. Register as a new publisher
  2. Login with an existing publisher ID 
  3. Create and Delete topics
  4. Send messages to topics
  5. View messages under each topic and also published by whom.

Subscription Functionality:
  1. Sign up as a new subscriber 
  2. Log in with your existing subscriber ID 
  3. Subscribe to Topics.
  4. Retrieve messages from Subscribed Topics 
  5. View Subscribed Topics.

## Requirements
1. Python 3.x 
2. 'socket' module (included in the standard library).
3. 'threading' module (included in the standard library)
4. 'json' module (found in the standard library)
5. 'uuid' module (found in the standard library)

## Code Structure:
1. **server.py**: Contains the server code that manages client connections, topics, and message delivery.
2. **client_api.py**: This file implements the Publisher and Subscriber classes for client interactions.
3. **main_menu.py**: Contains the user interface for interacting as a publisher or a subscriber.
4. **Makefile**: Automates tasks for starting the server, running the main program, running benchmarks, and cleaning up files.

## Running  the Project Manually:
1. Run the server by executing `python server.py` or `python3 server.py` in your terminal. This will open a terminal  window for the server where we can see all the server logs.
2. Run the main menu by executing `python Main_menu.py` or `python3 Main_menu.py` in your terminal.

## Running the program and all tests using MAKEFILE:
1. Run the main  menu by executing `make main_menu` in your terminal. After running  the main menu, you can interact with the system.
2. To kill the server terminal, type `make clean` to stop the server and exit the program.
3. Run all the benchmark/working tests by executing `make run_benchmarks` in your terminal. This will start the server and run all the tests and exit the program by cleaning up the files.

## Usage
1. Choose between Publisher and Subscriber mode from the main menu.
2. Follow the prompts to register, login, create topics, send messages, and pull messages.
