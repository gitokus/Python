import delphiTools3.base as dtb
import delphiTools3.usefulFunctions as usf
import objectScripts.CADS_3p5.calibration_decoder.decoder as dcdr
import numpy as np
import pandas as pd
from glob import glob
import os
from tqdm import tqdm


class VEHData():
    def __init__(self, mat_path, ffs_path=None):
        self.logname = os.path.basename(mat_path[:-4])
        self.mat = dtb.loadmat(mat_path, sort=True)
        if not ffs_path:
            ffs_path = mat_path[:-3] + 'ffs'
        self.ffs_path = ffs_path
        self.signals = {'ego_vel': self.mat['mudp']['vis']['vision_vehicle_info']['vehicleVelocity'],
                        'tgt_lt_vel': self.mat['mudp']['vis']['vision_obstacles_info']['visObs']['lat_vel'],
                        'tgt_lg_vel': self.mat['mudp']['vis']['vision_obstacles_info']['visObs']['long_vel'],
                        'ttc_accel': self.mat['mudp']['vis']['vision_obstacles_info']['visObs']['ttc_const_accel'],
                        'ttc_vel': self.mat['mudp']['vis']['vision_obstacles_info']['visObs']['ttc_const_vel'],
                        'uniqueID': self.mat['mudp']['vis']['vision_obstacles_info']['visObs']['uniqueID']}
        self.vis_func_info = self.mat['mudp']['vis']['vision_function_info']
        self.flags = [key for key in self.vis_func_info.keys() if 'Veh' in key and 'CIPO' not in key]
        self.extra_info = {'ego_vel': self.mat['mudp']['vis']['vision_vehicle_info']['vehicleVelocity'],
                           'grab_idx': self.mat['mudp']['vis']['vision_function_info']['imageIndex']}
        self.events = self.find_events()
        self.out_df = self.get_veh_aeb_data() if self.events else None

    def find_events(self):
        out_dict = {}
        for flag in self.flags:
            events = np.argwhere(self.vis_func_info[flag])
            if not np.any(events):  # If flag is not present - continue loop
                continue
            else:
                event_info = np.array(
                    [events.ravel(), self.vis_func_info[flag][events].ravel() - 1])  # 2D arr: [frame, objID-1]
                out_dict[flag] = usf.get_consecutive(event_info.transpose(), max_gap=4)
        return out_dict

    def get_veh_aeb_data(self):
        """
        Get information about Vehicle AEB event

        :return: pd.DataFrame with information
        """
        # sens = self.mat['dvlExt']['vis']['sys']['fcw_sense_level'][0]  # FCW Sensitivity
        sens = self.mat['mudp']['vfpState']['cals']['fcw_params']['warningSensitivityLevel'][-1].item()  # FCW Sensitivity
        events = []
        flag_translate = {'visOnlyVehBrake': 'full_brake', 'visOnlyVehPartialBrake': 'part_brake',
                          'visOnlyVehWarning': 'warning', 'visOnlyVehBrakeUnconfirmed': 'brake_unconf'}

        for f_name, f_data in self.events.items():
            for event in f_data:  # Iterate over events where flag was present throughout the log

                # Preprocessing
                beg_frame = event[0, 0]
                obj_id = event[0, 1]
                event_gid = self.extra_info['grab_idx'][beg_frame]
                un_ID = self.signals['uniqueID'][beg_frame, obj_id]  # Get obj unique ID
                obj_age = np.argwhere(self.signals['uniqueID'][:beg_frame, obj_id] == un_ID)
                obj_age = obj_age.shape[0]  # How long obj was detected before flag
                obj_vel = self.signals['tgt_lg_vel'][beg_frame, obj_id]
                host_vel = self.signals['ego_vel'][beg_frame]
                rel_vel = host_vel - obj_vel

                # Filling pandas Series with values
                out = pd.Series(data=[self.logname, beg_frame, event_gid, obj_age, f_name],
                                index=['logname', 'frame', 'GrabIndex', 'obj_age[frames]', 'flag_type'])
                try:
                    calib = dcdr.Vehicle(self.ffs_path, sens)
                    out['calibrated_ttc_t0'] = calib.get_ttc(rel_vel, host_vel, flag_translate[f_name])
                except:
                    print('Corrupted ffs file')
                    break
                for i, frame in enumerate(np.arange(beg_frame, beg_frame - 4, -1)):
                    if frame >= 0:
                        out[f'ttc_vel_t{-i}'] = np.around(self.signals['ttc_vel'][frame, obj_id], 2)
                        out[f'ttc_accel_t{-i}'] = np.around(self.signals['ttc_accel'][frame, obj_id], 2)
                    else:
                        out[f'ttc_vel_t{-i}'] = np.nan
                        out[f'ttc_accel_t{-i}'] = np.nan
                events.append(out)

        out = pd.concat(events, axis=1).transpose()
        # Remove duplicates; i.e. If multiple flags are present in log only first row will contain logname
        out['logname'] = out['logname'].mask(out['logname'].shift(1) == out['logname'])

        return out


