from client_api import Publisher
import time

def benchmark_create_topic(num_clients):
    start_time = time.time()
    publishers = []
    success_count = 0

    for i in range(num_clients):
        try:
            # Step 1: Attempt to connect and register a new Publisher
            publisher = Publisher('localhost', 12346)
            publishers.append(publisher)
            print(f"Registering Publisher {i + 1}...")
            registration_response = publisher.register()  # Register the publisher
            print(registration_response)

            if registration_response.get("status") == "Publisher registered successfully":
                # Step 2: Proceed to create a topic after registration
                topic_name = f"topic_{i}"
                print(f"Creating {topic_name}...")
                response = publisher.create_topic(topic_name)  # Create a topic
                print(response)
                if response.get("status") == "Topic created":
                    success_count += 1
                else:
                    print(f"Failed to create topic: {response}")
            else:
                print(f"Failed to register publisher {i + 1}: {registration_response}")
                break

        except Exception as e:
            # Capture any connection or communication error
            print(f"Failed to create topic for client {i + 1}: {e}")
            break

    end_time = time.time()

    total_time = end_time - start_time
    print(f"\nSuccessfully created {success_count} topics.")
    print(f"Time taken: {total_time:.2f} seconds.")
    if success_count > 0:
        print(f"Average time per topic: {total_time / success_count:.4f} seconds.\n")
    else:
        print("No topics were successfully created.\n")

    return success_count

if __name__ == "__main__":
    client_counts = [50]  # Start with low numbers and increase progressively
    max_successful_clients = 0

    for count in client_counts:
        print(f"\nBenchmarking with {count} clients:")
        successful_clients = benchmark_create_topic(count)

        # Stop if no new successful clients were added
        if successful_clients == max_successful_clients:
            print(f"Max throughput reached at {max_successful_clients} clients.")
            break

        # Update the maximum successful client count
        max_successful_clients = successful_clients

    print(f"\nBenchmark completed. Maximum successful clients: {max_successful_clients}")
