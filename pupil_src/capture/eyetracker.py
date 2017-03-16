
class Global_Container(object):
    pass

def eyetracker(ipc_sub_url):
    print("tracker started")
     # we need a serialiser 
    import msgpack as serializer
    import zmq
    import time
    ctx = zmq.Context()
    subscriber = ctx.socket(zmq.SUB)
    subscriber.connect(ipc_sub_url)
    #subscriber.set(zmq.SUBSCRIBE, 'notify.') #receive all notification messages
    #subscriber.set(zmq.SUBSCRIBE, 'logging.error') #receive logging error messages
    subscriber.set(zmq.SUBSCRIBE, b"gaze") #receive eye info
    #subscriber.set(zmq.SUBSCRIBE, '') #receive everything (don't do this)
    # you can setup multiple subscriber sockets
    # Sockets can be polled or read in different threads.
    while True:
        topic,payload = subscriber.recv_multipart()
        message = serializer.unpackb(payload, use_list=True)
        print(message[b'norm_pos'])
        time.sleep(10)