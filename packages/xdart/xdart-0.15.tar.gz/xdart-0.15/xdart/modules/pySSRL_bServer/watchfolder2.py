import sys
import time
import logging
import watchdog.observers
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

watchdog.observers.inotify_buffer.InotifyBuffer.delay = 0
if __name__ == "__main__":
    #logging.basicConfig(filename='log.txt',
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    event_handler = LoggingEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()