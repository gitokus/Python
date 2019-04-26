""" This module implements functions that look up values in ffs file for TTC, Ego Speed and Relative Speed """
import numpy as np
import pandas as pd
from scipy import interpolate


class SetFCW:
    def __init__(self, set_name, sensitivity=1):
        """
        Create set names which will be looked up in ffs file
        :param set_name: name of the function - used by FeatureFCW class
        :param sensitivity: sensitivity additive. Should be passed as numerical value:
        *0 - near
        *1 - medium
        *2 - far
        """
        sens_enum = {0: 'near', 1: 'medium', 2: 'far'}
        self.ego_spd = str('vEgo_vs_vRel_vEgoKneePts_' + set_name + ':').encode()
        self.rel_spd = str('vEgo_vs_vRel_vRelKneePts_' + set_name + ':').encode()
        self.threshold = str('vEgo_vs_vRel_threshAdditives_' + set_name + ':').encode()
        self.base_table = str(sens_enum[sensitivity].upper() + '_TTC_TABLE_' + set_name + ':').encode()
        self.base_spd = str('FCW_baseSpeeds_' + set_name + ':').encode()
        self.decoded_values = {}

    def find_values(self, ffs_file):
        """
        Look for TTC values for for all sets in specified ffs file. Find the line in ffs file which contains the
        name of the set.
        :param list ffs_file: List containing .ffs file split into lines

        :return DataFrame with values"""
        sens_additive = 0.3  # Typical additive for medium sensitivity

        for line in ffs_file:
            # Set's values in ffs are listed after':'(colon) sign so we're looking for values after the colon.
            # e.g. if set is: vEgo_vs_vRel_vEgoKneePts_setD: 8.33 11.11 13.88 16.67 20 function will return array with
            # numbers converted to float with 2 decimals stored as self.egoSpd
            if self.ego_spd in line:
                index = len(self.ego_spd)
                spd_values = [np.around(float(value), 2) for value in line[index + 1:].split()]
                spd_values = np.array(spd_values)
                self.decoded_values['Ego Vehicle Speed'] = spd_values

            if self.rel_spd in line:
                index = len(self.rel_spd)
                spd_values = [np.around(float(value), 2) for value in line[index + 1:].split()]
                spd_values = np.array(spd_values)

                # Flip values in array. Needs to be done in because that's the way ME did this algorithm
                spd_values = np.flip(spd_values, 0)
                self.decoded_values['Relative Speed'] = spd_values

            if self.threshold in line:
                index = len(self.threshold)
                tresh_values = [np.around(float(value), 2) for value in line[index + 1:].split()]

                # Create 5x5 array with TTC threshold values. However, I'm not sure if this array will always be 5x5...
                tresh_values = np.reshape(np.array(tresh_values), (5, 5))
                self.decoded_values['TTC thresholds'] = tresh_values

            if self.base_table in line:
                index = len(self.base_table)
                sens_additive = [np.float(value) for value in line[index + 1:].split()]

            if self.base_spd in line:
                index = len(self.base_spd) + 1
                # Base speed values are reported in mph. #JustMobilEyeThings
                # TO REMOVE-OLD LINE base_speed = [np.around(float(value)/3.6, 2) for value in line[index + 1:].split()]

                base_speed = [np.around(float(value)/2.23694, 2) for value in line[index + 1:].split()]
            # break the loop when values are found. This condition is a bit arbitrary and needs to be tested whether
            # it works for every .ffs file
            if "etc/paramVerification.db".encode() in line:
                break

        # check if all additives in sensitivity matrix are the same. If not we need to interpolate
        if isinstance(sens_additive, float):
            print('Could not find sensitivity additive values')
        elif len(set(sens_additive)) == 1:
            sens_additive = sens_additive[0]
        elif len(sens_additive) != len(base_speed):
            print('Multiple sensitivity values defined! \nCheck .ffs file for correctness. Assuming sensitive'
                  ' additive = 0.3 (typical value for Medium sensitivity)')
            sens_additive = 0.3
        else:
            inter = interpolate.interp1d(base_speed, sens_additive, bounds_error=False,
                                         fill_value=(sens_additive[0], sens_additive[-1]))
            sens_additive = []
            for spd in self.decoded_values['Ego Vehicle Speed']:
                additive = np.around(inter(spd).item(), 2)
                sens_additive.append(additive)
            sens_additive = np.array(sens_additive)

        # Add sensitivity additive to TTC thresholds and return all values in DataFrame
        # df1 = pd.DataFrame(np.around(self.decoded_values['TTC thresholds'] + sens_additive, 2),
        #              index=self.decoded_values['Relative Speed'],
        #              columns=self.decoded_values['Ego Vehicle Speed'])
        #
        # with pd.ExcelWriter('output.xlsx') as writer:
        #      df1.to_excel(writer, sheet_name='Sheet_name_1')

        return pd.DataFrame(np.around(self.decoded_values['TTC thresholds'] + sens_additive, 2),
                            index=self.decoded_values['Relative Speed'],
                            columns=self.decoded_values['Ego Vehicle Speed'])


