import sys,os
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
shared_modules_base=os.path.join(os.path.abspath(__file__).rsplit('/', 1)[0], 'src', 'shared_modules')
capture_base=os.path.join(os.path.abspath(__file__).rsplit('/', 1)[0], 'src', 'capture')
eyetracker_base=os.path.join(os.path.abspath(__file__).rsplit('/', 1)[0], 'src', 'eyetracker')
print(os.path.join(os.path.abspath(__file__), 'src', 'shared_modules'))

sys.path.append(shared_modules_base)
sys.path.append(os.path.join(shared_modules_base, 'gl_utils'))
sys.path.append(os.path.join(shared_modules_base, 'calibration_routines'))
sys.path.append(os.path.join(shared_modules_base, 'calibration_routines', 'optimization_calibration'))
sys.path.append(os.path.join(shared_modules_base, 'math_helper'))
sys.path.append(os.path.join(shared_modules_base, 'video_capture'))

sys.path.append(eyetracker_base)
sys.path.append(os.path.join(eyetracker_base, 'GUI'))

sys.path.append(capture_base)
sys.path.append(os.path.join(capture_base, 'pupil_detectors'))
build_exe_options = {"packages": ["os", "multiprocessing", "glfw", "OpenGL", "numpy"], "excludes": ["tkinter"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "eyetracker",
        version = "0.1",
        description ="Application for eyetracking.",
        options = {"build_exe": build_exe_options},
        executables = [Executable("./src/capture/main.py", base=base)])