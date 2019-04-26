from objectScripts.CADS_3p5.calibration_decoder import pedWarn, vehWarn
import pandas as pd


def read_ffs(path):
    with open(path, 'rb') as f:
        ffs = f.readlines()
        ffs = [line.rstrip() for line in ffs]
    return ffs


class Vehicle(vehWarn.FeatureVEH):
    def __init__(self, ffs_path, sensitivity=1):
        """
        Get calibration for Vehicle features
        :param ffs_path: path to .ffs file
        :param int sensitivity: Default - medium: Sensitivity setting. Available values:
        * 0 - "near"
        * 1 - "medium"
        * 2 - "far"
        """
        self.ffs = read_ffs(ffs_path)
        super().__init__(self.ffs, sensitivity)

    def get_all_cals(self):
        return self.all_featres


class VRU(pedWarn.FeatureVRU):
    def __init__(self, ffs_path, vru_type):
        """
        Get calibration for VRU features

        :param ffs_path: path to .ffs file
        :param int/str vru_type: Type of the VRU. Can be either passed as string or int. Available types:
        4 or "pedestrian";  9 or "bicycle"
        """
        self.ffs = read_ffs(ffs_path)
        super().__init__(vru_type, self.ffs)

    def get_all_cals(self):
        return self.all_features


if __name__ == '__main__':
    veh_test = Vehicle(r"\\10.224.20.32\sfo\EuNCAP\Logs\s412_EuNCAP\s412_long_ncap\KR6N086_FTP112_TC7_20180709_135608_019.ffs")
    print(veh_test.get_ttc(10, 8, 'warning'))
    # print(veh_test)
    veh_test.to_excel_veh(r'C:\Users\qj3x4n\Desktop')

    ped_test = VRU(r"\\10.224.20.32\sfo\EuNCAP\Logs\s412_EuNCAP\s412_long_ncap\KR6N086_FTP112_TC7_20180709_135608_019.ffs",
                   4)
    # print(ped_test)
    # ped_test.to_excel_ped(r'C:\Users\qj3x4n\Desktop')

    ped_test = VRU( r"\\10.224.20.32\sfo\EuNCAP\Logs\s412_EuNCAP\s412_long_ncap\KR6N086_FTP112_TC7_20180709_135608_019.ffs",
                   9)
    # print(ped_test)
    # ped_test.to_excel_bic(r'C:\Users\qjsjnz\Desktop')