class FeatureVEH:
    """ return values from specified ffs file for each function. Default sensitivity setting is 'medium'
     (other relevant settings: 'far', 'near').
    :return DataFrame with decoded values. """

    def __init__(self, ffs_file, sensitivity=1):
        """

        :param list ffs_file: .ffs file split into list of lines
        :param int sensitivity: sensitivity additive. Should be passed as numerical value:
        *0 - near
        *1 - medium
        *2 - far
        """
        self.warning = SetFCW('setD', sensitivity).find_values(ffs_file)
        self.full_brake = SetFCW('setE', sensitivity).find_values(ffs_file)
        self.part_brake = SetFCW('setF', sensitivity).find_values(ffs_file)
        self.brake_unconf = SetFCW('setG', sensitivity).find_values(ffs_file)


        # Add  name to each DataFrame
        self.warning.name = 'Forward Collision Warning'
        self.full_brake.name = 'Full Braking'
        self.part_brake.name = 'Partial Braking'
        self.brake_unconf.name = 'Partial Braking No FCV'

        self.all_features = [self.warning, self.part_brake, self.brake_unconf, self.full_brake]

    def to_excel_veh(self, path):

        df1 = pd.DataFrame(self.part_brake)
        df2 = pd.DataFrame(self.warning)
        df3 = pd.DataFrame(self.full_brake)
        df4 = pd.DataFrame(self.brake_unconf)

        with pd.ExcelWriter(path+'\output1.xlsx') as writer:
          df1.to_excel(writer, sheet_name='Vehicle cals', index_label='Partial Braking', startrow=1, startcol=0)
          df2.to_excel(writer, sheet_name='Vehicle cals', index_label='Forward Collision Warning', startrow=8,
                       startcol=0)
          df3.to_excel(writer, sheet_name='Vehicle cals', index_label='Full Braking', startrow=15, startcol=0)
          df4.to_excel(writer, sheet_name='Vehicle cals', index_label='Partial Braking No FCV', startrow=22, startcol=0)


    def get_ttc(self, rel_vel, ego_vel, flag_type):
        """
        Get value of TTC for given ego velocity, target velocity and flag type

        :param int/float rel_vel: Relative velocity; Rel_vel = Ego_vel - Target_vel
        :param int/float ego_vel: Ego vehicle's velocity
        :param str flag_type: Type of flag (function); Available types: 'full_brake', 'part_brake', 'warning',
        'brake_unconf'

        :return: value of Time To Collision
        """
        func_dict = {'warning': 0, 'part_brake': 1, 'brake_unconf': 2, 'full_brake': 3}
        func = self.all_features[func_dict[flag_type]]
        rel_spd_points = np.array(func.index)  # X coordinates
        ego_spd_points = np.array(func.columns)  # Y coordinates
        ttc_points = func.values  # values are already a np.array

        # np.meshgrid returns a list of arrays with coordinates of points. Need to convert it to np.array
        xy_points = np.array(np.meshgrid(rel_spd_points, ego_spd_points))  # xy_points is now 3D array
        xy_points = xy_points.transpose().reshape(25, 2)  # Make 2D array of point coordinates
        ttc_points = ttc_points.reshape(25)  # Input and output shapes need to match
        interp = interpolate.Rbf(xy_points[:, 0], xy_points[:, 1], ttc_points)

        min_ego_spd, max_ego_spd = np.min(ego_spd_points), np.max(ego_spd_points)
        min_rel_spd, max_rel_spd = np.min(rel_spd_points), np.max(rel_spd_points)

        # Higher/smaller velocities than calibrated should not be extrapolated
        if ego_vel > max_ego_spd:
            ego_vel = max_ego_spd
        if ego_vel < min_ego_spd:
            ego_vel = min_ego_spd
        if rel_vel > max_rel_spd:
            rel_vel = max_rel_spd
        if rel_vel < min_rel_spd:
            rel_vel = min_rel_spd

        return np.around(interp(rel_vel, ego_vel), 2)

    def __str__(self):
        return '\n'.join(['\n'.join([value.name, str(value)]) for value in self.all_features])
    # def printValues(self):
    #     for value in self.all_features:
    #         print(value.name, '\n', value, '\n')

