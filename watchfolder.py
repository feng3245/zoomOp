import sys
import os
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

class Event(LoggingEventHandler):
    def dispatch(self, event):
        if 'randomfile' in event.src_path:
            if os.path.exists(event.src_path):
                waitTillReady(event.src_path, callbackf)
def callbackf(x):
    print(x)
def waitTillReady(fl, callback):
    with open(fl, 'r') as f:
        try:
            f.read()
        except:
            time.sleep(1000)
            waitTillReady(fl, callback)
    callback(fl)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    event_handler = Event()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
