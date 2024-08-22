import subprocess
import os
import signal

class Subscriberhandler():
    def __init__(self):
        self.pids = []

    def create_subscriber(self, command):
        process = subprocess.Popen(command)
        self.pids.append(process.pid)

    def kill_subscriber(self, pid):
        try:
            os.kill(pid, signal.SIGTERM)
            self.pids.remove(pid)
            # print(f"[subhandler] Sent SIGTERM signal to process {pid}", flush=True)
        except OSError:
            print(f"[subhandler] Failed to send SIGTERM signal to process {pid}", flush=True)
