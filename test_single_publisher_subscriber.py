from client_api import Publisher, Subscriber
import time

def test_single_publisher_subscriber():
    # Initialize Publisher and Subscriber
    publisher = Publisher('localhost', 12346)
    subscriber = Subscriber('localhost', 12346)

    # Register Publisher
    print("Registering Publisher...")
    registration_response = publisher.register()  # Adjust if the method name differs
    print(registration_response)

    # Register Subscriber
    print("Registering Subscriber...")
    registration_response = subscriber.register()  # Adjust if the method name differs
    print(registration_response)

    # Create a topic
    print("Creating topic 'test_topic'...")
    topic_creation_response = publisher.create_topic('test_topic')  # Adjust method name if needed
    print(topic_creation_response)

    # Subscriber subscribes to the topic
    print("Subscribing to 'test_topic'...")
    subscription_response = subscriber.subscribe('test_topic')
    print(subscription_response)

    # Publisher sends a message
    print("Sending message 'Hello World!' to 'test_topic'...")
    send_response = publisher.send('test_topic', 'Hello World!')
    print(send_response)

    # Subscriber pulls the message
    print("Subscriber pulling messages from 'test_topic'...")
    pull_response = subscriber.pull('test_topic')
    print(pull_response)

if __name__ == "__main__":
    test_single_publisher_subscriber()
