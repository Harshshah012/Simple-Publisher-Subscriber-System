from client_api import Publisher
import time

def benchmark_delete_topic(num_topics):
    start_time = time.time()
    publishers = []
    success_count = 0

    # Register a publisher for topic deletion
    try:
        publisher = Publisher('localhost', 12346)
        publishers.append(publisher)
        print("Registering publisher...")
        print(publisher.register())  # Assuming you need to register first
    except Exception as e:
        print(f"Error during publisher registration: {e}")
        return success_count

    # Create topics to be deleted later
    try:
        for i in range(num_topics):
            topic_name = f"delete_topic_{i}"
            print(f"Creating topic '{topic_name}' for deletion...")
            publisher.create_topic(topic_name)  # Use the correct function here
    except Exception as e:
        print(f"Error during topic creation: {e}")
        return success_count

    # Try to delete topics
    for i in range(num_topics):
        try:
            topic_name = f"delete_topic_{i}"
            print(f"Deleting topic '{topic_name}'...")
            response = publisher.delete_topic(topic_name)  # Use the delete function here
            print(response)
            success_count += 1
        except Exception as e:
            print(f"Error during topic deletion: {e}")
            break

    end_time = time.time()

    total_time = end_time - start_time
    print(f"\nSuccessfully deleted {success_count} topics.")
    print(f"Time taken: {total_time:.2f} seconds.")
    
    return success_count

if __name__ == "__main__":
    client_counts = [50]  # Adjust as needed
    max_successful_deletions = 0

    for count in client_counts:
        print(f"\nBenchmarking topic deletion with {count} topics:")
        successful_deletions = benchmark_delete_topic(count)

        # Stop if no new successful deletions were added
        if successful_deletions == max_successful_deletions:
            print(f"Max deletion throughput reached at {max_successful_deletions} topics.")
            break

        # Update the maximum successful deletion count
        max_successful_deletions = successful_deletions

    print(f"\nBenchmark completed. Maximum successful deletions: {max_successful_deletions}")
