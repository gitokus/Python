import numpy as np
import pandas as pd
import os
import openpyxl
from scipy import interpolate


class SetPCW:
    def __init__(self, ped_type, set_name):
        # Find speed kneepoints (this set is named differently than the sets for TTC). If looking for pedestrain's
        # speed values we need to change the pedType to "warn" since that's the naming convention in ffs file.
        if ped_type == 'pedestrian':
            ped_type = 'warn'
            self.ego_spd = str('PCW_' + set_name + '_speed_kneePoints:').encode()
        else:
            self.ego_spd = str('PCW_' + set_name + '_speed_kneePoints_bicycle:').encode()

        # Create names for threshold sets. //'Night' applies only to bicycle
        self.threshold_norm = str('PCW_' + set_name + '_TTC_kneePoints_' + ped_type + ':').encode()
        self.threshold_far = str('PCW_' + set_name + '_TTC_kneePoints_' + ped_type + '_far:').encode()
        self.threshold_near = str('PCW_' + set_name + '_TTC_kneePoints_' + ped_type + '_near:').encode()
        self.threshold_night = str('PCW_' + set_name + '_TTC_kneePoints_' + ped_type + '_night:').encode()

        self.set_names = [self.ego_spd, self.threshold_near, self.threshold_norm, self.threshold_far, self.threshold_night]
        self.values = [[]]
        self.row_names = self.values[0]

    def find_values(self, ffs_file):
        # Look for TTC values for for all sets in specified ffs file. Find the line in
        # ffs file which contains the name of the set. Set's values in ffs are listed
        # after':'(colon) String of values is split and converted to float numbers with 2 decimal points
        for name in self.set_names:
            for line in ffs_file:
                if name in line:
                    value_ttc = [np.around(float(value), 2) for value in line[len(name) + 1:].split()]
                    # append values and name to list.
                    self.values[0].append(name)
                    self.values.append(value_ttc)
                    break  # stop the loop when values are found

        return pd.DataFrame(data=self.values[1:], index=self.row_names,
                            columns=[str(int(round(x * 3.6))) + 'kph' for x in self.values[1]])


class FeatureVRU:
    """ Class for decoding values for every feature that's part of Pedestrian
    Collision Warning functionality"""

    def __init__(self, type_vru, ffs_file):
        """
        Find every function's values for specified VRU type (ped/bic) and ffs file
        :param int/str type_vru: Type of the VRU. Can be either passed as string or int. Available types:
        * 4 or "pedestrian"
        * 9 or "bicycle"
        :param list ffs_file: .ffs file split into list of lines
        """
        if not isinstance(type_vru, str):
            type_vru = "pedestrian" if type_vru == 4 else "bicycle"

        self.full_brake = SetPCW(type_vru, 'L1').find_values(ffs_file)
        self.part_brake = SetPCW(type_vru, 'L2').find_values(ffs_file)
        self.warning = SetPCW(type_vru, 'L3').find_values(ffs_file)
        self.brake_unconf = SetPCW(type_vru, 'L4').find_values(ffs_file)

        # Assign name to each DataFrame so each functionality is clearly distinguished

        self.full_brake.name = "Autonomous Emergency Braking " + type_vru.upper()
        self.part_brake.name = "Partial Braking Only " + type_vru.upper()
        self.warning.name = "Warning Only " + type_vru.upper()
        self.brake_unconf.name = "AEB - No Forward Collision Warning " \
                                 + type_vru.upper()
        self.all_features = [self.warning, self.part_brake, self.brake_unconf, self.full_brake]

    def to_excel_ped(self, path):

        df1 = pd.DataFrame(self.part_brake)
        df2 = pd.DataFrame(self.warning)
        df3 = pd.DataFrame(self.full_brake)
        df4 = pd.DataFrame(self.brake_unconf)

        writer = pd.ExcelWriter(path+'\output1.xlsx', engine='openpyxl')

        if os.path.exists(path+'\output1.xlsx'):
            book = openpyxl.load_workbook(path+'\output1.xlsx')
            writer.book = book

        df1.to_excel(writer, sheet_name='Pedestrian cals', index_label='Partial Braking Only PEDESTRIAN',
                                 startrow=1, startcol=0)
        df2.to_excel(writer, sheet_name='Pedestrian cals', index_label='Warning Only PEDESTRIAN', startrow=8,
                                 startcol=0)
        df3.to_excel(writer, sheet_name='Pedestrian cals', index_label='Autonomous Emergency Braking PEDESTRIAN',
                                 startrow=15, startcol=0)
        df4.to_excel(writer, sheet_name='Pedestrian cals',
                                 index_label='AEB - No Forward Collision Warning PEDESTRIAN', startrow=22,
                                 startcol=0)
        writer.save()
        writer.close()

    def to_excel_bic(self, path):
        df1 = pd.DataFrame(self.part_brake)
        df2 = pd.DataFrame(self.warning)
        df3 = pd.DataFrame(self.full_brake)
        df4 = pd.DataFrame(self.brake_unconf)

        writer = pd.ExcelWriter(path+'\output1.xlsx', engine='openpyxl')

        if os.path.exists(path+'\output1.xlsx'):
            book = openpyxl.load_workbook(path+'\output1.xlsx')
            writer.book = book

        df1.to_excel(writer, sheet_name='Bicycle clas', index_label='Partial Braking Only BICYCLE',
                         startrow=1, startcol=0)
        df2.to_excel(writer, sheet_name='Bicycle clas', index_label='Warning Only BICYCLE', startrow=8,
                         startcol=0)
        df3.to_excel(writer, sheet_name='Bicycle clas', index_label='Autonomous Emergency Braking BICYCLE',
                         startrow=15, startcol=0)
        df4.to_excel(writer, sheet_name='Bicycle clas',
                         index_label='AEB - No Forward Collision Warning BICYCLE', startrow=22,
                         startcol=0)
        writer.save()
        writer.close()

    def get_ttc(self, vel, flag_type, sensitivity=1):
        """
        Get value of TTC for given function, velocity and sensitivity

        :param int/float vel: host vehicle velocity in meters/sec
        :param str flag_type: type of flag. Available types: 'full_brake', 'part_brake', 'warning', 'brake_unconf'
        :param int sensitivity: Sensitivity level. Available values:
        0 - near; 1 - medium; 2 - far; 3 - night

        :return value of Time To Collision
        """

        func_dict = {'warning': 0, 'part_brake': 1, 'brake_unconf': 2, 'full_brake': 3}
        func = self.all_features[func_dict[flag_type]]
        ttc_points = func.iloc[sensitivity+1]
        spd_points = func.iloc[0]
        inter = interpolate.interp1d(spd_points, ttc_points)
        if vel < spd_points.min():
            return ttc_points.iloc[0]  # TTC for speed below min_spd_point should be constant
        elif vel > spd_points.max():
            return ttc_points.iloc[-1]  # TTC for speed above max_spd_point should be constant
        else:
            return np.around(inter(vel).item(), 2)  # Get item of single-element np.array

    def __str__(self):
        return '\n'.join(['\n'.join([value.name, str(value)]) for value in self.all_features])

# def print_values(self):
#     """ print each dataframe with decoded values with its name """
#     for value in self.all_features:
#         print(value.name, '\n', value, '\n')
