from client_api import Publisher
import time

def benchmark_send_message(num_clients):
    start_time = time.time()
    publishers = []
    success_count = 0

    # Step 1: Register a publisher and create a common topic for all clients (if it doesn't already exist)
    try:
        publisher_for_topic = Publisher('localhost', 12346)
        print("Registering Publisher for topic creation...")
        registration_response = publisher_for_topic.register()
        print(registration_response)

        if registration_response.get("status") == "Publisher registered successfully":
            # Try to create the benchmark topic, but handle if it already exists
            print("Creating 'benchmark_topic' (if not already exists)...")
            create_topic_response = publisher_for_topic.create_topic("benchmark_topic")
            print(create_topic_response)

            if "Topic already exists" in create_topic_response.get("status", ""):
                print("Topic already exists. Proceeding with the benchmark.")
            elif create_topic_response.get("status") != "Topic created":
                print(f"Failed to create benchmark topic: {create_topic_response}")
                return 0  # Exit if topic creation fails for any other reason
        else:
            print(f"Failed to register publisher for topic creation: {registration_response}")
            return 0  # Exit if registration fails

    except Exception as e:
        print(f"Failed to create benchmark topic: {e}")
        return 0  # Exit if an exception occurs during topic creation

    # Step 2: Try to connect, register each publisher, and send messages from all clients
    for i in range(num_clients):
        try:
            publisher = Publisher('localhost', 12346)
            publishers.append(publisher)

            # Register each publisher
            print(f"Registering Publisher {i + 1}...")
            registration_response = publisher.register()
            print(registration_response)

            if registration_response.get("status") == "Publisher registered successfully":
                # Proceed to send the message
                message = f"Message {i} from client {i}"
                print(f"Client {i} sending message...")
                response = publisher.send("benchmark_topic", message)
                print(response)
                success_count += 1
            else:
                print(f"Failed to register publisher {i + 1}: {registration_response}")
                break

        except Exception as e:
            print(f"Failed to send message for client {i + 1}: {e}")
            break

    end_time = time.time()

    total_time = end_time - start_time
    print(f"\nSuccessfully sent messages from {success_count} clients.")
    print(f"Time taken: {total_time:.2f} seconds.")
    if success_count > 0:
        print(f"Average time per message: {total_time / success_count:.4f} seconds.\n")
    else:
        print("No messages were successfully sent.\n")

    return success_count

if __name__ == "__main__":
    client_counts = [50]  # Gradually increase client count
    max_successful_clients = 0

    for count in client_counts:
        print(f"\nBenchmarking message sending with {count} clients:")
        successful_clients = benchmark_send_message(count)

        # Stop if no new successful clients were added
        if successful_clients == max_successful_clients:
            print(f"Max throughput reached at {max_successful_clients} clients.")
            break

        # Update the maximum successful client count
        max_successful_clients = successful_clients

    print(f"\nBenchmark completed. Maximum successful clients: {max_successful_clients}")
