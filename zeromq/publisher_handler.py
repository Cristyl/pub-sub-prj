import subprocess
import os
import signal

class Publisherhandler():
    def __init__(self):
        self.pids = []

    def create_publisher(self, command):
        process = subprocess.Popen(command)
        self.pids.append(process.pid)

    def kill_publisher(self, pid):
        try:
            os.kill(pid, signal.SIGTERM)
            self.pids.remove(pid)
            # print(f"[pubhandler] Sent SIGTERM signal to process {pid}", flush=True)
        except OSError:
            print(f"[pubhandler] Failed to send SIGTERM signal to process {pid}", flush=True)
