import zmq
import sys
import signal
from time import time
from utils import create_topic, CONST

class Subscriber():
    def __init__(self):
        # setup signal handler for SIGTERM
        signal.signal(signal.SIGTERM, self.sigterm_handler)
        signal.signal(signal.SIGUSR1, self.sigusr1_handler)
    
        # prepare our context and subscriber
        self.ports = CONST.SUBS_PORT
        self.id_sub = sys.argv[1]
        self.binding_keys = create_topic('subscriber')
        self.elapsed = 0
        self.dict = {}
        self.lost_messages = 0

        context = zmq.Context()
        self.socket = context.socket(zmq.SUB)
        for port in self.ports:
            self.socket.connect(f"tcp://localhost:{port}")
        
        if not self.binding_keys:
            sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
            sys.exit(1)

        for binding_key in self.binding_keys:
            self.socket.setsockopt_string(zmq.SUBSCRIBE, binding_key)

        print(f'[sub #{self.id_sub}] Connected to {self.ports} ports and topics {self.binding_keys}. Waiting for logs', flush=True)

        self.file = open(f'latencies{self.id_sub}.txt', 'w')
        
        while not self.elapsed:
            message = self.socket.recv()
            topic, send_time, m, id_pub, counter = message.decode('utf-8').split(':')
            counter = int(counter)
            expected_message = self.dict.get((id_pub, topic), 0)
            arrival_time = int(time() * 1000) # in ms
            latency = arrival_time - int(send_time)
            self.file.write(str(latency) + '\n')
            
            if expected_message >= counter:
                continue

            elif counter - expected_message > 1 and expected_message != 0:
                print(f"[sub #{self.id_sub}] Lost a message", flush=True)
                self.lost_messages += counter - expected_message - 1

            self.dict[(id_pub, topic)] = counter
            print(f"[sub #{self.id_sub}] Got in {latency}ms: {m}", flush=True)

    def sigterm_handler(self, sig, frame):
        print(f"[sub #{self.id_sub}] Crashed", flush=True)
        self.file.close()
        with open(f'mess_lost{self.id_sub}.txt', 'w') as f:
            f.write(str(self.lost_messages))
        sys.exit(0)

    def sigusr1_handler(self, sig, frame):
        print(f"[sub #{self.id_sub}] Exited", flush=True)
        self.file.close()
        with open(f'mess_lost{self.id_sub}.txt', 'w') as f:
            f.write(str(self.lost_messages))
        self.socket.close()
        sys.exit(0)

Subscriber()