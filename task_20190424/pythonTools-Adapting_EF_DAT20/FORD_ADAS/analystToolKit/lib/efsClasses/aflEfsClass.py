import numpy as np

from analystToolKit.lib.efsClasses import efsFrameClass


class aflEFs(efsFrameClass.EFClass):
    def __init__(self):
        self.function = 'AFL'

    def appendDetails(self, dat2p0):
        if dat2p0:
            self.header += ['ahbcAvailable', 'approachingJunction', 'beamRequest', 'bottomAngle', 'classification',
                            'clearFieldOfView', 'constructionArea', 'eventsDetectedByte', 'f_oncomingLaneNotDark',
                            'highwayDetected', 'id', 'isTruck', 'leftAngle', 'longPos', 'numOfActiveLightSpots',
                            'pixelBottom', 'pixelLeft', 'pixelRight', 'pixelTop', 'rightAngle', 'topAngle', 'vdID',
                            'villageDetected']
            errorNameList = []
            for eventsDict in self.eventsDictList:
                index = int(np.where(self.visIndex == eventsDict['eventIndex'])[0][0])
                columnID = eventsDict['eventColumnID']
                try:
                    eventsDict['clearFieldOfView'] = \
                        self.mat["mudp"]["eyeq"]["Lights"]["vis_light_sensor_data_info"]["activeLightSensorInfo"]["clearFieldOfView"][index]
                except:
                    errorNameList.append('clearFieldOfView')

                try:
                    eventsDict['f_oncomingLaneNotDark'] = self.get_bit(
                        self.mat["mudp"]["eyeq"]["Lights"]["vis_light_sensor_data_info"]["activeLightSensorInfo"]["light_Sensor_Detections_byte"][index],
                        bit_number_from_right=3
                    )
                except:
                    errorNameList.append('f_oncomingLaneNotDark')

                try:
                    eventsDict['approachingJunction'] = self.get_bit(
                        self.mat["mudp"]["eyeq"]["Lights"]["vis_light_sensor_data_info"]["activeLightSensorInfo"]["light_Sensor_Detections_byte"][index],
                        bit_number_from_right=4)
                except:
                    errorNameList.append('approachingJunction')

                try:
                    eventsDict['highwayDetected'] = self.get_bit(
                        self.mat["mudp"]["eyeq"]["Lights"]["vis_light_sensor_data_info"]["activeLightSensorInfo"]["light_Sensor_Detections_byte"][index],
                        bit_number_from_right=1)
                except:
                    errorNameList.append('highwayDetected')

                # # maybe will turn out to be useful in future? For now it is replaced by the numOfActiveLightSpots
                # (See below)
                # try:
                #     # same as oncoming vehicle?
                #     eventsDict['oncomingSpots'] = self.get_bit(
                #         self.mat['mudp']['vis']['vision_active_light_sensor_info']['activeLightSensorInfo'][
                #             'events_Detected_byte'][index],
                #         1)
                # except:
                #     errorNameList.append('oncomingSpots')
                # try:
                #     # same as preceding vehicle
                #     eventsDict['precedingSpots'] = self.get_bit(
                #         self.mat['mudp']['vis']['vision_active_light_sensor_info']['activeLightSensorInfo'][
                #             'events_Detected_byte'][index],
                #         2)
                #     eventsDict['precedingSpots'] = \
                #         self.mat['mudp']['vis']['vision_active_light_sensor_info']['activeLightSensorInfo'][
                #             'events_Detected_byte'][index]
                # except:
                #     errorNameList.append('precedingSpots')
                try:
                    eventsDict['numOfActiveLightSpots'] = \
                        self.mat["mudp"]["eyeq"]["Lights"]["vis_light_sensor_data_info"]["activeLightSensorInfo"]["numOfActiveLightSpots"][index]
                except:
                    errorNameList.append('numOfActiveLightSpots')

                try:
                    eventsDict['villageDetected'] = self.get_bit(
                        self.mat["mudp"]["eyeq"]["Lights"]["vis_light_sensor_data_info"]["activeLightSensorInfo"]["light_Sensor_Detections_byte"][index],
                        bit_number_from_right=2)
                except:
                    errorNameList.append('villageDetected')

                try:
                    eventsDict['ahbcAvailable'] = \
                        self.mat["mudp"]["eyeq"]["Lights"]["vis_light_sensor_data_info"]["activeLightSensorInfo"]["ahbcAvailable"][index]
                except:
                    errorNameList.append('ahbcAvailable')

                try:
                    eventsDict['beamRequest'] = \
                        self.mat["mudp"]["eyeq"]["Lights"]["vis_light_sensor_data_info"]["activeLightSensorInfo"]["beamRequest"][index]
                except:
                    errorNameList.append('beamRequest')

                try:  # now it's a bitfield. Needs to be decoded in post-processing
                    eventsDict['eventsDetectedByte'] = \
                        self.mat["mudp"]["eyeq"]["Lights"]["vis_light_sensor_data_info"]["activeLightSensorInfo"]["events_Detected_byte"][index]
                except:
                    errorNameList.append('eventsDetectedByte')

                try:
                    eventsDict['constructionArea'] = self.get_bit(
                        self.mat["mudp"]["eyeq"]["Road"]["vis_road_data_info"]["roadInfo"]["roadMarkerInfo"]["roadMarker_ambigLinePatt_const_byte"][index],
                        bit_number_from_right=2)
                except:
                    errorNameList.append('constructionArea')

                # matrix signals
                if not columnID == -1:
                    try:
                        eventsDict['classification'] = \
                            self.mat["mudp"]["eyeq"]["Lights"]["vis_light_sensor_data_info"]["activeLightSensorInfo"]["activeLightSpots"]["classification"][
                                index][columnID]
                    except:
                        errorNameList.append('classification')

                    try:
                        eventsDict['id'] = \
                            self.mat["mudp"]["eyeq"]["Lights"]["vis_light_sensor_data_info"]["activeLightSensorInfo"]["activeLightSpots"]["id"][
                                index][columnID]
                    except:
                        errorNameList.append('id')

                    try:
                        eventsDict['longPos'] = \
                            self.mat["mudp"]["eyeq"]["Lights"]["vis_light_sensor_data_info"]["activeLightSensorInfo"]["activeLightSpots"]["longPos"][
                                index][columnID]
                    except:
                        errorNameList.append('longPos')

                    try:
                        eventsDict['bottomAngle'] = \
                            self.mat["mudp"]["eyeq"]["Lights"]["vis_light_sensor_data_info"]["activeLightSensorInfo"]["activeLightSpots"]["bottomAngle"][
                                index][columnID]
                    except:
                        errorNameList.append('bottomAngle')

                    try:
                        eventsDict['leftAngle'] = \
                            self.mat["mudp"]["eyeq"]["Lights"]["vis_light_sensor_data_info"]["activeLightSensorInfo"]["activeLightSpots"]["leftAngle"][
                                index][columnID]
                    except:
                        errorNameList.append('leftAngle')

                    try:
                        eventsDict['rightAngle'] = \
                            self.mat["mudp"]["eyeq"]["Lights"]["vis_light_sensor_data_info"]["activeLightSensorInfo"]["activeLightSpots"]["rightAngle"][
                                index][columnID]
                    except:
                        errorNameList.append('rightAngle')

                    try:
                        eventsDict['topAngle'] = \
                            self.mat["mudp"]["eyeq"]["Lights"]["vis_light_sensor_data_info"]["activeLightSensorInfo"]["activeLightSpots"]["topAngle"][
                                index][columnID]
                    except:
                        errorNameList.append('topAngle')

                    try:
                        eventsDict['pixelBottom'] = \
                            self.mat["mudp"]["eyeq"]["Lights"]["vis_light_sensor_data_info"]["activeLightSensorInfo"]["activeLightSpots"]["pixelBottom"][
                                index][columnID]
                    except:
                        errorNameList.append('pixelBottom')

                    try:
                        eventsDict['pixelLeft'] = \
                            self.mat["mudp"]["eyeq"]["Lights"]["vis_light_sensor_data_info"]["activeLightSensorInfo"]["activeLightSpots"]["pixelLeft"][
                                index][columnID]
                    except:
                        errorNameList.append('pixelLeft')

                    try:
                        eventsDict['pixelRight'] = \
                            self.mat["mudp"]["eyeq"]["Lights"]["vis_light_sensor_data_info"]["activeLightSensorInfo"]["activeLightSpots"]["pixelRight"][
                                index][columnID]
                    except:
                        errorNameList.append('pixelRight')

                    try:
                        eventsDict['pixelTop'] = \
                            self.mat["mudp"]["eyeq"]["Lights"]["vis_light_sensor_data_info"]["activeLightSensorInfo"]["activeLightSpots"]["pixelTop"][
                                index][columnID]
                    except:
                        errorNameList.append('pixelTop')

                    try:
                        eventsDict['isTruck'] = \
                            self.mat["mudp"]["eyeq"]["Lights"]["vis_light_sensor_data_info"]["activeLightSensorInfo"]["activeLightSpots"]["isTruck"][
                                index][columnID]
                    except:
                        errorNameList.append('isTruck')

                    try:
                        eventsDict['vdID'] = \
                            self.mat["mudp"]["eyeq"]["Lights"]["vis_light_sensor_data_info"]["activeLightSensorInfo"]["activeLightSpots"]["vdID"][
                                index][columnID]
                    except:
                        errorNameList.append('vdID')

            return list(set(errorNameList))

        else:
            self.header += ['adaptiveRequest', 'ahbcAvailable', 'angleVertical', 'angleWidth', 'approachingJunction',
                            'beamRequest', 'classification', 'clearFieldOfView', 'closestObjectDistance',
                            'constructionArea', 'eventsDetected', 'f_oncomingLaneNotDark', 'gridFrequency',
                            'highwayDetected', 'highwayGuardrails', 'horizontalAngle', 'id', 'longPos',
                            'oncomingSpots', 'precedingSpots', 'verticalAngle', 'villageDetected']
            errorNameList = []
            for eventsDict in self.eventsDictList:
                index = int(np.where(self.visIndex == eventsDict['eventIndex'])[0][0])
                columnID = eventsDict['eventColumnID']
                try:
                    eventsDict['clearFieldOfView'] = \
                        self.mat['mudp']['vis']['vision_active_light_sensor_info']['clearFieldOfView'][index]
                except:
                    errorNameList.append('clearFieldOfView')
                try:
                    eventsDict['f_oncomingLaneNotDark'] = \
                        self.mat['mudp']['vis']['vision_active_light_sensor_info']['f_oncomingLaneNotDark'][index]
                except:
                    errorNameList.append('f_oncomingLaneNotDark')
                try:
                    eventsDict['approachingJunction'] = \
                        self.mat['mudp']['vis']['vision_active_light_sensor_info']['approachingJunction'][index]
                except:
                    errorNameList.append('approachingJunction')
                try:
                    eventsDict['gridFrequency'] = \
                        self.mat['mudp']['vis']['vision_active_light_sensor_info']['gridFrequency'][index]
                except:
                    errorNameList.append('gridFrequency')
                try:
                    eventsDict['highwayDetected'] = \
                        self.mat['mudp']['vis']['vision_active_light_sensor_info']['highwayDetected'][index]
                except:
                    errorNameList.append('highwayDetected')
                try:
                    eventsDict['highwayGuardrails'] = \
                        self.mat['mudp']['vis']['vision_active_light_sensor_info']['highwayGuardrails'][index]
                except:
                    errorNameList.append('highwayGuardrails')
                try:
                    eventsDict['oncomingSpots'] = \
                        self.mat['mudp']['vis']['vision_active_light_sensor_info']['oncomingSpots'][index]
                except:
                    errorNameList.append('oncomingSpots')
                try:
                    eventsDict['precedingSpots'] = \
                        self.mat['mudp']['vis']['vision_active_light_sensor_info']['precedingSpots'][index]
                except:
                    errorNameList.append('precedingSpots')
                try:
                    eventsDict['villageDetected'] = \
                        self.mat['mudp']['vis']['vision_active_light_sensor_info']['villageDetected'][index]
                except:
                    errorNameList.append('villageDetected')
                try:
                    eventsDict['adaptiveRequest'] = \
                        self.mat['mudp']['vis']['vision_ahbc_info']['adaptiveRequest'][index]
                except:
                    errorNameList.append('adaptiveRequest')
                try:
                    eventsDict['ahbcAvailable'] = \
                        self.mat['mudp']['vis']['vision_ahbc_info']['ahbcAvailable'][index]
                except:
                    errorNameList.append('ahbcAvailable')
                try:
                    eventsDict['angleVertical'] = \
                        self.mat['mudp']['vis']['vision_ahbc_info']['angleVertical'][index]
                except:
                    errorNameList.append('angleVertical')
                try:
                    eventsDict['beamRequest'] = \
                        self.mat['mudp']['vis']['vision_ahbc_info']['beamRequest'][index]
                except:
                    errorNameList.append('beamRequest')
                try:
                    eventsDict['closestObjectDistance'] = \
                        self.mat['mudp']['vis']['vision_ahbc_info']['closestObjectDistance'][index]
                except:
                    errorNameList.append('closestObjectDistance')
                try:
                    eventsDict['eventsDetected'] = \
                        self.mat['mudp']['vis']['vision_ahbc_info']['eventsDetected'][index]
                except:
                    errorNameList.append('eventsDetected')
                try:
                    eventsDict['constructionArea'] = \
                        self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['f_constructionArea'][index]
                except:
                    errorNameList.append('constructionArea')
                # matrix signals
                if not columnID == -1:
                    try:
                        eventsDict['angleWidth'] = \
                            self.mat['mudp']['vis']['vision_active_light_sensor_info']['activeLightSpots']['angleWidth'][
                                index][columnID]
                    except:
                        errorNameList.append('angleWidth')
                    try:
                        eventsDict['classification'] = \
                            self.mat['mudp']['vis']['vision_active_light_sensor_info']['activeLightSpots'][
                                'classification'][
                                index][columnID]
                    except:
                        errorNameList.append('classification')
                    try:
                        eventsDict['horizontalAngle'] = \
                            self.mat['mudp']['vis']['vision_active_light_sensor_info']['activeLightSpots'][
                                'horizontalAngle'][
                                index][columnID]
                    except:
                        errorNameList.append('horizontalAngle')
                    try:
                        eventsDict['id'] = \
                            self.mat['mudp']['vis']['vision_active_light_sensor_info']['activeLightSpots']['id'][
                                index][columnID]
                    except:
                        errorNameList.append('id')
                    try:
                        eventsDict['longPos'] = \
                            self.mat['mudp']['vis']['vision_active_light_sensor_info']['activeLightSpots']['longPos'][
                                index][columnID]
                    except:
                        errorNameList.append('longPos')
                    try:
                        eventsDict['verticalAngle'] = \
                            self.mat['mudp']['vis']['vision_active_light_sensor_info']['activeLightSpots']['verticalAngle'][
                                index][columnID]
                    except:
                        errorNameList.append('verticalAngle')

            return list(set(errorNameList))


    # HELPERS FUNCTIONS #
    def bitget(self, x, nbit):
        x >>= nbit - 1
        return x % 2

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

        data.append([self.groupIndexes(indexes), 'EF_template(ID)', 'This is template event finder(Comment)', '-1'])
        return {'len': len(data), 'data': data}


    def ef_ElectronicSignsAsLights(self, HEIGHT_THRESHOLD=640, MAX_GAP=40, MIN_PEAKS=1, hOffset=10, vOffset=10):
        """
        EF 1: Electronic signs/Traffic lights

        :return: EF gives back dict structure with data len and data itself
        """
        if self.dat2p0:
            # TODO (low priority)
            print("Not ready yet.")
            return

        lsBottom = self.mat['mudp']['vis']['vision_active_light_sensor_info']['activeLightSpots']['pixelBottom']
        lsTop = self.mat['mudp']['vis']['vision_active_light_sensor_info']['activeLightSpots']['pixelTop']
        lsLeft = self.mat['mudp']['vis']['vision_active_light_sensor_info']['activeLightSpots']['pixelLeft']
        lsRight = self.mat['mudp']['vis']['vision_active_light_sensor_info']['activeLightSpots']['pixelRight']
        objBottom = self.mat['mudp']['vis']['vision_obstacles_info']['visObs']['pixel_bottom']
        objTop = self.mat['mudp']['vis']['vision_obstacles_info']['visObs']['pixel_top']
        objLeft = self.mat['mudp']['vis']['vision_obstacles_info']['visObs']['pixel_left']
        objRight = self.mat['mudp']['vis']['vision_obstacles_info']['visObs']['pixel_right']
        city = self.mat['mudp']['vis']['vision_active_light_sensor_info']['villageDetected']
        highway = self.mat['mudp']['vis']['vision_active_light_sensor_info']['highwayDetected']
        classification = \
            self.mat['mudp']['vis']['vision_active_light_sensor_info']['activeLightSpots']['classification']
        data = []

        if 'approachingJunction' in dict.keys(self.mat['mudp']['vis']['vision_active_light_sensor_info']):
            trafficSignal = self.mat['mudp']['vis']['vision_active_light_sensor_info']['approachingJunction']
            aj = 1
        else:
            trafficSignal = np.zeros(self.visLen)
            aj = 0
        comment = ''

        # vertical and horizontal centroid position of each lightspot
        hLsPos = (lsLeft + lsRight) // 2
        vLsPos = (lsTop + lsBottom) // 2
        # acceptable offset for cover
        indexes = []

        trafficValid = (aj == 1) * (trafficSignal > 0) + (aj == 0) * np.any(classification == 7, axis=1)
        toBeChecked = ((city == 0) + (highway == 1)) * (~ trafficValid)

        for index in range(self.visLen):
            if toBeChecked[index]:
                event_in_line = 0
                for j in range(10):
                    if vLsPos[index][j] > HEIGHT_THRESHOLD:
                        covered = 0
                        for k in range(15):  # sprawdz pokrycie przez obiekty wizyjne
                            if objBottom[index][k] - vOffset <= vLsPos[index][j] <= objTop[index][k] + vOffset and \
                                                            objLeft[index][k] - hOffset <= hLsPos[index][j] <= \
                                                    objRight[index][k] + hOffset:
                                covered = 1
                                break
                        if covered == 0:
                            event_in_line = 1
                            break
                if event_in_line == 1:
                    comment = 'Electronic sign recognized as lightspot'
                    indexes.append(index)

        if indexes:
            data.append([self.groupIndexes(indexes, MAX_GAP, MIN_PEAKS), 'ElecSign/TrafLight', comment, -1])

        return {'len': len(data), 'data': data}

    def ef_LightCones(self, prevframe=5):
        """
        EF 3: Possible light cone detection

        :return: EF gives back dict structure with data len and data itself
        """
        if self.dat2p0:
            # TODO (low priority)
            print("Not ready yet.")
            return

        data = []
        indexes = []
        empty = []
        oncoming = []
        classification = self.mat['mudp']['vis']['vision_active_light_sensor_info']['activeLightSpots'][
            'classification']
        highway = self.mat['mudp']['vis']['vision_active_light_sensor_info']['highwayDetected']
        city = self.mat['mudp']['vis']['vision_active_light_sensor_info']['villageDetected']
        events = self.mat['mudp']['vis']['vision_ahbc_info']['eventsDetected']

        for index in range(self.visLen):
            num_of_onc = 0
            num_of_empty = 0
            for ls_num in range(10):
                if classification[index][ls_num] == 1 or classification[index][ls_num] == 3:
                    num_of_onc += 1
                elif classification[index][ls_num] == 0:
                    num_of_empty += 1
            if num_of_onc > 0:
                oncoming.append(1)
            else:
                oncoming.append(0)
            if num_of_empty == 10:
                empty.append(1)
            else:
                empty.append(0)

            if index - prevframe >= 0:
                if empty[index - 1] == 1 and oncoming[index] == 1 and highway[index] == 0 and city[index] == 0 and \
                                self.bitget(events[index], 5) == 0:
                    indexes.append(index - prevframe)

        if indexes:
            data.append([self.groupIndexes(indexes), 'Light Cone possible', 'Light Cone possible', -1])

        return {'len': len(data), 'data': data}

    # suggestion: Once it will be possible to pass parameter to EF, refactor the following ef_Class1-8.
    def classFind(self, param):
        data = []
        if self.dat2p0:
            classifications = \
                self.mat["mudp"]["eyeq"]["Lights"]["vis_light_sensor_data_info"]["activeLightSensorInfo"]["activeLightSpots"]["classification"]
            ids = \
                self.mat["mudp"]["vis"]["vision_active_light_sensor_info"]["activeLightSensorInfo"]["activeLightSpots"]["id"]
        else:
            classifications = \
                self.mat['mudp']['vis']['vision_active_light_sensor_info']['activeLightSpots']['classification']
            ids = self.mat['mudp']['vis']['vision_active_light_sensor_info']['activeLightSpots']['id']

        for col in range(classifications.shape[-1]):
            indexes = []
            prevID = ids[0, col]
            for index in range(1, self.visLen):
                if classifications[index, col] == param and \
                                prevID == ids[index, col]:
                    indexes.append(index)
                prevID = ids[index, col]

            if indexes:
                data.append([self.groupIndexes(indexes), 'classification_' + str(param),
                             'classification == ' + str(param), col])

        return {'len': len(data), 'data': data}

    def ef_Class1(self):
        """
        EF 4: classification == 1

        :return: EF gives back dict structure with data len and data itself
        """
        return self.classFind(1)


    def ef_Class2(self):
        """
        EF 5: classification == 2

        :return: EF gives back dict structure with data len and data itself
        """
        return self.classFind(2)


    def ef_Class3(self):
        """
        EF 6: classification == 3

        :return: EF gives back dict structure with data len and data itself
        """
        return self.classFind(3)


    def ef_Class4(self):
        """
        EF 7: classification == 4

        :return: EF gives back dict structure with data len and data itself
        """
        return self.classFind(4)


    def ef_Class5(self):
        """
        EF 8: classification == 5

        :return: EF gives back dict structure with data len and data itself
        """
        return self.classFind(5)


    def ef_Class6(self):
        """
        EF 9: classification == 6

        :return: EF gives back dict structure with data len and data itself
        """
        return self.classFind(6)


    def ef_Class7(self):
        """
        EF 9: classification == 7

        :return: EF gives back dict structure with data len and data itself
        """
        return self.classFind(7)

    def ef_Class8(self):
        """
        classification == 8
        :return: EF gives back dict structure with data len and data itself
        """
        return self.classFind(8)

    def ef_UrbanArea(self, MAX_GAP=100, MIN_PEAKS=1):
        """
        EF 10: Urban area ON
        EF goes through mat indexes and check if UA flag change comparing to previous index.
        If so, index is added to indexes list. EF finds only changes in UA signal, so only frequent
        flickering is reported, constant detection is discarded (depends on groupIndexes params)

        :param MAX_GAP: maxGap parameters of groupIndexes() (see groupIndexes info)
        :param MIN_PEAKS: minPeaks parameters of groupIndexes() (see groupIndexes info)
        :return: EF gives back dict structure with data len and data itself
        """
        if self.dat2p0:
            urbanArea = self.get_bit(
                self.mat["mudp"]["eyeq"]["Lights"]["vis_light_sensor_data_info"]["activeLightSensorInfo"]["light_Sensor_Detections_byte"],
                bit_number_from_right=2)
        else:
            urbanArea = self.mat['mudp']['vis']['vision_active_light_sensor_info']['villageDetected']

        data = []
        indexes = []
        for index in range(1, self.visLen):
            if not urbanArea[index - 1] and urbanArea[index] or \
                            urbanArea[index - 1] and not urbanArea[index]:
                indexes.append(index)

        data.append([self.groupIndexes(indexes, MAX_GAP, MIN_PEAKS), 'Urban area', 'UA flag changed', -1])

        return {'len': len(data), 'data': data}

    def ef_UrbanAreaTownSign(self, FRAME_GAP=200, MAX_GAP=50, MIN_PEAKS=1):
        """
        EF 11: Urban area OFF, when passing town enter sign
        EF goes through mat indexes and search for TOWN_START traffic signs.
        If urban area is active when sign has conf == 1, event is dischared.
        Otherwise, EF check if urban area is set in range of FRAME_GAP parameter.
        Index, then, is added to indexes list.

        :param FRAME_GAP: maxFrame parameter for urban area to be set after TOWN_START sign
        :param MAX_GAP: maxGap parameters of groupIndexes() (see groupIndexes info)
        :param MIN_PEAKS: minPeaks parameters of groupIndexes() (see groupIndexes info)
        :return: EF gives back dict structure with data len and data itself
        """

        if self.dat2p0:
            # TODO (low priority)
            print("Not ready yet.")
            return
        else:
            urbanArea = self.mat['mudp']['vis']['vision_active_light_sensor_info']['villageDetected']
            ahbcAvailable = self.mat['mudp']['vis']['vision_ahbc_info']['ahbcAvailable']

            conf_matrix = \
                self.mat['mudp']['vis']['vision_traffic_sign_info'][
                    'trafficSigns'][
                    'signConfidence']
            sign_types_matrix = \
                self.mat['mudp']['vis']['vision_traffic_sign_info'][
                    'trafficSigns'][
                    'signType']

            town_start_conf1 = (sign_types_matrix == 11) * (conf_matrix == 1)

        data = []
        indexes = []
        for index in range(self.visLen):
            if ahbcAvailable[index] == 2 and any(town_start_conf1[index]) and not urbanArea[index]:
                for i in range(FRAME_GAP):
                    if urbanArea[min(index + i, self.visLen - 1)]:
                        lastIndex = min(index + i, self.visLen - 1)
                        break
                    else:
                        lastIndex = index
                indexes += range(index, lastIndex + 1)

        data.append(
            [self.groupIndexes(indexes, MAX_GAP, MIN_PEAKS), 'Urban area TS', 'Passing TownStart when UA is off',
             -1])

        return {'len': len(data), 'data': data}

    def ef_TailLightsDisappearance(self, MAX_GAP=0, MIN_PEAKS=1):
        """
        EF 12: Distant tail lights disappear while there are no other tail lights detected
        EF goes through mat indexes and check if UA flag change compering to previous index.
        If so, index is added to indexes list. EF find only changes in UA signal, so only frequent
        flickering is raported, constant detection is discarded (depend on groupIndexes params)

        :param MAX_GAP: maxGap parameters of groupIndexes() (see groupIndexes info)
        :param MIN_PEAKS: minPeaks parameters of groupIndexes() (see groupIndexes info)
        :return: EF gives back dict structure with data len and data itself
        """
        if self.dat2p0:
            longPos = self.mat["mudp"]["eyeq"]["Lights"]["vis_light_sensor_data_info"]["activeLightSensorInfo"]["activeLightSpots"]["longPos"]
            classification = self.mat["mudp"]["eyeq"]["Lights"]["vis_light_sensor_data_info"]["activeLightSensorInfo"]["activeLightSpots"]["classification"]
        else:
            longPos = self.mat['mudp']['vis']['vision_active_light_sensor_info']['activeLightSpots']['longPos']
            classification = self.mat['mudp']['vis']['vision_active_light_sensor_info']['activeLightSpots']['classification']
        tailLampId = 2
        pairOfTailLampsId = 4
        minimal_distance = 400

        preceding = np.logical_or((classification == tailLampId), (classification == pairOfTailLampsId))

        data = []
        indexes = []
        for index in range(self.visLen - 1):
            columns_with_preceding = np.argwhere(preceding[index, :])[:, 0]
            if len(columns_with_preceding) == 1:
                col = columns_with_preceding[0]
                if longPos[index, col] >= minimal_distance and 1 not in preceding[index + 1, :]:
                    indexes.append(index)

        data.append(
            [self.groupIndexes(indexes, MAX_GAP, MIN_PEAKS), 'Distant tail lights disappear',
             'Distant tail lights disappear while there are no other tail lights detected', -1])

        return {'len': len(data), 'data': data}

    def ef_HighBeamFlicker(self, MAX_GAP=0, MIN_PEAKS=1, window_width=200):
        """
        EF 13: Possible high beam flickering caused by missed detection of distant taillights
        EF goes through mat indexes and check if UA flag change compering to previous index.
        If so, index is added to indexes list. EF find only changes in UA signal, so only frequent
        flickering is raported, constant detection is discarded (depend on groupIndexes params)

        :param MAX_GAP: maxGap parameters of groupIndexes() (see groupIndexes info)
        :param MIN_PEAKS: minPeaks parameters of groupIndexes() (see groupIndexes info)
        :param window_width: width of a window (number of frames) which goes through the entire log. It looks for
            situations when all preceding light spots disappear. If three such situations occur within the window,
            then all three are reported as events.
        :return: EF gives back dict structure with data len and data itself
        """
        if self.dat2p0:
            classification = self.mat["mudp"]["eyeq"]["Lights"]["vis_light_sensor_data_info"]["activeLightSensorInfo"]["activeLightSpots"]["classification"]
        else:
            classification = self.mat['mudp']['vis']['vision_active_light_sensor_info']['activeLightSpots']['classification']
        tailLampId = 2
        pairOfTailLampsId = 4

        preceding = np.logical_or((classification == tailLampId), (classification == pairOfTailLampsId))
        preceding = np.max(preceding, axis=1)

        data = []
        indexes = []
        preceding_appears = [-3000, -2000, -1000]
        for index in range(1, self.visLen):
            if preceding[index - 1] == 1 and preceding[index] == 0:
                preceding_appears.pop(0)
                preceding_appears.append(index)
                if preceding_appears[-1] - preceding_appears[0] < window_width:
                    indexes += preceding_appears
        indexes = sorted(set(indexes))

        data.append(
            [self.groupIndexes(indexes, MAX_GAP, MIN_PEAKS), 'Possible high beam flickering',
             'Possible high beam flickering caused by missed detection of distant taillights', -1])

        return {'len': len(data), 'data': data}


    def ef_HighVAngleDetections(self, vert_angle=-0.04):
        """
        EF 14: Detections of lights spots with untypical high vertical angle - e.g. on Street lamps,
        Electronic Traffic Signs etc.
        :param vert_angle: Vertical Angle of all types lights spots.
        :return: EF gives back dict structure with data len and data itself
        """

        if self.dat2p0:
            classifications = self.mat["mudp"]["eyeq"]["Lights"]["vis_light_sensor_data_info"]["activeLightSensorInfo"]["activeLightSpots"]["classification"]
            vAngle = self.mat["mudp"]["eyeq"]["Lights"]["vis_light_sensor_data_info"]["activeLightSensorInfo"]["activeLightSpots"]["bottomAngle"]
        else:
            classifications = self.mat['mudp']['vis']['vision_active_light_sensor_info']['activeLightSpots']['classification']
            vAngle = self.mat['mudp']['vis']['vision_active_light_sensor_info']['activeLightSpots']['verticalAngle']
        class_matrix = [1, 2, 3, 4, 5, 6]

        data = []

        if self.dat2p0:
            vert_angle *= -1.  # in DAT2.0 angle above horizon is positive in contrary to CADS3.5
            for col in range(classifications.shape[-1]):
                indexes = []
                for index in range(1, self.visLen):
                    if classifications[index, col] in class_matrix and vAngle[index, col] > vert_angle:
                        indexes.append(index)

                if indexes:
                    data.append([self.groupIndexes(indexes), 'High Vertical Angle',
                                 'High Vertical Angle ', col])

        else:
            for col in range(classifications.shape[-1]):
                indexes = []
                for index in range(1, self.visLen):
                    if classifications[index, col] in class_matrix and vAngle[index, col] < vert_angle:
                        indexes.append(index)

                if indexes:
                    data.append([self.groupIndexes(indexes), 'High Vertical Angle',
                                 'High Vertical Angle ', col])

        return {'len': len(data), 'data': data}

    def ef_DancingLightSpot(self, minFrames=4, maxFrames=8):
        """
        EF 15: Dancing Light Spot

        Dancing light spot (leading or oncoming) appears.

        :param minFrames:
        :param maxFrames:
        :return:
        """
        if self.dat2p0:
            classification = self.mat["mudp"]["eyeq"]["Lights"]["vis_light_sensor_data_info"]["activeLightSensorInfo"]["activeLightSpots"]["classification"]
            id = self.mat["mudp"]["eyeq"]["Lights"]["vis_light_sensor_data_info"]["activeLightSensorInfo"]["activeLightSpots"]["id"]
            pixelLeft = self.mat["mudp"]["eyeq"]["Lights"]["vis_light_sensor_data_info"]["activeLightSensorInfo"]["activeLightSpots"]["pixelLeft"]
            pixelRight = self.mat["mudp"]["eyeq"]["Lights"]["vis_light_sensor_data_info"]["activeLightSensorInfo"]["activeLightSpots"]["pixelRight"]
        else:
            classification = self.mat['mudp']['vis']['vision_active_light_sensor_info']['activeLightSpots']['classification']
            id = self.mat['mudp']['vis']['vision_active_light_sensor_info']['activeLightSpots']['id']
            pixelTop = self.mat['mudp']['vis']['vision_active_light_sensor_info']['activeLightSpots']['pixelTop']
            pixelBottom = self.mat['mudp']['vis']['vision_active_light_sensor_info']['activeLightSpots']['pixelBottom']
            pixelLeft = self.mat['mudp']['vis']['vision_active_light_sensor_info']['activeLightSpots']['pixelLeft']
            pixelRight = self.mat['mudp']['vis']['vision_active_light_sensor_info']['activeLightSpots']['pixelRight']

        data = []
        indexes = []
        for col in range(len(classification[0, :])):
            for row in range(len(classification[:, 0])):
                if row == 0:
                    continue
                if classification[row, col] not in [2, 4]:
                    continue
                if id[row, col] in id[row-1, :]:
                    continue
                firstRow, firstCol = row, col

                # find the last row and the last column
                i = firstRow
                while i < len(classification[:, 0]):
                    if id[firstRow, col] in id[i, :]:
                        i += 1
                    else:
                        lastRow = i - 1
                        break
                else:
                    # if the light spot lasts until the end of this log, go to the next column
                    break

                # maxRight = np.max(pixelRight[firstRow:lastRow + 1, col])
                # minLeft = np.min(pixelLeft[firstRow:lastRow + 1, col])

                # calculate maximum width
                # maxWidth = np.max(pixelRight[firstRow:lastRow + 1, col] - pixelLeft[firstRow:lastRow + 1, col])

                if 1 < lastRow - firstRow < 8:  # why 8??
                    indexes += list(range(firstRow, lastRow+1))

        indexes = sorted(set(indexes))
        if indexes:
            data.append([self.groupIndexes(indexes), 'Dancing Light Spot',
                         'Dancing light spot replaces correct detection', -1])
        return {'len': len(data), 'data': data}

    def ef_HRSDetected(self, MAX_GAP=0, MIN_PEAKS=1, one_sign_per_event=False, no_light_spots=False, no_urban_area=False):
        """
        EF 16: Highly Reflective Sign detected

        :param MAX_GAP:
        :param MIN_PEAKS:
        :param one_event_per_sign: if True, then each sign generates exactly one event
        :param no_light_spots: if True, HRS are reported only when there are no light spots on the scene
        :param no_urban_area: if True, HRS are reported only when Urban Area is not detected
        :return:
        """

        if self.dat2p0:
            lightSpotId = self.mat["mudp"]["eyeq"]["Lights"]["vis_light_sensor_data_info"]["activeLightSensorInfo"]["activeLightSpots"]["id"]
            lightSignId = self.mat["mudp"]["eyeq"]["Lights"]["vis_light_sensor_data_info"]["activeLightSensorInfo"]["reflectiveSigns"]["lightSignID"]
            urbanArea = self.get_bit(
                self.mat["mudp"]["eyeq"]["Lights"]["vis_light_sensor_data_info"]["activeLightSensorInfo"]["light_Sensor_Detections_byte"],
                bit_number_from_right=2)
        else:
            lightSpotId = self.mat['mudp']['vis']['vision_active_light_sensor_info']['activeLightSpots']['id']
            try:
                lightSignId = self.mat['mudp']['vis']['vision_active_light_sensor_info']['reflectiveSigns']['lightSignId']
            except KeyError as e:
                print("ERROR: Signal ", e, " not available")
                return
            urbanArea = self.mat['mudp']['vis']['vision_active_light_sensor_info']['villageDetected']
        lightSpotsPresent = np.any(lightSpotId, axis=1)

        data = []
        hrsPresent = lightSignId > 0
        if no_light_spots:
            hrsPresent *= np.transpose([lightSpotsPresent == 0])
        if no_urban_area:
            hrsPresent *= np.transpose([urbanArea == 0])

        if one_sign_per_event:
            for col in range(len(lightSignId[0, :])):
                hrsPresent = hrsPresent[:, col]
                indexes = list(np.argwhere(hrsPresent)[:, 0])
                if indexes:
                    data.append(
                        [self.groupIndexes(indexes, MAX_GAP, MIN_PEAKS), 'Highly Reflective Sign detected',
                         'Highly Reflective Sign detected', -1])
        else:
            hrsPresent = np.any(hrsPresent, axis=1)
            indexes = list(np.argwhere(hrsPresent)[:, 0])
            if indexes:
                data.append(
                    [self.groupIndexes(indexes, MAX_GAP, MIN_PEAKS), 'Highly Reflective Sign detected',
                     'Highly Reflective Sign detected', -1])

        return {'len': len(data), 'data': data}

    def ef_ChangingSizeOfHRS(self, MAX_GAP=20, MIN_PEAKS=1):
        """
        EF 17: Highly Reflective Sign changes size rapidly

        :param MAX_GAP:
        :param MIN_PEAKS:
        :return:
        """
        def is_same_sign_n_frames_before(n, signId, row, col):
            return signId[row, col] > 0 and signId[row, col] == signId[row-n, col]

        def area_changed_at_least_k_times(n, k, area, row, col):
            if k < 0:
                return
            if k < 1:
                k = 1/k
            return area[row, col] < 1/k * area[row-n, col] or area[row, col] > k * area[row-n, col]

        def is_area_big_enough(n, area, row, col, threshold=0.002):
            return area[row-n, col] > threshold

        if self.dat2p0:
            lightSignId = self.mat["mudp"]["eyeq"]["Lights"]["vis_light_sensor_data_info"]["activeLightSensorInfo"]["reflectiveSigns"]["lightSignID"]
            top = self.mat["mudp"]["eyeq"]["Lights"]["vis_light_sensor_data_info"]["activeLightSensorInfo"]["reflectiveSigns"]["lightSignTopAngle"]
            bottom = self.mat["mudp"]["eyeq"]["Lights"]["vis_light_sensor_data_info"]["activeLightSensorInfo"]["reflectiveSigns"]["lightSignBottomAngle"]
            left = self.mat["mudp"]["eyeq"]["Lights"]["vis_light_sensor_data_info"]["activeLightSensorInfo"]["reflectiveSigns"]["lightSignLeftAngle"]
            right = self.mat["mudp"]["eyeq"]["Lights"]["vis_light_sensor_data_info"]["activeLightSensorInfo"]["reflectiveSigns"]["lightSignRightAngle"]
        else:
            try:
                lightSignId = self.mat['mudp']['vis']['vision_active_light_sensor_info']['reflectiveSigns']['lightSignId']
                top = self.mat['mudp']['vis']['vision_active_light_sensor_info']['reflectiveSigns']['lightSignTopAngle']
                bottom = self.mat['mudp']['vis']['vision_active_light_sensor_info']['reflectiveSigns']['lightSignBottomAngle']
                left = self.mat['mudp']['vis']['vision_active_light_sensor_info']['reflectiveSigns']['lightSignLeftAngle']
                right = self.mat['mudp']['vis']['vision_active_light_sensor_info']['reflectiveSigns']['lightSignRightAngle']
            except KeyError as e:
                print("ERROR: Signal ", e, " not available")
                return

        width = right - left
        height = top - bottom
        area = width * height

        data = []
        indexes = []
        n = 3
        k = 2.0

        for col in range(lightSignId.shape[1]):
            for row in range(3, lightSignId.shape[0]):
                if is_same_sign_n_frames_before(n=n, signId=lightSignId, row=row, col=col) and \
                        area_changed_at_least_k_times(n=n, k=k, area=area, row=row, col=col) and \
                        is_area_big_enough(n, area, row, col):
                    indexes.append(row)

        indexes = sorted(set(indexes))
        if indexes:
            data.append([self.groupIndexes(indexes, MAX_GAP, MIN_PEAKS), 'HRS Changes size rapidly',
                         'HRS Changes size rapidly', -1])

        return {'len': len(data), 'data': data}

    def ef_FailSafes(self, MAX_GAP=0, MIN_PEAKS=1):
        """
        EF 18: FailSafes severity levels > 0.

        :param MAX_GAP:
        :param MIN_PEAKS:
        :return:
        """

        data = []

        failSafeKeys = [
            'frozenWindshieldSeverityLevel',
            'partialBlockageSeverityLevel',
            'fullBlockageSeverityLevel',
            'blurredImageSeverityLevel',
            'foggySpotsSeverityLevel',
            'smearedSpotsSeverityLevel',
            'spotRaysSeverityLevel',
            'selfGlareSeverityLevel'
            ]
        maxSeverityLevel = None
        for key in failSafeKeys:
            try:
                if maxSeverityLevel is None:
                    maxSeverityLevel = self.mat['mudp']['vis']['vision_failsafes'][key]
                else:
                    maxSeverityLevel = np.maximum(maxSeverityLevel, self.mat['mudp']['vis']['vision_failsafes'][key])
            except Exception as exc:
                raise exc

        for severityLevel in [1, 2, 3]:
            indexes = list(np.argwhere(maxSeverityLevel == severityLevel)[:, 0])
            if indexes:
                data.append([self.groupIndexes(indexes, MAX_GAP, MIN_PEAKS), 'FailSave severity level > 0',
                             'Max severity level == ' + str(severityLevel), -1])
        return {'len': len(data), 'data': data}

    def ef_ApproachingJunction(self, MAX_GAP=0, MIN_PEAKS=1):
        """
        EF 18: Approaching Junction signal set to 1.

        :param MAX_GAP:
        :param MIN_PEAKS:
        :return:
        """

        if self.dat2p0:
            approachingJunction = self.get_bit(self.mat["mudp"]["eyeq"]["Lights"]["vis_light_sensor_data_info"]["activeLightSensorInfo"]["light_Sensor_Detections_byte"],
                                               bit_number_from_right=4)
        else:
            try:
                approachingJunction = self.mat['mudp']['vis']['vision_active_light_sensor_info']['approachingJunction']
            except KeyError as e:
                print("ERROR: Signal ", e, " not available")
                return

        data = []
        indexes = list(np.argwhere(approachingJunction)[:, 0])
        if indexes:
            data.append([self.groupIndexes(indexes, MAX_GAP, MIN_PEAKS), 'Approaching junction',
                         'Approaching junction', -1])
        return {'len': len(data), 'data': data}

    def ef_LightObjectOccluded(self):
        if self.dat2p0:
            classification = self.mat["mudp"]["eyeq"]["Lights"]["vis_light_sensor_data_info"]["activeLightSensorInfo"]["activeLightSpots"]["classification"]
            id = self.mat["mudp"]["eyeq"]["Lights"]["vis_light_sensor_data_info"]["activeLightSensorInfo"]["activeLightSpots"]["id"]
            # pixelTop = self.mat["mudp"]["eyeq"]["Lights"]["vis_light_sensor_data_info"]["activeLightSensorInfo"]["activeLightSpots"]["pixelTop"]
            # pixelBottom = self.mat["mudp"]["eyeq"]["Lights"]["vis_light_sensor_data_info"]["activeLightSensorInfo"]["activeLightSpots"]["pixelBottom"]
            pixelLeft = self.mat["mudp"]["eyeq"]["Lights"]["vis_light_sensor_data_info"]["activeLightSensorInfo"]["activeLightSpots"]["pixelLeft"]
            # pixelRight = self.mat["mudp"]["eyeq"]["Lights"]["vis_light_sensor_data_info"]["activeLightSensorInfo"]["activeLightSpots"]["pixelRight"]
        else:
            classification = self.mat['mudp']['vis']['vision_active_light_sensor_info']['activeLightSpots']['classification']
            id = self.mat['mudp']['vis']['vision_active_light_sensor_info']['activeLightSpots']['id']
            # pixelTop = self.mat['mudp']['vis']['vision_active_light_sensor_info']['activeLightSpots']['pixelTop']
            # pixelBottom = self.mat['mudp']['vis']['vision_active_light_sensor_info']['activeLightSpots']['pixelBottom']
            pixelLeft = self.mat['mudp']['vis']['vision_active_light_sensor_info']['activeLightSpots']['pixelLeft']
            # pixelRight = self.mat['mudp']['vis']['vision_active_light_sensor_info']['activeLightSpots']['pixelRight']

        headLampId = 1
        pairOfHeadLampsId = 3

        numberOfOncoming = \
            np.count_nonzero(classification == headLampId, axis=1) + 2 * np.count_nonzero(classification == pairOfHeadLampsId, axis=1)

        data = []
        indexes = []
        for col in range(id.shape[1]):
            for row in range(id.shape[0] - 1):
                score = 0
                if classification[row, col] == pairOfHeadLampsId and id[row, col] not in id[row + 1, :]:
                    score += 1
                if numberOfOncoming[row] == numberOfOncoming[row + 1] + 1:
                    score += 1
                if pixelLeft[row, col] > 100:  # what is 100?
                    score += 1

                if score >= 3:
                    indexes.append(row)
        if indexes:
            data.append([self.groupIndexes(indexes), 'Light object occluded',
                         'Oncoming light object probably occluded', -1])
        return {'len': len(data), 'data': data}

    def ef_PossibleLostObjectReasonCodeUseCase(self, leftMargin=250, rightMargin=250, minBBoxVerticalDiff=250):

        def getBoundingBox(mat):
            """
            Calculate coordinates of a bounding box which contains all detected light objects.

            :param mat: loaded .mat file
            :return:
                boxTop - array of top coordinates of the bounding box (length of the array == nr of frames)
                boxBottom
                boxLeft
                boxRight
                boxValid - array of boolean: True if there is any light source detected, otherwise false (length of the
                    array == nr of frames)
            """
            classification = self.mat['mudp']['vis']['vision_active_light_sensor_info'][
                'activeLightSpots']['classification']
            spotTop = self.mat['mudp']['vis']['vision_active_light_sensor_info']['activeLightSpots']['pixelTop']
            spotBottom = self.mat['mudp']['vis']['vision_active_light_sensor_info']['activeLightSpots']['pixelBottom']
            spotLeft = self.mat['mudp']['vis']['vision_active_light_sensor_info']['activeLightSpots']['pixelLeft']
            spotRight = self.mat['mudp']['vis']['vision_active_light_sensor_info']['activeLightSpots']['pixelRight']

            boxTop = np.zeros(classification.shape[0], dtype=np.int32)
            boxBottom = np.zeros(classification.shape[0], dtype=np.int32)
            boxLeft = np.zeros(classification.shape[0], dtype=np.int32)
            boxRight = np.zeros(classification.shape[0], dtype=np.int32)
            boxValid = np.zeros(classification.shape[0], dtype=np.bool_)

            validClassifications = [1, 2, 3, 4, 5, 7]

            for row in range(classification.shape[0]):
                for col in range(classification.shape[1]):
                    if classification[row, col] in validClassifications:
                        if not boxValid[row]:
                            boxTop[row] = spotTop[row, col]
                            boxBottom[row] = spotBottom[row, col]
                            boxLeft[row] = spotLeft[row, col]
                            boxRight[row] = spotRight[row, col]
                            boxValid[row] = True
                        else:
                            boxTop[row] = max(boxTop[row], spotTop[row, col])
                            boxBottom[row] = min(boxBottom[row], spotBottom[row, col])
                            boxLeft[row] = min(boxLeft[row], spotLeft[row, col])
                            boxRight[row] = max(boxRight[row], spotRight[row, col])

            return boxTop, boxBottom, boxLeft, boxRight, boxValid

        if self.dat2p0:
            #TODO (mid priority)
            return
        boxTop, boxBottom, boxLeft, boxRight, boxValid = getBoundingBox(self.mat)
        urbanArea = self.mat['mudp']['vis']['vision_active_light_sensor_info']['villageDetected']

        data = []
        indexes = []
        for row in range(urbanArea.shape[0] - 1): # for each frame (for each row in the .mat file)
            if not urbanArea[row] and boxValid[row]: # if urban area is not detected and there is at least one light object detected
                if boxValid[row + 1]: # if there are also some light spots in the next frame
                    if (boxLeft[row] > leftMargin and boxLeft[row + 1] - boxLeft[row] > minBBoxVerticalDiff) or \
                            (boxRight[row] < 1280 - rightMargin and boxRight[row] - boxRight[row + 1] > minBBoxVerticalDiff):
                        # report an event
                        indexes.append(row)
                else: # if there are no light spots in the next frarme
                    if boxLeft[row] > leftMargin and boxRight[row] < 1280 - rightMargin:
                        # report an event
                        indexes.append(row)
        if indexes:
            data.append([self.groupIndexes(indexes), 'Possible Lost Object Reason Code Use Case',
                         'Possible Lost Object Reason Code Use Case', -1])
        return {'len': len(data), 'data': data}

    def ef_OncomingChangesToUnclassified(self):

        if self.dat2p0:
            classification = self.mat["mudp"]["eyeq"]["Lights"]["vis_light_sensor_data_info"]["activeLightSensorInfo"]["activeLightSpots"]["classification"]
        else:
            classification = self.mat['mudp']['vis']['vision_active_light_sensor_info']['activeLightSpots']['classification']

        data = []
        indexes = []
        for row in range(1, classification.shape[0]):
            diffNumOfOncoming = np.count_nonzero((classification[row, :] == 1) | (classification[row, :] == 3)) - \
                                np.count_nonzero((classification[row - 1, :] == 1) | (classification[row - 1, :] == 3))
            diffNumOfUnclassified = np.count_nonzero(classification[row, :] == 6) - \
                                    np.count_nonzero(classification[row - 1, :] == 6)
            if diffNumOfOncoming == -1 and diffNumOfUnclassified == 1:
                indexes.append(row)

        if indexes:
            data.append([self.groupIndexes(indexes), 'OncomingChangesToUnclassified',
                         'Oncoming light object changes to Unclassified', -1])
        return {'len': len(data), 'data': data}

    def ef_LightObjectSizeRapidlyChanges(self):

        if self.dat2p0:
            # TODO (mid priority)
            return
        id = self.mat['mudp']['vis']['vision_active_light_sensor_info'][
            'activeLightSpots']['id']
        classification = self.mat['mudp']['vis']['vision_active_light_sensor_info'][
            'activeLightSpots']['classification']
        pixelTop = np.int32(self.mat['mudp']['vis']['vision_active_light_sensor_info'][
            'activeLightSpots']['pixelTop'])
        pixelBottom = np.int32(self.mat['mudp']['vis']['vision_active_light_sensor_info'][
            'activeLightSpots']['pixelBottom'])
        pixelLeft = np.int32(self.mat['mudp']['vis']['vision_active_light_sensor_info'][
            'activeLightSpots']['pixelLeft'])
        pixelRight = np.int32(self.mat['mudp']['vis']['vision_active_light_sensor_info'][
            'activeLightSpots']['pixelRight'])

        data = []
        indexes = []
        indexes_far_right = []
        for col in range(id.shape[1]):
            for row in range(1, id.shape[0]):
                if (
                    (id[row, col] > 0) and
                    (classification[row, col] in (1, 2, 3, 4)) and
                    (id[row - 1, col] == id[row, col])
                ):
                    width_current = pixelRight[row, col] - pixelLeft[row, col]
                    width_previous = pixelRight[row - 1, col] - pixelLeft[row - 1, col]

                    if width_current - width_previous > 2 * width_previous and width_current > 150:
                        if pixelRight[row, col] < 1280 - 100:
                            indexes.append(row)
                        else:
                            indexes_far_right.append(row)

        if indexes:
            data.append([self.groupIndexes(indexes), 'LightObjectSizeRapidlyChanges',
                         'Size of a light object changes rapidly', -1])
        if indexes_far_right:
            data.append([self.groupIndexes(indexes_far_right), 'LightObjectSizeRapidlyChanges',
                         'Size of a light object changes rapidly. Light object near the right edge of the FoV.', -1])
        return {'len': len(data), 'data': data}
