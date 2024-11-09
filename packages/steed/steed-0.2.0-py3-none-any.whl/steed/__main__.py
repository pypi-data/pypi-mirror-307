import sys
import threading
import click
import queue
import os
import signal

class ByteTrackingQueue(queue.Queue):
    def __init__(self, max_bytes, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_bytes = max_bytes
        self.current_bytes = 0
        self._byte_lock = self._init_lock()

    def put(self, item, *args, **kwargs):
        item_size = len(item) if item else 0
        with self._byte_lock:
            super().put(item, *args, **kwargs)
            self.current_bytes += item_size

    def get(self, *args, **kwargs):
        item = super().get(*args, **kwargs)
        item_size = len(item) if item else 0
        with self._byte_lock:
            self.current_bytes -= item_size
        return item

    def _init_lock(self):
        return queue.LifoQueue().mutex

def writer_thread(out_queue):
    while True:
        chunk = out_queue.get()
        if chunk is None:
            break
        sys.stdout.buffer.write(chunk)
        sys.stdout.buffer.flush()
        out_queue.task_done()

@click.command()
@click.option("--unlink", '-u', is_flag = True, default = False, show_default = True, help="Unlink file on crash or terminate")
@click.option('--max-queue-bytes', default=1048576, help="Maximum bytes allowed in the queue.")
@click.argument('file', type=click.Path())
def main(unlink, max_queue_bytes, file):
    out_queue = ByteTrackingQueue(max_bytes=max_queue_bytes)
    writer = threading.Thread(target=writer_thread, args=(out_queue,))
    writer.start()

    # Define a flag for termination
    terminate_flag = {'terminate': False}

    def handle_termination(signum, frame):
        """Signal handler for termination signals."""
        terminate_flag['terminate'] = True
        print("\nReceived termination signal. Cleaning up...", file=sys.stderr)

    # Register signal handlers for SIGINT and SIGTERM
    signal.signal(signal.SIGINT, handle_termination)
    signal.signal(signal.SIGTERM, handle_termination)

    try:
        with open(file, "wb") as file_w, open(file, "rb") as file_r:
            while True:
                # Check for termination signal
                if terminate_flag['terminate']:
                    raise KeyboardInterrupt  # Force cleanup in finally

                # Continuously read from stdin in binary mode
                chunk = sys.stdin.buffer.read(4096)
                if not chunk:
                    break
                file_w.write(chunk)
                file_w.flush()

                # Enqueue data only if under max capacity
                if out_queue.current_bytes < max_queue_bytes // 2 and file_r.tell() < file_w.tell():
                    next_chunk = file_r.read(2048)
                    if next_chunk:
                        out_queue.put(next_chunk)
    except (Exception, KeyboardInterrupt):
        # If an error occurs or interrupted, delete the file
        if os.path.exists(file) and unlink:
            os.unlink(file)
    finally:
        # Ensure the writer thread exits
        out_queue.put(None)
        writer.join()

if __name__ == "__main__":
    main()
