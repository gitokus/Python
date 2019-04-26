import delphiTools3.base as dtb
import numpy as np
import pandas as pd
import glob
import os

class FusSignal:
    """ Class to be used for Fusion Signals.
    use get_synchronized to return dictionary of synchronized fusion signals"""
    def __init__(self, mat):
        self.imageIndex = mat['mudp']['vis']['vision_obstacles_info']['imageIndex'].astype('int32')
        self.grabIndex = mat['mudp']['tsel']['commonETSELInfo']['grab_index'].astype('int32')
        self.combined = np.empty((len(self.imageIndex,), 2))
        self._synchronize()

    def _synchronize(self):
        # Find indices of fusIndexes that match visIndexes. Return both indexes in one matrix=[fusIndx, VisIndx]
        if self.imageIndex[-1] < self.imageIndex[0]:
            # Create temp variables to avoid need to changing imageIndex and grabIndex matrixes
            temp_image_index, temp_grab_index = np.copy(self.imageIndex), np.copy(self.grabIndex)
            temp_image_index[np.argwhere(self.imageIndex == 1)[0][0]:, ] += 65535
            temp_grab_index[np.argwhere(self.grabIndex ==1)[0][0]:, ] += 65535

            # Some mats have larger last GrabIndex than last ImageIndex. Not the prettiest way to deal with
            # it but it works...
            if self.imageIndex[-1] > self.grabIndex[-1]:
                self.matchingIdx = np.searchsorted(temp_grab_index, temp_image_index)[:-1]
                self.combined = np.stack([self.matchingIdx, np.arange(len(self.imageIndex[:-1]))], axis=1)
            else:
                self.matchingIdx = np.searchsorted(temp_grab_index, temp_image_index)
                self.combined = np.stack([self.matchingIdx, np.arange(len(self.imageIndex))], axis=1)
        else:
            if self.imageIndex[-1] > self.grabIndex[-1]:
                self.matchingIdx = np.searchsorted(self.grabIndex, self.imageIndex)[:-1]
                self.combined = np.stack([self.matchingIdx, np.arange(len(self.imageIndex[:-1]))], axis=1)
            else:
                self.matchingIdx = np.searchsorted(self.grabIndex, self.imageIndex)
                self.combined = np.stack([self.matchingIdx, np.arange(len(self.imageIndex))], axis=1)

    def get_synchronized(self, signals_dict):
        fus, vis = np.transpose(self.combined)
        out = {}
        fus[fus>=917] = 915  # If fusion logging stopped before vis logging add a line similar to this
        for key, val in signals_dict.items():
            out[key] = val[fus]
        return out


class Path(FusSignal):
    def __init__(self, mat):
        super().__init__(mat)
        # self.signals = signal.FusSignal(mat)
        self.mat = mat
        self.path_signals = {
            'offset': mat['mudp']['tsel']['commonETSELInfo']['predictedPath']['predicted_path_lane_center_offset'],
            'angle': mat['mudp']['tsel']['commonETSELInfo']['predictedPath']['predicted_path_coef_k'],
            'c0': mat['mudp']['tsel']['commonETSELInfo']['predictedPath']['predicted_path_coef_c0'],
            'c1': mat['mudp']['tsel']['commonETSELInfo']['predictedPath']['predicted_path_coef_c1']}
        self.synchronize()

    def synchronize(self):
       return super().get_synchronized(self.path_signals)

    def get_path(self, frame=None, grab_index=None, path_range=np.arange(0, 50, 0.5)):
        """ Get path at desired frame (or grab_index). Path range can be either list of values (e.g. np.arange) or
        one value. Default path range is 50 meters"""
        if grab_index:
            frame = np.argwhere(self.image_index == grab_index)[0][0]
        fus_index = self.combined[frame, 0]

        # Get path coefficients
        a0 = self.path_signals['offset'][fus_index]  # Lateral offset
        a1 = np.tan(self.path_signals['angle'][fus_index])  # heading angle
        a2 = self.path_signals['c0'][fus_index] / 2
        a3 = self.path_signals['c1'][fus_index] / 6

        # Calculate path as 3rd order polynomial
        path_poly = a0 + a1 * path_range + a2 * np.power(path_range, 2) + a3 * np.power(path_range, 3)
        path_poly = np.negative(path_poly)
        if not isinstance(path_range, (np.ndarray, list)):
            # If range is single number return only path's value at one point
            return path_poly
        else:
            return path_range, path_poly  # X=path_range, Y=path_polynomial

    def get_distance_from_path(self, target_ID, frame=None, grab_index=None):
        """ Get the distance between centerline of path and target. Bear in mind that target_ID in mat starts at 0"""
        if grab_index:
            frame = np.argwhere(self.image_index == grab_index)[0][0]
        lat_pos = self.mat['mudp']['vis']['vision_obstacles_info']['visObs']['lat_pos'][frame, target_ID]
        long_pos = self.mat['mudp']['vis']['vision_obstacles_info']['visObs']['long_pos'][frame, target_ID]
        path_value = self.get_path(frame, path_range=long_pos)  # get the value of path at VRU's long_pos
        distance = -lat_pos - path_value  # Positions are reported in coordinate system with opposite signs
        return long_pos, distance


