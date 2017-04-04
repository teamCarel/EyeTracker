
class Global_Container(object):
    pass

def eyetracker():
    #printListeners()
    print("tracker started")
    import zmq
    import msgpack
    from time import sleep
    ctx = zmq.Context()
    # The requester talks to Pupil remote and receives the session unique IPC SUB PORT
    requester = ctx.socket(zmq.REQ)
    ip = '127.0.0.1' #If you talk to a different machine use its IP.
    port = 50020 #The port defaults to 50020 but can be set in the GUI of Pupil Capture.
    requester.connect('tcp://%s:%s'%(ip,port)) 
    sleep(5)
  

    notification = {'subject':'eye_process.should_start','eye_id' : 0}
    topic = 'notify.' + notification['subject']
    payload = msgpack.dumps(notification)
    requester.send_multipart((topic.encode(),payload))
    print (requester.recv())
    
    sleep(5)
    
    notification = {'subject':'show_eye_cam'}
    topic = 'notify.' + notification['subject']
    payload = msgpack.dumps(notification)
    requester.send_multipart((topic.encode(),payload))
    print (requester.recv())

    sleep(15)
    
    notification = {'subject':'calibration.should_start'}
    topic = 'notify.' + notification['subject']
    payload = msgpack.dumps(notification)
    requester.send_multipart((topic.encode(),payload))
    print (requester.recv())  
    
    sleep(30)
    
    requester.send(b'SUB_PORT')
    sub_port = requester.recv().decode()
    
    subscriber = ctx.socket(zmq.SUB)
    
    subscriber.connect('tcp://%s:%s'%(ip,sub_port)) 
    subscriber.set(zmq.SUBSCRIBE, b'gaze') #receive all notification messages
    #subscriber.set(zmq.SUBSCRIBE, b'pupil.0')
    i = 0
    while i<10:
        topic,payload = subscriber.recv_multipart()
        message = msgpack.loads(payload)
        print (topic,':',message)
        i=i+1
        sleep(10)
    
    notification = {'subject':'launcher_process.should_stop'}
    topic = 'notify.' + notification['subject']
    payload = msgpack.dumps(notification)
    requester.send_multipart((topic.encode(),payload))
    print (requester.recv())  


# 
#     while True:
#         notification = {'subject':'show_eye_cam'}
#         topic = 'notify.' + notification['subject']
#         payload = msgpack.dumps(notification)
#         requester.send_multipart((topic.encode(),payload))
#         print (requester.recv())
#         sleep(15)
def printListeners():
    import zmq, msgpack
    from zmq_tools import Msg_Receiver
    ctx = zmq.Context()
    url = 'tcp://127.0.0.1'

# open Pupil Remote socket
    requester = ctx.socket(zmq.REQ)
    requester.connect('%s:%s' % (url, 50020))
    requester.send(b'SUB_PORT')
    ipc_sub_port = requester.recv()

# setup message receiver
    sub_url = '%s:%s' % (url, ipc_sub_port)
    receiver = Msg_Receiver(ctx, sub_url.encode(), topics=(b'notify.meta.doc',))

# construct message
    topic = 'notify.meta.should_doc'
    payload = msgpack.dumps({'subject':'meta.should_doc'})
    requester.send_multipart([topic, payload])

# wait and print responses
    while True:
        topic, payload = receiver.recv()
        actor = payload.get('actor')
        doc = payload.get('doc')
        print ('%s: %s')%(actor,doc)
