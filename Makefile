.PHONY: all clean run test benchmark ping-pong start_server stop_server

# Define the Python interpreter to use
PYTHON = /usr/bin/python3

# Define the server script
SERVER_SCRIPT = server.py

# Define the test scripts
MAIN_PROGRAM = Main_menu.py
BENCHMARK_CREATE_TOPIC = benchmark_create_topic.py
BENCHMARK_SEND_MESSAGE = benchmark_send_message.py
BENCHMARK_PULL_MESSAGE = benchmarkpullsub.py
BENCHMARK_REGISTER_PUBLISHER = benchmarkregisterpub.py
BENCHMARK_REGISTER_SUBSCRIBER = benchmarkregsub.py
BENCHMARK_DELETE_TOPIC = benchmarkdeltopic.py
BENCHMARK_SUBSCRIBE = benchmarksubsub.py
PING_PONG_TEST = ping_pong_test.py

# Default rule
all: main_program run_benchmarks

# Store server process ID to allow clean shutdown
SERVER_PID_FILE = server.pid

# Rule to start the server
start_server:
		@echo "Starting the server..."
		$(PYTHON) $(SERVER_SCRIPT) & echo $$! > $(SERVER_PID_FILE)
		sleep 3  # Allow server time to initialize

# Rule to stop the server
stop_server:
	@if [ -f $(SERVER_PID_FILE) ]; then \
		kill `cat $(SERVER_PID_FILE)` && rm $(SERVER_PID_FILE); \
		echo "Server stopped."; \
	else \
		echo "No server running."; \
	fi

# Rule to Main Menu Program
main_program: start_server
		@echo  "Running Main Menu Program..."
		$(PYTHON) $(MAIN_PROGRAM)

# Rule to run all benchmarks
run_benchmarks: start_server
		@echo "Running create topic benchmark..."
		$(PYTHON) $(BENCHMARK_CREATE_TOPIC)

		@echo "Running send message benchmark..."
		$(PYTHON) $(BENCHMARK_SEND_MESSAGE)

		@echo "Running pull message benchmark..."
		$(PYTHON) $(BENCHMARK_PULL_MESSAGE)

		@echo "Running register publisher benchmark..."
		$(PYTHON) $(BENCHMARK_REGISTER_PUBLISHER)

		@echo "Running register subscriber benchmark..."
		$(PYTHON) $(BENCHMARK_REGISTER_SUBSCRIBER)

		@echo "Running delete topic benchmark..."
		$(PYTHON) $(BENCHMARK_DELETE_TOPIC)

		@echo "Running subscribe benchmark..."
		$(PYTHON) $(BENCHMARK_SUBSCRIBE)

		@echo "Running ping pong test..."
		$(PYTHON) $(PING_PONG_TEST)

	$(MAKE) stop_server  # Stop the server after running benchmarks

# Clean up rule to stop the server and clean up files
clean:
	@echo "Cleaning up..."
	$(MAKE) stop_server  # Stop the server if it's running
	rm -f *.pyc
	rm -rf __pycache__


