import numpy as np

from analystToolKit.lib.efsClasses import efsFrameClass


class tsrEFs(efsFrameClass.EFClass):
    def __init__(self):
        self.function = 'TSR'

    def appendDetails(self, dat2p0):

        errorNameList = []
        if dat2p0:
            self.header += ['ctimeu', 'signType', 'signValue', 'signSupplementalType1', 'signSupplementalType2',
                            'signRelevantDecision', 'signSuppConfidence1', 'signSuppConfidence2', 'f_signElectronic',
                            'f_signEmbedded', 'signLocation', 'signLocationLane', 'signLongPosition', 'signLatPosition',
                            'signConfidence', 'signID', 'currentMarket']
            for eventsDict in self.eventsDictList:
                index = int(np.where(self.visIndex == eventsDict['eventIndex'])[0][0])
                columnID = eventsDict['eventColumnID']
                try:
                    eventsDict['currentMarket'] = self.mat["mudp"]["eyeq"]["Signs"]["vis_traffic_signs_data_info"]["tsrInfo"]["currentMarket"][
                        index]
                except:
                    errorNameList.append('currentMarket')

                try:
                    eventsDict['ctimeu'] = self.mat["mudp"]["eyeq"]["Signs"]["header"]["cTime"][index]
                except:
                    errorNameList.append('ctimeu')

                # matrix signals
                if not columnID == -1:
                    try:
                        eventsDict['signID'] = \
                            self.mat["mudp"]["eyeq"]["Signs"]["vis_traffic_signs_data_info"]["tsrInfo"]["trafficSigns"]["signID"][
                                index][columnID]
                    except:
                        errorNameList.append('signID')

                    try:
                        eventsDict['signLongPosition'] = \
                            self.mat["mudp"]["eyeq"]["Signs"]["vis_traffic_signs_data_info"]["tsrInfo"]["trafficSigns"]['signLongPosition'][
                                index][columnID]
                    except:
                        errorNameList.append('signLongPosition')

                    try:
                        eventsDict['signLatPosition'] = \
                            self.mat["mudp"]["eyeq"]["Signs"]["vis_traffic_signs_data_info"]["tsrInfo"]["trafficSigns"]['signLatPosition'][
                                index][columnID]
                    except:
                        errorNameList.append('signLatPosition')

                    try:
                        eventsDict['signConfidence'] = \
                            self.mat["mudp"]["eyeq"]["Signs"]["vis_traffic_signs_data_info"]["tsrInfo"]["trafficSigns"]['signConfidence'][
                                index][columnID]
                    except:
                        errorNameList.append('signConfidence')

                    try:
                        eventsDict['signType'] = \
                            self.mat["mudp"]["eyeq"]["Signs"]["vis_traffic_signs_data_info"]["tsrInfo"]["trafficSigns"]['signType'][
                                index][columnID]
                    except:
                        errorNameList.append('signType')

                    try:
                        eventsDict['signSupplementalType1'] = \
                            self.mat["mudp"]["eyeq"]["Signs"]["vis_traffic_signs_data_info"]["tsrInfo"]["trafficSigns"]['signSupplementalType1'][
                                index][columnID]
                    except:
                        errorNameList.append('signSupplementalType1')

                    try:
                        eventsDict['signSupplementalType2'] = \
                            self.mat['mudp']['vis']['vision_traffic_sign_info']['tsrInfo']['trafficSigns']['signSupplementalType2'][
                                index][columnID]
                    except:
                        errorNameList.append('signSupplementalType2')

                    try:
                        eventsDict['signSuppConfidence1'] = \
                            self.mat["mudp"]["eyeq"]["Signs"]["vis_traffic_signs_data_info"]["tsrInfo"]["trafficSigns"]['signSuppConfidence1'][
                                index][columnID]
                    except:
                        errorNameList.append('signSuppConfidence1')

                    try:
                        eventsDict['signSuppConfidence2'] = \
                            self.mat["mudp"]["eyeq"]["Signs"]["vis_traffic_signs_data_info"]["tsrInfo"]["trafficSigns"]['signSuppConfidence2'][
                                index][columnID]
                    except:
                        errorNameList.append('signSuppConfidence2')

                    try:
                        eventsDict['f_signElectronic'] = 'Data not available in DAT 2.0'
                    except:
                        errorNameList.append('f_signElectronic')

                    try:
                        eventsDict['signRelevantDecision'] = \
                            self.mat["mudp"]["eyeq"]["Signs"]["vis_traffic_signs_data_info"]["tsrInfo"]["trafficSigns"]['signRelevantDecision'][
                                index][columnID]
                    except:
                        errorNameList.append('signRelevantDecision')

            return list(set(errorNameList))

        else:
            self.header += ['ctimeu', 'signType', 'signValue', 'signSupplementalType1', 'signSupplementalType2',
                            'signRelevantDecision', 'f_signElectronic', 'f_signEmbedded', 'signLocation',
                            'signLocationLane', 'signLongPosition', 'signLatPosition', 'signConfidence',
                            'signID', 'currentMarket']
            for eventsDict in self.eventsDictList:
                index = int(np.where(self.visIndex == eventsDict['eventIndex'])[0][0])
                columnID = eventsDict['eventColumnID']
                try:
                    eventsDict['currentMarket'] = \
                        self.mat['mudp']['vis']['vision_traffic_sign_info'][
                            'currentMarket'][index]
                except:
                    errorNameList.append('currentMarket')
                try:
                    eventsDict['ctimeu'] = \
                        self.mat['mudp']['vis']['header']['cTime'][index]
                except:
                    errorNameList.append('ctimeu')
                # matrix signals
                if not columnID == -1:
                    try:
                        eventsDict['signID'] = \
                            self.mat['mudp']['vis']['vision_traffic_sign_info'][
                                'trafficSigns']['signID'][
                                index][columnID]
                    except:
                        errorNameList.append('signID')
                    try:
                        eventsDict['signLongPosition'] = \
                            self.mat['mudp']['vis']['vision_traffic_sign_info'][
                                'trafficSigns']['signLongPosition'][index][columnID]
                    except:
                        errorNameList.append('signLongPosition')
                    try:
                        eventsDict['signLatPosition'] = \
                            self.mat['mudp']['vis']['vision_traffic_sign_info'][
                                'trafficSigns']['signLatPosition'][index][columnID]
                    except:
                        errorNameList.append('signLatPosition')
                    try:
                        eventsDict['signConfidence'] = \
                            self.mat['mudp']['vis']['vision_traffic_sign_info'][
                                'trafficSigns']['signConfidence'][index][columnID]
                    except:
                        errorNameList.append('signConfidence')
                    try:
                        eventsDict['signType'] = \
                            self.mat['mudp']['vis']['vision_traffic_sign_info'][
                                'trafficSigns']['signType'][
                                index][columnID]
                    except:
                        errorNameList.append('signType')
                    try:
                        eventsDict['signSupplementalType1'] = \
                            self.mat['mudp']['vis']['vision_traffic_sign_info'][
                                'trafficSigns']['signSupplementalType1'][index][
                                columnID]
                    except:
                        errorNameList.append('signSupplementalType1')
                    try:
                        eventsDict['signSupplementalType2'] = \
                            self.mat['mudp']['vis']['vision_traffic_sign_info'][
                                'trafficSigns']['signSupplementalType2'][index][
                                columnID]
                    except:
                        errorNameList.append('signSupplementalType2')
                    try:
                        eventsDict['signLocation'] = \
                            self.mat['mudp']['vis']['vision_traffic_sign_info'][
                                'trafficSigns']['signLocation'][index][columnID]
                    except:
                        errorNameList.append('signLocation')
                    try:
                        eventsDict['signLocationLane'] = \
                            self.mat['mudp']['vis']['vision_traffic_sign_info'][
                                'trafficSigns']['signLocationLane'][index][columnID]
                    except:
                        errorNameList.append('signLocationLane')
                    try:
                        eventsDict['signValue'] = \
                            self.mat['mudp']['vis']['vision_traffic_sign_info'][
                                'trafficSigns']['signValue'][index][columnID]
                    except:
                        errorNameList.append('signValue')
                    try:
                        eventsDict['f_signElectronic'] = \
                            self.mat['mudp']['vis']['vision_traffic_sign_info'][
                                'trafficSigns']['f_signElectronic'][index][columnID]
                    except:
                        errorNameList.append('f_signElectronic')
                    try:
                        eventsDict['signRelevantDecision'] = \
                            self.mat['mudp']['vis']['vision_traffic_sign_info'][
                                'trafficSigns']['signRelevantDecision'][index][
                                columnID]
                    except:
                        errorNameList.append('signRelevantDecision')
                    try:
                        eventsDict['f_signEmbedded'] = \
                            self.mat['mudp']['vis']['vision_traffic_sign_info'][
                                'trafficSigns']['f_signEmbedded'][index][columnID]
                    except:
                        errorNameList.append('f_signEmbedded')

            return list(set(errorNameList))


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
        imageIndex = self.mat['mudp']['vis']['vision_function_info'][
            'imageIndex']

        data = []
        indexes = []
        for index in range(self.visLen):
            if index % 2 == 0:
                indexes.append(index)

        data.append([self.groupIndexes(indexes), 'EF_template(ID)',
                     'This is template event finder(Comment)', '-1'])
        return {'len': len(data), 'data': data}

    def ef_SignConfidence1(self, findAll=True):
        """
        EF 1: Sign confidence equal 1.0
        EF checks for confidence conditions. If index is valid,it is added to indexes list, as it contains wanted event.

        :return: EF gives back dict structure with data len and data itself
        """

        if self.dat2p0:
            conf_matrix = \
                self.mat["mudp"]["eyeq"]["Signs"]["vis_traffic_signs_data_info"]["tsrInfo"]["trafficSigns"]['signConfidence']
            sign_types_matrix = \
                self.mat["mudp"]["eyeq"]["Signs"]["vis_traffic_signs_data_info"]["tsrInfo"]["trafficSigns"]['signType']
            sign_types_to_find_matrix = np.zeros_like(sign_types_matrix, bool)

            if findAll:
                sign_types_to_find_list = list(range(380))
            else:
                # the following may be edit. See PDD documentation:
                # http://confluenceprod1.delphiauto.net:8090/display/DSG/MobilEye+-+Aptiv+Interface+DAT2.0+project?preview=/77496484/77496491/ADAS_ECU_SPI_EyeQ4_SW6_0.pdf
                sign_types_to_find_list = [0,  # Speed Limit 10',
                                           1  # Speed Limit 20',
                                           ]

        else:
            conf_matrix = \
                self.mat['mudp']['vis']['vision_traffic_sign_info']['trafficSigns']['signConfidence']
            sign_types_matrix = \
                self.mat['mudp']['vis']['vision_traffic_sign_info']['trafficSigns']['signType']
            sign_types_to_find_matrix = np.zeros_like(sign_types_matrix, bool)

            sign_types_to_find_list = [1,  # SPEED_LIMIT_START',
                                       2,  # SPEED_LIMIT_END',
                                       5,  # HIGHWAY_START',
                                       6,  # HIGHWAY_END',
                                       7,  # FREEWAY_START',
                                       8,  # FREEWAY_END',
                                       11,  # TOWN_START',
                                       12,  # TOWN_END',
                                       13,  # LOW_SPEED_AREA_START',
                                       14,  # LOW_SPEED_AREA_END',
                                       16,  # NO_OVERTAKING_START',
                                       17,  # NO_OVERTAKING_END',
                                       19,  # ADVISORY_SPEED_LIMIT_START',
                                       24,  # NO_OVERTAKING_TRUCK_START',
                                       25,  # NO_OVERTAKING_TRUCK_END',
                                       26,  # ROUND_ABOUT',
                                       27]  # END_OF_ALL',

        # generating matrix with accepted sign types

        for s_type in sign_types_to_find_list:
            sign_types_to_find_matrix |= sign_types_matrix == s_type
        # matrix with confidence == 1.00
        # print(np.where(conf_matrix>0))
        conf1_matrix_bool = conf_matrix == 1.0
        # signs of listed type which reached confidence 1.00
        conf1_type_matrix_bool = np.logical_and(conf1_matrix_bool,
                                                sign_types_to_find_matrix)
        conf1_matrix = np.argwhere(conf1_type_matrix_bool)

        data = []
        for i in range(sign_types_matrix.shape[-1]):
            indexes = []
            # indexes.append(i)
            index = np.argwhere(conf1_matrix[:, 1] == i)
            for each in conf1_matrix[:, 0][index]:
                indexes += list(each)
            if indexes:
                data.append([self.groupIndexes(indexes), 'sign_conf_1',
                             'signConfidence == 1.00',i])
        return {'len': len(data), 'data': data}


    def ef_CurrentMarketChanged(self):
        """
        EF 2: Current market changes its value
        EF checks for confidence conditions. If index is valid,it is added to indexes list, as it contains wanted event.

        :return: EF gives back dict structure with data len and data itself
        """
        if self.dat2p0:
            current_market_matrix = \
                self.mat["mudp"]["eyeq"]["Signs"]["vis_traffic_signs_data_info"]["tsrInfo"]["currentMarket"]
        else:
            current_market_matrix = \
                self.mat['mudp']['vis']['vision_traffic_sign_info']['currentMarket']

        data = []
        diff_current_market_matrix = np.diff(current_market_matrix)
        if np.any(diff_current_market_matrix):
            indexes = np.nonzero(diff_current_market_matrix)
            if indexes:
                data.append([self.groupIndexes(indexes), 'market_change',
                             'currentMarket changes its value', -1])
        return {'len': len(data), 'data': data}


    def ef_SignConfidanceDrop_unfinished(self):
        """
        EF 3: Sign confidence drops from value lesser than 1.00 to 0.00
        EF checks for confidence conditions. If index is valid,it is added to indexes list, as it contains wanted event.

        :return: EF gives back dict structure with data len and data itself
        """
        if self.dat2p0:
            # TODO (low priority)
            print("Not ready yet.")
            return

        confMatrix = \
            self.mat['mudp']['vis']['vision_traffic_sign_info'][
                'trafficSigns'][
                'signConfidence']
        data = []

        for i in range(8):
            indexes = []
            confdrop_column_logical = np.logical_and(
                np.diff(confMatrix[:, i]) < 0.,
                np.diff(confMatrix[:, i]) > -1.)
            indexes_list_of_lists = np.argwhere(confdrop_column_logical)
            indexes = [n[0] for n in indexes_list_of_lists]
            # todo unfinished
            # index = np.argwhere(confOneMatrix[:, 1] == i)
            # for each in confOneMatrix[:, 0][index]:
            #     indexes += list(each)
            if indexes:
                data.append([self.groupIndexes(indexes), 'sign_conf_drop',
                             'signConfidence drop',
                             i])
        return {'len': len(data), 'data': data}


    def ef_StopYieldSigns(self):
        """
        EF 1: Sign confidence equal 1.0
        EF checks for confidence conditions. If index is valid,it is added to indexes list, as it contains wanted event.

        :return: EF gives back dict structure with data len and data itself
        """
        if self.dat2p0:
            conf_matrix = self.mat["mudp"]["eyeq"]["Signs"]["vis_traffic_signs_data_info"]["tsrInfo"]["trafficSigns"]['signConfidence']
            sign_types_matrix = self.mat["mudp"]["eyeq"]["Signs"]["vis_traffic_signs_data_info"]["tsrInfo"]["trafficSigns"]['signType']
            sign_types_to_find_list = [168,  # 'YIELD',
                                         210,  # 'STOP',
                                         199,  # 'NO_ENTRANCE',
                                         250,  # 'NO_ENTRANCE',
                                         52    # 'Pedestrian Crossing'
                                         ]
        else:
            conf_matrix = self.mat['mudp']['vis']['vision_traffic_sign_info']['trafficSigns']['signConfidence']
            sign_types_matrix = self.mat['mudp']['vis']['vision_traffic_sign_info']['trafficSigns']['signType']

            sign_types_to_find_list = [10,  # 'YIELD',
                                       15,  # 'STOP',
                                       18,  # 'NO_ENTRANCE',
                                       20]  # 'NO_ENTRANCE_ALERT',

        sign_types_to_find_matrix = np.zeros_like(sign_types_matrix, bool)
        data = []

        # generating matrix with accepted sign types
        for s_type in sign_types_to_find_list:
            sign_types_to_find_matrix |= sign_types_matrix == s_type
        # matrix with confidence == 1.00
        conf1_matrix_bool = conf_matrix == 1
        # signs of listed type which reached confidence 1.00
        conf1_type_matrix_bool = np.logical_and(conf1_matrix_bool,
                                                sign_types_to_find_matrix)
        conf1_matrix = np.argwhere(conf1_type_matrix_bool)
        for i in range(conf_matrix.shape[-1]):
            indexes = []
            index = np.argwhere(conf1_matrix[:, 1] == i)
            for each in conf1_matrix[:, 0][index]:
                indexes += list(each)
            if indexes:
                data.append([self.groupIndexes(indexes), 'sign_yield_stop_wwa',
                             'Yield, STOP, WWA',
                             i])
        return {'len': len(data), 'data': data}


    def ef_VelOverSignLimit(self, THRESHOLD=6):
        """
        EF 5: Speed limit start signs treated as relevant when they should not

        EF checks if the difference between vehicle speed and detected speed limit sign value is bigger than specified threshold
        Mostly this EF finds falsely detected low speed limit signs when host speed is high

        """
        if self.dat2p0:
            conf_matrix = self.mat["mudp"]["eyeq"]["Signs"]["vis_traffic_signs_data_info"]["tsrInfo"]["trafficSigns"]['signConfidence']
            sign_types_matrix = self.mat["mudp"]["eyeq"]["Signs"]["vis_traffic_signs_data_info"]["tsrInfo"]["trafficSigns"]['signType']
            relevant_decision_matrix = self.mat["mudp"]["eyeq"]["Signs"]["vis_traffic_signs_data_info"]["tsrInfo"]["trafficSigns"]['signRelevantDecision']
            # sign_value =
            current_market = self.mat["mudp"]["eyeq"]["Signs"]["vis_traffic_signs_data_info"]["tsrInfo"]["currentMarket"][0]
            veh_speed_list = self.mat["mudp"]["eyeq"]["SRP"]["vis_srp_msg_info"]["visSRP"]["vehicleVelocity"]

            sign_types_to_find_dict = {0: 10,  # signType=0 => Speed limit 10
                                       1: 20,   # signType=1 => Speed limit 20
                                       2: 30,  # ... see PDD documentation:
            # http://confluenceprod1.delphiauto.net:8090/display/DSG/MobilEye+-+Aptiv+Interface+DAT2.0+project?preview=/77496484/77496491/ADAS_ECU_SPI_EyeQ4_SW6_0.pdf
                                       3: 40,
                                       4: 50,
                                       5: 60,
                                       6: 70,
                                       7: 80,
                                       8: 90,
                                       9: 100,
                                       10: 110,
                                       11: 120,
                                       12: 130,
                                       13: 140,
                                       100: 5,
                                       101: 15,
                                       102: 25,
                                       103: 35,
                                       104: 45,
                                       105: 55,
                                       106: 65,
                                       107: 75,
                                       108: 85,
                                       109: 95,
                                       110: 105,
                                       111: 115,
                                       112: 125,
                                       113: 135,
                                       114: 145,
                                       }

            sign_types_to_find_list = list(sign_types_to_find_dict.keys())
        else:
            conf_matrix = self.mat['mudp']['vis']['vision_traffic_sign_info']['trafficSigns']['signConfidence']
            sign_types_matrix = self.mat['mudp']['vis']['vision_traffic_sign_info']['trafficSigns']['signType']
            relevant_decision_matrix = self.mat['mudp']['vis']['vision_traffic_sign_info']['trafficSigns']['signRelevantDecision']
            sign_value = self.mat['mudp']['vis']['vision_traffic_sign_info']['trafficSigns']['signValue']
            current_market = self.mat['mudp']['vis']['vision_traffic_sign_info']['currentMarket'][0]
            veh_speed_list = self.mat['mudp']['vis']['vision_vehicle_info']['vehicleVelocity']

            sign_types_to_find_list = [1]  # SPEED_LIMIT_START'

        if current_market in [2, 4, 8, 11]:  # scaling veh_speed for mph or kph
            veh_speed_list = veh_speed_list * 3600.0 / 1609.0
            threshold = THRESHOLD / 1.6  # threshold for mph
        else:
            veh_speed_list = veh_speed_list * 3600.0 / 1000.0
            threshold = THRESHOLD  # kph threshold

        sign_types_to_find_matrix = np.zeros_like(sign_types_matrix, bool)

        # generating matrix with accepted sign types
        for s_type in sign_types_to_find_list:
            sign_types_to_find_matrix |= sign_types_matrix == s_type
        # matrix with confidence == 1.00
        conf1_matrix_bool = conf_matrix == 1
        # signs of listed type which reached confidence 1.00
        conf1_type_matrix_bool = np.logical_and(conf1_matrix_bool,
                                                sign_types_to_find_matrix)

        conf1_type_relevant_bool = np.logical_and(conf1_type_matrix_bool,
                                                  relevant_decision_matrix == 0)
        # array containing Relevant,conf1,speed_limit signs
        conf1_matrix = np.argwhere(conf1_type_relevant_bool)

        data = []
        for i in range(conf_matrix.shape[-1]):
            indexes = []
            index = np.argwhere(conf1_matrix[:, 1] == i)
            for each in conf1_matrix[:, 0][index]:
                if self.dat2p0:
                    if (veh_speed_list[each] - sign_types_to_find_dict[sign_types_matrix[each, i][0]]) > threshold:
                        indexes += list(each)
                else:
                    if (veh_speed_list[each] - sign_value[each, i]) > threshold:
                        indexes += list(each)
            if indexes:
                data.append([self.groupIndexes(indexes), 'speed difference',
                             'Vehicle speed much bigger than detected SL sign value',
                             i])
        return {'len': len(data), 'data': data}

    def ef_Spd_limit_30_zone(self):

        if self.dat2p0:
            # TODO (low priority)
            print("Not ready yet.")
            return
        tsr = self.mat['mudp']['vis']['vision_traffic_sign_info']['trafficSigns']
        s_type = tsr['signType']
        s_conf = tsr['signConfidence']
        s_val = tsr['signValue']
        s_supl_type1 = tsr['signSupplementalType1']
        s_supl_type2 = tsr['signSupplementalType2']

        s_type = np.array(s_type == 1, int)
        s_val = np.array(s_val == 30, int)
        s_conf = np.array(s_conf == 1, int)
        s_supl_type1 = np.array(s_supl_type1 == 13, int)
        s_supl_type2 = np.array(s_supl_type2 == 13, int)
        s_supl = s_supl_type1 | s_supl_type2  # Supl_1 OR supl_2

        to_find = s_supl * s_type * s_val * s_conf  # True if all arrays are True
        data = []

        if not np.any(to_find):
            return {'len': len(data), 'data': data}
        else:
            indexes = np.argwhere(to_find)[:,0].tolist()
            for index in indexes:
                data.append([self.groupIndexes([index]), '30 kph ZONE', '', -1])

        return {'len': len(data), 'data': data}