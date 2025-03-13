import sys
import threading
import time


class Spinner:
    def __init__(self, message="Loading"):
        self.message = message
        self.spinning = False
        self.spinner_chars = ["/", "-", "\\", "|"]
        self.spinner_thread = None

    def spin(self):
        i = 0
        while self.spinning:
            sys.stdout.write(
                f"\r{self.message} {self.spinner_chars[i % len(self.spinner_chars)]}")
            sys.stdout.flush()
            time.sleep(0.1)
            i += 1

    def start(self):
        self.spinning = True
        self.spinner_thread = threading.Thread(target=self.spin)
        self.spinner_thread.daemon = True
        self.spinner_thread.start()

    def stop(self):
        self.spinning = False
        if self.spinner_thread:
            self.spinner_thread.join()
        # Clear the line
        sys.stdout.write("\r" + " " * (len(self.message) + 2) + "\r")
        sys.stdout.flush()
