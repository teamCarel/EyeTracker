
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
     
    sleep(10)
    
#     notification = {'subject':'start_plugin','name' : 'Manual_Marker_Calibration'}
#     topic = 'notify.' + notification['subject']
#     payload = msgpack.dumps(notification)
#     requester.send_multipart((topic.encode(),payload))
#     print (requester.recv())
#      
#     sleep(10)
    
    notification = {'subject':'calibration.should_start'}
    topic = 'notify.' + notification['subject']
    payload = msgpack.dumps(notification)
    requester.send_multipart((topic.encode(),payload))
    print (requester.recv())