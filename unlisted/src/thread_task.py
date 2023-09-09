import threading

class ThreadTask(object):
    """ Handles threads """
    def __init__(self, target_function, args):
        self.target_function = target_function
        self.args = args
        self.is_running = False
        self.thread = None

    def start(self):
        if not self.is_running:
            self.is_running = True
            self.thread = threading.Thread(target=self._run)
            self.thread.start()

    def stop(self):
        if self.is_running:
            self.is_running = False
            self.thread.join()  # Wait for the thread to finish

    def _run(self):
        self.target_function(
            *self.args
        )