class VFPSignal:
    """  Class for VFPState signals.
    Use get_synchronized to return dictionary of VFPState signals synchronized with vision """
    def __init__(self, mat):
        self.vehIndex = mat['mudp']['vfpState']['cmd_msg']['veh_state_info']['vehIndex']
        self.vehIndexUsed = mat['mudp']['vis']['vision_obstacles_info']['vehIndexUsed']
        self.vfp_index = np.empty((len(self.vehIndexUsed),1))
        self._synchronize()

    def _synchronize(self):
        self.vfp_index = np.searchsorted(self.vehIndex, self.vehIndexUsed)

    def get_synchronized(self, signals_dict):
        out = {}
        for key, val in signals_dict.items():
            out[key] = val[self.vfp_index]
        return out


class TrackletSignal:
    """ Class for synchronizing tracklet detections"""
    def __init__(self, mat):
        self.lookIndex = mat['mudp']['tlet']['tracker_outputs']['tracklet_reports']['look_index'].astype('int32')
        self.grabIndex = mat['mudp']['tsel']['commonETSELInfo']['grab_index'].astype('int32')
        self.tlet_numbers = mat['mudp']['tlet']['tracker_outputs']['tracklet_reports']['tracklets']['gid']
        self.imageIndex = mat['mudp']['vis']['vision_obstacles_info']['imageIndex'].astype('int32')
        self._synchronize_with_fusion()

    def get_full_matrix(self, signal):
        """ Return full matrix of tracklets (128 columns). IF drops in signals were present a neighbour detection is
        copied (same behavior as in DV-Tool)"""
        signal = self._handle_drops(signal)
        return signal.reshape((int(signal.shape[0] / 2)), 128)

    def _synchronize_with_fusion(self):
        self._drop_redundant()
        if self.imageIndex[-1] < self.imageIndex[0]:
            self.imageIndex[np.argwhere(self.imageIndex == 1)[0][0]:, ] += 65535
            self.grabIndex[np.argwhere(self.grabIndex == 1)[0][0]:, ] += 65535
        self.tlet_index = np.searchsorted(self.imageIndex, self.grabIndex)
        return self.tlet_index

    def _drop_redundant(self):  # GrabIndex usually has one redundant value. Either at the beginning or end
        if self.grabIndex.shape[0] %2 == 0:
            print('Log containing even number of GIds')
            pass
        elif self.grabIndex[-1] != self.grabIndex[-2]:
            self.grabIndex = np.delete(self.grabIndex, -1)
        elif self.grabIndex[0] != self.grabIndex[1]:
            self.grabIndex = np.delete(self.grabIndex, 0)
        else:
            # Some logs don't have redundant index. In this case we need to insert one more GId at the end to maintain
            # even number of detections
            self.grabIndex = np.insert(self.grabIndex, -1, self.grabIndex[-1], axis=0)

    def _handle_drops(self, signal):
        """ Check if there were drops in signal i.e. if there are two same IDs of tracklets detected one
            after another. If so, insert previous detection into signal to maintain order"""
        drops_LR = []
        drops_MR = []
        for i in range(1, len(self.tlet_numbers)):
            if self.tlet_numbers[i][0] == 65 and self.tlet_numbers[i - 1][0] == 65:
                drops_LR.append(i)
            if self.tlet_numbers[i][0] == 1 and self.tlet_numbers[i - 1][0] == 1:
                drops_MR.append(i)

        for index in range(len(self.tlet_numbers), 0, -1):  # Iterate backwards to maintain index order
            if index in drops_LR:
                signal = np.insert(signal, index, signal[index - 2], axis=0)  # Copy and insert previous LR detection
            if index in drops_MR:  # MR drops
                signal = np.insert(signal, index, signal[index - 2], axis=0)  # Copy and insert previous MR detection

        # First detection has to be LR and last has to be MR detection
        if self.tlet_numbers[0][0] == 65:
            signal = np.insert(signal, 0, signal[1], axis=0)
        if self.tlet_numbers[-1][0] == 1:
            signal = np.insert(signal, -1, signal[-2], axis=0)
            print('log starts with LR tlets')

        self._check_lengths(signal)

        return signal

    def _check_lengths(self, signal):
        """ Since every .mat file seems to be different, sometimes the only way to make this script work is to insert
         missing indexes into tlet_index. This function copies lat indexes and appends them if lengths of signals don't
         match"""
        if signal.shape[0] != self.tlet_index.shape[0]:
            missing = signal.shape[0] - self.tlet_index.shape[0]
            for i in range(missing):
                self.tlet_index = np.append(self.tlet_index, self.tlet_index[-1])

    # --------------------SPRAWDZIC get_synchronized ----------------------------------
    def get_synchronized(self, signals_dict):
        pass
        out = {}
        for key, val in signals_dict.items():
            out[key] = val[self.tlet_index]