class VRUData:
    def __init__(self, mat_path, ffs_path=None):
        self.logname = os.path.basename(mat_path[:-4])
        self.mat = dtb.loadmat(mat_path, sort=True)
        if not ffs_path:
            ffs_path = mat_path[:-3] + 'ffs'
        self.ffs_path = ffs_path
        self.signals = {'ego_vel': self.mat['mudp']['vis']['vision_vehicle_info']['vehicleVelocity'],
                        'ttc_accel': self.mat['mudp']['vis']['vision_obstacles_info']['visObs']['ttc_const_accel'],
                        'ttc_vel': self.mat['mudp']['vis']['vision_obstacles_info']['visObs']['ttc_const_vel'],
                        'uniqueID': self.mat['mudp']['vis']['vision_obstacles_info']['visObs']['uniqueID'],
                        'class': self.mat['mudp']['vis']['vision_obstacles_info']['visObs']['obstacle_class']}
        self.vis_func_info = self.mat['mudp']['vis']['vision_function_info']
        self.flags = [key for key in self.vis_func_info.keys() if 'VRU' in key]
        self.extra_info = {'ego_vel': self.mat['mudp']['vis']['vision_vehicle_info']['vehicleVelocity'],
                           'grab_idx': self.mat['mudp']['vis']['vision_function_info']['imageIndex']}
        self.events = self.find_events()
        self.out_df = self.get_vru_aeb_data() if self.events else None

    def find_events(self):
        out_dict = {}
        for flag in self.flags:
            events = np.argwhere(self.vis_func_info[flag])
            if not np.any(events):  # If flag is not present - continue loop
                continue
            else:
                event_info = np.array(
                    [events.ravel(), self.vis_func_info[flag][events].ravel() - 1])  # 2D arr: [frame, objID-1]
                out_dict[flag] = usf.get_consecutive(event_info.transpose(), max_gap=4)
        return out_dict

    @staticmethod
    def get_status(df):
        for model in ['ttc_vel_', 'ttc_accel_']:
            calibd = df['calibrated_ttc_t0']
            timing_cols = [col for col in df.index if model in col]
            # vel_cols = [col for col in df.columns if 'ttc_vel' in col]
            temp_df = df[timing_cols] - calibd
            temp_df.reset_index(drop=True, inplace=True)
            if np.all(temp_df.values > 0):
                df[model + 'status'] = 'Too early flag'
                continue
            if np.all(temp_df.values < 0):
                df[model + 'status'] = '2+ frames too late'
                continue
            if temp_df[0] < 0 and temp_df[1] >= 0:
                df[model + 'status'] = 'Correct flag'
                continue
            if temp_df[1] < 0 and temp_df[2] >= 0:
                df[model + 'status'] = '1 frame too late'
                continue
            if temp_df[2] < 0 and temp_df[3] >= 0:
                df[model + 'status'] = '2 frames too late'
                continue
        return df

    def get_vru_aeb_data(self):
        """
        Get information about Vehicle VRU event

        :return: pd.DataFrame with information
        """
        # Preprocessing
        sens = self.mat['dvlExt']['vis']['sys']['fcw_sense_level'][0]  # FCW Sensitivity
        events = []
        flag_translate = {'visOnlyVRUBrake': 'full_brake', 'visOnlyVRUPartialBrake': 'part_brake',
                          'visOnlyVRUWarning': 'warning', 'visOnlyVRUBrakeUnconfirmed': 'brake_unconf'}

        for f_name, f_data in self.events.items():
            for event in f_data:  # Iterate over events where flag was present throughout the log

                beg_frame = event[0, 0]
                obj_id = event[0, 1]
                event_gid = self.extra_info['grab_idx'][beg_frame]
                un_id = self.signals['uniqueID'][beg_frame, obj_id]  # Get obj unique ID
                obj_age = np.argwhere(self.signals['uniqueID'][:beg_frame, obj_id] == un_id)
                obj_age = obj_age.shape[0]  # How long obj was detected before flag
                obj_class = self.signals['class'][beg_frame, obj_id]
                host_vel = self.signals['ego_vel'][beg_frame]

                # Filling pandas Series with values
                out = pd.Series(data=[self.logname, beg_frame, event_gid, obj_age, f_name],
                                index=['logname', 'frame', 'GrabIndex', 'obj_age[frames]', 'flag_type'])
                calib = dcdr.VRU(self.ffs_path, obj_class)
                out['calibrated_ttc_t0'] = calib.get_ttc(host_vel, flag_translate[f_name], sens)
                for i, frame in enumerate(np.arange(beg_frame, beg_frame - 4, -1)):
                    if frame >= 0:
                        out[f'ttc_vel_t{-i}'] = np.around(self.signals['ttc_vel'][frame, obj_id], 2)
                        out[f'ttc_accel_t{-i}'] = np.around(self.signals['ttc_accel'][frame, obj_id], 2)
                    else:
                        out[f'ttc_vel_t{-i}'] = np.nan
                        out[f'ttc_accel_t{-i}'] = np.nan
                self.get_status(out)
                events.append(out)
        out = pd.concat(events, axis=1).transpose()
        # Remove duplicates; i.e. If multiple flags are present in log only first row will contain logname
        out['logname'] = out['logname'].mask(out['logname'].shift(1) == out['logname'])

        return out


