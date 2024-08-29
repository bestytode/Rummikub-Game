import time

class Timer:
    def __init__(self, limit):
        self.limit = limit  # Time limit for the timer in seconds
        self.start_time = None
        self.is_running = False

    def start(self):
        self.start_time = time.time()
        self.is_running = True

    def get_time_left(self):
        if not self.is_running:
            return 0
        elapsed = time.time() - self.start_time
        return max(0, self.limit - elapsed)

    def is_expired(self):
        return self.get_time_left() <= 0

    def reset(self):
        self.start_time = None
        self.is_running = False
    
    def expire_now(self):
        # Set the start time to the current time minus the limit
        self.start_time = time.time() - self.limit
        self.is_running = True