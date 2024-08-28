import subprocess
import os
import signal


class Brokerhandler():
    def __init__(self):
        self.pid = None

    def create_broker(self, command):
        process = subprocess.Popen(command)
        self.pid = process.pid

    def kill_broker(self):
        try:
            os.kill(self.pid, signal.SIGTERM)
            # print(f"[brokerhandler] Sent SIGTERM signal to process {pid}", flush=True)
        except OSError:
            print(f"[brokerhandler] Failed to send SIGTERM signal to process {self.pid}", flush=True)
