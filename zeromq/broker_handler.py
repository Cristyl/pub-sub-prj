import subprocess
import os
import signal


class Brokerhandler():
    def __init__(self):
        self.pids = []

    def create_broker(self, command):
        process = subprocess.Popen(command)
        self.pids.append(process.pid)

    def kill_broker(self, pid):
        try:
            os.kill(pid, signal.SIGTERM)
            self.pids[self.pids.index(pid)] = None
            # print(f"[brokerhandler] Sent SIGTERM signal to process {pid}", flush=True)
        except OSError:
            print(f"[brokerhandler] Failed to send SIGTERM signal to process {pid}", flush=True)
    
    def close_broker(self, pid):
        try:
            os.kill(pid, signal.SIGUSR1)
            self.pids[self.pids.index(pid)] = None
            # print(f"[brokerhandler] Sent SIGURS1 signal to process {pid}", flush=True)
        except OSError:
            print(f"[brokerhandler] Failed to send SIGUSR1 signal to process {pid}", flush=True)
