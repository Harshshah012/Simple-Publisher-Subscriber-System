from client_api import Subscriber, Publisher
import time

def benchmark_pull(num_topics):
    start_time = time.time()
    subscriber = Subscriber('localhost', 12346)
    
    # Register subscriber
    print("Registering subscriber...")
    print(subscriber.register())  # Assuming you need to register first

    # Create topics and send messages to them
    publisher = Publisher('localhost', 12346)
    publisher.register()  # Register publisher if needed

    try:
        for i in range(num_topics):
            topic_name = f"pull_topic_{i}"
            print(f"Creating topic '{topic_name}' and sending messages...")
            publisher.create_topic(topic_name)  # Use the correct function here
            for j in range(5):  # Sending 5 messages per topic
                publisher.send(topic_name, f'Message {j} from {topic_name}')
    except Exception as e:
        print(f"Error during topic creation or message sending: {e}")
        return 0  # Exit if unable to create topics or send messages

    success_count = 0

    # Try to pull messages from topics
    for i in range(num_topics):
        try:
            topic_name = f"pull_topic_{i}"
            print(f"Pulling messages from '{topic_name}'...")
            messages = subscriber.pull(topic_name)  # Use the pull function here
            print(f"Pulled messages: {messages}")
            success_count += len(messages)  # Count the messages pulled
        except Exception as e:
            print(f"Error during pulling messages from {topic_name}: {e}")
            break

    end_time = time.time()

    total_time = end_time - start_time
    print(f"\nSuccessfully pulled {success_count} messages.")
    print(f"Time taken: {total_time:.2f} seconds.")

    return success_count

if __name__ == "__main__":
    client_counts = [50]  # Adjust as needed
    max_successful_pulls = 0

    for count in client_counts:
        print(f"\nBenchmarking pull operation with {count} topics:")
        successful_pulls = benchmark_pull(count)

        # Stop if no new successful pulls were added
        if successful_pulls == max_successful_pulls:
            print(f"Max pull throughput reached at {max_successful_pulls} messages.")
            break

        # Update the maximum successful pull count
        max_successful_pulls = successful_pulls

    print(f"\nBenchmark completed. Maximum successful pulls: {max_successful_pulls}")
