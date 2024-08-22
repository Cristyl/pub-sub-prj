import subprocess
import os
import signal


class Brokerhandler():
    def __init__(self):
        self.pub_port = '5560'
        self.sub_port = '5559'
        self.pid = None

    def create_broker(self, command):
        process = subprocess.Popen(command)
        self.pid = process.pid

    def kill_broker(self):
        try:
            os.kill(self.pid, signal.SIGTERM)
            self.pid = None
            # print(f"[pubhandler] Sent SIGTERM signal to process {pid}", flush=True)
        except OSError:
            print(f"[brokerhandler] Failed to send SIGTERM signal to process {self.pid}", flush=True)
