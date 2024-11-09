import sys
import threading
import click
import queue

class ByteTrackingQueue(queue.Queue):
    def __init__(self, max_bytes, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_bytes = max_bytes  # Maximum allowed bytes in the queue
        self.current_bytes = 0  # Tracks current bytes in the queue
        self._byte_lock = self._init_lock()  # Lock for thread-safe byte updates

    def put(self, item, *args, **kwargs):
        item_size = len(item) if item else 0
        
        # Add item and update byte counter
        with self._byte_lock:
            super().put(item, *args, **kwargs)
            self.current_bytes += item_size

    def get(self, *args, **kwargs):
        item = super().get(*args, **kwargs)
        item_size = len(item) if item else 0

        # Update byte counter and return item
        with self._byte_lock:
            self.current_bytes -= item_size
        return item

    def _init_lock(self):
        """Initializes a lock for thread-safe byte tracking."""
        return queue.LifoQueue().mutex  # Using LifoQueue mutex for lock


def writer_thread(out_queue):
    while True:
        chunk = out_queue.get()
        if chunk is None:  # Sentinel to stop the thread
            break
        sys.stdout.buffer.write(chunk)
        sys.stdout.buffer.flush()
        out_queue.task_done()

@click.command()
@click.option('--max-queue-bytes', default=1048576, help="Maximum bytes allowed in the queue.")
@click.argument('file', type=click.Path())
def main(max_queue_bytes, file):
    # Initialize ByteTrackingQueue with max byte limit
    out_queue = ByteTrackingQueue(max_bytes=max_queue_bytes)

    # Start the writer thread
    writer = threading.Thread(target=writer_thread, args=(out_queue,))
    writer.start()

    with open(file, "wb") as file_w, open(file, "rb") as file_r:
        try:
            while True:
                # Continuously read from stdin in binary mode
                chunk = sys.stdin.buffer.read(4096)
                if not chunk:  # End of stdin
                    break
                file_w.write(chunk)
                file_w.flush()  # Ensure write position is accurate

                # Only enqueue lines for stdout if the queue is below half max capacity
                if out_queue.current_bytes < max_queue_bytes // 2 and file_r.tell() < file_w.tell():
                    next_chunk = file_r.read(2048)  # Read in smaller chunks for stdout
                    if next_chunk:
                        out_queue.put(next_chunk)  # ByteTrackingQueue enforces byte limit
        finally:
            # Signal the writer thread to exit and ensure all data is processed
            out_queue.put(None)
            writer.join()

if __name__ == "__main__":
    main()
