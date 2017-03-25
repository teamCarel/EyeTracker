
class Global_Container(object):
    pass

def eyetracker(g_pool):
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
    
    args={'name':'test','frame_size':(1920,1080),'frame_rate' : 30}
    notification = {'subject':'start_plugin','name' : 'Fake_Source','args':args}
    topic = 'notify.' + notification['subject']
    payload = msgpack.dumps(notification)
    requester.send_multipart((topic.encode(),payload))
    print (requester.recv())
       
    sleep(1)
    
    notification = {'subject':'start_plugin','name' : 'Dummy_Gaze_Mapper'}
    topic = 'notify.' + notification['subject']
    payload = msgpack.dumps(notification)
    requester.send_multipart((topic.encode(),payload))
    print (requester.recv())
     
    notification = {'subject':'start_plugin','name' : 'Screen_Marker_Calibration'}
    topic = 'notify.' + notification['subject']
    payload = msgpack.dumps(notification)
    requester.send_multipart((topic.encode(),payload))
    print (requester.recv())  
    
    notification = {'subject':'calibration.should_start'}
    topic = 'notify.' + notification['subject']
    payload = msgpack.dumps(notification)
    requester.send_multipart((topic.encode(),payload))
    print (requester.recv())
    
    #eyetracker2(g_pool)

def eyetracker2(g_pool):
    import zmq, msgpack
    from time import sleep
    from zmq_tools import Msg_Receiver
    ctx = zmq.Context()
    url = 'tcp://127.0.0.1'
    
    # open Pupil Remote socket
    requester = ctx.socket(zmq.REQ)
    requester.connect('%s:%s'%(url,50020))
    requester.send(b'SUB_PORT')
    ipc_sub_port = requester.recv().decode()
    
    # setup message receiver
    sub_url = ('%s:%s')%(url,ipc_sub_port)
    receiver = Msg_Receiver(ctx,sub_url,topics=(b'notify.meta.doc',))    
    
    # construct message
    topic = b'notify.start_plugin'
    payload = msgpack.dumps({'subject':'start_plugin','name':'Screen_Marker_Calibration'})
    requester.send_multipart([topic,payload])
    receiver.recv()
    sleep(1)
    
    # wait and print responses
    # construct message
    topic = b'notify.meta.should_doc'
    payload = msgpack.dumps({'subject':'meta.should_doc'})
    requester.send_multipart([topic,payload])
    

    while True:
        topic, payload = receiver.recv()
        actor = payload.get('actor')
        doc = payload.get('doc')
        print ('%s:%s'%(actor,doc))
