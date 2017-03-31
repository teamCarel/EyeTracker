
class Global_Container(object):
    pass

def eyetracker():
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
    
#     sleep(5)
#     
#     notification = {'subject':'set_detection_mapping_mode','eye_id' : 0}
#     topic = 'notify.' + notification['subject']
#     payload = msgpack.dumps(notification)
#     requester.send_multipart((topic.encode(),payload))
#     print (requester.recv())
    
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

    sleep(10)
    
    notification = {'subject':'calibration.should_start'}
    topic = 'notify.' + notification['subject']
    payload = msgpack.dumps(notification)
    requester.send_multipart((topic.encode(),payload))
    print (requester.recv())  
    
    sleep(1)
    
    requester.send(b'SUB_PORT')
    sub_port = requester.recv().decode()
    
    subscriber = ctx.socket(zmq.SUB)
    
    subscriber.connect('tcp://%s:%s'%(ip,sub_port)) 
    subscriber.set(zmq.SUBSCRIBE, b'gaze') #receive all notification messages


    while True:
        topic,payload = subscriber.recv_multipart()
        message = msgpack.loads(payload)
        print (topic,':',message)
        sleep(30)

# 
#     while True:
#         notification = {'subject':'show_eye_cam'}
#         topic = 'notify.' + notification['subject']
#         payload = msgpack.dumps(notification)
#         requester.send_multipart((topic.encode(),payload))
#         print (requester.recv())
#         sleep(15)
