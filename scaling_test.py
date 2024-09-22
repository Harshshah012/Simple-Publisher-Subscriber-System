from client_api import Subscriber, Publisher
import time

def scaling_test(num_pairs):
    start_time = time.time()
    subscribers = []
    publishers = []
    success_count = 0

    # Create common topics for the pairs
    try:
        for i in range(num_pairs):
            publisher = Publisher('localhost', 12346)
            publisher.register()  # Ensure the publisher is registered before creating the topic
            publishers.append(publisher)
            topic = f"scaling_topic_{i}"
            publisher.create_topic(topic)  # Adjust based on actual method name if needed
            print(f"Created topic '{topic}' for client pair {i}.")
    except Exception as e:
        print(f"Failed to create topics: {e}")
        return success_count

    # Try to connect multiple subscribers and publishers in pairs
    for i in range(num_pairs):
        try:
            subscriber = Subscriber('localhost', 12346)
            subscriber.register()  # Ensure the subscriber is registered before subscribing to the topic
            subscribers.append(subscriber)
            topic = f"scaling_topic_{i}"
            subscriber.subscribe(topic)
            print(f"Subscriber {i} subscribed to {topic}.")
            success_count += 1
        except TimeoutError:
            print(f"TimeoutError: Failed to connect subscriber {i}. Stopping test.")
            break
        except Exception as e:
            print(f"Error with client pair {i}: {e}")
            break

    end_time = time.time()

    total_time = end_time - start_time
    print(f"\nSuccessfully connected {success_count} subscriber-publisher pairs.")
    print(f"Time taken: {total_time:.2f} seconds.")
    
    return success_count

if __name__ == "__main__":
    client_counts = [50]  # Gradually increase client pairs
    max_successful_pairs = 0

    for count in client_counts:
        print(f"\nScaling test with {count} subscriber-publisher pairs:")
        successful_pairs = scaling_test(count)

        # Stop if no new successful pairs were added
        if successful_pairs == max_successful_pairs:
            print(f"Max connection limit reached at {max_successful_pairs} pairs.")
            break

        # Update the maximum successful pair count
        max_successful_pairs = successful_pairs

    print(f"\nScaling test completed. Maximum successful subscriber-publisher pairs: {max_successful_pairs}")
