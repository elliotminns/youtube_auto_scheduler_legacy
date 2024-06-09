import atexit
from queue_manager import load_queue, save_queue
from cli import cli_menu

if __name__ == "__main__":
    load_queue()
    atexit.register(save_queue)
    cli_menu()
