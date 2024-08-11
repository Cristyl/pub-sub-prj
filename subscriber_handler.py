import subprocess
import os
import signal

class Subscriberhandler():
    def __init__(self, number_of_subscribers, exchange_names):
        self.number_of_subscribers = number_of_subscribers
        self.exchange_names = exchange_names

    def create_subscriber(self, command, pids):
        process = subprocess.Popen(command)
        pids.append(process.pid)

    def kill_subscriber(self, pid, pids):
        try:
            os.kill(pid, signal.SIGTERM)
            pids.remove(pid)
            # print(f"[subhandler] Sent SIGTERM signal to process {pid}", flush=True)
        except OSError:
            print(f"[subhandler] Failed to send SIGTERM signal to process {pid}", flush=True)
        
        