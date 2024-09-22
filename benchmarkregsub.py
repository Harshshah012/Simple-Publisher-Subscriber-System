from client_api import Subscriber
import time

def benchmark_register_subscriber(num_clients):
    start_time = time.time()
    subscribers = []
    success_count = 0

    for i in range(num_clients):
        try:
            # Attempt to connect and register a new Subscriber
            subscriber = Subscriber('localhost', 12346)
            subscribers.append(subscriber)
            print(f"Registering Subscriber {i + 1}...")
            response = subscriber.register()
            print(response)
            success_count += 1
        except Exception as e:
            # Capture the connection error or registration failure
            print(f"Failed to register Subscriber {i + 1}: {e}")
            break

    end_time = time.time()

    total_time = end_time - start_time
    print(f"\nSuccessfully registered {success_count} subscribers.")
    print(f"Time taken: {total_time:.2f} seconds.")
    if success_count > 0:
        print(f"Average time per registration: {total_time / success_count:.4f} seconds.\n")
    else:
        print("No subscribers were successfully registered.\n")

    return success_count

if __name__ == "__main__":
    client_counts = [50]  # Start with low numbers and increase progressively
    max_successful_clients = 0

    for count in client_counts:
        print(f"\nBenchmarking subscriber registration with {count} clients:")
        successful_clients = benchmark_register_subscriber(count)

        # Stop if no new successful clients were added
        if successful_clients == max_successful_clients:
            print(f"Max registration throughput reached at {max_successful_clients} clients.")
            break

        # Update the maximum successful client count
        max_successful_clients = successful_clients

    print(f"\nBenchmark completed. Maximum successful clients: {max_successful_clients}")
