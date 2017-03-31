'''
(*)~---------------------------------------------------------------------------
Pupil - eye tracking platform
Copyright (C) 2012-2017  Pupil Labs

Distributed under the terms of the GNU
Lesser General Public License (LGPL v3.0).
See COPYING and COPYING.LESSER for license details.
---------------------------------------------------------------------------~(*)
'''


# import detector classes from sibling files
from . screen_marker_calibration import Screen_Marker_Calibration
from . adjust_calibration import Adjust_Calibration
from . gaze_mappers import Dummy_Gaze_Mapper, Monocular_Gaze_Mapper, Binocular_Gaze_Mapper,Vector_Gaze_Mapper,Binocular_Vector_Gaze_Mapper,Dual_Monocular_Gaze_Mapper
