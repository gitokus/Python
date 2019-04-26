"""
-------------------- DAT2.0 MODULE -----------------------------------
This module implements classes of different types of signals used in DAT2.0. Each class has it's own function used for
synchronizing detections with vision.
"""

import numpy as np


class VFPSignal:
    """  Class for VFPState signals.
    Use get_synchronized to return dictionary of VFPState signals synchronized with vision """
    def __init__(self, mat):
        self.vehIndex = mat['mudp']['vfpState']['veh']['state']['veh_index']
        self.vehIndexUsed = mat['mudp']['vis']['vision_AEB_info']['visFunc']['vehIndexUsed']
        self.vfp_index = np.searchsorted(self.vehIndex, self.vehIndexUsed)

    def get_synchronized(self, signals_dict):
        out = {}
        for key, val in signals_dict.items():
            out[key] = val[self.vfp_index]
        return out

# TODO Fusion Class, Tracklet Class, Synchronize Side Radars
