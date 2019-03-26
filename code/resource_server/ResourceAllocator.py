# import logging
import time
from threading import Lock


class ResourceAllocator:

    def __init__(self, num_keys=34, time_window=900, window_limit=15):
        self._lock = Lock()
        self.val = None
        self.num_keys = num_keys
        self.timers = dict()
        self.time_window = time_window
        self.window_limit = window_limit

        for i in range(0, self.num_keys):
            self.timers[i] = [0, 0]

    def change_params(self, window_limit, time_window):
        self.time_window = time_window
        self.window_limit = window_limit

    def get_resource_index(self):
        """
        Returns index of the resource to use for making requests to get data
        if none of the resources are available, then send number of seconds until the resource is not available
        :return: Index resource if available otherwise time until none of the resources are available
        """
        result = -1
        max_sleep_time = self.time_window
        with self._lock:
            while result == -1:
                for i in range(0, self.num_keys):
                    curr_sleep_time = max((self.timers[i][0] + self.time_window) - time.time(), 0)

                    max_sleep_time = min(max_sleep_time, curr_sleep_time)

                    if self.timers[i][1] >= self.window_limit and self.timers[i][0] + self.time_window < time.time():
                        self.timers[i][0] = 0
                        self.timers[i][1] = 0

                    if self.timers[i][1] < self.window_limit:
                        result = i
                        break

                if result == -1:  # case when all streams are rate limited
                    # logging.warning('sleeping for %d seconds.' % max_sleep_time)
                    # time.sleep(max_sleep_time)
                    return -1 * max_sleep_time

            if self.timers[result][0] == 0:
                self.timers[result][0] = time.time()

            self.timers[result][1] += 1

            return result
