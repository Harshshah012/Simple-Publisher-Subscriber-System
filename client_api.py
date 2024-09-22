import socket
import json

# Publisher class handles all operations related to a publisher
class Publisher:
    # Initializing publisher with server details and create a TCP socket
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))  # Establishing connection to the server
        self.publisher_id = None  # This will store the publisher's unique ID after registration

    # Registering the publisher with the server
    def register(self):
        request = "REGISTER_PUBLISHER"
        self.socket.sendall(request.encode())  # Sending the registration request to the server
        response = self.socket.recv(1024).decode()  # Receiving server's response

        if not response:
            return {"status": "Error: No response from server"}  # Error Handling

        try:
            response_data = json.loads(response)  # Trying to parse the server's response
        except json.JSONDecodeError:
            return {"status": "Error: Invalid response format", "response": response}

        # If registration is successful, will store the publisher ID
        if response_data.get("status") == "Publisher registered successfully":
            self.publisher_id = response_data["publisher_id"]
        return response_data

    # Login to the server using an existing publisher ID
    def login(self, publisher_id):
        request = f"LOGIN_PUBLISHER {publisher_id}"
        self.socket.sendall(request.encode())  # Sending login request
        response = self.socket.recv(1024).decode()  # Receiving response

        if not response:
            return {"status": "Error: No response from server"}  # Error Handling

        try:
            response_data = json.loads(response)  # Parsing the response
        except json.JSONDecodeError:
            return {"status": "Error: Invalid response format"}

        # If login is successful, store the publisher ID
        if response_data.get("status") == "Logged in successfully":
            self.publisher_id = publisher_id
        return response_data

    # Create a new topic on the server
    def create_topic(self, topic):
        if self.publisher_id:
            # Sending a request to create a new topic, only if publisher is registered
            request = f"CREATE_TOPIC {self.publisher_id} {topic}"
            self.socket.sendall(request.encode())
            response = self.socket.recv(1024).decode()
            return json.loads(response)  # Return server's response
        return {"status": "Publisher not registered"}

    # Delete an existing topic from the server
    def delete_topic(self, topic):
        if self.publisher_id:
            request = f"DELETE_TOPIC {self.publisher_id} {topic}"
            self.socket.sendall(request.encode())  # Sending delete topic request
            response = self.socket.recv(1024).decode()
            return json.loads(response)
        return {"status": "Publisher not registered"}

    # Send a message to a specific topic
    def send(self, topic, message):
        if self.publisher_id:
            # Formatting the request with publisher ID, topic, and message
            request = f"SEND {self.publisher_id} {topic} {message}"
            self.socket.sendall(request.encode())  # Send message request
            response = self.socket.recv(1024).decode()
            return json.loads(response)
        return {"status": "Publisher not registered"}

    # Retrieve all available topics from the server
    def get_topics(self):
        request = "GET_TOPICS"
        self.socket.sendall(request.encode())  # Request the list of topics
        response = self.socket.recv(1024).decode()
        return json.loads(response)  # Return the parsed list of topics

    # Close the connection with the server
    def disconnect(self):
        self.socket.close()

# Subscriber class handles operations for a subscriber
class Subscriber:
    # Initializing subscriber with server details and create a TCP socket
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))  # Establishing connection to the server
        self.subscriber_id = None
        self.subscribed_topics = []  # Track subscribed topics
        self.last_messages = {}  # Track the last messages pulled per topic

    # Registering the subscriber with the server
    def register(self):
        request = "REGISTER_SUBSCRIBER"
        self.socket.sendall(request.encode())  # Send registration request
        response = self.socket.recv(1024).decode()

        if not response:
            return {"status": "Error: No response from server"}  # Error Handling

        try:
            response_data = json.loads(response)  # Parsing server's response
        except json.JSONDecodeError:
            return {"status": "Error: Invalid response format"}

        # If registration is successful, stores the subscriber ID
        if response_data.get("status") == "Subscriber registered successfully":
            self.subscriber_id = response_data.get("subscriber_id")
        return response_data

    # Login using an existing subscriber ID
    def login(self, subscriber_id):
        request = f"LOGIN_SUBSCRIBER {subscriber_id}"
        self.socket.sendall(request.encode())  # Sending login request
        response = self.socket.recv(1024).decode()

        if not response:
            return {"status": "Error: No response from server"}  # Error Handling

        try:
            response_data = json.loads(response)  # Parsing server's response
        except json.JSONDecodeError:
            return {"status": "Error: Invalid response format"}

        # If login is successful, load the subscriber's topics
        if response_data.get("status") == "Logged in successfully":
            self.subscriber_id = subscriber_id
            self.load_subscribed_topics()
        return response_data

    # Fetch all topics the subscriber is subscribed to
    def load_subscribed_topics(self):
        if self.subscriber_id:
            request = f"GET_SUBSCRIBED_TOPICS {self.subscriber_id}"
            self.socket.sendall(request.encode())  # Requesting the subscribed topics list
            response = self.socket.recv(1024).decode()

            if not response:
                return {"status": "Error: No response from server"}

            try:
                response_data = json.loads(response)
            except json.JSONDecodeError:
                return {"status": "Error: Invalid response format"}

            # Updating the subscriber's list of topics
            if response_data.get("status") == "Success":
                self.subscribed_topics = response_data.get("subscribed_topics", [])
            return response_data
        return {"status": "Subscriber not registered"}

    # Subscribe to a specific topic
    def subscribe(self, topic):
        if self.subscriber_id:
            request = f"SUBSCRIBE {self.subscriber_id} {topic}"
            self.socket.sendall(request.encode())  # Send subscription request
            response = self.socket.recv(1024).decode()

            if not response:
                return {"status": "Error: No response from server"}

            try:
                response_data = json.loads(response)
            except json.JSONDecodeError:
                return {"status": "Error: Invalid response format"}

            # If subscription is successful, add topic to local list
            if response_data.get("status").startswith("Subscriber"):
                self.subscribed_topics.append(topic)
            return response_data
        return {"status": "Subscriber not registered"}

    # Pull new messages from a topic
    def pull(self, topic):
        if self.subscriber_id:
            request = f"PULL {self.subscriber_id} {topic}"
            self.socket.sendall(request.encode())  # Send pull request
            response = self.socket.recv(1024).decode()
            response_data = json.loads(response)

            # Store the last message for the topic if messages were pulled
            if response_data.get("status") == "Messages pulled":
                messages = response_data.get('messages', [])
                if messages:
                    self.last_messages[topic] = messages[-1]
                return response_data
            return {"status": "No new messages."}
        return {"status": "Subscriber not registered"}

    # Close the connection with the server
    def disconnect(self):
        self.socket.close()