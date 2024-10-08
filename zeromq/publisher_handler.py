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
            self.pids[self.pids.index(pid)] = None
            # print(f"[pubhandler] Sent SIGTERM signal to process {pid}", flush=True)
        except OSError:
            print(f"[pubhandler] Failed to send SIGTERM signal to process {pid}", flush=True)
    
    def close_publisher(self, pid):
        try:
            os.kill(pid, signal.SIGUSR1)
            self.pids[self.pids.index(pid)] = None
            # print(f"[pubhandler] Sent SIGURS1 signal to process {pid}", flush=True)
        except OSError:
            print(f"[pubhandler] Failed to send SIGUSR1 signal to process {pid}", flush=True)
