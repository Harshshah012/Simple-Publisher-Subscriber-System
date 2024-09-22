import socket
import threading
import json
import uuid

# Set maximum message size in bytes (for example, 1024 bytes)
MAX_MESSAGE_SIZE = 1024

# Dictionaries to store registered publishers, subscribers, and their subscriptions
registered_publishers = {}
registered_subscribers = {}
subscribed_topics_per_subscriber = {}  # For Mapping subscriber ID to their subscribed topics
topics = {}  # Dictionary to store topics and their messages
last_pulled = {}  # Keeps track of the last pulled message for each subscriber on each topic
lock = threading.Lock()  # Lock for ensuring thread safety when multiple threads access shared data

# Function to handle client requests
def client_handler(connection, address):
    global topics
    print(f"Connected by {address}")

    try:
        while True:
            try:
                # Receive data from the client
                data = connection.recv(1024).decode()
                if not data:  # If no data, exit the loop
                    break

                print(f"Received request: {data}")
                request_parts = data.split()  # Splitting the received data into parts
                command = request_parts[0]  
                response = {}  # Initializing response as an empty dictionary

                with lock:  # Ensuring thread safety for shared resources
                    # Handle different commands sent by clients
                    if command == "REGISTER_PUBLISHER":
                        # Register as a new publisher by generating a unique ID
                        publisher_id = str(uuid.uuid4())
                        registered_publishers[publisher_id] = True
                        response = {"status": "Publisher registered successfully", "publisher_id": publisher_id}

                    elif command == "LOGIN_PUBLISHER":
                        # Log in publisher using the previous publisher ID
                        publisher_id = request_parts[1]
                        if publisher_id in registered_publishers:
                            response = {"status": "Logged in successfully"}
                        else:
                            response = {"status": "Error: Publisher not registered"}

                    elif command == "CREATE_TOPIC":
                        # Create a new topic
                        publisher_id = request_parts[1]
                        topic = request_parts[2]

                        if publisher_id not in registered_publishers:
                            response = {"status": "Error: Publisher not registered"}
                        elif topic in topics:
                            response = {"status": "Error: Topic already exists"}
                        else:
                            topics[topic] = []  # Initialize topic with an empty list of messages
                            response = {"status": "Topic created"}

                    elif command == "DELETE_TOPIC":
                        # Delete an existing topic
                        publisher_id = request_parts[1]
                        topic = request_parts[2]

                        if publisher_id not in registered_publishers:
                            response = {"status": "Error: Publisher not registered"}
                        elif topic in topics:
                            del topics[topic]  # Remove the topic
                            response = {"status": "Topic deleted"}
                        else:
                            response = {"status": "Error: Topic not found"}

                    elif command == "SEND":
                        # Send a message to a topic
                        publisher_id = request_parts[1]
                        topic = request_parts[2]
                        message = " ".join(request_parts[3:])  # Joining the rest of the message parts

                        if len(message) > MAX_MESSAGE_SIZE:
                            # If message exceeds max size, return an error
                            response = {"status": f"Error: Message size exceeds {MAX_MESSAGE_SIZE} characters."}
                        elif publisher_id not in registered_publishers:
                            response = {"status": "Error: Publisher not registered"}
                        elif topic not in topics:
                            response = {"status": "Error: Topic not found"}
                        else:
                            topics[topic].append({"publisher_id": publisher_id, "message": message})  # Add message to the topic
                            response = {"status": "Message sent", "data": {"topic": topic, "message": message}}

                    elif command == "GET_TOPICS":
                        # Return a list of all topics with their messages
                        response = {
                            "status": "Success",
                            "data": {topic: messages for topic, messages in topics.items()}
                        }

                    elif command == "REGISTER_SUBSCRIBER":
                        # Registering a new subscriber by generating a unique ID
                        subscriber_id = str(uuid.uuid4())
                        registered_subscribers[subscriber_id] = True
                        subscribed_topics_per_subscriber[subscriber_id] = []  # Initializing an empty list of subscribed topics
                        response = {"status": "Subscriber registered successfully", "subscriber_id": subscriber_id}

                    elif command == "LOGIN_SUBSCRIBER":
                        # Log in a subscriber using their subscriber ID
                        subscriber_id = request_parts[1]
                        if subscriber_id in registered_subscribers:
                            response = {"status": "Logged in successfully"}
                        else:
                            response = {"status": "Error: Subscriber not registered"}

                    elif command == "SUBSCRIBE":
                        # Subscriber subscribes to a topic
                        subscriber_id = request_parts[1]
                        topic = request_parts[2]

                        if subscriber_id not in registered_subscribers:
                            response = {"status": "Error: Subscriber not registered"}
                        elif topic not in topics:
                            response = {"status": "Error: Topic does not exist"}
                        else:
                            if topic not in subscribed_topics_per_subscriber[subscriber_id]:
                                subscribed_topics_per_subscriber[subscriber_id].append(topic)  # Add topic to subscriber's list
                            response = {"status": f"Subscriber {subscriber_id} subscribed to {topic}"}

                    elif command == "PULL":
                        # Pull new messages for a subscriber from a specific topic
                        subscriber_id = request_parts[1]
                        topic = request_parts[2]

                        if subscriber_id not in registered_subscribers:
                            response = {"status": "Error: Subscriber not registered"}
                        elif topic in topics:
                            messages = topics[topic]
                            # Check for new messages since the last pull
                            last_message_index = last_pulled.get(subscriber_id, {}).get(topic, -1)
                            new_messages = messages[last_message_index + 1:]  # Get new messages
                            if new_messages:
                                # Update last pulled index for this topic
                                last_pulled.setdefault(subscriber_id, {})[topic] = last_message_index + len(new_messages)
                                response = {"status": "Messages pulled", "messages": new_messages}
                            else:
                                response = {"status": "No new messages."}
                        else:
                            response = {"status": "Error: Topic not found"}

                    elif command == "GET_SUBSCRIBED_TOPICS":
                        # Return the list of topics the subscriber is subscribed to
                        subscriber_id = request_parts[1]
                        if subscriber_id in registered_subscribers:
                            subscribed_topics_list = subscribed_topics_per_subscriber.get(subscriber_id, [])
                            response = {"status": "Success", "subscribed_topics": subscribed_topics_list}
                        else:
                            response = {"status": "Error: Subscriber not registered"}

                    else:
                        # Handling invalid command
                        response = {"status": "Error: Invalid command"}

                # Sending response back to the client as a JSON string
                connection.sendall(json.dumps(response).encode())

            except ConnectionResetError:
                print(f"Client {address} disconnected unexpectedly.")
                break
            except BrokenPipeError:
                print(f"Broken pipe while communicating with {address}. Client may have disconnected.")
                break
            except Exception as e:
                print(f"Error handling request: {e}")
                break
    
    finally:
        # Closing the connection when done
        connection.close()

# Function to start the server
def start_server():
    host = 'localhost'
    port = 12346
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))  # Bind the socket to the address and port
    server_socket.listen(5)  # Listen for up to 5 connections
    print(f"Server started on {host}:{port}")

    try:
        while True:
            # Accept new client connections
            connection, address = server_socket.accept()
            # Start a new thread to handle each client
            threading.Thread(target=client_handler, args=(connection, address)).start()
    except KeyboardInterrupt:
        print("\nShutting down the server.")
    finally:
        server_socket.close()  # Close the server socket when done

# Main entry point to start the server
if __name__ == "__main__":
    start_server()