path = r'D:\NCAP'
mat_list = glob(r'D:\NCAP\*.mat')
# ffs_list = glob(r'Z:\JIRA\ADAS-2389\ffs_files\*.ffs')


veh_events = []
vru_events = []
for i, mat in enumerate(mat_list):
    log_name = os.path.basename(mat)
    print(i, log_name)
    # ffs = [file for file in ffs_list if log_name[:-4] in file][0]
    # ffs = r"F:\CAD3p5_tickets\ADAS-1902\ADAS_E16FOR01T_20181001_ckout_B515MCA_DCV_AHBC_DL_210006_001.ffs"
    ffs = r"D:\NCAP\KR3N581_CBLA_20190129_130946_001.ffs"
    # veh = VEHData(mat, ffs)
    # vru = VRUData(mat, ffs)
    try:
        veh = VEHData(mat, ffs)
        vru = VRUData(mat, ffs)
        veh_events.append(veh.out_df)
        vru_events.append(vru.out_df)
    except Exception as e:
        print(e)

# Save csv only if any events were present
if any(isinstance(vru_events[i], pd.DataFrame) for i in range(len(vru_events))):
    vru_events = pd.concat(vru_events).reset_index(drop=True)

    # Rearrange columns
    cols = vru_events.columns.tolist()
    ttc_accel_cols = ['ttc_accel_t0', 'ttc_accel_t-1', 'ttc_accel_t-2', 'ttc_accel_t-3', 'ttc_accel_status']
    ttc_vel_cols = ['ttc_vel_t0', 'ttc_vel_t-1', 'ttc_vel_t-2', 'ttc_vel_t-3', 'ttc_vel_status']
    info_cols = ['logname', 'frame', 'obj_age[frames]', 'GrabIndex','flag_type', 'calibrated_ttc_t0']
    # ttc_vel_cols = cols[6::2]
    # new_cols = cols[:6] + ttc_accel_cols + ttc_vel_cols
    # vru_events = vru_events[new_cols]  # Assing with rearranged columns
    vru_events = vru_events[info_cols + ttc_accel_cols + ttc_vel_cols]  # Assing with rearranged columns
    vru_events.to_csv(os.path.join(path, 'VRU_events.csv'), index=False)
if any(isinstance(veh_events[i], pd.DataFrame) for i in range(len(veh_events))):
    veh_events = pd.concat(veh_events).reset_index(drop=True)

    # Rearrange columns
    cols = veh_events.columns.tolist()
    ttc_accel_cols = ['ttc_accel_status', 'ttc_accel_t0', 'ttc_accel_t-1', 'ttc_accel_t-2', 'ttc_accel_t-3']
    ttc_vel_cols = ['ttc_vel_status', 'ttc_vel_t0', 'ttc_vel_t-1', 'ttc_vel_t-2', 'ttc_vel_t-3']
    info_cols = ['logname', 'frame', 'obj_age[frames]', 'GrabIndex', 'flag_type']
    # ttc_accel_cols = cols[7::2]
    # ttc_vel_cols = cols[6::2]
    # new_cols = cols[:6] + ttc_accel_cols + ttc_vel_cols
    # veh_events = veh_events[new_cols]  # Assing with rearranged columns
    vru_events = vru_events[info_cols + ttc_accel_cols + ttc_vel_cols]  # Assing with rearranged columns
    veh_events.to_csv(os.path.join(path, 'VEH_events.csv'), index=False)




