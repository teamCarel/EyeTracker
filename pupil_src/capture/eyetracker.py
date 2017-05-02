import zmq
import zmq_tools
import msgpack
import sys
from copy import deepcopy
from time import sleep
from math import floor
from multiprocessing import Process

watch_interval = 10
watch_threshold= 0.7
conf_threshold = 0.7

class Eyetracker():
    #TODO documentation

    def __init__(self,ipc_push_url,ipc_sub_url):#, user_dir):
        print("tracker started")
        ctx = zmq.Context()
        # create communication sockets
        self.ipc_push_url = ipc_push_url
        self.ipc_sub_url = ipc_sub_url
        #TODO user settigns directory?
        #self.user_dir = user_dir
        #dictionary for computed screen limits
        self.screen_limits = {'x_min' : sys.maxsize, 'x_max' : -sys.maxsize -1, 'y_min' : sys.maxsize, 'y_max' : -sys.maxsize -1, 'x_range': None, 'y_range': None}
       
    def showEyeCam(self):
        sleep(1)
        ctx = zmq.Context()
        ipc_pub = zmq_tools.Msg_Dispatcher(ctx, self.ipc_push_url)
        ipc_pub.notify({'subject':'show_eye_cam'})
    
    def closeAll(self):
        ctx = zmq.Context()
        ipc_pub = zmq_tools.Msg_Dispatcher(ctx, self.ipc_push_url)
        ipc_pub.notify({'subject':'show_eye_cam'})
        ipc_pub.notify({'subject':'eye_process.should_stop'}) 
        ipc_pub.notify({'subject':'launcher_process.should_stop'})
    def calibrate(self):
        sleep(5)
        ctx = zmq.Context()
        ipc_pub = zmq_tools.Msg_Dispatcher(ctx, self.ipc_push_url)
        ipc_sub = zmq_tools.Msg_Receiver(ctx, self.ipc_sub_url, topics=('notify',))
        ipc_pub.notify({'subject':'calibration.should_start'})
        while True:
            while ipc_sub.new_data:
                topic,payload = ipc_sub.recv()
                if('calibration.failed' in topic):
                    #reset x and y ranges to signalize failed calibration
                    self.screen_limits['x_range'] = None
                    self.screen_limits['y_range'] = None
                    return False
                elif('calibration.successful' in topic):
#                     self.screen_limits['x_range'] = self.screen_limits['x_max']-self.screen_limits['x_min']
#                     self.screen_limits['y_range'] = self.screen_limits['y_max']-self.screen_limits['y_min']
                    self.screen_limits['x_range'] = 1
                    self.screen_limits['y_range'] = 1
                    print("calib suc")
                    Process(target=self.tileDetection,name='tileDet',args=(3,2,)).start()
                    return True
#                 elif('gaze' in topic):
#                     #TODO test if b'... is needed
#                     gaze_pos = payload['norm_pos']
#                     print(gaze_pos)
#                     # recalibrate screen limits
#                     #if(gaze_pos[0] < 1 & gaze_pos[0] > 0 & gaze_pos[1] < 1  & gaze_pos[1] > 0):
#                     if((gaze_pos[0] < 1) & (gaze_pos[1] < 1) & (gaze_pos[0] > 0) & (gaze_pos[1] > 0)):
#                         self.screen_limits['x_min'] = min(gaze_pos[0],self.screen_limits['x_min'])
#                         self.screen_limits['y_min'] = min(gaze_pos[1],self.screen_limits['y_min'])
#                         self.screen_limits['x_max'] = max(gaze_pos[0],self.screen_limits['x_max'])
#                         self.screen_limits['y_max'] = max(gaze_pos[1],self.screen_limits['y_max'])
                        
    def tileDetection(self,cols,rows):
        sleep(5)
        print("tile")
        if( (self.screen_limits['x_range'] == None) | (self.screen_limits['y_range'] == None) ):
            print("error: not calibrated")
            return -1
        ctx = zmq.Context()
        ipc_sub = zmq_tools.Msg_Receiver(ctx, self.ipc_sub_url, topics=('gaze',))
        x_range_step = self.screen_limits['x_range'] / cols
        y_range_step = self.screen_limits['y_range'] / rows
        timestamp_old = 0
        tile_dict = {}
        for i in range(cols * rows): tile_dict[i]=set()
        print("dict created")
        sleep(5)#musi tu byt bez toho nefunguje
        while ipc_sub.new_data:
            print("data")
            while True:
                print("inner")
                topic,payload = ipc_sub.recv()
                #TODO test if b'... is needed
                gaze_pos = payload['norm_pos']
                print(gaze_pos)
                confidence = payload['confidence']
                timestamp_new = int(payload['timestamp'])
                if(timestamp_old == 0): timestamp_old = timestamp_new
                elif(timestamp_old != timestamp_new):
                    selected_tile = None
                    selected_len = 0;
                    tile_dict_new = deepcopy(tile_dict)
                    for i in tile_dict.keys():
                        for tile_timestamp in tile_dict[i]:
                            #remove old data from set
                            if(timestamp_new - tile_timestamp > watch_interval): tile_dict_new[i].remove(tile_timestamp)
                        if((len(tile_dict[i]) > watch_interval * watch_threshold) & (selected_len < len(tile_dict[i]))):
                            selected_tile = i
                            selected_len = len(tile_dict[i])
                    if(selected_tile != None): 
                        print("res",selected_tile)
                        return selected_tile   
                    tile_dict = tile_dict_new       
                #filter out errors
                #if((gaze_pos[0] < self.screen_limits['x_max']) & (gaze_pos[1] < self.screen_limits['y_max']) & (gaze_pos[0] > self.screen_limits['x_min']) & (gaze_pos[1] > self.screen_limits['y_min']) & (confidence > conf_threshold)):
                if((gaze_pos[0] < 1) & (gaze_pos[1] < 1) & (gaze_pos[0] > 0) & (gaze_pos[1] > 0) & (confidence > conf_threshold)):
#                     tile_x = floor((gaze_pos[0] - self.screen_limits['x_min']) / x_range_step)
#                     tile_y = floor((gaze_pos[1] - self.screen_limits['x_min']) / y_range_step)
                    tile_x = floor(gaze_pos[0] / x_range_step)
                    tile_y = floor(gaze_pos[1] / y_range_step)
                    #add new timestamp to set
                    print(tile_x+tile_y*cols)
                    tile_dict[tile_x+tile_y*cols].add(timestamp_new)
                timestamp_old = timestamp_new
#old function for testing
def eyetrackOld():  
    #printListeners()
    print("tracker started")
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
