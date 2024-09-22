from client_api import Publisher
from client_api import Subscriber

# Function to run the publisher interface
def run_publisher():
    publisher = Publisher('localhost', 12346)
    publisher_id = None  # To keep track of publisher's ID

    while True:
        # Display publisher options
        print("\nPublisher Menu:")
        if publisher_id is None:
            print("1. Register Publisher")
            print("2. Login with Publisher ID")
        else:
            print("3. Create Topic")
            print("4. Delete Topic")
            print("5. Send Message")
            print("6. View All Topics")
        print("7. Exit")

        user_choice = input("Choose an option (1-7): ")

        if user_choice == '1' and publisher_id is None:
            # Registering the publisher
            response = publisher.register()
            print("Register response:", response)
            if response.get("status") == "Publisher registered successfully":
                publisher_id = response["publisher_id"]

        elif user_choice == '2' and publisher_id is None:
            # Logging in the publisher
            publisher_id_input = input("Enter your publisher ID: ")
            response = publisher.login(publisher_id_input)
            print(response)
            if response.get("status") == "Logged in successfully":
                publisher_id = publisher_id_input

        elif user_choice == '3' and publisher_id is not None:
            # Creating a new topic
            topic = input("Enter the topic name to create: ").strip()
            if topic:
                response = publisher.create_topic(topic)
                print(response)
            else:
                print("Topic name cannot be empty.")

        elif user_choice == '4' and publisher_id is not None:
            # Deleting an existing topic
            topic = input("Enter the topic name to delete: ").strip()
            if topic:
                response = publisher.delete_topic(topic)
                print(response)
            else:
                print("Topic name cannot be empty.")

        elif user_choice == '5' and publisher_id is not None:
            # Sending a message to a topic
            topic = input("Enter the topic name to send a message to: ").strip()
            message = input("Enter the message: ").strip()
            if topic and message:
                response = publisher.send(topic, message)
                print(response)
            else:
                print("Both topic and message cannot be empty.")

        elif user_choice == '6' and publisher_id is not None:
            # Viewing all topics
            topics_response = publisher.get_topics()
            
            if topics_response.get("status") == "Error":
                print(topics_response.get("response", "An error occurred."))
            elif "data" in topics_response:  # Ensure the response contains data
                topics = topics_response["data"]
                if topics:  # Display topics and their messages
                    for topic, messages in topics.items():
                        print(f"Topic: {topic}")
                        if messages:
                            print(" Messages:")
                            for msg in messages:
                                print(f"  - {msg['message']} (Published by: {msg['publisher_id']})")
                        else:
                            print(" No messages available.")
                else:
                    print("No topics available.")
            else:
                print("No topics available.")

        elif user_choice == '7':
            # Exiting publisher mode
            print("Exiting Publisher.")
            publisher.disconnect()
            break

        else:
            print("Invalid option or please register/login first.")


# Function to run the subscriber interface
def run_subscriber():
    subscriber = Subscriber('localhost', 12346)
    registered = False  # Track whether the subscriber is registered

    while True:
        # Display subscriber options
        print("\nSubscriber Menu:")
        if not registered:
            print("1. Register Subscriber")
            print("2. Login with Subscriber ID")
        else:
            print("3. Subscribe to Topic")
            print("4. Pull Messages")
            print("5. View Subscribed Topics")
        print("6. Exit")

        user_choice = input("Choose an option (1-6): ")

        if user_choice == '1' and not registered:
            # Registering the subscriber
            response = subscriber.register()
            print(response)
            if response.get("status") == "Subscriber registered successfully":
                registered = True

        elif user_choice == '2' and not registered:
            # Logging in the subscriber
            subscriber_id = input("Enter your subscriber ID: ").strip()
            response = subscriber.login(subscriber_id)
            print(response)
            if response.get("status") == "Logged in successfully":
                registered = True

        elif user_choice == '3' and registered:
            # Subscribing to a topic
            topic = input("Enter the topic name to subscribe to: ").strip()
            if topic:
                response = subscriber.subscribe(topic)
                print(response)

        elif user_choice == '4' and registered:
            # Pulling messages from a subscribed topic
            topic = input("Enter the topic name to pull messages from: ").strip()
            if topic:
                response = subscriber.pull(topic)
                messages = response.get('messages', [])
                if messages:
                    print(f"Messages from topic '{topic}':")
                    for message in messages:
                        print(f" - {message}")
                else:
                    print(response.get("status", "No new messages."))

        elif user_choice == '5' and registered:
            # Viewing subscribed topics and last messages
            if subscriber.subscribed_topics:
                print("Subscribed Topics:")
                for topic in subscriber.subscribed_topics:
                    last_message = subscriber.last_messages.get(topic, "No messages received yet.")
                    print(f" - {topic}: Last Message: {last_message}")
            else:
                print("No topics subscribed.")

        elif user_choice == '6':
            # Exiting subscriber mode
            print("Exiting Subscriber.")
            subscriber.disconnect()
            break

        else:
            print("Invalid option or please register/login first.")


# Main menu to choose between publisher or subscriber mode
def main_menu():
    while True:
        print("\nMain Menu:")
        print("1. Publisher")
        print("2. Subscriber")
        print("3. Exit")

        choice = input("Choose an option (1-3): ")

        if choice == '1':
            run_publisher()
        elif choice == '2':
            run_subscriber()
        elif choice == '3':
            print("Exiting the application.")
            break
        else:
            print("Invalid option, please choose again.")


if __name__ == "__main__":
    main_menu()  # Start the main menu interface
