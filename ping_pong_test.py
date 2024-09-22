from client_api import Publisher, Subscriber
import time

def ping_pong_test():
    # Register and set up Publisher 1 and Subscriber 1
    print("Registering Publisher 1...")
    publisher_1 = Publisher('localhost', 12346)
    publisher_1.register()
    
    print("Registering Subscriber 1...")
    subscriber_1 = Subscriber('localhost', 12346)
    subscriber_1.register()

    # Register and set up Publisher 2 and Subscriber 2
    print("Registering Publisher 2...")
    publisher_2 = Publisher('localhost', 12346)
    publisher_2.register()
    
    print("Registering Subscriber 2...")
    subscriber_2 = Subscriber('localhost', 12346)
    subscriber_2.register()

    # Attempt to create topics (assuming the correct method is `create_topic`)
    print("Creating topics...")
    publisher_1.create_topic('ping')  # Replace with the correct method name
    publisher_2.create_topic('pong')  # Replace with the correct method name

    # Subscriber 1 subscribes to 'pong', Subscriber 2 subscribes to 'ping'
    print("Subscribing subscribers to topics...")
    subscriber_1.subscribe('pong')
    subscriber_2.subscribe('ping')

    start_time = time.time()

    # Ping-Pong messaging loop
    print("Starting Ping-Pong test...")
    for i in range(50):  # Adjust the number of rounds as needed (currently 5 rounds for testing)
        print(f"Ping-Pong round {i + 1}")
        
        # Publisher 1 sends a 'ping' message
        publisher_1.send('ping', f'ping {i}')
        # Subscriber 2 pulls the 'ping' message
        msg = subscriber_2.pull('ping')
        print(f"Subscriber 2 pulled message: {msg}")

        # Publisher 2 sends a 'pong' response
        publisher_2.send('pong', f'pong {i}')
        # Subscriber 1 pulls the 'pong' message
        msg = subscriber_1.pull('pong')
        print(f"Subscriber 1 pulled message: {msg}")

    end_time = time.time()
    print(f"Ping-Pong test completed in {end_time - start_time:.2f} seconds.")

if __name__ == "__main__":
    ping_pong_test()
