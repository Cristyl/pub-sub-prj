import subprocess
import os
import signal

class Publisherhandler():
    def __init__(self, number_of_publishers, exchange_names):
        self.number_of_publishers = number_of_publishers
        self.exchange_names = exchange_names

    def create_publisher(self, command, pids):
        process = subprocess.Popen(command)
        pids.append(process.pid)

    def kill_publisher(self, pid, pids):
        try:
            os.kill(pid, signal.SIGTERM)
            pids.remove(pid)
            # print(f"[pubhandler] Sent SIGTERM signal to process {pid}", flush=True)
        except OSError:
            print(f"[pubhandler] Failed to send SIGTERM signal to process {pid}", flush=True)
