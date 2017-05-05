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
        # save communication sockets urls
        self.ipc_push_url = ipc_push_url
        self.ipc_sub_url = ipc_sub_url

    def showEyeCam(self):
        ctx = zmq.Context()
        ipc_pub = zmq_tools.Msg_Dispatcher(ctx, self.ipc_push_url)
        ipc_pub.notify({'subject':'show_eye_cam'})
    
    def closeAll(self):
        ctx = zmq.Context()
        ipc_pub = zmq_tools.Msg_Dispatcher(ctx, self.ipc_push_url)
        ipc_pub.notify({'subject':'world_process.should_stop'})
    def calibrate(self):
        ctx = zmq.Context()
        ipc_pub = zmq_tools.Msg_Dispatcher(ctx, self.ipc_push_url)
        ipc_sub = zmq_tools.Msg_Receiver(ctx, self.ipc_sub_url, topics=('notify',))
        ipc_pub.notify({'subject':'calibration.should_start'})
        while True:
            while ipc_sub.new_data:
                topic,payload = ipc_sub.recv()
                if('calibration.failed' in topic):
                    return False
                elif('calibration.successful' in topic):
                    return True
                        
    def tileDetection(self,cols,rows):
        print("tile detect started")
        ctx = zmq.Context()
        ipc_sub = zmq_tools.Msg_Receiver(ctx, self.ipc_sub_url, topics=('gaze',))
        x_range_step = 1 / (cols - 1)
        y_range_step = 1 / (rows - 1)
        timestamp_old = 0
        tile_dict = {}
        for x in range(cols): 
            for y in range(rows): 
                tile_dict[str(x)+':'+str(y)]=set()
        sleep(1)#musi tu byt bez toho nefunguje
        while ipc_sub.new_data:
            while True:
                topic,payload = ipc_sub.recv()
                gaze_pos = payload['norm_pos']
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
                        arr = selected_tile.split(':')
                        return {'x':int(arr[0]),'y':rows-int(arr[1])}
                    tile_dict = tile_dict_new       
                #filter out errors
                if((gaze_pos[0] < 1) & (gaze_pos[1] < 1) & (gaze_pos[0] > 0) & (gaze_pos[1] > 0) & (confidence > conf_threshold)):
                    tile_x = floor(gaze_pos[0] / x_range_step)
                    tile_y = floor(gaze_pos[1] / y_range_step)
                    #add new timestamp to set
                    tile_dict[str(tile_x)+':'+str(tile_y)].add(timestamp_new)
                timestamp_old = timestamp_new
