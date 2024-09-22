from client_api import Subscriber
from client_api import Publisher
import time

def benchmark_subscribe(num_topics):
    start_time = time.time()
    subscribers = []
    success_count = 0

    # Create a common subscriber for all topics
    try:
        subscriber = Subscriber('localhost', 12346)
        subscribers.append(subscriber)
        print("Registering subscriber...")
        print(subscriber.register())  # Assuming you need to register first
    except Exception as e:
        print(f"Error during subscriber registration: {e}")
        return success_count

    # Create topics to subscribe to
    try:
        for i in range(num_topics):
            topic_name = f"subscribe_topic_{i}"
            print(f"Creating topic '{topic_name}' for subscription...")
            # Assuming you have a Publisher object to create topics
            publisher = Publisher('localhost', 12346)
            publisher.register()  # Register publisher if needed
            publisher.create_topic(topic_name)  # Use the correct function here
    except Exception as e:
        print(f"Error during topic creation: {e}")
        return success_count

    # Try to subscribe to topics
    for i in range(num_topics):
        try:
            topic_name = f"subscribe_topic_{i}"
            print(f"Subscribing to '{topic_name}'...")
            response = subscriber.subscribe(topic_name)  # Use the subscribe function here
            print(response)
            success_count += 1
        except Exception as e:
            print(f"Error during subscription: {e}")
            break

    end_time = time.time()

    total_time = end_time - start_time
    print(f"\nSuccessfully subscribed to {success_count} topics.")
    print(f"Time taken: {total_time:.2f} seconds.")
    
    return success_count

if __name__ == "__main__":
    client_counts = [50]  # Adjust as needed
    max_successful_subscriptions = 0

    for count in client_counts:
        print(f"\nBenchmarking subscription with {count} topics:")
        successful_subscriptions = benchmark_subscribe(count)

        # Stop if no new successful subscriptions were added
        if successful_subscriptions == max_successful_subscriptions:
            print(f"Max subscription throughput reached at {max_successful_subscriptions} topics.")
            break

        # Update the maximum successful subscription count
        max_successful_subscriptions = successful_subscriptions

    print(f"\nBenchmark completed. Maximum successful subscriptions: {max_successful_subscriptions}")
