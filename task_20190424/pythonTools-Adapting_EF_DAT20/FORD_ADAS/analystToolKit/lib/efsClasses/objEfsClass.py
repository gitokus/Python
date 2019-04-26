import numpy as np

from analystToolKit.lib.efsClasses import efsFrameClass


class objEFs(efsFrameClass.EFClass):
    def __init__(self):
        self.function = 'OBJ'


    def appendDetails(self, dat2p0):

        if dat2p0:
            self.header += ['autoFixOk', 'alignment_horizon', 'alignment_yaw'] + \
                          [key for key in sorted(
                              self.mat['mudp']['vis']['vision_obstacles_info']['visObjects']['visObs']['physicalState'].keys())]

            errorNameList = []
            for eventsDict in self.eventsDictList:
                index = int(np.where(self.visIndex == eventsDict['eventIndex'])[0][0])
                columnID = eventsDict['eventColumnID']
                try:
                    eventsDict['autoFixOk'] = 'No available in DAT2.0'
                except:
                    errorNameList.append('autoFixOk')
                try:
                    eventsDict['alignment_horizon'] = 'No available in DAT2.0'
                except:
                    errorNameList.append('alignment_horizon')
                try:
                    eventsDict['alignment_yaw'] = 'No available in DAT2.0'
                except:
                    errorNameList.append('alignment_yaw')
                # matrix signals
                if not eventsDict == -1:
                    for key in [key for key in
                                sorted(self.mat['mudp']['vis']['vision_obstacles_info']['visObjects']['visObs']['physicalState'].keys())]:
                        try:
                            eventsDict[key] = \
                                self.mat['mudp']['vis']['vision_obstacles_info']['visObjects']['visObs']['physicalState'][key][index][columnID]
                        except:
                            errorNameList.append(key)

            return list(set(errorNameList))
        else:

            self.header += ['autoFixOk', 'alignment_horizon', 'alignment_yaw'] + \
                           [key for key in sorted(
                               self.mat['mudp']['vis']['vision_obstacles_info']['visObs'].keys())]

            errorNameList = []
            for eventsDict in self.eventsDictList:
                index = int(np.where(self.visIndex == eventsDict['eventIndex'])[0][0])
                columnID = eventsDict['eventColumnID']
                try:
                    eventsDict['autoFixOk'] = self.mat['mudp']['vis']['vision_camera_alignment_info']['autoFixOk'][index]
                except:
                    errorNameList.append('autoFixOk')
                try:
                    eventsDict['alignment_horizon'] = self.mat['mudp']['vis']['vision_camera_alignment_info'][
                        'cameraAlignment']['horizon'][index]
                except:
                    errorNameList.append('alignment_horizon')
                try:
                    eventsDict['alignment_yaw'] = self.mat['mudp']['vis']['vision_camera_alignment_info'][
                        'cameraAlignment']['yaw'][index]
                except:
                    errorNameList.append('alignment_yaw')
                # matrix signals
                if not eventsDict == -1:
                    for key in [key for key in sorted(self.mat['mudp']['vis']['vision_obstacles_info']['visObs'].keys())]:
                        try:
                            eventsDict[key] = \
                                self.mat['mudp']['vis']['vision_obstacles_info']['visObs'][key][index][columnID]
                        except:
                            errorNameList.append(key)

            return list(set(errorNameList))

    def isNewlyDetected(self, detection_status):
        """
        Checks whether detection status is "new".
        :param detection_status: Single value of detection status
        :return: True or false
        """
        return detection_status == 1

    def isPedestrianOrCyclist(self, obj_type):
        """
        Check whether detected object is either pedestrian or cyclist
        :param obj_type: Single value of obstacle_class
        :return: True or false
        """
        return obj_type in (4, 9)

    def get_path_center_at_dist(self, x, c0, c1, k, offset):
        """
        Calculate lateral position of center of predicted path at given longitudinal distance using polynomial formula:
        a3 * x**3 + a2 * x**2 + a1 * x + a0
        :param x: distance
        :param c0: parameter needed for polynomial; a2 = c0/2
        :param c1: parameter needed for polynomial; a3 = c1/6
        :param k: parameter needed for polynomial; a1 = tan(k)
        :param offset: parameter needed for polynomial; a0
        :return: lateral position of center of predicted path at given longitudinal distance
        """
        a0 = offset
        a1 = np.tan(k)
        a2 = c0/2
        a3 = c1/6
        return a0 + a1*x + a2*x**2 + a3*x**3

    def get_ttc_vel(self, delta_v, delta_dist):
        ttc = np.divide(delta_dist, delta_v, out=np.full_like(delta_v, 7), where=(delta_v != 0))
        return ttc

    def get_ttc_accel(self, d_accel, d_vel, d_dist):
        """
        Get TTC assuming constant acceleration. Function is solving quadratic equation:
        (1/2)*delta_accel*t^2 + delta_vel*t - delta_dist = 0
        Then, it determines which of the polynomial roots should be used:
        1. If one of roots is negative, return positive one
        2. If both roots are positive, return smaller one
        :param d_accel: (delta acceleration) Difference in acceleration between host and target
        :param d_vel: (delta velocity) Difference in velocity between host and target
        :param d_dist: (delta distance) Distance between host and target
        :return: TTC value
        """
        coeffs = [0.5 * d_accel, d_vel, -d_dist]
        roots = np.roots(coeffs)
        roots = roots[roots > 0]  # Negative TTCs don't make sense
        roots = roots[np.isreal(roots)]  # Use Isreal to drop complex results
        if len(roots) == 0:
            return 7  # Assume 7 as default value of TTC
        if len(roots) == 1:
            return roots.item()
        if len(roots) == 2:
            t1, t2 = roots
            return t1 if t1 < t2 else t2

    @staticmethod
    def get_bit(number, bit_number_from_right):
        return (number >> bit_number_from_right) & 1

    # EVENT FINDERS #
    def ef_template(self):
        """
        TEMPLATE EVENT FINDER
        It wont be executed, DO NOT delete this.
        EF reads all needed data from mat, then create empty data and indexes lists.
        It goes through every index in mat and check conditions. If conditions are met,
        index is appended to indexes list. After checking every index, indexes are appended
        to data list along with comment and EF ID.
        At this point it is possible to add another for loop, after declaring data, and before
        declaring indexes. It will result in running EF few times, ie for every line (lines must
        be declared earlier) and appending to data with different comment per each line.
        It is preffered to use EFsFrame method groupIndexes when appending indexes to data,
        in order to get rid of noises in event detection signal.

        :return: EF gives back dict structure with data len and data itself
        """
        imageIndex = self.mat['mudp']['vis']['vision_function_info']['imageIndex']

        data = []
        indexes = []
        for index in range(self.visLen):
            if index % 2 == 0:
                indexes.append(index)

        data.append([self.groupIndexes(indexes), 'EF_template(ID)', 'This is template event finder(Comment)'])
        return {'len': len(data), 'data': data}


    def ef_BrakeSignals(self):
        """
        EF1: Brake signals

        :return: EF gives back dict structure with data len and data itself
        """
        if self.dat2p0:
            brakeSignals = {'VRUBrake': self.mat["mudp"]["eyeq"]["AEB"]["vis_aeb_msg_info"]["visAEB"]["visOnlyVRUBrake"],
                            'VRUPartialBrake': self.mat["mudp"]["eyeq"]["AEB"]["vis_aeb_msg_info"]["visAEB"]["visOnlyVRUPartialBrake"],
                            'VRUWarning': self.mat["mudp"]["eyeq"]["AEB"]["vis_aeb_msg_info"]["visAEB"]["visOnlyVRUWarning"],
                            'VehBrake': self.mat["mudp"]["eyeq"]["AEB"]["vis_aeb_msg_info"]["visAEB"]["visOnlyVehBrake"],
                            'VehPartialBrake': self.mat["mudp"]["eyeq"]["AEB"]["vis_aeb_msg_info"]["visAEB"]["visOnlyVehPartialBrake"],
                            'VehWarning': self.mat["mudp"]["eyeq"]["AEB"]["vis_aeb_msg_info"]["visAEB"]["visOnlyVehWarning"],
                            'PCAiWarning': self.mat["mudp"]["eyeq"]["AEB"]["vis_aeb_msg_info"]["visAEB"]["visOnlyPCAiWarning"],
                            'PCAiBrake': self.mat["mudp"]["eyeq"]["AEB"]["vis_aeb_msg_info"]["visAEB"]["visOnlyPCAiBrake"],
                            'PCAiPartBrake': self.mat["mudp"]["eyeq"]["AEB"]["vis_aeb_msg_info"]["visAEB"]["visOnlyPCAiPartialBrake"]}
            age = self.mat["mudp"]["eyeq"]["Obstacles"]["vis_obstacles_msg_info"]["visObjects"]["visObs"]["age"]

        else:

            brakeSignals = {'VRUBrake': self.mat['mudp']['vis']['vision_function_info']['visOnlyVRUBrake'],
                            'VRUBrakeUnconfirmed': self.mat['mudp']['vis']['vision_function_info'][
                                'visOnlyVRUBrakeUnconfirmed'],
                            'VRUPartialBrake': self.mat['mudp']['vis']['vision_function_info']['visOnlyVRUPartialBrake'],
                            'VRUWarning': self.mat['mudp']['vis']['vision_function_info']['visOnlyVRUWarning'],
                            'VehBrake': self.mat['mudp']['vis']['vision_function_info']['visOnlyVehBrake'],
                            'VehBrakeUnconfirmed': self.mat['mudp']['vis']['vision_function_info'][
                                'visOnlyVehBrakeUnconfirmed'],
                            'VehPartialBrake': self.mat['mudp']['vis']['vision_function_info']['visOnlyVehPartialBrake'],
                            'VehWarning': self.mat['mudp']['vis']['vision_function_info']['visOnlyVehWarning'],
                            'PCAiWarning': self.mat['mudp']['vis']['vision_function_info']['visOnlyPCAiWarning'],
                            'PCAiBrake': self.mat['mudp']['vis']['vision_function_info']['visOnlyPCAiBrake'],
                            'PCAiPartBrake': self.mat['mudp']['vis']['vision_function_info']['visOnlyPCAiPartialBrake']}
            age = self.mat['mudp']['vis']['vision_obstacles_info']['visObs']['detection_status']

        data = []
        for i in range(age.shape[-1]):
            for key in brakeSignals.keys():
                indexes = []
                for index in range(self.visLen):
                    if brakeSignals[key][index] == (i + 1):
                        indexes.append(index)
                data.append([self.groupIndexes(indexes), 'Brake signals',
                             key + ' occured', i])

        return {'len': len(data), 'data': data}


    def ef_PartialAutoFixOk(self):
        """
        EF2: Partial autoFixOk
        DAT2.0 -> signal not available

        :return: EF gives back dict structure with data len and data itself
        """
        if self.dat2p0:
            print("NOT AVAILABLE IN DAT 2.0 DUE TO MISSING SIGNAL")
            return

        else:
            autoFixOk = self.mat['mudp']['vis']['vision_camera_alignment_info']['autoFixOk']

            data = []
            indexes = []

            if not min(autoFixOk) == max(autoFixOk):
                for index in range(self.visLen):
                    if autoFixOk[index] == 1:
                        indexes.append(index)
                data.append([self.groupIndexes(indexes), 'Partial autoFixOk',
                             'AutoFixOk ON', -1])

            return {'len': len(data), 'data': data}
    def ef_PedDetetction(self):
        """
        Cheks if ped was detected by system.
        Useful when searching for FP pedestraian detections on Highway
        :return:
        """
        if self.dat2p0:
            classification = self.mat["mudp"]["eyeq"]["Obstacles"]["vis_obstacles_msg_info"]["visObjects"]["visObs"]["classification"]
            long_pos = self.mat["mudp"]["eyeq"]["Obstacles"]["vis_obstacles_msg_info"]["visObjects"]["visObs"]["physicalState"]["longDistance"]
            lat_pos = self.mat["mudp"]["eyeq"]["Obstacles"]["vis_obstacles_msg_info"]["visObjects"]["visObs"]["physicalState"]["latDistance"]

        else:
            print("Only DAT2.0")
            return
        indexes = []
        data = []
        for col in range(classification.shape[-1]):
            for index in range(1, self.visLen-1):

                 if (classification[index, col] == 4) and (long_pos[index, col] <=60.0) and ((lat_pos[index, col] >= -20.0) and (lat_pos[index, col] <= 20.0)):
                     indexes.append(index)
        data.append([self.groupIndexes(indexes), 'Pedestrian detection', 'Ped on highway', col])

        return  {'len': len(data), 'data': data}

    def ef_VEH_TRK_Detetction(self):
        """
        Cheks if ped was detected by system.
        Useful when searching for FP pedestraian detections on Highway
        :return:
        """
        if self.dat2p0:
            classification = self.mat["mudp"]["eyeq"]["Obstacles"]["vis_obstacles_msg_info"]["visObjects"]["visObs"]["classification"]
            motionOrientattion =self.mat["mudp"]["eyeq"]["Obstacles"]["vis_obstacles_msg_info"]["visObjects"]["visObs"]["mobilityState"]["motionOrientation"]
            long_vel = self.mat["mudp"]["eyeq"]["Obstacles"]["vis_obstacles_msg_info"]["visObjects"]["visObs"]["physicalState"]["absoluteLongVelocity"]
            self.visLen = self.visLen-1
        else:
            print("Only DAT2.0")
            return
        indexes = []
        data = []

        for col in range(classification.shape[-1]):
            for index in range(1, self.visLen):
                # if classification[index, col] == 4 and classification[index-1, col] != 4:
                if (classification[index, col] in [0, 1] and long_vel[index, col] > 0.0):
                    indexes.append(index)
        data.append([self.groupIndexes(indexes), 'Veh_Trk detection', 'Veh_trk highway', col])

        return  {'len': len(data), 'data': data}

    def ef_CameraAlignment(self):
         """
         EF3: Changes in cameraAlignment
         DAT2.0 -> signal not available

         :return: EF gives back dict structure with data len and data itself
        """
         if self.dat2p0:
            horizon = self.mat["mudp"]["vehCal"]["vis_params"]["horizonKA"]
            yaw = self.mat["mudp"]["vehCal"]["vis_params"]["yawKA"]
            # print("NOT AVAILABLE IN DAT 2.0 DUE TO MISSING SIGNALS")

         else:
            horizon = self.mat['mudp']['vis']['vision_camera_alignment_info']['cameraAlignment']['horizon']
            yaw = self.mat['mudp']['vis']['vision_camera_alignment_info']['cameraAlignment']['yaw']

         data = []
         for name, sig in zip(['Horizon', 'Yaw'], [horizon, yaw]):
            indexes = []
            if not min(sig) == max(sig):
                for index in range(1, self.visLen):
                    if not sig[index - 1] == sig[index]:
                        indexes.append(index)
                data.append([self.groupIndexes(indexes), 'cameraAlignment changes',
                             name + ' changed', -1])
         return {'len': len(data), 'data': data}


    def ef_VRUWrongMatching(self):
        """
         EF4: VRUs matched with trcklets from curb, sidewalk, lamp posts etc

         DAT2.0 -> not operational

         :return: EF gives back dict structure with data len and data itself
                  Data contains incorrectly mapped tracklet ID and longitudinal
                  position + vision ID of an object and longitudinal position
         """
        if self.dat2p0:
            print("NOT AVAILABLE IN DAT 2.0 DUE TO MISSING SIGNALS")
            return

        else:
            visObs = self.mat['mudp']['vis']['vision_obstacles_info']
            tletReports = self.mat['mudp']['tlet']['tracker_outputs']['tracklet_reports']

            wrongMatchingSignals = {'pedOnPavement': visObs['visObs']['pedestrian_on_pavement'],
                                    'tletsMatched': visObs['visObs']['tlet_match'],
                                    'visLongPos': visObs['visObs']['long_pos'],
                                    'imageIndex': visObs['imageIndex'],
                                    'tletLongPos': tletReports['tracklets']['vcs_long_posn'],
                                    'lookIndex': tletReports['look_index'],
                                    'grabIndex': self.mat['mudp']['fus']
                                    ['log_data_fusion_tracker']
                                    ['status']['grabIndex']}
            data = []
            for i in range(15):
                events = []
                mappedTlets = []
                indexes = []
                for j in range(self.visLen):
                    if wrongMatchingSignals['pedOnPavement'][j][i]:
                        visPos = wrongMatchingSignals['visLongPos'][j][i]

                        # Mapped tlets are stored as 3D array
                        mappedTlets = wrongMatchingSignals['tletsMatched'][j][i][:]
                        imageIndex = wrongMatchingSignals['imageIndex'][j]

                        # Tracklets detections have different sampling than vis detections. Find matIndex of grabIndex that
                        # corresponds to imageIndex in order to synchronize detections. note: matIndex = index of element
                        # in .mat file
                        matIndexTlet = np.where(wrongMatchingSignals
                                                ['grabIndex'] == imageIndex)
                        matIndexTlet = matIndexTlet[0][0]

                        # Need two matIndexes of tracklets(one for LR detection, one for MR detections)
                        matIndexTlet = [matIndexTlet - 1, matIndexTlet]
                        mappedTletsLongPos = []
                        for trackletID in mappedTlets:
                            # tletID = 0 means no tlets were matched with object
                            if trackletID == 0:
                                continue
                            # Tracklets 65-128 are MR tracklets
                            if trackletID > 64:  # positions of MR tracklets are stored in odd matIndexes
                                trackletID -= 65
                                oddIndex = (matIndexTlet[0]
                                            if matIndexTlet[0] % 2 == 1
                                            else matIndexTlet[1])
                                # append list: [tletID, tletPos]
                                mappedTletsLongPos.append([trackletID + 65, wrongMatchingSignals['tletLongPos'][oddIndex]
                                                           [trackletID]])
                            else:
                                trackletID -= 1
                                # positions of LR tracklets are stored in even matIndexes
                                evenIndex = (matIndexTlet[0]
                                             if matIndexTlet[0] % 2 == 0
                                             else matIndexTlet[1])
                                mappedTletsLongPos.append([trackletID + 1,
                                                           wrongMatchingSignals['tletLongPos'][evenIndex]
                                                           [trackletID]])
                        # tletPos is a list with tletID and tlet long position. e.g. tletPos = [128, 11.23654]
                        for tletPos in mappedTletsLongPos:
                            if tletPos[1] < 1:
                                continue
                            if visPos - tletPos[1] > 2.5:  # Check if tracklets mapped with ped are 2.5m closer
                                indexes.append(j)
                                events.append([tletPos[0], tletPos[1], visPos])

                if indexes:
                    newIndexes = self.groupIndexes(indexes, maxGap=5)
                    for item in newIndexes:
                        # Find the index which item had in indexes list (before grouping)
                        eventIndex = indexes.index(item[0])

                        # Append data with frame + visID, tletID and tletPos + objectID (vision)
                        data.append([[item], 'visPos: ' + str(events[eventIndex][2]) + 'tletPos: ' +
                                     str(events[eventIndex][1]) + 'tletID: ' + str(events[eventIndex][0]), 'objectID: ' +
                                     str(i + 1)])

            return {'len': len(data), 'data': data}

    def ef_AEBShutdownCheck(self):

        """
        DAT2.0 -> signal not available
        :return:
        """

        if self.dat2p0:
            print("NOT AVAILABLE IN DAT 2.0 DUE TO MISSING SIGNALS")
            return

        else:

            mapping = ['POS_DIFF_KALMAN_VAL',
                       'ROI_DIFF_VC_FCV',
                       'FCV_FCW_TTC',
                       'CO_FOF_DIFF',
                       'DT_ERR',
                       'IMAGER_DATA_ROWS_COLS ',
                       'YAW_HORIZON_DEVIATION',
                       'CODE_CRC',
                       'OLD_EGODATA_LAT',
                       'OUT_OF_FOCUS',
                       'video_error_in_last_frame',
                       'temperature_out_of_limits',
                       'PLL_error',
                       'Parameter_CRC_error',
                       'Rolling_frame_counter',
                       'Vehicle_signal_CRC_error',
                       'Vehicle_signals_corrupted',
                       'FcvSigFfi']

            aeb_shutdown = self.mat['mudp']['vis']['vision_function_info']['aeb_shutdown']
            aeb_shutdown_reason = self.mat['mudp']['vis']['vision_function_info']['aeb_shutdown_reason']

            data = []
            for bit in range(18):  # bits 0-17
                flag = (aeb_shutdown_reason % 2 ** (bit + 1)) > (2 ** bit - 1)
                indexes = np.argwhere(flag).ravel()
                indexes = list(indexes)
                eventFinderID = ''
                comment = ''
                if indexes:
                    and_values = np.logical_and(aeb_shutdown[indexes], aeb_shutdown_reason[indexes])
                    xor_values = np.logical_xor(aeb_shutdown[indexes], aeb_shutdown_reason[indexes])
                    if all(and_values):
                        eventFinderID = mapping[bit]
                        comment = 'AEBShutdown & AEBShutdownReason.bit' + str(bit) + ' is set'
                    if all(xor_values):
                        if bit:
                            eventFinderID = mapping[bit]
                            comment = 'Only AEBShutdownReason.bit' + str(bit) + ' is set'
                        else:
                            eventFinderID = 'No reason'
                            comment = 'Only AEBShutdown is set'
                    data.append([self.groupIndexes(indexes), eventFinderID, comment])

            return {'len': len(data), 'data': data}

    def ef_uniqueDetectedCIPO(self):
        """
        EF looking for unique closest in path objects.
        Findsall objects reported by MobilEye as CIPO at first occurence.
        In comment longitudinal distance (dist), obstacle class (obj_type) and light conditions that is day/ dusk/ night
         (light) are provided in form of "dist|obj_type|light".
        Distance is measured relative to the front of car, not to the camera.

        DAT2.0 -> unique ID signal not available

        :return: dict structure with data len and data itself
        """

        if self.dat2p0:
            print("NOT AVAILABLE IN DAT 2.0 DUE TO MISSING SIGNALS")

            # cipo = self.mat["mudp"]["eyeq"]["Obstacles"]["vis_obstacles_msg_info"]["visObjects"]["visObs"]["isCipv"]
            # detection_status = self.mat["mudp"]["vis"]["vision_obstacles_info"]["visObjects"]["visObs"]["age"]
            # dist = self.mat["mudp"]["vis"]["vision_obstacles_info"]["visObjects"]["visObs"]["physicalState"]["longDistance"]
            # obj_type = self.mat["mudp"]["vis"]["vision_obstacles_info"]["visObjects"]["visObs"]["classification"]
            # light = self.mat["mudp"]["eyeq"]["Lights"]["vis_light_sensor_data_info"]["activeLightSensorInfo"]["ahbcAvailable"]
            # dist_camera_front_of_car = self.mat["mudp"]["lrosStream04"]["UDP_Gen1"]["LROS_X_Dist_FrtFasciaToCam"][0]



        else:
            cipo = self.mat['mudp']['vis']['vision_function_info']['visOnlyVehCIPO']
            detection_status = self.mat['mudp']['vis']['vision_obstacles_info']['visObs']['detection_status']
            dist = self.mat['mudp']['vis']['vision_obstacles_info']['visObs']['long_pos']
            obj_type = self.mat['mudp']['vis']['vision_obstacles_info']['visObs']['obstacle_class']
            light = self.mat['mudp']['vis']['vision_ahbc_info']['ahbcAvailable']
            dist_camera_front_of_car = \
                self.mat['mudp']['vfpState']['cals']['vision_params']['vehDependentParam']['referencePointX_mm'][0] / 1000.

        data = []
        indexes = []
        events = []
        prev_detection_status = cipo[0]

        for index in range(1, self.visLen):
            col_id = cipo[index] - 1
            if cipo[index] != 0:
                if detection_status[index, col_id] in (1, 2) and prev_detection_status == 0:
                    indexes.append(index)
                    events.append({'dist': dist[index + 1, col_id] - dist_camera_front_of_car,
                                   'obj_type': obj_type[index + 1, col_id],
                                   'light': light[index + 1]})
                    prev_detection_status = detection_status[index, col_id]
            else:
                prev_detection_status = 0

        if indexes:
            grouped_indexes = self.groupIndexes(indexes, maxGap=2)
            for item in grouped_indexes:
                event_index = indexes.index(item[0])

                data.append([[item], 'unique detected closest in path object',
                             str(events[event_index]['dist']) + '|' +
                             str(events[event_index]['obj_type']) + '|' +
                             str(events[event_index]['light'])])

        return {'len': len(data), 'data': data}

    def ef_pedestrianOrCyclistInPath(self, OFFSET=3):
        """
        EF looking for pedestrians and cyclist in path or within an arbitrary lateral width from predicted path.
        In comment longitudinal distance (dist), obstacle class (obj_type) and light conditions that is day/ dusk/ night
         (light) and also "debugging" aimed values: index, column number, grab index, TSEL index are provided in form
         of "dist|obj_type|light|index|column|grab_idx|tsel_idx".
        Distance is measured relative to the front of car, not to the camera.
        :param OFFSET: offset from the center of predicted path which extends area for searching.
        :return: dict structure with data len and data itself
        """
        if self.dat2p0:
            print("NOT AVAILABLE IN DAT 2.0 DUE TO MISSING SIGNALS")
            return

        else:
            detection_status = self.mat['mudp']['vis']['vision_obstacles_info']['visObs']['detection_status']
            dist = self.mat['mudp']['vis']['vision_obstacles_info']['visObs']['long_pos']
            obj_type = self.mat['mudp']['vis']['vision_obstacles_info']['visObs']['obstacle_class']
            light = self.mat['mudp']['vis']['vision_ahbc_info']['ahbcAvailable']
            lat_dist = self.mat['mudp']['vis']['vision_obstacles_info']['visObs']['lat_pos']
            dist_camera_front_of_car = \
                self.mat['mudp']['vfpState']['cals']['vision_params']['vehDependentParam']['referencePointX_mm'][0] / 1000.

            vis_index = self.mat['mudp']['vis']['vision_obstacles_info']['imageIndex']
            track_index = self.mat['mudp']['tsel']['commonETSELInfo']['grab_index']

            predicted_path_center_offset = self.mat['mudp']['tsel']['commonETSELInfo']['predictedPath']['predicted_path_lane_center_offset']
            predicted_path_width = self.mat['mudp']['tsel']['commonETSELInfo']['predictedPath']['predicted_path_lane_width']
            predicted_path_c0 = self.mat['mudp']['tsel']['commonETSELInfo']['predictedPath']['predicted_path_coef_c0']
            predicted_path_c1 = self.mat['mudp']['tsel']['commonETSELInfo']['predictedPath']['predicted_path_coef_c1']
            predicted_path_k = self.mat['mudp']['tsel']['commonETSELInfo']['predictedPath']['predicted_path_coef_k']

        data = []
        indexes = []
        events = []
        for col_id in range(15):
            for index in range(self.visLen):
                if self.isNewlyDetected(detection_status[index, col_id]) and self.isPedestrianOrCyclist(obj_type[index, col_id]):
                    grab_idx = vis_index[index]
                    tsel_idx = np.argwhere(track_index == grab_idx)[0, 0]
                    c0 = predicted_path_c0[tsel_idx]
                    c1 = predicted_path_c1[tsel_idx]
                    k = predicted_path_k[tsel_idx]
                    path_width = predicted_path_width[tsel_idx]
                    path_offset = predicted_path_center_offset[tsel_idx]

                    path_center = self.get_path_center_at_dist(dist[index, col_id], c0, c1, k, path_offset)
                    path_left_border = path_center - path_width/2 if OFFSET == 0 else path_center - OFFSET
                    path_right_border = path_center + path_width/2 if OFFSET == 0 else path_center + OFFSET

                    if path_left_border < lat_dist[index, col_id] < path_right_border:
                        indexes.append(index)
                        events.append({'dist': dist[index, col_id] - dist_camera_front_of_car,
                                       'obj_type': obj_type[index, col_id],
                                       'light': light[index],
                                       'index': index,   # DEBUG
                                       'column': col_id,   # DEBUG
                                       'grab_idx': grab_idx, # DEBUG
                                       'tsel_idx': tsel_idx # DEBUG
                                       })
        if indexes:
            grouped_indexes = self.groupIndexes(indexes, maxGap=2)
            for item in grouped_indexes:
                event_index = indexes.index(item[0])

                data.append([[item], 'pedestrian or cyclist in path',
                             str(events[event_index]['dist']) + '|' +
                             str(events[event_index]['obj_type']) + '|' +
                             str(events[event_index]['light']) + '|' +
                             str(events[event_index]['index']) + '|' +
                             str(events[event_index]['column']) + '|' +
                             str(events[event_index]['grab_idx']) + '|' +
                             str(events[event_index]['tsel_idx'])
                             ])

        return {'len': len(data), 'data': data}

    def ef_TTC_Comparison(self):
        if self.dat2p0:
            print("NOT AVAILABLE IN DAT 2.0 DUE TO MISSING SIGNALS")
            return

        else:
            VRU_flags = ['visOnlyVRUWarning', 'visOnlyVRUPartialBrake', 'visOnlyVRUBrakeUnconfirmed', 'visOnlyVRUBrake']
            vis = self.mat['mudp']['vis']['vision_function_info']
            visObs = self.mat['mudp']['vis']['vision_obstacles_info']['visObs']
            visIndex = vis['imageIndex']

            fus = self.mat['mudp']['fus']['log_data_fusion_tracker']
            host_accel = fus['veh']['host_long_accel']
            host_speed = fus['veh']['host_speed']
            fusIndex = fus['status']['grabIndex']

            data = []

            for flag in VRU_flags:
                eventFinderID = flag
                flag_matrix = vis[flag]
                indexes = list(np.argwhere(flag_matrix > 0).flatten())

                for event_indexes in self.groupIndexes(indexes):
                    id = event_indexes[0]
                    fusID = np.argwhere(fusIndex == visIndex[id]).flatten()[0]
                    if host_accel[fusID] > 0.3:
                        visObjID = flag_matrix[id]
                        delta_accel = host_accel[fusID] - visObs['long_accel'][id][visObjID - 1]
                        delta_vel = host_speed[fusID] - visObs['long_vel'][id][visObjID - 1]
                        delta_dist = visObs['long_pos'][id][visObjID - 1]
                        fus_ttc_vel = self.get_ttc_vel(delta_vel, delta_dist)
                        fus_ttc_accel = self.get_ttc_accel(delta_accel, delta_vel, delta_dist)
                        comment = ''.join(['fus_ttc_vel: ', str(fus_ttc_vel), ', fus_ttc_accel: ', str(fus_ttc_accel), ', host_accel: ', str(host_accel[fusID])])
                        data.append([self.groupIndexes(event_indexes), eventFinderID, comment, visObjID - 1])

            return {'len': len(data), 'data': data}

    def ef_RT_detection(self):
        if self.dat2p0:
            RTx_visID = self.mat['mudp']['tsel']['accMovingTracks']['track_id']
            RTx_long_dist = self.mat['mudp']['tsel']['accMovingTracks']['vcs_long_posn']
        else:
            #TODO: add CADS3.5 signals
            print("Only DAT2.0")
            return
        indexes = []
        data = []
        for col in range(RTx_visID.shape[-1]):
            indexes = []
            for index in range(len(RTx_visID)):
                # if classification[index, col] == 4 and classification[index-1, col] != 4:
                if (RTx_visID[index, col] != 0) or (RTx_long_dist[index, col] > 0.0):
                    indexes.append(index)
            data.append([self.groupIndexes(indexes), 'RTx detection', 'RT{} detection'.format(col +1), col])
        return  {'len': len(data), 'data': data}

    def ef_isPredicted(self):
        if self.dat2p0:
            bit_field = self.mat["mudp"]["eyeq"]["Obstacles"]["vis_obstacles_msg_info"]["visObjects"]["visObs"]["visObj_Pred_DrvArea_Close_byte"]
        else:
            # TODO: add CADS3.5 signals
            print("Only DAT2.0")
            return

        data = []
        for col in range(bit_field.shape[1]):
            indexes = []
            is_predicted_rows = np.argwhere(self.get_bit(number=bit_field[:, col],
                                                         bit_number_from_right=0))[:, 0]
            indexes += list(is_predicted_rows)

            if indexes:
                data.append([self.groupIndexes(indexes), 'isPredicted', 'isPredicted==1', col])
        return {'len': len(data), 'data': data}
