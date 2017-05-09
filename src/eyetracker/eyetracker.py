from copy import deepcopy
from time import sleep
from math import floor

watch_interval = 10
watch_threshold = 0.7
conf_threshold = 0.7

def showEyeCam(self):
    import zmq
    import zmq_tools
    ctx = zmq.Context()
    ipc_pub = zmq_tools.Msg_Dispatcher(ctx, self.ipc_push_url)
    ipc_pub.notify({'subject':'show_eye_cam'})

class Eyetracker():
    #TODO documentation

    def __init__(self,ipc_push_url,ipc_sub_url):
        """
        ipc_push_url = PUSH url of pupil IPC backbone
        ipc_SUB_url = SUB url of pupil IPC backbone
        """
        # save communication sockets urls
        self.ipc_push_url = ipc_push_url
        self.ipc_sub_url = ipc_sub_url

    def showEyeCam(self):
        """
        Sends an IPC notification to show a window with eye camera view.
        """
        import zmq
        import zmq_tools
        ctx = zmq.Context()
        ipc_pub = zmq_tools.Msg_Dispatcher(ctx, self.ipc_push_url)
        ipc_pub.notify({'subject':'show_eye_cam'})
    
    def closeAll(self):
        """
        Sends an IPC notification to close pupil backend processes.
        """
        import zmq
        import zmq_tools
        ctx = zmq.Context()
        ipc_pub = zmq_tools.Msg_Dispatcher(ctx, self.ipc_push_url)
        ipc_pub.notify({'subject':'world_process.should_stop'})
        
    def calibrate(self):
        """
        Sends an IPC notification to start calibration.
        Blocks thread until calibration is finished and returns
        True when it finished successfully or
        False when it failed.
        """
        import zmq
        import zmq_tools
        ctx = zmq.Context()
        ipc_pub = zmq_tools.Msg_Dispatcher(ctx, self.ipc_push_url)
        ipc_sub = zmq_tools.Msg_Receiver(ctx, self.ipc_sub_url, topics=('notify.calibration',))
        ipc_pub.notify({'subject':'calibration.should_start'})
        while True:
            while ipc_sub.new_data:
                topic,payload = ipc_sub.recv()
                if('calibration.failed' in topic):
                    return False
                elif('calibration.successful' in topic):
                    return True
                        
    def tileDetection(self,rows,cols):
        """
        cols = columns of image grid
        rows = rows of image grid
        
        Starts detection of the tile user is looking at in the image grid.
        Reads gaze positions until at least watch_threshold * watch_interval
        seconds have beeen spent looking at a single tile. Discards all
        gaze positions with confidence smaller than conf_threshold.

        Returns a dictionary with x and y poisitons of the selected tile, starting at
        the top left corner with [0,0].
        """
        import zmq
        import zmq_tools
        ctx = zmq.Context()
        ipc_pub = zmq_tools.Msg_Dispatcher(ctx, self.ipc_push_url)
        ipc_sub = zmq_tools.Msg_Receiver(ctx, self.ipc_sub_url, topics=('gaze',))
        #wait for the socket
        sleep(1)
        #reset timestamps
        ipc_pub.notify({'subject':'T 0'})
        x_range_step = 1 / cols
        y_range_step = 1 / rows
        timestamp_old = 0
        tile_dict = {}
        for x in range(cols): 
            for y in range(rows): 
                tile_dict[str(x)+':'+str(y)]=set()
        #wait for the socket
        sleep(1)
        while ipc_sub.new_data:
            while True:
                topic,payload = ipc_sub.recv()
                gaze_pos = payload['norm_pos']
                confidence = payload['confidence']
                #print(gaze_pos," ",confidence)
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
                        print(selected_tile)
                        return {'x':int(arr[0]),'y':rows-int(arr[1])-1}
                        #return {'x':int(arr[0]),'y':cols-int(arr[1])}
                    tile_dict = tile_dict_new       
                #filter out errors
                if((gaze_pos[0] < 1) & (gaze_pos[1] < 1) & (gaze_pos[0] > 0) & (gaze_pos[1] > 0) & (confidence > conf_threshold)):
                    tile_x = floor(gaze_pos[0] / x_range_step)
                    tile_y = floor(gaze_pos[1] / y_range_step)
                   #print(tile_x," ",tile_y)
                    #add new timestamp to set
                    tile_dict[str(tile_x)+':'+str(tile_y)].add(timestamp_new)
                timestamp_old = timestamp_new
