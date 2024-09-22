import matplotlib.pyplot as plt

# Replace these lists with your actual benchmarking results after running the tests
num_clients = [5, 50, 500, 4095]  # Number of clients tested

# Actual data from your benchmarking tests
# Time in seconds for createTopic(), send() and pull()
times_create_topic = [0.0035, 0.02, 0.14, 8.475]  
times_send_message = [0.0045, 0.02, 0.15, 7.61]  
times_pull_message = [0.002, 0.02, 0.13, 0.97] 
times_register_publisher = [0.0035, 0.02, 0.16, 6.69]
times_register_subscriber = [0.0035, 0.02, 0.15, 6.22]
times_delete_topic = [0.0001, 0.01, 0.08, 0.41]
times_subscribe_topic = [0.0001, 0.02, 0.19, 1.67]

# Plot for registerpublisher()
plt.figure(figsize=(10, 6))
plt.plot(num_clients, times_register_publisher, marker='o', label='Register Publisher', color='yellow')
plt.title('Throughput: Register Publisher')
plt.xlabel('Number of Publishers Registered')
plt.ylabel('Time (seconds)')
plt.grid(True)
plt.legend()
plt.savefig('register_publisher_throughput.png')  # Save the graph to a file
plt.show()

# Plot for registersubscriber()
plt.figure(figsize=(10, 6))
plt.plot(num_clients, times_register_subscriber, marker='o', label='Register Subscriber', color='blue')
plt.title('Throughput: Register Subscriber')
plt.xlabel('Number of Subscribers Registered')
plt.ylabel('Time (seconds)')
plt.grid(True)
plt.legend()
plt.savefig('register_subscriber_throughput.png')  # Save the graph to a file
plt.show()

# Plot for deleteTopic()
plt.figure(figsize=(10, 6))
plt.plot(num_clients, times_delete_topic, marker='o', label='Delete Topic', color='blue')
plt.title('Throughput: Delete Topic')
plt.xlabel('Number of Topics Deleted')
plt.ylabel('Time (seconds)')
plt.grid(True)
plt.legend()
plt.savefig('delete_topic_throughput.png')  # Save the graph to a file
plt.show()

# Plot for subscribeeTopic()
plt.figure(figsize=(10, 6))
plt.plot(num_clients, times_subscribe_topic, marker='o', label='Subscribe Topic', color='blue')
plt.title('Throughput: Subscribe Topic')
plt.xlabel('Number of Topics Subscribed')
plt.ylabel('Time (seconds)')
plt.grid(True)
plt.legend()
plt.savefig('subscribe_topic_throughput.png')  # Save the graph to a file
plt.show()


# Plot for createTopic()
plt.figure(figsize=(10, 6))
plt.plot(num_clients, times_create_topic, marker='o', label='Create Topic', color='blue')
plt.title('Throughput: Create Topic')
plt.xlabel('Number of Topics Created')
plt.ylabel('Time (seconds)')
plt.grid(True)
plt.legend()
plt.savefig('create_topic_throughput.png')  # Save the graph to a file
plt.show()

# Plot for send() operation
plt.figure(figsize=(10, 6))
plt.plot(num_clients, times_send_message, marker='o', label='Send Message', color='green')
plt.title('Throughput: Send Message')
plt.xlabel('Number of Messeges Sent')
plt.ylabel('Time (seconds)')
plt.grid(True)
plt.legend()
plt.savefig('send_message_throughput.png')  # Save the graph to a file
plt.show()

# Plot for pull() operation
plt.figure(figsize=(10, 6))
plt.plot(num_clients, times_pull_message, marker='o', label='Pull Message', color='red')
plt.title('Throughput: Pull Message')
plt.xlabel('Number of Messages Pulled')
plt.ylabel('Time (seconds)')
plt.grid(True)
plt.legend()
plt.savefig('pull_message_throughput.png')  # Save the graph to a file
plt.show()
