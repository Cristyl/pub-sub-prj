import zmq

class Subscriber():
    def __init__(self):
    
        # Prepare our context and publisher
        context    = zmq.Context(1)
        subscriber = context.socket(zmq.SUB)
        subscriber.connect("tcp://localhost:5563")
        subscriber.setsockopt(zmq.SUBSCRIBE, "B")
        
        while True:
            # Read envelope with address
            [address, contents] = subscriber.recv_multipart()
            print("[%s] %s\n" % (address, contents))
        
        # We never get here but clean up anyhow
        subscriber.close()
        context.term()