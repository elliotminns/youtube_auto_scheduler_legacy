import threading
from cli import cli_menu
from schedule import start_scheduler

def main():
    # Load the queue from file
    from queue_manager import load_queue
    load_queue()

    # Start the scheduler in a new thread
    scheduler_thread = threading.Thread(target=start_scheduler)
    scheduler_thread.daemon = True  # This ensures the thread will exit when the main program exits
    scheduler_thread.start()
    print("Starting Scheduler...")

    # Run the CLI menu
    cli_menu()

if __name__ == "__main__":
    main()
