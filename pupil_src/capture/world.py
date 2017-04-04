'''
(*)~---------------------------------------------------------------------------
Pupil - eye tracking platform
Copyright (C) 2012-2017  Pupil Labs

Distributed under the terms of the GNU
Lesser General Public License (LGPL v3.0).
See COPYING and COPYING.LESSER for license details.
---------------------------------------------------------------------------~(*)
'''
import os
import platform


class Global_Container(object):
    pass


def world(timebase, eyes_are_alive, ipc_pub_url, ipc_sub_url,
          ipc_push_url, user_dir, version):
    """Reads world video and runs plugins.

    Creates a window, gl context.
    Grabs images from a capture.
    Maps pupil to gaze data
    Can run various plug-ins.

    Reacts to notifications:
        ``set_detection_mapping_mode``
        ``eye_process.started``
        ``start_plugin``

    Emits notifications:
        ``eye_process.should_start``
        ``eye_process.should_stop``
        ``set_detection_mapping_mode``
        ``world_process.started``
        ``world_process.stopped``
        ``recording.should_stop``: Emits on camera failure
        ``launcher_process.should_stop``

    Emits data:
        ``gaze``: Gaze data from current gaze mapping plugin.``
        ``*``: any other plugin generated data in the events
               that it not [dt,pupil,gaze].
    """

    # We defer the imports because of multiprocessing.
    # Otherwise the world process each process also loads the other imports.
    # This is not harmful but unnecessary.

    # general imports
    import logging

    # networking
    import zmq
    import zmq_tools

    # zmq ipc setup
    zmq_ctx = zmq.Context()
    ipc_pub = zmq_tools.Msg_Dispatcher(zmq_ctx, ipc_push_url)
    notify_sub = zmq_tools.Msg_Receiver(zmq_ctx, ipc_sub_url, topics=('notify',))

    # log setup
    logging.getLogger("OpenGL").setLevel(logging.ERROR)
    logger = logging.getLogger()
    logger.handlers = []
    logger.setLevel(logging.INFO)
    logger.addHandler(zmq_tools.ZMQ_handler(zmq_ctx, ipc_push_url))
    # create logger for the context of this function
    logger = logging.getLogger(__name__)

    # display
    import glfw
    from pyglui import cygl, __version__ as pyglui_version
    assert pyglui_version >= '1.2'
    import gl_utils

    # helpers/utils
    from methods import delta_t, get_system_info, timer
    from uvc import get_time_monotonic
    logger.info('Application Version: {}'.format(version))
    logger.info('System Info: {}'.format(get_system_info()))

    # trigger pupil detector cpp build:
    import pupil_detectors
    del pupil_detectors

    # Plug-ins
    from plugin import Plugin, Plugin_List
    # Calibration
    from calibration_routines.screen_marker_calibration import Screen_Marker_Calibration as Calibration_Plugin
    # Gaze mapping #TODO: Change to Monocular?
    from calibration_routines.gaze_mappers import Dummy_Gaze_Mapper as Gaze_Mapper_Plugin
    # Video Source #TODO: change to UVC
    from video_capture.uvc_backend import UVC_Source as Video_Source_Plugin
    # Fixation detector #TODO: needed?
    #from fixation_detector import Fixation_Detector_2D
    from pupil_remote import Pupil_Remote
    #from pupil_groups import Pupil_Groups
    #from surface_tracker import Surface_Tracker

    #from frame_publisher import Frame_Publisher
    from blink_detection import Blink_Detection
    from pupil_data_relay import Pupil_Data_Relay

    # g_pool holds variables for this process they are accesible to all plugins
    g_pool = Global_Container()
    g_pool.app = 'capture'
    g_pool.process = 'world'
    g_pool.user_dir = user_dir
    g_pool.version = version
    g_pool.timebase = timebase
    g_pool.zmq_ctx = zmq_ctx
    g_pool.ipc_pub = ipc_pub
    g_pool.ipc_pub_url = ipc_pub_url
    g_pool.ipc_sub_url = ipc_sub_url
    g_pool.ipc_push_url = ipc_push_url
    g_pool.eyes_are_alive = eyes_are_alive

    def get_timestamp():
        return get_time_monotonic() - g_pool.timebase.value
    g_pool.get_timestamp = get_timestamp
    g_pool.get_now = get_time_monotonic

    # manage plugins
    plugin_by_index = [Gaze_Mapper_Plugin,Calibration_Plugin,Video_Source_Plugin,Pupil_Data_Relay,Pupil_Remote, Blink_Detection]
    name_by_index = [p.__name__ for p in plugin_by_index]
    plugin_by_name = dict(zip(name_by_index, plugin_by_index))

    default_capture_settings = {
        'preferred_names': ["Pupil Cam1 ID2"],
        'frame_size': (1280, 720),
        'frame_rate': 30
    }
 
    default_plugins = [("UVC_Source", default_capture_settings),
                       ('Pupil_Data_Relay', {}),
                       ('UVC_Manager', {}),
                       ('Dummy_Gaze_Mapper', {}),
                       ('Screen_Marker_Calibration', {}),
                       ('Pupil_Remote', {}),
                       ('Fixation_Detector_3D', {})]

    tick = delta_t()

    def get_dt():
        return next(tick)

    g_pool.detection_mapping_mode = '2d'
    g_pool.active_gaze_mapping_plugin = Gaze_Mapper_Plugin(g_pool)

    def launch_eye_process(eye_id, delay=0):
        n = {'subject': 'eye_process.should_start.{}'.format(eye_id),
             'eye_id': eye_id, 'delay': delay}
        ipc_pub.notify(n)

    def stop_eye_process(eye_id):
        n = {'subject': 'eye_process.should_stop', 'eye_id': eye_id}
        ipc_pub.notify(n)

    def start_stop_eye(eye_id, make_alive):
        if make_alive:
            launch_eye_process(eye_id)
        else:
            stop_eye_process(eye_id)

    def handle_notifications(n):
        subject = n['subject']
        if subject == 'set_detection_mapping_mode':
            if n['mode'] == '2d':
                if ("Vector_Gaze_Mapper" in
                        g_pool.active_gaze_mapping_plugin.class_name):
                    logger.warning("The gaze mapper is not supported in 2d mode. Please recalibrate.")
                    g_pool.plugins.add(plugin_by_name['Dummy_Gaze_Mapper'])
            g_pool.detection_mapping_mode = n['mode']
        elif subject == 'start_plugin':
            g_pool.plugins.add(
                plugin_by_name[n['name']], args=n.get('args', {}))
        elif subject == 'eye_process.started':
            n = {'subject': 'set_detection_mapping_mode',
                 'mode': g_pool.detection_mapping_mode}
            ipc_pub.notify(n)
        elif subject.startswith('meta.should_doc'):
            ipc_pub.notify({'subject': 'meta.doc',
                            'actor': g_pool.app,
                            'doc': world.__doc__})
            for p in g_pool.plugins:
                if (p.on_notify.__doc__
                        and p.__class__.on_notify != Plugin.on_notify):
                    ipc_pub.notify({'subject': 'meta.doc',
                                    'actor': p.class_name,
                                    'doc': p.on_notify.__doc__})

    # window and gl setup
    glfw.glfwInit()
    main_window = glfw.glfwCreateWindow(1, 1, "Pupil Backend")
    glfw.glfwSetWindowPos(main_window, -1, -1)
    glfw.glfwMakeContextCurrent(main_window)
    cygl.utils.init()
    g_pool.main_window = main_window

    # plugins that are loaded based on user settings from previous session
    g_pool.plugins = Plugin_List(g_pool, plugin_by_name, default_plugins)

    # gl_state settings
    gl_utils.basic_gl_setup()

    # create a timer to control window update frequency
    window_update_timer = timer(1 / 60)
    def window_should_update():
        return next(window_update_timer)

    #hide window
    glfw.glfwHideWindow(main_window)
    ipc_pub.notify({'subject': 'world_process.started'})
    logger.warning('Process started.')


    # Event loop
    while not glfw.glfwWindowShouldClose(main_window):

        # fetch newest notifications
        new_notifications = []
        while notify_sub.new_data:
            t, n = notify_sub.recv()
            new_notifications.append(n)

        # notify each plugin if there are new notifications:
        for n in new_notifications:
            handle_notifications(n)
            for p in g_pool.plugins:
                p.on_notify(n)


        #a dictionary that allows plugins to post and read events
        events = {}
        # report time between now and the last loop interation
        events['dt'] = get_dt()

        # allow each Plugin to do its work.
        for p in g_pool.plugins:
            p.recent_events(events)

        # check if a plugin need to be destroyed
        g_pool.plugins.clean()

        # send new events to ipc:
        if 'pupil_positions' in events:
            del events['pupil_positions']  # already on the wire
        if 'gaze_positions' in events:   
            del events['gaze_positions']  # sent earlier
        if 'frame' in events:
            del events['frame']  #send explicity with frame publisher
        del events['dt']  #no need to send this
        for topic, data in events.items():
            assert(isinstance(data, (list, tuple)))
            for d in data:
                ipc_pub.send(topic, d)

        glfw.glfwMakeContextCurrent(main_window)
        # render visual feedback from loaded plugins
        if window_should_update() and gl_utils.is_window_visible(main_window):
            g_pool.capture.gl_display()
            for p in g_pool.plugins:
                p.gl_display()
            #g_pool.gui.update()
            glfw.glfwSwapBuffers(main_window)
        glfw.glfwPollEvents()

    glfw.glfwRestoreWindow(main_window)  # need to do this for windows os

    # de-init all running plugins
    for p in g_pool.plugins:
        p.alive = False
    g_pool.plugins.clean()
    g_pool.gui.terminate()
    glfw.glfwDestroyWindow(main_window)
    glfw.glfwTerminate()

    g_pool.capture.deinit_gui()

    # shut down eye processes:
    stop_eye_process(0)
    stop_eye_process(1)

    logger.info("Process shutting down.")
    ipc_pub.notify({'subject': 'world_process.stopped'})

    # shut down launcher
    n = {'subject': 'launcher_process.should_stop'}
    ipc_pub.notify(n)
    zmq_ctx.destroy()