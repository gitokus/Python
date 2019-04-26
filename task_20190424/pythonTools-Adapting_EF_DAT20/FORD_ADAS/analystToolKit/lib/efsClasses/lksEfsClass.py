import numpy as np

from analystToolKit.lib.efsClasses import efsFrameClass


class lksEFs(efsFrameClass.EFClass):
    def __init__(self):
        self.function = 'LKS'


    def appendDetails(self, ):
        self.header += ['vehVel', 'constructionArea', 'Lane_chng',
                        'LLn_hRange', 'LLn_status', 'LLn_color', 'LLn_type', 'LLn_ambig',
                        'LLn_conf', 'LLn_SfConf', 'LLn_tuneConf', 'LLn_roadPrediction',
                        'RLn_hRange', 'RLn_status', 'RLn_color', 'RLn_type', 'RLn_ambig',
                        'RLn_conf', 'RLn_SfConf', 'RLn_tuneConf', 'RLn_roadPrediction',
                        'LRe_hRange', 'LRe_status', 'LRe_type', 'LRe_conf', 'LRe_tuneConf', 'LRe_relevant',
                        'RRe_hRange', 'RRe_status', 'RRe_type', 'RRe_conf', 'RRe_tuneConf', 'RRe_relevant']
        errorNameList = []
        if self.dat2p0:

            for eventsDict in self.eventsDictList:
                index = int(np.where(self.visIndex == eventsDict['eventIndex'])[0][0])
                try:
                    eventsDict['vehVel'] = np.NaN
                        # self.mat['mudp']['vis']['vision_vehicle_info']['vehicleVelocity'][index] * 3.6
                        #TODO: get vehVel from VFP state or wait for new streams in matFiles
                except:
                    errorNameList.append('vehVel')
                try:
                    eventsDict['constructionArea'] = \
                        self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['f_constructionArea'][index]
                    #TODO: where the const_area is in mat? is it extracted?
                except:
                    errorNameList.append('constructionArea')
                try:
                    eventsDict['Lane_chng'] = \
                        self.mat['mudp']['vis']['vision_road_info']['roadInfo']['laneChange'][index]
                except:
                    errorNameList.append('Lane_chng')
                try:
                    eventsDict['LLn_start_range'] = \
                        self.mat['mudp']['vis']['vision_road_info']['roadInfo']['roadMarkerInfo']['hostLeftMarker']['laneMarker']['startRange'][index]
                except:
                    errorNameList.append('LLn_start_Range')
                try:
                    eventsDict['LLn_end_range'] = \
                        self.mat['mudp']['vis']['vision_road_info']['roadInfo']['roadMarkerInfo']['hostLeftMarker']['laneMarker']['endRange'][index]
                except:
                    errorNameList.append('LLn_end_range')
                try:
                    eventsDict['LLn_status'] = "no info"
                    #TODO: find status in dat2.0
                except:
                    errorNameList.append('LLn_status')
                try:
                    eventsDict['LLn_color'] = \
                        self.mat['mudp']['vis']['vision_road_info']['roadInfo']['roadMarkerInfo']['hostLeftMarker']['laneMarkerColor'][index]
                except:
                    errorNameList.append('LLn_color')
                try:
                    eventsDict['LLn_type'] = \
                        self.mat['mudp']['vis']['vision_road_info']['roadInfo']['roadMarkerInfo']['hostLeftMarker']['laneMarkerType'][index]
                except:
                    errorNameList.append('LLn_type')
                try:
                    eventsDict['LLn_ambig'] = \
                        self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['f_ambiguousLinePatternLeft'][
                            index]
                    #TODO: write function to decode bitfiled values
                except:
                    errorNameList.append('LLn_ambig')
                try:
                    eventsDict['LLn_conf'] = \
                        self.mat['mudp']['vis']['vision_road_info']['roadInfo']['roadMarkerInfo']['hostLeftMarker']['laneMarkerConf']['confidence'][index]
                except:
                    errorNameList.append('LLn_conf')
                try:
                    eventsDict['LLn_SfConf'] = \
                        self.mat['mudp']['vis']['vision_road_info']['roadInfo']['roadMarkerInfo']['hostLeftMarker']['laneMarkerConf']['sfConf'][index]
                except:
                    errorNameList.append('LLn_SfConf')
                try:
                    eventsDict['LLn_tuneConf'] = "available only in fusion data"
                    #TODO: ask what is tuned confidence
                except:
                    errorNameList.append('LLn_tuneConf')
                try:
                    eventsDict['LLn_roadPrediction'] = \
                        self.mat['mudp']['vis']['vision_road_info']['roadInfo']['roadMarkerInfo']['roadPredictionLeft_byte'][index]
                except:
                    errorNameList.append('LLn_roadPrediction')



                try:
                    eventsDict['RLn_start_range'] = \
                        self.mat['mudp']['vis']['vision_road_info']['roadInfo']['roadMarkerInfo']['hostRightMarker']['laneMarker']['startRange'][index]
                except:
                    errorNameList.append('RLn_start_range')

                try:
                    eventsDict['RLn_end_range'] = \
                        self.mat['mudp']['vis']['vision_road_info']['roadInfo']['roadMarkerInfo']['hostRightMarker']['laneMarker']['endRange'][index]
                except:
                    errorNameList.append('RLn_end_range')
                try:
                    eventsDict['RLn_status'] ="Not avaiable in DAT20"
                except:
                    errorNameList.append('RLn_status')
                try:
                    eventsDict['RLn_color'] = self.mat['mudp']['vis']['vision_road_info']['roadInfo']['roadMarkerInfo']['hostRightMarker']['laneMarkerColor'][index]
                except:
                    errorNameList.append('RLn_color')
                try:
                    eventsDict['RLn_type'] = self.mat['mudp']['vis']['vision_road_info']['roadInfo']['roadMarkerInfo']['hostRightMarker']['laneMarkerType'][index]
                except:
                    errorNameList.append('RLn_type')
                try:
                    #TODO: decode bitfield
                    eventsDict['RLn_ambig'] = self.mat['mudp']['vis']['vision_road_info']['roadInfo']['roadMarkerInfo']['roadMarker_ambigLinePatt_const_byte'][
                            index]
                except:
                    errorNameList.append('RLn_ambig')
                try:
                    eventsDict['RLn_conf'] = self.mat['mudp']['vis']['vision_road_info']['roadInfo']['roadMarkerInfo']['hostRightMarker']['laneMarkerConf']['confidence'][index]
                except:
                    errorNameList.append('RLn_conf')
                try:
                    eventsDict['RLn_SfConf'] = \
                        self.mat['mudp']['vis']['vision_road_info']['roadInfo']['roadMarkerInfo']['hostRightMarker']['laneMarkerConf']['sfConf'][
                            index]
                except:
                    errorNameList.append('RLn_SfConf')
                try:
                    eventsDict['RLn_tuneConf'] = "Not available in DAt20"
                except:
                    errorNameList.append('RLn_tuneConf')
                try:
                    eventsDict['RLn_roadPrediction'] = \
                        self.mat['mudp']['vis']['vision_road_info']['roadInfo']['roadMarkerInfo']['roadPredictionRight_byte'][index]
                except:
                    errorNameList.append('RLn_roadPrediction')
                try:
                    eventsDict['LRe_start_range'] = \
                        self.mat['mudp']['vis']['vision_road_info']['roadInfo']['roadBorderInfo']['leftRoadBorder']['roadBorder']['startRange'][index]
                except:
                    errorNameList.append('LRe_start_range')

                try:
                    eventsDict['LRe_end_range'] = \
                        self.mat['mudp']['vis']['vision_road_info']['roadInfo']['roadBorderInfo']['leftRoadBorder']['roadBorder']['endRange'][index]
                except:
                    errorNameList.append('LRe_end_range')

                try:
                    eventsDict['LRe_status'] = "Not available in DAT20"
                except:
                    errorNameList.append('LRe_status')

                try:
                    eventsDict['LRe_type'] = \
                        self.mat['mudp']['vis']['vision_road_info']['roadInfo']['roadBorderInfo']['leftRoadBorder']['roadBorderType'][index]
                except:
                    errorNameList.append('LRe_type')
                try:
                    eventsDict['LRe_conf'] = \
                        self.mat['mudp']['vis']['vision_road_info']['roadInfo']['roadBorderInfo']['leftRoadBorder']['roadBorderConf']['confidence'][index]
                except:
                    errorNameList.append('LRe_conf')
                try:
                    eventsDict['LRe_tuneConf'] = "Not avilable in DAT2.0"
                except:
                    errorNameList.append('LRe_tuneConf')

                try:
                    eventsDict['RRe_start_range'] = \
                        self.mat['mudp']['vis']['vision_road_info']['roadInfo']['roadBorderInfo']['rightRoadBorder']['roadBorder']['startRange'][index]
                except:
                    errorNameList.append('RRe_start_range')
                try:
                    eventsDict['RRe_end_range'] = \
                        self.mat['mudp']['vis']['vision_road_info']['roadInfo']['roadBorderInfo']['rightRoadBorder']['roadBorder']['endRange'][index]
                except:
                    errorNameList.append('RRe_end_range')
                try:
                    eventsDict['RRe_status'] = "not available in DAT2.0"
                except:
                    errorNameList.append('RRe_status')
                try:
                    eventsDict['RRe_type'] = \
                        self.mat['mudp']['vis']['vision_road_info']['roadInfo']['roadBorderInfo']['rightRoadBorder']['roadBorderType'][index]
                except:
                    errorNameList.append('RRe_type')
                try:
                    eventsDict['RRe_conf'] = \
                        self.mat['mudp']['vis']['vision_road_info']['roadInfo']['roadBorderInfo']['rightRoadBorder']['roadBorderConf']['confidence'][index]
                except:
                    errorNameList.append('RRe_conf')
                try:
                    eventsDict['RRe_tuneConf'] = "Not available in DAT2.0"
                except:
                    errorNameList.append('RRe_tuneConf')
                try:
                    eventsDict['LRe_relevant'] = self.isReRelevant(index, 'LRe')
                except:
                    errorNameList.append('LRe_relevant')
                try:
                    eventsDict['RRe_relevant'] = self.isReRelevant(index, 'RRe')
                except:
                    errorNameList.append('RRe_relevant')

            return list(set(errorNameList))
        else:


            for eventsDict in self.eventsDictList:
                index = int(np.where(self.visIndex == eventsDict['eventIndex'])[0][0])
                try:
                    eventsDict['vehVel'] = \
                        self.mat['mudp']['vis']['vision_vehicle_info']['vehicleVelocity'][index] * 3.6
                except:
                    errorNameList.append('vehVel')
                try:
                    eventsDict['constructionArea'] = \
                        self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['f_constructionArea'][index]
                except:
                    errorNameList.append('constructionArea')
                try:
                    eventsDict['Lane_chng'] = \
                        self.mat['mudp']['vis']['vision_road_info']['laneChange'][index]
                except:
                    errorNameList.append('Lane_chng')
                try:
                    eventsDict['LLn_hRange'] = \
                        self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostLeftIndividualMarker'][
                            'laneMarker']['range'][index]
                except:
                    errorNameList.append('LLn_hRange')
                try:
                    eventsDict['LLn_status'] = \
                        self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostLeftIndividualMarker'][
                            'laneMarker']['status'][index]
                except:
                    errorNameList.append('LLn_status')
                try:
                    eventsDict['LLn_color'] = \
                        self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostLeftIndividualMarker'][
                            'laneMarkerColor'][index]
                except:
                    errorNameList.append('LLn_color')
                try:
                    eventsDict['LLn_type'] = \
                        self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostLeftIndividualMarker'][
                            'laneMarkerType'][index]
                except:
                    errorNameList.append('LLn_type')
                try:
                    eventsDict['LLn_ambig'] = \
                        self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['f_ambiguousLinePatternLeft'][index]
                except:
                    errorNameList.append('LLn_ambig')
                try:
                    eventsDict['LLn_conf'] = \
                        self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostLeftIndividualMarker'][
                            'laneMarkerConf']['confLKA'][index] % 4
                except:
                    errorNameList.append('LLn_conf')
                # try:
                #     eventsDict['LLn_SfConf'] = \
                #         self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostLeftIndividualSfConfShutdown'][
                #             index]
                # except:
                #     errorNameList.append('LLn_SfConf')
                try:
                    eventsDict['LLn_tuneConf'] = \
                        self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostLeftIndividualMarker'][
                            'laneMarkerConf']['tuneConfidence'][index]
                except:
                    errorNameList.append('LLn_tuneConf')
                try:
                    eventsDict['LLn_roadPrediction'] = \
                        self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['roadPredictionLeft'][index]
                except:
                    errorNameList.append('LLn_roadPrediction')
                try:
                    eventsDict['RLn_hRange'] = \
                        self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostRightIndividualMarker'][
                            'laneMarker']['range'][index]
                except:
                    errorNameList.append('RLn_hRange')
                try:
                    eventsDict['RLn_status'] = \
                        self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostRightIndividualMarker'][
                            'laneMarker']['status'][index]
                except:
                    errorNameList.append('RLn_status')
                try:
                    eventsDict['RLn_color'] = \
                        self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostRightIndividualMarker'][
                            'laneMarkerColor'][index]
                except:
                    errorNameList.append('RLn_color')
                try:
                    eventsDict['RLn_type'] = \
                        self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostRightIndividualMarker'][
                            'laneMarkerType'][index]
                except:
                    errorNameList.append('RLn_type')
                try:
                    eventsDict['RLn_ambig'] = \
                        self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['f_ambiguousLinePatternRight'][index]
                except:
                    errorNameList.append('RLn_ambig')
                try:
                    eventsDict['RLn_conf'] = \
                        self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostRightIndividualMarker'][
                            'laneMarkerConf']['confLKA'][index] % 4
                except:
                    errorNameList.append('RLn_conf')
                try:
                    eventsDict['RLn_SfConf'] = \
                        self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostRightIndividualSfConfShutdown'][
                            index]
                except:
                    errorNameList.append('RLn_SfConf')
                try:
                    eventsDict['RLn_tuneConf'] = \
                        self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostRightIndividualMarker'][
                            'laneMarkerConf']['tuneConfidence'][index]
                except:
                    errorNameList.append('RLn_tuneConf')
                try:
                    eventsDict['RLn_roadPrediction'] = \
                        self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['roadPredictionRight'][index]
                except:
                    errorNameList.append('RLn_roadPrediction')
                try:
                    eventsDict['LRe_hRange'] = \
                        self.mat['mudp']['vis']['vision_road_info']['mergedRoadEdgeInfo']['leftRoadEdge']['roadEdge'][
                            'range'][index]
                except:
                    errorNameList.append('LRe_hRange')
                try:
                    eventsDict['LRe_status'] = \
                        self.mat['mudp']['vis']['vision_road_info']['mergedRoadEdgeInfo']['leftRoadEdge']['roadEdge'][
                            'status'][index]
                except:
                    errorNameList.append('LRe_status')
                try:
                    eventsDict['LRe_type'] = \
                        self.mat['mudp']['vis']['vision_road_info']['mergedRoadEdgeInfo']['leftRoadEdge'][
                            'type'][index]
                except:
                    errorNameList.append('LRe_type')
                try:
                    eventsDict['LRe_conf'] = \
                        self.mat['mudp']['vis']['vision_road_info']['mergedRoadEdgeInfo']['leftRoadEdge']['roadEdgeConf'][
                            'confLKA'][index] % 4
                except:
                    errorNameList.append('LRe_conf')
                try:
                    eventsDict['LRe_tuneConf'] = \
                        self.mat['mudp']['vis']['vision_road_info']['mergedRoadEdgeInfo']['leftRoadEdge']['roadEdgeConf'][
                            'tuneConfidence'][index]
                except:
                    errorNameList.append('LRe_tuneConf')
                try:
                    eventsDict['RRe_hRange'] = \
                        self.mat['mudp']['vis']['vision_road_info']['mergedRoadEdgeInfo']['rightRoadEdge']['roadEdge'][
                            'range'][index]
                except:
                    errorNameList.append('RRe_hRange')
                try:
                    eventsDict['RRe_status'] = \
                        self.mat['mudp']['vis']['vision_road_info']['mergedRoadEdgeInfo']['rightRoadEdge']['roadEdge'][
                            'status'][index]
                except:
                    errorNameList.append('RRe_status')
                try:
                    eventsDict['RRe_type'] = \
                        self.mat['mudp']['vis']['vision_road_info']['mergedRoadEdgeInfo']['rightRoadEdge'][
                            'type'][index]
                except:
                    errorNameList.append('RRe_type')
                try:
                    eventsDict['RRe_conf'] = \
                        self.mat['mudp']['vis']['vision_road_info']['mergedRoadEdgeInfo']['rightRoadEdge']['roadEdgeConf'][
                            'confLKA'][index] % 4
                except:
                    errorNameList.append('RRe_conf')
                try:
                    eventsDict['RRe_tuneConf'] = \
                        self.mat['mudp']['vis']['vision_road_info']['mergedRoadEdgeInfo']['rightRoadEdge']['roadEdgeConf'][
                            'tuneConfidence'][index]
                except:
                    errorNameList.append('RRe_tuneConf')
                try:
                    eventsDict['LRe_relevant'] = self.isReRelevant(index, 'LRe')
                except:
                    errorNameList.append('LRe_relevant')
                try:
                    eventsDict['RRe_relevant'] = self.isReRelevant(index, 'RRe')
                except:
                    errorNameList.append('RRe_relevant')

            return list(set(errorNameList))


    # HELPERS FUNCTIONS #
    def polyToPoints(self, index, factors, hRange):
        """
        Internal method used within EFs. Translate poly factors of given lane into points to be drawn on
        frame from video.

        :param index: index in mat file where data should be extracted
        :param factors: array of factors for given line
        :param hRange: array of range of given line
        :return: returns two 5 element lists with x and y cords
        """
        xPoints = []
        yPoints = []

        focalLength = float(
            self.mat['mudp']['vfpState']['cals']['vision_params']['vehIndependentParam']['focalLength'][index])
        pixelsPerDegree = float(
            self.mat['mudp']['vfpState']['cals']['vision_params']['vehIndependentParam']['pixelsPerDegree'][index])
        referencePointX = float(
            self.mat['mudp']['vfpState']['cals']['vision_params']['vehDependentParam']['referencePointX_mm'][
                index]) / 1000
        cameraHeight = float(
            self.mat['mudp']['vfpState']['cals']['vision_params']['vehDependentParam']['cameraHeight_mm'][index]) / 1000
        pitch = -1 * float(
            self.mat['mudp']['vis']['vision_camera_alignment_info']['cameraAlignment']['horizon'][
                index] / pixelsPerDegree)
        yaw = float(self.mat['mudp']['vis']['vision_camera_alignment_info']['cameraAlignment'][
                        'yaw'][index] / pixelsPerDegree)
        roll = float(
            self.mat['mudp']['vis']['vision_camera_alignment_info']['cameraAlignment']['rollAngle'][
                index] / pixelsPerDegree)
        imagerWidth = 1280
        imagerHeight = 960

        Y = list(np.linspace(0, hRange, 5))
        X = list(np.polyval(factors, Y))

        for j in range(5):
            camX = X[j]
            camY = Y[j] + referencePointX
            camZ = -cameraHeight

            cam2X = camX * np.cos(np.deg2rad(yaw)) + camY * np.sin(np.deg2rad(yaw))
            cam2Y = camY * np.cos(np.deg2rad(yaw)) - camX * np.sin(np.deg2rad(yaw))
            cam2Z = camZ

            cam3X = cam2X
            cam3Y = cam2Y * np.cos(np.deg2rad(pitch)) + cam2Z * np.sin(np.deg2rad(pitch))
            cam3Z = cam2Z * np.cos(np.deg2rad(pitch)) - cam2Y * np.sin(np.deg2rad(pitch))

            p = focalLength / cam3Y * cam3X
            q = focalLength / cam3Y * cam3Z

            imageX = (p * np.cos(np.deg2rad(roll))) + (q * np.sin(np.deg2rad(roll)))
            imageY = (q * np.cos(np.deg2rad(roll))) - (p * np.sin(np.deg2rad(roll)))

            xPoints.append((imagerWidth / 2) + imageX)
            yPoints.append((imagerHeight / 2) - imageY)

        return xPoints, yPoints


    def isReRelevant(self, index, name):
        """
        Internal method to check if at given index RE is relevant to system. If coresponding line exists,
        RE should be no further then 0.5m from line, else RE should be no further then 3 m from car.

        :param index: index in mat file where data should be checked
        :param name: define left or right RE
        :return: true if RE is relevant, false if not
        """

        if self.dat2p0:
            if name == 'RRe':
                reA0 = abs(
                    self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadBorderInfo']['rightRoadBorder']['roadBorder']['a0'][
                        index])
                lnA0 = abs(self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadMarkerInfo']['hostRightMarker']['laneMarker']['a0'][index])
            elif name == 'LRe':
                reA0 = abs(
                    self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadBorderInfo']['leftRoadBorder']['roadBorder']['a0'][
                        index])
                lnA0 = abs(self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadMarkerInfo']['hostLeftMarker']['laneMarker']['a0'][index])
            else:
                return 1
        else:

            if name == 'RRe':
                reA0 = abs(self.mat['mudp']['vis']['vision_road_info']['mergedRoadEdgeInfo']['rightRoadEdge']['roadEdge']['a0'][index])
                lnA0 = abs(self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostRightIndividualMarker'][
                    'laneMarker']['a0'][index])
            elif name == 'LRe':
                reA0 = abs(self.mat['mudp']['vis']['vision_road_info']['mergedRoadEdgeInfo']['leftRoadEdge']['roadEdge']['a0'][index])
                lnA0 = abs(self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostLeftIndividualMarker'][
                    'laneMarker']['a0'][index])
            else:
                return 1

        if reA0 != 0:
            if lnA0 == 0:
                if reA0 < 3:
                    return 1
            else:
                if abs(lnA0 - reA0) < 0.55:
                    return 1
        return 0


    def isLaneChanging(self, index, OFFSET=0):
        """
        Internal method to check if at given index car is changing lane. It has build in offset before
        and after given index. After setting range of indexes, checks laneChange signal if any value was
        on. If so, return true, else return false.

        :param index: index in mat file where data should be checked
        :param OFFSET: offset to given index, extend range of relevant indexes
        :return: true if at given index range laneChange flag was up at any point, else false
        """

## CHANGED
        if self.dat2p0:
            laneChange = self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['laneChange']

        else:
            laneChange = self.mat['mudp']['vis']['vision_road_info']['laneChange']

        minI = max(index - OFFSET//2, 0)
        maxI = min(index + OFFSET//2, len(laneChange))

        if any(laneChange[minI: maxI + 1]):
            return 1
        else:
            return 0


    def isVelValid(self, index, VEL_OFFSET):
        """
        Internal method that checks if vehicleVelocity is higher then VEL_OFFSET (offset at which system detect lines
        correctly). It handles 0 values array after resim, returning valid (true).
        :param index: index at which vel is checked
        :param VEL_OFFSET: minimal speed at which it returns valid
        :return: valid signal (True or False)
        """
        if self.dat2p0:
            if not max(self.mat['mudp']['VSE']['vse_out']['vcs_long_velocity']):
                return 1
            else:
                vehVel = self.mat['mudp']['VSE']['vse_out']['vcs_long_velocity'][index] * 3.6
                if vehVel > VEL_OFFSET:
                    return 1
                else:
                    return 0

        else:

            if not max(self.mat['mudp']['vis']['vision_vehicle_info']['vehicleVelocity']):
                return 1
            else:
                vehVel = self.mat['mudp']['vis']['vision_vehicle_info']['vehicleVelocity'][index] * 3.6
                if vehVel > VEL_OFFSET:
                    return 1
                else:
                    return 0


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

    def ef_NoisyLaneDetections(self, VEL_OFFSET=60, CHANGE_LANE_DUR=100, V_OFFSET_A0=0.16,
             V_OFFSET_A1=0.08, H_OFFSET=50, MAX_GAP=40, MIN_PEAKS=2):
        """
        EF 1: Noisy lane detections
        EF checks for relevancy conditions: reRelevancy (if lane is RE), laneChange and velocity.
        Also it drops indexes where line is not detected or was not detected frame before.
        Finally if index is valid, EF checks differences between previous index and current one.
        If this difference is greater then offsets, index is added to indexes list, as it contains wanted event.

        :param VEL_OFFSET: minimal speed, at which system should detect lanes correctly
        :param CHANGE_LANE_DUR: offset to isLaneChanging(), extending laneChanging blockage
        :param V_OFFSET_A0: vertical offset for factor A0
        :param V_OFFSET_A1: vertical offset for factor A1
        :param H_OFFSET: horizontal offset
        :param MAX_GAP: maxGap parameters of groupIndexes() (see groupIndexes info)
        :param MIN_PEAKS: minPeaks parameters of groupIndexes() (see groupIndexes info)
        :return: EF gives back dict structure with data len and data itself
        """

        if self.dat2p0:

            LLn = {'name': 'LLn',
                   'hPoly':
                       [self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadMarkerInfo'][
                            'hostLeftMarker']['laneMarker']['a3'],
                        self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadMarkerInfo'][
                            'hostLeftMarker']['laneMarker']['a2'],
                        self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadMarkerInfo'][
                            'hostLeftMarker']['laneMarker']['a1'],
                        self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadMarkerInfo'][
                            'hostLeftMarker']['laneMarker']['a0']],
                   'hRange':
                       self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadMarkerInfo'][
                           'hostLeftMarker']['laneMarker']['endRange']
                       - self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadMarkerInfo'][
                           'hostLeftMarker']['laneMarker']['startRange']}
            RLn = {'name': 'RLn',
                   'hPoly':
                       [self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadMarkerInfo'][
                            'hostRightMarker']['laneMarker']['a3'],
                        self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadMarkerInfo'][
                            'hostRightMarker']['laneMarker']['a2'],
                        self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadMarkerInfo'][
                            'hostRightMarker']['laneMarker']['a1'],
                        self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadMarkerInfo'][
                            'hostRightMarker']['laneMarker']['a0']],
                   'hRange':
                       self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadMarkerInfo'][
                           'hostRightMarker']['laneMarker']['endRange']
                   - self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadMarkerInfo'][
                           'hostRightMarker']['laneMarker']['startRange']}
            LRe = {'name': 'LRe',
                   'hPoly':
                       [self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadBorderInfo'][
                            'leftRoadBorder']['roadBorder']['a3'],
                        self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadBorderInfo'][
                            'leftRoadBorder']['roadBorder']['a2'],
                        self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadBorderInfo'][
                            'leftRoadBorder']['roadBorder']['a1'],
                        self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadBorderInfo'][
                            'leftRoadBorder']['roadBorder']['a0']],
                   'hRange':
                       self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadBorderInfo'][
                           'leftRoadBorder']['roadBorder']['endRange']
                   - self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadBorderInfo'][
                           'leftRoadBorder']['roadBorder']['startRange']}
            RRe = {'name': 'RRe',
                   'hPoly':
                       [self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadBorderInfo'][
                            'rightRoadBorder']['roadBorder']['a3'],
                        self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadBorderInfo'][
                            'rightRoadBorder']['roadBorder']['a2'],
                        self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadBorderInfo'][
                            'rightRoadBorder']['roadBorder']['a1'],
                        self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadBorderInfo'][
                            'rightRoadBorder']['roadBorder']['a0']],
                   'hRange':
                       self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadBorderInfo'][
                           'rightRoadBorder']['roadBorder']['endRange']
                       - self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadBorderInfo'][
                           'rightRoadBorder']['roadBorder']['startRange'] }

        else:

            LLn = {'name': 'LLn',
                   'hPoly':
                       [self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostLeftIndividualMarker'][
                            'laneMarker']['a3'],
                        self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostLeftIndividualMarker'][
                            'laneMarker']['a2'],
                        self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostLeftIndividualMarker'][
                            'laneMarker']['a1'],
                        self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostLeftIndividualMarker'][
                            'laneMarker']['a0']],
                   'hRange':
                       self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostLeftIndividualMarker'][
                           'laneMarker']['range']}
            RLn = {'name': 'RLn',
                   'hPoly':
                       [self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostRightIndividualMarker'][
                            'laneMarker']['a3'],
                        self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostRightIndividualMarker'][
                            'laneMarker']['a2'],
                        self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostRightIndividualMarker'][
                            'laneMarker']['a1'],
                        self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostRightIndividualMarker'][
                            'laneMarker']['a0']],
                   'hRange':
                       self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostRightIndividualMarker'][
                           'laneMarker']['range']}
            LRe = {'name': 'LRe',
                   'hPoly':
                       [self.mat['mudp']['vis']['vision_road_info']['mergedRoadEdgeInfo']['leftRoadEdge']['roadEdge'][
                            'a3'],
                        self.mat['mudp']['vis']['vision_road_info']['mergedRoadEdgeInfo']['leftRoadEdge']['roadEdge'][
                            'a2'],
                        self.mat['mudp']['vis']['vision_road_info']['mergedRoadEdgeInfo']['leftRoadEdge']['roadEdge'][
                            'a1'],
                        self.mat['mudp']['vis']['vision_road_info']['mergedRoadEdgeInfo']['leftRoadEdge']['roadEdge'][
                            'a0']],
                   'hRange':
                       self.mat['mudp']['vis']['vision_road_info']['mergedRoadEdgeInfo']['leftRoadEdge']['roadEdge'][
                           'range']}
            RRe = {'name': 'RRe',
                   'hPoly':
                       [self.mat['mudp']['vis']['vision_road_info']['mergedRoadEdgeInfo']['rightRoadEdge']['roadEdge'][
                            'a3'],
                        self.mat['mudp']['vis']['vision_road_info']['mergedRoadEdgeInfo']['rightRoadEdge']['roadEdge'][
                            'a2'],
                        self.mat['mudp']['vis']['vision_road_info']['mergedRoadEdgeInfo']['rightRoadEdge']['roadEdge'][
                            'a1'],
                        self.mat['mudp']['vis']['vision_road_info']['mergedRoadEdgeInfo']['rightRoadEdge']['roadEdge'][
                            'a0']],
                   'hRange':
                       self.mat['mudp']['vis']['vision_road_info']['mergedRoadEdgeInfo']['rightRoadEdge']['roadEdge'][
                           'range']}

        data = []
        for line in [RLn, LLn, RRe, LRe]:
            indexes = []
            for index in range(1, self.visLen):
                if (self.isLaneChanging(index, CHANGE_LANE_DUR) or not self.isVelValid(index, VEL_OFFSET) or
                        not line['hRange'][index] or not line['hRange'][index - 1]):
                    continue
                if 'Re' in line['name'] and not self.isReRelevant(index, line['name']):
                    continue
                if (abs(line['hPoly'][3][index - 1] - line['hPoly'][3][index]) > V_OFFSET_A0) or \
                        (abs(line['hPoly'][2][index - 1] - line['hPoly'][2][index]) > V_OFFSET_A1) or \
                        (abs(line['hRange'][index - 1] - line['hRange'][index] > max(
                            line['hRange'][index - 1], line['hRange'][index])) * H_OFFSET // 100):
                    indexes.append(index)

            data.append([self.groupIndexes(indexes, MAX_GAP, MIN_PEAKS), 'Noisy detections',
                         line['name'] + ' flickering'])

        return {'len': len(data), 'data': data}

    def ef_Drops(self, VEL_OFFSET=60, CHANGE_LANE_DUR=100, MAX_DROP_DUR=40,
             REPLACE_DIST=0.2, MAX_GAP=0, MIN_PEAKS=1):
        """
        EF2: Drops in lane detection
        EF checks for relevancy conditions: reRelevancy (if lane is RE), laneChange and velocity.
        Then current index is checked for lane presence between previous index and current.
        There are two possible differences: either there was lane detected and now it disappear and
        its marked as last drop. Or line was not detected and now it is. In that case, duration between
        last drop and current index is checked. If it is smaller than MAX_DROP_DUR indexes between last drop
        and current index contain drop event.
        At last, drop event is checked if lane before and after drop is in same vertical position and
        if during drop, corresponding lane/re was not replacing it. Only if both answers are yes, the event
        is valid and added to indexes list and appended to data.

        :param VEL_OFFSET: minimal speed, at which system should detect lanes correctly
        :param CHANGE_LANE_DUR: offset to isLaneChanging(), extending laneChanging blockage
        :param MAX_DROP_DUR: max number of frames, not detected lane is consider drop
        :param REPLACE_DIST: vertical offset for compering lane before and after drop
        :param MAX_GAP: maxGap parameters of groupIndexes() (see groupIndexes info)
        :param MIN_PEAKS: minPeaks parameters of groupIndexes() (see groupIndexes info)
        :return: EF gives back dict structure with data len and data itself
        """

        if self.dat2p0:

            # host left marker
            HL = {'name': 'HL',
                   'hPoly':
                       [self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadMarkerInfo']
                        ['hostLeftMarker']['laneMarker']['a3'],
                        self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadMarkerInfo']
                        ['hostLeftMarker']['laneMarker']['a2'],
                        self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadMarkerInfo']
                        ['hostLeftMarker']['laneMarker']['a1'],
                        self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadMarkerInfo']
                        ['hostLeftMarker']['laneMarker']['a0']],
                   'hRange':
                       self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadMarkerInfo']
                       ['hostLeftMarker']['laneMarker']['endRange']
                        - self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadMarkerInfo']
                       ['hostLeftMarker']['laneMarker']['startRange']}
            # host right marker
            HR = {'name': 'HR',
                   'hPoly':
                       [self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadMarkerInfo']
                        ['hostRightMarker']['laneMarker']['a3'],
                        self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadMarkerInfo']
                        ['hostRightMarker']['laneMarker']['a2'],
                        self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadMarkerInfo']
                        ['hostRightMarker']['laneMarker']['a1'],
                        self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadMarkerInfo']
                        ['hostRightMarker']['laneMarker']['a0']],
                   'hRange':
                       self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadMarkerInfo']
                       ['hostRightMarker']['laneMarker']['endRange']
                       - self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadMarkerInfo']
                       ['hostRightMarker']['laneMarker']['startRange']}
            # next left left
            NLL = {'name': 'NLL',
                   'hPoly':
                       [self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadMarkerInfo'][
                            'nextLeftLeftMarker']['laneMarker']['a3'],
                        self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadMarkerInfo'][
                            'nextLeftLeftMarker']['laneMarker']['a2'],
                        self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadMarkerInfo'][
                            'nextLeftLeftMarker']['laneMarker']['a1'],
                        self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadMarkerInfo'][
                            'nextLeftLeftMarker']['laneMarker']['a0']],
                   'hRange':
                       self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadMarkerInfo'][
                           'nextLeftLeftMarker']['laneMarker']['endRange']
                        - self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadMarkerInfo'][
                           'nextLeftLeftMarker']['laneMarker']['startRange']}
            # next left right
            NLR = {'name': 'NLR',
                   'hPoly':
                       [self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadMarkerInfo'][
                            'nextLeftRightMarker']['laneMarker']['a3'],
                        self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadMarkerInfo'][
                            'nextLeftRightMarker']['laneMarker']['a2'],
                        self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadMarkerInfo'][
                            'nextLeftRightMarker']['laneMarker']['a1'],
                        self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadMarkerInfo'][
                            'nextLeftRightMarker']['laneMarker']['a0']],
                   'hRange':
                       self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadMarkerInfo'][
                           'nextLeftRightMarker']['laneMarker']['endRange']
                        - self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadMarkerInfo'][
                           'nextLeftRightMarker']['laneMarker']['startRange']}
            # next right left
            NRL = {'name': 'NRL',
                   'hPoly':
                       [self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadMarkerInfo'][
                            'nextRightLeftMarker']['laneMarker']['a3'],
                        self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadMarkerInfo'][
                            'nextRightLeftMarker']['laneMarker']['a2'],
                        self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadMarkerInfo'][
                            'nextRightLeftMarker']['laneMarker']['a1'],
                        self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadMarkerInfo'][
                            'nextRightLeftMarker']['laneMarker']['a0']],
                   'hRange':
                       self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadMarkerInfo'][
                           'nextRightLeftMarker']['laneMarker']['endRange']
                        - self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadMarkerInfo'][
                           'nextRightLeftMarker']['laneMarker']['startRange']}
            # next right right
            NRR = {'name': 'NRR',
                   'hPoly':
                       [self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadMarkerInfo'][
                            'nextRightRightMarker']['laneMarker']['a3'],
                        self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadMarkerInfo'][
                            'nextRightRightMarker']['laneMarker']['a2'],
                        self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadMarkerInfo'][
                            'nextRightRightMarker']['laneMarker']['a1'],
                        self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadMarkerInfo'][
                            'nextRightRightMarker']['laneMarker']['a0']],
                   'hRange':
                       self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadMarkerInfo'][
                           'nextRightRightMarker']['laneMarker']['endRange']
                        - self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadMarkerInfo'][
                           'nextRightRightMarker']['laneMarker']['startRange']}
            # left road border
            LRB = {'name': 'LRB',
                   'hPoly':
                       [self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadBorderInfo'][
                            'leftRoadBorder']['roadBorder']['a3'],
                        self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadBorderInfo'][
                            'leftRoadBorder']['roadBorder']['a2'],
                        self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadBorderInfo'][
                            'leftRoadBorder']['roadBorder']['a1'],
                        self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadBorderInfo'][
                            'leftRoadBorder']['roadBorder']['a0']],
                   'hRange':
                       self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadBorderInfo'][
                           'leftRoadBorder']['roadBorder']['endRange']
                        - self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadBorderInfo'][
                           'leftRoadBorder']['roadBorder']['startRange']}
            # left road border
            RRB = {'name': 'RRB',
                   'hPoly':
                       [self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadBorderInfo'][
                            'rightRoadBorder']['roadBorder']['a3'],
                        self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadBorderInfo'][
                            'rightRoadBorder']['roadBorder']['a2'],
                        self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadBorderInfo'][
                            'rightRoadBorder']['roadBorder']['a1'],
                        self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadBorderInfo'][
                            'rightRoadBorder']['roadBorder']['a0']],
                   'hRange':
                       self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadBorderInfo'][
                           'rightRoadBorder']['roadBorder']['endRange']
                        - self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadBorderInfo'][
                           'rightRoadBorder']['roadBorder']['startRange']}

            data = []
            for line in [HL, HR, NLL, NLR, NRL, NRR, LRB, RRB]:
                indexes = []
                lastDrop = (-100, -100)
                for index in range(1, self.visLen):
                    if self.isLaneChanging(index, CHANGE_LANE_DUR) or not self.isVelValid(index, VEL_OFFSET):
                        continue
                    if line['hRange'][index - 1] and not line['hRange'][index]:
                        if 'Re' in line['name'] and not self.isReRelevant(index - 1, line['name']):
                            continue
                        lastDrop = (index, line['hPoly'][3][index - 1])
                    elif not line['hRange'][index - 1] and line['hRange'][index]:
                        if index - lastDrop[0] < MAX_DROP_DUR and abs(lastDrop[1] - line['hPoly'][3][index]) <= 0.16:
                            if (line['name'] == 'LLn' and
                                        abs(LRe['hPoly'][3][index - 1] - line['hPoly'][3][index]) > REPLACE_DIST) or \
                                    (line['name'] == 'RLn' and
                                        abs(RRe['hPoly'][3][index - 1] - line['hPoly'][3][index]) > REPLACE_DIST) or \
                                    line['name'] == 'RRe' or line['name'] == 'LRe':
                                indexes += range(lastDrop[0], index + 1)

                data.append([self.groupIndexes(indexes, MAX_GAP, MIN_PEAKS), 'Drops', line['name'] + ' drop'])

            return {'len': len(data), 'data': data}

        else:

            LLn = {'name': 'LLn',
                   'hPoly':
                       [self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostLeftIndividualMarker'][
                            'laneMarker']['a3'],
                        self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostLeftIndividualMarker'][
                            'laneMarker']['a2'],
                        self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostLeftIndividualMarker'][
                            'laneMarker']['a1'],
                        self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostLeftIndividualMarker'][
                            'laneMarker']['a0']],
                   'hRange':
                       self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostLeftIndividualMarker'][
                           'laneMarker']['range']}
            RLn = {'name': 'RLn',
                   'hPoly':
                       [self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostRightIndividualMarker'][
                            'laneMarker']['a3'],
                        self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostRightIndividualMarker'][
                            'laneMarker']['a2'],
                        self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostRightIndividualMarker'][
                            'laneMarker']['a1'],
                        self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostRightIndividualMarker'][
                            'laneMarker']['a0']],
                   'hRange':
                       self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostRightIndividualMarker'][
                           'laneMarker']['range']}
            LRe = {'name': 'LRe',
                   'hPoly':
                       [self.mat['mudp']['vis']['vision_road_info']['mergedRoadEdgeInfo']['leftRoadEdge']['roadEdge'][
                            'a3'],
                        self.mat['mudp']['vis']['vision_road_info']['mergedRoadEdgeInfo']['leftRoadEdge']['roadEdge'][
                            'a2'],
                        self.mat['mudp']['vis']['vision_road_info']['mergedRoadEdgeInfo']['leftRoadEdge']['roadEdge'][
                            'a1'],
                        self.mat['mudp']['vis']['vision_road_info']['mergedRoadEdgeInfo']['leftRoadEdge']['roadEdge'][
                            'a0']],
                   'hRange':
                       self.mat['mudp']['vis']['vision_road_info']['mergedRoadEdgeInfo']['leftRoadEdge']['roadEdge'][
                           'range']}
            RRe = {'name': 'RRe',
                   'hPoly':
                       [self.mat['mudp']['vis']['vision_road_info']['mergedRoadEdgeInfo']['rightRoadEdge']['roadEdge'][
                            'a3'],
                        self.mat['mudp']['vis']['vision_road_info']['mergedRoadEdgeInfo']['rightRoadEdge']['roadEdge'][
                            'a2'],
                        self.mat['mudp']['vis']['vision_road_info']['mergedRoadEdgeInfo']['rightRoadEdge']['roadEdge'][
                            'a1'],
                        self.mat['mudp']['vis']['vision_road_info']['mergedRoadEdgeInfo']['rightRoadEdge']['roadEdge'][
                            'a0']],
                   'hRange':
                       self.mat['mudp']['vis']['vision_road_info']['mergedRoadEdgeInfo']['rightRoadEdge']['roadEdge'][
                           'range']}

            data = []
            for line in [RLn, LLn, RRe, LRe]:
                indexes = []
                lastDrop = (-100, -100)
                for index in range(1, self.visLen):
                    if self.isLaneChanging(index, CHANGE_LANE_DUR) or not self.isVelValid(index, VEL_OFFSET):
                        continue
                    if line['hRange'][index - 1] and not line['hRange'][index]:
                        if 'Re' in line['name'] and not self.isReRelevant(index - 1, line['name']):
                            continue
                        lastDrop = (index, line['hPoly'][3][index - 1])
                    elif not line['hRange'][index - 1] and line['hRange'][index]:
                        if index - lastDrop[0] < MAX_DROP_DUR and abs(lastDrop[1] - line['hPoly'][3][index]) <= 0.16:
                            if (line['name'] == 'LLn' and
                                        abs(LRe['hPoly'][3][index - 1] - line['hPoly'][3][index]) > REPLACE_DIST) or \
                                    (line['name'] == 'RLn' and
                                        abs(RRe['hPoly'][3][index - 1] - line['hPoly'][3][index]) > REPLACE_DIST) or \
                                    line['name'] == 'RRe' or line['name'] == 'LRe':
                                indexes += range(lastDrop[0], index + 1)

                data.append([self.groupIndexes(indexes, MAX_GAP, MIN_PEAKS), 'Drops', line['name'] + ' drop'])

            return {'len': len(data), 'data': data}


    def ef_ReplacingLaneByRE(self, VEL_OFFSET=60, CHANGE_LANE_DUR=100, MAX_REPLACE_DUR=40,
             REPLACE_DIST=0.2, MAX_GAP=0, MIN_PEAKS=1):
        """
        EF3: Replacing lane by RE
        EF checks for relevancy conditions: laneChange and velocity (only line are being checked).
        Then current index is checked for lane presence between previous index and current.
        There are two possible differences: either there was lane detected and now it disappear and
        its marked as last drop. Or line was not detected and now it is. In that case, duration between
        last drop and current index is checked. If it is smaller than MAX_REPLACE_DUR indexes between last drop
        and current index contain drop event.
        At last, drop event is checked if lane before and after drop is in same vertical position and
        if during drop, corresponding lane/re was replacing it. Only if both answers are yes, the event
        is valid and added to indexes list and appended to data.

        :param VEL_OFFSET: minimal speed, at which system should detect lanes correctly
        :param CHANGE_LANE_DUR: offset to isLaneChanging(), extending laneChanging blockage
        :param MAX_REPLACE_DUR: max number of frames, not detected lane is consider drop
        :param REPLACE_DIST: vertical offset for compering lane before and after drop
        :param MAX_GAP: maxGap parameters of groupIndexes() (see groupIndexes info)
        :param MIN_PEAKS: minPeaks parameters of groupIndexes() (see groupIndexes info)
        :return: EF gives back dict structure with data len and data itself
        """
        LLn = {'name': 'LLn',
               'hPoly':
                   [self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostLeftIndividualMarker'][
                        'laneMarker']['a3'],
                    self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostLeftIndividualMarker'][
                        'laneMarker']['a2'],
                    self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostLeftIndividualMarker'][
                        'laneMarker']['a1'],
                    self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostLeftIndividualMarker'][
                        'laneMarker']['a0']],
               'hRange':
                   self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostLeftIndividualMarker'][
                       'laneMarker']['range']}
        RLn = {'name': 'RLn',
               'hPoly':
                   [self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostRightIndividualMarker'][
                        'laneMarker']['a3'],
                    self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostRightIndividualMarker'][
                        'laneMarker']['a2'],
                    self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostRightIndividualMarker'][
                        'laneMarker']['a1'],
                    self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostRightIndividualMarker'][
                        'laneMarker']['a0']],
               'hRange':
                   self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostRightIndividualMarker'][
                       'laneMarker']['range']}
        LRe = {'name': 'LRe',
               'hPoly':
                   [self.mat['mudp']['vis']['vision_road_info']['mergedRoadEdgeInfo']['leftRoadEdge']['roadEdge'][
                        'a3'],
                    self.mat['mudp']['vis']['vision_road_info']['mergedRoadEdgeInfo']['leftRoadEdge']['roadEdge'][
                        'a2'],
                    self.mat['mudp']['vis']['vision_road_info']['mergedRoadEdgeInfo']['leftRoadEdge']['roadEdge'][
                        'a1'],
                    self.mat['mudp']['vis']['vision_road_info']['mergedRoadEdgeInfo']['leftRoadEdge']['roadEdge'][
                        'a0']],
               'hRange':
                   self.mat['mudp']['vis']['vision_road_info']['mergedRoadEdgeInfo']['leftRoadEdge']['roadEdge'][
                       'range']}
        RRe = {'name': 'RRe',
               'hPoly':
                   [self.mat['mudp']['vis']['vision_road_info']['mergedRoadEdgeInfo']['rightRoadEdge']['roadEdge'][
                        'a3'],
                    self.mat['mudp']['vis']['vision_road_info']['mergedRoadEdgeInfo']['rightRoadEdge']['roadEdge'][
                        'a2'],
                    self.mat['mudp']['vis']['vision_road_info']['mergedRoadEdgeInfo']['rightRoadEdge']['roadEdge'][
                        'a1'],
                    self.mat['mudp']['vis']['vision_road_info']['mergedRoadEdgeInfo']['rightRoadEdge']['roadEdge'][
                        'a0']],
               'hRange':
                   self.mat['mudp']['vis']['vision_road_info']['mergedRoadEdgeInfo']['rightRoadEdge']['roadEdge'][
                       'range']}

        data = []
        for line in [RLn, LLn]:
            indexes = []
            lastDrop = (-100, -100)
            for index in range(1, self.visLen):
                if self.isLaneChanging(index, CHANGE_LANE_DUR) or not self.isVelValid(index, VEL_OFFSET):
                    continue
                if line['hRange'][index - 1] and not line['hRange'][index]:
                    lastDrop = (index, line['hPoly'][3][index - 1])
                elif not line['hRange'][index - 1] and line['hRange'][index]:
                    if index - lastDrop[0] < MAX_REPLACE_DUR and abs(lastDrop[1] - line['hPoly'][3][index]) <= 0.16:
                        if (line['name'] == 'LLn' and
                                    abs(LRe['hPoly'][3][index - 1] - line['hPoly'][3][index]) <= REPLACE_DIST) or \
                                (line['name'] == 'RLn' and
                                    abs(RRe['hPoly'][3][index - 1] - line['hPoly'][3][index]) <= REPLACE_DIST):
                            indexes += range(lastDrop[0], index + 1)

            data.append(
                [self.groupIndexes(indexes, MAX_GAP, MIN_PEAKS), 'Replacments', line['name'] + ' replaced by RE'])

        return {'len': len(data), 'data': data}

# this ef utilize bit change, in future signal obtained can be swapped with this create by Michał Barej
    def ef_ConstructionAreaFlickering(self, MAX_GAP=40, MIN_PEAKS=2):
        """
        EF4: Flickering construction area detection
        EF goes through mat indexes and check if CA flag change compering to previous index.
        If so, index is added to indexes list. EF find only changes in CA signal, so only frequent
        flickering is raported, constant detection is discarded (depend on groupIndexes params)

        :param MAX_GAP: maxGap parameters of groupIndexes() (see groupIndexes info)
        :param MIN_PEAKS: minPeaks parameters of groupIndexes() (see groupIndexes info)
        :return: EF gives back dict structure with data len and data itself
        """
        if self.dat2p0:
            constArea = self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadMarkerInfo'][
                'roadMarker_ambigLinePatt_const_byte']

            data = []
            indexes = []
            for index in range(1, self.visLen):
                if not '{0:03b}'.format(constArea[index - 1])[2] and '{0:03b}'.format(constArea[index])[2] or \
                        '{0:03b}'.format(constArea[index - 1])[2] and not '{0:03b}'.format(constArea[index])[2]:
                    indexes.append(index)

            data.append([self.groupIndexes(indexes, MAX_GAP, MIN_PEAKS), 'Noisy CA', 'CA flag flickering'])

            return {'len': len(data), 'data': data}

        else:
            constArea = self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['f_constructionArea']

            data = []
            indexes = []
            for index in range(1, self.visLen):
                if not constArea[index - 1] and constArea[index] or \
                                constArea[index - 1] and not constArea[index]:
                    indexes.append(index)

            data.append([self.groupIndexes(indexes, MAX_GAP, MIN_PEAKS), 'Noisy CA', 'CA flag flickering'])

            return {'len': len(data), 'data': data}


    # def ef_SFC(self,MAX_GAP = 40, MIN_PEAKS = 1):
    #     """
    #     EF3: Single frame classifier
    #     EF goes through mat indexes and check if SFConf flag was on.
    #     If so, index is added to indexes list. EF find every detection where this flag was on,
    #     so it generate lots of output.
    #
    #     :param MAX_GAP: maxGap parameters of groupIndexes() (see groupIndexes info)
    #     :param MIN_PEAKS: minPeaks parameters of groupIndexes() (see groupIndexes info)
    #     :return: EF gives back dict structure with data len and data itself
    #     """
    #     LLn = {'name': 'LLn',
    #            'SfConf':
    #                self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostLeftIndividualSfConfShutdown']}
    #     RLn = {'name': 'RLn',
    #            'SfConf':
    #                self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostRightIndividualSfConfShutdown']}
    #
    #     data = []
    #     for line in [RLn, LLn]:
    #         indexes = []
    #         for index in range(1, self.visLen):
    #             if line['SfConf'][index]:
    #                 indexes.append(index)
    #
    #         data.append(
    #             [self.groupIndexes(indexes, MAX_GAP, MIN_PEAKS), 'SFClass', line['name'] + ' single frame classifier on'])
    #
    #     return {'len': len(data), 'data': data}
    #
    # def ef_SFC_and_Ambigous_flag(self,MAX_GAP = 40, MIN_PEAKS = 1):
    #     """
    #     EF3: Single frame classifier
    #     EF goes through mat indexes and check if SFConf flag was on and LKACONF == 150 (3) and Ambigous flag is set.
    #     If so, index is added to indexes list. EF find every detection where this flag was on,
    #     so it generate lots of output.
    #
    #     :param MAX_GAP: maxGap parameters of groupIndexes() (see groupIndexes info)
    #     :param MIN_PEAKS: minPeaks parameters of groupIndexes() (see groupIndexes info)
    #     :return: EF gives back dict structure with data len and data itself
    #     """
    #     LLn = {'name': 'LLn',
    #            'SfConf':
    #                self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostLeftIndividualSfConfShutdown'],
    #             'HSP_Conf':
    #                self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostLeftWithHighSpeedPredMarker']['laneMarkerConf']['confLKA'],
    #             'Ambigous_flag':
    #                self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['f_ambiguousLinePatternLeft']}
    #     RLn = {'name': 'RLn',
    #            'SfConf':
    #                self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostRightIndividualSfConfShutdown'],
    #             'HSP_Conf':
    #                self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostRightWithHighSpeedPredMarker']['laneMarkerConf']['confLKA'],
    #             'Ambigous_flag':
    #                 self. mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['f_ambiguousLinePatternRight']
    #                }
    #
    #     data = []
    #     for line in [RLn, LLn]:
    #         indexes = []
    #         for index in range(1, self.visLen):
    #             if ((line['SfConf'][index] == 1) and (line['Ambigous_flag'][index] == 1) and (line['HSP_Conf'][index] == 150)):
    #                 indexes.append(index)
    #
    #         data.append(
    #            [self.groupIndexes(indexes, MAX_GAP, MIN_PEAKS), 'SFC & LKACONF=150 & Ambigous_flag', line['name'] + ' SFC & LKACONF=150 & Ambigous flag'])
    #
    #     return {'len': len(data), 'data': data}
    #
    # def ef_Ambigous_flag_highConf_HSP(self,MAX_GAP = 40, MIN_PEAKS = 1):
    #     """
    #     EF3: High confidence for HSP model and Ambigous flag set
    #     EF goes through mat indexes and check if LKACONF == 150 (3) and Ambigous flag is set.
    #     If so, index is added to indexes list. EF find every detection where this flag was on,
    #     so it generate lots of output.
    #
    #     :param MAX_GAP: maxGap parameters of groupIndexes() (see groupIndexes info)
    #     :param MIN_PEAKS: minPeaks parameters of groupIndexes() (see groupIndexes info)
    #     :return: EF gives back dict structure with data len and data itself
    #     """
    #     LLn = {'name': 'LLn',
    #            'SfConf':
    #                self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostLeftIndividualSfConfShutdown'],
    #             'HSP_Conf':
    #                self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostLeftWithHighSpeedPredMarker']['laneMarkerConf']['confLKA'],
    #             'Ambigous_flag':
    #                self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['f_ambiguousLinePatternLeft']}
    #     RLn = {'name': 'RLn',
    #            'SfConf':
    #                self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostRightIndividualSfConfShutdown'],
    #             'HSP_Conf':
    #                self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostRightWithHighSpeedPredMarker']['laneMarkerConf']['confLKA'],
    #             'Ambigous_flag':
    #                 self. mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['f_ambiguousLinePatternRight']
    #                }
    #
    #     data = []
    #     for line in [RLn, LLn]:
    #         indexes = []
    #         for index in range(1, self.visLen):
    #             if ((line['Ambigous_flag'][index] == 1) and (line['HSP_Conf'][index] == 150)):
    #                 indexes.append(index)
    #
    #         data.append(
    #            [self.groupIndexes(indexes, MAX_GAP, MIN_PEAKS), 'LKACONF=150 & Ambigous_flag', line['name'] + 'LKACONF=150 & Ambigous flag'])
    #
    #     return {'len': len(data), 'data': data}



    def ef_ParallelLanes(self, CHANGE_LANE_DUR=100, MAX_DIRECTION_DIFFERENCE=0.2, MAX_GAP=40, MIN_PEAKS=2):
        """
        EF6: Parallelism of lines
        EF goes through mat indexes and check if dir(ection) of both lines differ more then MAX_DIRECTION_DIFFERENCE.
        If so, index is added to indexes list. Dir is calculeted as first derivative in x0 where x0 is hRange of longer
        line.

        :param CHANGE_LANE_DUR: offset to isLaneChanging(), extending laneChanging blockage
        :param MAX_DIRECTION_DIFFERENCE: max difference between lines direction
        :param MAX_GAP: maxGap parameters of groupIndexes() (see groupIndexes info)
        :param MIN_PEAKS: minPeaks parameters of groupIndexes() (see groupIndexes info)
        :return: EF gives back dict structure with data len and data itself
        """
        LLn = {'name': 'LLn',
               'hPoly':
                   [self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostLeftIndividualMarker'][
                        'laneMarker']['a3'],
                    self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostLeftIndividualMarker'][
                        'laneMarker']['a2'],
                    self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostLeftIndividualMarker'][
                        'laneMarker']['a1'],
                    self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostLeftIndividualMarker'][
                        'laneMarker']['a0']],
               'hRange':
                   self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostLeftIndividualMarker'][
                       'laneMarker']['range']}
        RLn = {'name': 'RLn',
               'hPoly':
                   [self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostRightIndividualMarker'][
                        'laneMarker']['a3'],
                    self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostRightIndividualMarker'][
                        'laneMarker']['a2'],
                    self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostRightIndividualMarker'][
                        'laneMarker']['a1'],
                    self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostRightIndividualMarker'][
                        'laneMarker']['a0']],
               'hRange':
                   self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostRightIndividualMarker'][
                       'laneMarker']['range']}

        data = []
        indexes = []
        for index in range(1, self.visLen):
            if (self.isLaneChanging(index, CHANGE_LANE_DUR) or
                    not LLn['hRange'][index] or not RLn['hRange'][index]):
                continue
            maxRange = max(LLn['hRange'][index], RLn['hRange'][index])
            LLnDerivativePoly = [3 * LLn['hPoly'][0][index], 2 * LLn['hPoly'][1][index], LLn['hPoly'][2][index]]
            RLnDerivativePoly = [3 * RLn['hPoly'][0][index], 2 * RLn['hPoly'][1][index], RLn['hPoly'][2][index]]
            LLnDir = np.polyval(LLnDerivativePoly, maxRange)
            RLnDir = np.polyval(RLnDerivativePoly, maxRange)

            if abs(LLnDir - RLnDir) > MAX_DIRECTION_DIFFERENCE:
                indexes.append(index)

        data.append([self.groupIndexes(indexes, MAX_GAP, MIN_PEAKS), 'Parallelism', 'Lines are not parallel' ])

        return {'len': len(data), 'data': data}


    def ef_ReNewGeometry(self, VEL_OFFSET=60, MAX_GAP=2, MIN_PEAKS=1):
        """
        EF7: RE New Geometry

        :param VEL_OFFSET: minimal speed, at which system should detect lanes correctly
        :param CHANGE_LANE_DUR: offset to isLaneChanging(), extending laneChanging blockage
        :param MAX_GAP: maxGap parameters of groupIndexes() (see groupIndexes info)
        :param MIN_PEAKS: minPeaks parameters of groupIndexes() (see groupIndexes info)
        :return: EF gives back dict structure with data len and data itself
        """
        LRe = {'name': 'LRe',
               'hRange': self.mat['mudp']['vis']['vision_road_info']['mergedRoadEdgeInfo']['leftRoadEdge']['roadEdge'][
                       'range'],
               'status': self.mat['mudp']['vis']['vision_road_info']['mergedRoadEdgeInfo']['leftRoadEdge']['roadEdge'][
                       'status'],}

        RRe = {'name': 'RRe',
               'hRange': self.mat['mudp']['vis']['vision_road_info']['mergedRoadEdgeInfo']['rightRoadEdge']['roadEdge'][
                       'range'],
               'status': self.mat['mudp']['vis']['vision_road_info']['mergedRoadEdgeInfo']['rightRoadEdge']['roadEdge'][
                   'status'],
               }

        data = []
        for line in [RRe, LRe]:
            indexes = []
            for index in range(1, self.visLen):
                if (not self.isReRelevant(index, line['name']) or
                        not self.isVelValid(index, VEL_OFFSET) or
                        not line['hRange'][index - 1]):
                     continue
                if line['status'][index] == 2:
                    indexes.append(index)

            data.append(
                [self.groupIndexes(indexes, MAX_GAP, MIN_PEAKS), 'New Geometry', line['name'] + ' new geometry '])

        return {'len': len(data), 'data': data}

    def ef_BottsDots(self, MAX_GAP=40, MIN_PEAKS=1):
        """
        EF8: Finding line type botts dots
        EF goes through mat indexes and check the line type and color flag.
        If so, index is added to indexes list. EF find every detection of botts dots and blue lines,
        so it generate lots of output.

        :param MAX_GAP: maxGap parameters of groupIndexes() (see groupIndexes info)
        :param MIN_PEAKS: minPeaks parameters of groupIndexes() (see groupIndexes info)
        :return: EF gives back dict structure with data len and data itself
        """
        if self.dat2p0:
            LLn = {'name': 'LLn',
                   'LnType':
                       self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadMarkerInfo'][
                           'hostLeftMarker']['laneMarkerType'],
                   'LnColor':
                       self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadMarkerInfo'][
                           'hostLeftMarker']['laneMarkerColor']}
            RLn = {'name': 'RLn',
                   'LnType':
                       self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadMarkerInfo'][
                           'hostRightMarker']['laneMarkerType'],
                   'LnColor':
                       self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadMarkerInfo'][
                           'hostRightMarker']['laneMarkerColor']}

        else:

            LLn = {'name': 'LLn',
                   'LnType':
                       self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostLeftIndividualMarker'][
                           'laneMarkerType'],
                   'LnColor':
                       self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostLeftIndividualMarker'][
                           'laneMarkerColor']}
            RLn = {'name': 'RLn',
                   'LnType':
                       self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostRightIndividualMarker'][
                           'laneMarkerType'],
                   'LnColor':
                       self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostRightIndividualMarker'][
                           'laneMarkerColor']}

        data = []
        for line in [RLn, LLn]:
            indexes = []
            for index in range(1, self.visLen):
                if line['LnType'][index] == 4:
                    indexes.append(index)

            data.append(
                [self.groupIndexes(indexes, MAX_GAP, MIN_PEAKS), 'LnType', line['name'] + 'Botts Dots'])

            indexes = []
            for index in range(1, self.visLen):
                if line['LnColor'][index] == 3:
                    indexes.append(index)

            data.append([self.groupIndexes(indexes, MAX_GAP, MIN_PEAKS), 'LnColor', line['name'] + 'Blue Line'])

        return {'len': len(data), 'data': data}

# this ef utilize bit change, in future signal obtained can be swapped with this create by Michał Barej
    def ef_AmbiguousFlagFlickering(self, MAX_GAP=40, MIN_PEAKS=2):
        """
        EF9: Ambiguous flag flickering
        EF goes through mat indexes and check if CA flag change compering to previous index.
        If so, index is added to indexes list. EF find only changes in CA signal, so only frequent
        flickering is raported, constant detection is discarded (depend on groupIndexes params)

        :param MAX_GAP: maxGap parameters of groupIndexes() (see groupIndexes info)
        :param MIN_PEAKS: minPeaks parameters of groupIndexes() (see groupIndexes info)
        :return: EF gives back dict structure with data len and data itself
        """

        if self.dat2p0:

            roadMarker = self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadMarkerInfo'][
                'roadMarker_ambigLinePatt_const_byte']

            LNn_list = []
            RLn_list = []

            for item in range(1, self.visLen):
                LNn_list.append(('{0:03b}'.format(roadMarker[item]))[0])
                RLn_list.append(('{0:03b}'.format(roadMarker[item]))[1])


            LLn = {'name': 'LLn',
                   'LnAmbig': LNn_list}
            RLn = {'name': 'RLn',
                   'LnAmbig': RLn_list}


            data = []
            for line in [RLn, LLn]:
                indexes = []
                for index in range(1, self.visLen -1 ):
                    if not line['LnAmbig'][index - 1] and line['LnAmbig'][index] or \
                                    line['LnAmbig'][index - 1] and not line['LnAmbig'][index]:
                        indexes.append(index)

                data.append([self.groupIndexes(indexes, MAX_GAP, MIN_PEAKS), 'Noisy Ambig', 'Ambig flickering'])

            return {'len': len(data), 'data': data}


        else:

            LLn = {'name': 'LLn',
                   'LnAmbig':
                       self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['f_ambiguousLinePatternLeft']}
            RLn = {'name': 'RLn',
                   'LnAmbig':
                       self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['f_ambiguousLinePatternRight']}

            data = []
            for line in [RLn, LLn]:
                indexes = []
                for index in range(1, self.visLen):
                    if not line['LnAmbig'][index - 1] and line['LnAmbig'][index] or \
                                    line['LnAmbig'][index - 1] and not line['LnAmbig'][index]:
                        indexes.append(index)

                data.append([self.groupIndexes(indexes, MAX_GAP, MIN_PEAKS), 'Noisy Ambig', 'Ambig flickering'])

            return {'len': len(data), 'data': data}

    def ef_REsOnSameSide(self):
        """
        EF:10 Both REs (barriers) on the same side
        EF goes through mat indexes and check if product of right RE (barrier) and left RE (barrier) is a positive number.
        If so, index is added to indexes list.
        """

        # ## MAPPING
        # 0 - road edge
        # 1 - curb
        # 2 - barier
        # 3 - conespoles

        if self.dat2p0:
            LRe = self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo'][
                'roadBorderInfo']['leftRoadBorder']['roadBorder']['a0']
            RRe = self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo'][
                'roadBorderInfo']['rightRoadBorder']['roadBorder']['a0']

            LBa = self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo'][
                'roadBorderInfo']['leftRoadBorder']['roadBorder']['a0']
            RBa = self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo'][
                'roadBorderInfo']['rightRoadBorder']['roadBorder']['a0']

            LB_type = self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo'][
                'roadBorderInfo']['leftRoadBorder']['roadBorderType']

            RB_type = self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo'][
                'roadBorderInfo']['rightRoadBorder']['roadBorderType']

            data = []

            isConflict = (LRe * RRe > 0) + (LBa * RBa > 0)
            indexes = np.argwhere(isConflict)[:, 0]
            indexes = list(indexes)
            data.append([self.groupIndexes(indexes), 'Both road edges (barriers) on the same side' + str(LB_type)
                         + str(RB_type) ,'Both road edges (barriers) on the same side'])


        else:
            LRe = self.mat['mudp']['vis']['vision_road_info']['roadEdgeInfo']['leftRoadEdge']['roadEdge']['a0']
            RRe = self.mat['mudp']['vis']['vision_road_info']['roadEdgeInfo']['rightRoadEdge']['roadEdge']['a0']

            LBa = self.mat['mudp']['vis']['vision_barrier_info']['leftVisBarrier']['visBarrier']['a0']
            RBa = self.mat['mudp']['vis']['vision_barrier_info']['rightVisBarrier']['visBarrier']['a0']

            data = []

            isConflict = (LRe * RRe > 0) + (LBa * RBa > 0)
            indexes = np.argwhere(isConflict)[:, 0]
            indexes = list(indexes)
            data.append([self.groupIndexes(indexes), 'Both road edges (barriers) on the same side',
                         'Both road edges (barriers) on the same side'])


        # right_a0 = self.mat['mudp']['vis']['vision_barrier_info']['rightVisBarrier']['visBarrier']['a0']
        # left_a0 = self.mat['mudp']['vis']['vision_barrier_info']['leftVisBarrier']['visBarrier']['a0']
        #
        # data = []
        # indexes = []
        # for index in range(self.visLen):
        #     if right_a0[index] * left_a0[index] > 0:
        #         indexes.append(index)
        #
        # data.append([self.groupIndexes(indexes), 'Both road edges (barriers) on the same side' , 'Both road edges (barriers) on the same side'])
        return {'len': len(data), 'data': data}


    def ef_RoadPredictionFlags(self, MAX_GAP=5, MIN_PEAKS=1):
        """
        EF11: roadPrediction bits are set

        FOR CADS3.5

        EF goes through mat indexes and checks if any of the following bits is set:
        - bit 0 = Diverging lane-marks Prediction
        - bit 1 = Other Side based Prediction
        - bit 2 = Merge prediction
        - bit 3 = Extrapolation
        - bit 4 = Occluded Lane-Mark Extrapolation
        - bit 5 = Headway Oriented Extrapolation
        - bit 6 = Highway Exit Spain

        FOR DAT2.0

        - bit 0 = RESERVED (undefined)
        - bit 1 = Occluded
        - bit 2 = Other_Side
        - bit 3 = Override
        - bit 4 = Dist_Based_Extrapolation
        - bit 5 = Headway_Oriented

        If two different flags are set to 1 at the same time, they are reported as separate events.

        :param MAX_GAP: maxGap parameters of groupIndexes() (see groupIndexes info)
        :param MIN_PEAKS: minPeaks parameters of groupIndexes() (see groupIndexes info)
        :return: EF gives back dict structure with data len and data itself
        """

        if self.dat2p0:
            roadPredLeft = self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadMarkerInfo']['roadPredictionLeft_byte']
            roadPredRight = self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadMarkerInfo']['roadPredictionRight_byte']

            flagNames = [
                'None',
                'Occluded',
                'Other_side',
                'Override',
                'Dist_Based_Extrapolation',
                'Headway_Oriented'
            ]

            data = []

            for side in ['left', 'right']:
                if side == 'left':
                    roadPred = roadPredLeft
                else:
                    roadPred = roadPredRight
                for bit in range(6):  # bits 0-5
                    flag = (roadPred % 2 ** (bit + 1)) > (2 ** bit - 1)
                    indexes = np.argwhere(flag).ravel()
                    indexes = list(indexes)
                    eventFinderID = 'roadPrediction.bit' + str(bit) + ' is set'
                    comment = side + ' line: ' + flagNames[bit]
                    data.append([self.groupIndexes(indexes, MAX_GAP, MIN_PEAKS), eventFinderID, comment])

            return {'len': len(data), 'data': data}



        else:
            roadPredLeft = self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['roadPredictionLeft']
            roadPredRight = self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['roadPredictionRight']

            flagNames = [
                'Diverging lane-marks Prediction',
                'Other Side based Prediction',
                'Merge prediction',
                'Extrapolation',
                'Occluded Lane-Mark Extrapolation',
                'Headway Oriented Extrapolation',
                'Highway Exit Spain'
            ]

            data = []

            for side in ['left', 'right']:
                if side == 'left':
                    roadPred = roadPredLeft
                else:
                    roadPred = roadPredRight
                for bit in range(7):  # bits 0-6
                    flag = (roadPred % 2 ** (bit + 1)) > (2 ** bit - 1)
                    indexes = np.argwhere(flag).ravel()
                    indexes = list(indexes)
                    eventFinderID = 'roadPrediction.bit' + str(bit) + ' is set'
                    comment = side + ' line: ' + flagNames[bit]
                    data.append([self.groupIndexes(indexes, MAX_GAP, MIN_PEAKS), eventFinderID, comment])

        return {'len': len(data), 'data': data}

    def ef_LmOnWrongSide(self,THRES= 0.5, MAX_GAP=40, MIN_PEAKS=1):
        """
        EF12: LM on wrong side of a car (a0 has opposite sign)

        :param MAX_GAP: maxGap parameters of groupIndexes() (see groupIndexes info)
        :param MIN_PEAKS: minPeaks parameters of groupIndexes() (see groupIndexes info)
        :return: EF gives back dict structure with data len and data itself
        """
        if self.dat2p0:
            LLn = {'name': 'LLn',
               'a0': self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadMarkerInfo'][
                   'hostLeftMarker']['laneMarker']['a0'],
               'sign': 1}


            RLn = {'name': 'RLn',
                   'a0': self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadMarkerInfo'][
                       'hostRightMarker']['laneMarker']['a0'],
                   'sign': -1}

        else:
            LLn = {'name': 'LLn',
                   'a0': self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostLeftIndividualMarker'][
                       'laneMarker']['a0'],
                   'sign': 1}

            RLn = {'name': 'RLn',
                   'a0': self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostRightIndividualMarker'][
                       'laneMarker']['a0'],
                   'sign': -1}

        data = []
        for line in [RLn, LLn]:
            indexes = []
            for index in range(1, self.visLen):
                if line['a0'][index] * line['sign'] > THRES:
                    indexes.append(index)

            data.append([self.groupIndexes(indexes, MAX_GAP, MIN_PEAKS), 'Wrong LM side',
                         line['name'] + ' reported with opposite sign'])

        return {'len': len(data), 'data': data}

    def ef_ReTypeFlickering(self, VEL_OFFSET=60, CHANGE_LANE_DUR=100, MAX_GAP=20, MIN_PEAKS=2):
        """
        EF13: RE type flickering

        :param VEL_OFFSET:
        :param CHANGE_LANE_DUR:
        :param MAX_GAP:
        :param MIN_PEAKS:
        :return:
        """

        if self.dat2p0:

            LRe = {'name': 'LRe',
                   'hPoly':
                       [self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadBorderInfo']
                        ['leftRoadBorder']['roadBorder']['a3'],
                        self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadBorderInfo']
                   ['leftRoadBorder']['roadBorder']['a2'],
                        self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadBorderInfo']
                        ['leftRoadBorder']['roadBorder']['a1'],
                        self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadBorderInfo']
                  ['leftRoadBorder']['roadBorder']['a0']],

                        #hrange = endRange - startRange
                   'hRange':
                       self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadBorderInfo']
                        ['leftRoadBorder']['roadBorder']['endRange'] - self.mat['mudp']['eyeq']['Road']
                       ['vis_road_data_info']['roadInfo']['roadBorderInfo']['leftRoadBorder']['roadBorder']['startRange'],

                   'type': self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']
                   ['roadBorderInfo']['leftRoadBorder']['roadBorderType']}

            RRe = {'name': 'RRe',
                   'hPoly':
                       [self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadBorderInfo'][
                            'rightRoadBorder']['roadBorder']['a3'],
                        self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadBorderInfo'][
                            'rightRoadBorder']['roadBorder']['a2'],
                        self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadBorderInfo'][
                            'rightRoadBorder']['roadBorder']['a1'],
                        self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadBorderInfo'][
                            'rightRoadBorder']['roadBorder']['a0']],
                   'hRange':
                       self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadBorderInfo'][
                           'rightRoadBorder']['roadBorder']['endRange']
                - self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadBorderInfo'][
                           'rightRoadBorder']['roadBorder']['startRange'],
                   'type': self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadBorderInfo'][
                       'rightRoadBorder']['roadBorderType']}

        else:
            LRe = {'name': 'LRe',
                   'hPoly':
                       [self.mat['mudp']['vis']['vision_road_info']['mergedRoadEdgeInfo']['leftRoadEdge']['roadEdge'][
                            'a3'],
                        self.mat['mudp']['vis']['vision_road_info']['mergedRoadEdgeInfo']['leftRoadEdge']['roadEdge'][
                            'a2'],
                        self.mat['mudp']['vis']['vision_road_info']['mergedRoadEdgeInfo']['leftRoadEdge']['roadEdge'][
                            'a1'],
                        self.mat['mudp']['vis']['vision_road_info']['mergedRoadEdgeInfo']['leftRoadEdge']['roadEdge'][
                            'a0']],
                   'hRange':
                       self.mat['mudp']['vis']['vision_road_info']['mergedRoadEdgeInfo']['leftRoadEdge']['roadEdge'][
                           'range'],
                   'type': self.mat['mudp']['vis']['vision_road_info']['mergedRoadEdgeInfo']['leftRoadEdge']['type']}

            RRe = {'name': 'RRe',
                   'hPoly':
                       [self.mat['mudp']['vis']['vision_road_info']['mergedRoadEdgeInfo']['rightRoadEdge']['roadEdge'][
                            'a3'],
                        self.mat['mudp']['vis']['vision_road_info']['mergedRoadEdgeInfo']['rightRoadEdge']['roadEdge'][
                            'a2'],
                        self.mat['mudp']['vis']['vision_road_info']['mergedRoadEdgeInfo']['rightRoadEdge']['roadEdge'][
                            'a1'],
                        self.mat['mudp']['vis']['vision_road_info']['mergedRoadEdgeInfo']['rightRoadEdge']['roadEdge'][
                            'a0']],
                   'hRange':
                       self.mat['mudp']['vis']['vision_road_info']['mergedRoadEdgeInfo']['rightRoadEdge']['roadEdge'][
                           'range'],
                   'type': self.mat['mudp']['vis']['vision_road_info']['mergedRoadEdgeInfo']['rightRoadEdge']['type']}

        data = []
        for line in [RRe, LRe]:
            indexes = []
            for index in range(1, self.visLen):
                if self.isLaneChanging(index, CHANGE_LANE_DUR) or not self.isVelValid(index, VEL_OFFSET):
                    continue
                if (line['type'][index - 1] == 1 and line['type'][index] == 2) or \
                        (line['type'][index - 1] == 2 and line['type'][index] == 1):
                    indexes.append(index)

            data.append(
                [self.groupIndexes(indexes, MAX_GAP, MIN_PEAKS), 'RE type flicker',
                 line['name'] + ' type flickering.'])

        return {'len': len(data), 'data': data}

    def ef_FailSafesLMConf(self, MAX_GAP=0, MIN_PEAKS=0, CONF_THRESHOLD=1):
        """
        EF14: failSafes with high laneMarkerConfidence
        EF searches for any failSafes except from 'excluded_types'
        occurring while left OR right laneMarkerConfidence is high (>= CONF_THRESHOLD)

        :param MAX_GAP: maxGap parameters of groupIndexes() (see groupIndexes info)
        :param MIN_PEAKS: minPeaks parameters of groupIndexes() (see groupIndexes info)
        :param CONF_THRESHOLD: min. accepted lane marker confidence value (in ME mapping <=> scale 0-2)
        :return:
        """

        excluded_types = ['ddrRamCrcFailure', 'frameIndex', 'imageIndex', 'pllFailure', 'radarCommErrorCounter']
        failSafeTypes = [key for key in (self.mat['mudp']['vis']['vision_failsafes']).keys()
                         if key not in excluded_types]

        failSafeFlags = {failSafeType:self.mat['mudp']['vis']['vision_failsafes'][failSafeType]
                         for failSafeType in failSafeTypes}
        LMconf = self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostLeftIndividualMarker'][
                        'laneMarkerConf']['confLKA']
        RMconf = self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostRightIndividualMarker'][
                        'laneMarkerConf']['confLKA']

        mapDayNight = {0:'day', 1:'dusk', 2:'night'}
        mapConf = {240:0, 150:2, 105:1}  # ME mapping
        data = []
        for type in failSafeTypes:
            indexes = []
            for index in range(1, self.visLen):
                if mapConf[LMconf[index]] >= CONF_THRESHOLD or mapConf[RMconf[index]] >= CONF_THRESHOLD:
                    if failSafeFlags[type][index] > 0:
                        indexes.append(index)

            for event_indexes in self.groupIndexes(indexes, MAX_GAP, MIN_PEAKS):
                comment = '{}_{}'.format(type, max(failSafeFlags[type][event_indexes]))
                day_night_arr = self.mat['mudp']['vis']['vision_ahbc_info']['ahbcAvailable'][event_indexes]
                comment += '-' + mapDayNight[int(round(np.mean( day_night_arr )))]

                data.append(
                    [self.groupIndexes(event_indexes, MAX_GAP, MIN_PEAKS), 'failsafes', comment])

        return {'len': len(data), 'data': data}

    def ef_LowConfDetections(self, MAX_GAP=2, MIN_PEAKS=0, CHANGE_LANE_DUR=20):
        """
        EF15: no roadEdge with low laneMarkerConfidence
        EF searches for events defined as lack of roadEdge detection (conf==0) and low laneMarkerConfidence (==1, ME).
        It is done separately for each side.
        In comment, it adds message if lane change occurred close to event.

        :param MAX_GAP: maxGap parameters of groupIndexes() (see groupIndexes info)
        :param MIN_PEAKS: minPeaks parameters of groupIndexes() (see groupIndexes info)
        :param CHANGE_LANE_DUR: offset to isLaneChanging(), extending laneChanging blockage
        :return:
        """
        if self.dat2p0:
            # new mapping { 0 2 3, 0 no line detected, 2 low confidence, 3 full confidence}

            LMconf = self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadMarkerInfo'][
                'hostLeftMarker']['laneMarkerConf']['confidence']

            RMconf = self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadMarkerInfo'][
                'hostRightMarker']['laneMarkerConf']['confidence']

            LEconf = self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadBorderInfo'][
                'leftRoadBorder']['roadBorderConf']['confidence']
            REconf = self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadBorderInfo'][
                'rightRoadBorder']['roadBorderConf']['confidence']

            mapConf = {0: 0, 3: 2, 2: 1}  # ME mapping

            data = []
            for side in [(LMconf, LEconf, 'left'), (RMconf, REconf, 'right')]:
                line, edge, side_name = side
                indexes = []
                for index in range(1, self.visLen):
                    if mapConf[edge[index]] == 0 and mapConf[line[index]] == 1:
                        indexes.append(index)

                for event_indexes in self.groupIndexes(indexes, MAX_GAP, MIN_PEAKS):
                    comment = side_name
                    changed = any([self.isLaneChanging(idx, CHANGE_LANE_DUR) for idx in event_indexes])
                    if changed: comment += '_laneChanged'
                    data.append([self.groupIndexes(event_indexes, MAX_GAP, MIN_PEAKS), 'no roadEdge', comment])

            return {'len': len(data), 'data': data}

        else:

            LMconf = self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostLeftIndividualMarker'][
                'laneMarkerConf']['confLKA']
            RMconf = self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostRightIndividualMarker'][
                'laneMarkerConf']['confLKA']
            LEconf = self.mat['mudp']['vis']['vision_road_info']['roadEdgeInfo']['leftRoadEdge']['roadEdgeConf'][
                'confLKA']
            REconf = self.mat['mudp']['vis']['vision_road_info']['roadEdgeInfo']['rightRoadEdge']['roadEdgeConf'][
                'confLKA']

            mapConf = {240: 0, 150: 2, 105: 1}  # ME mapping

            data = []
            for side in [(LMconf, LEconf, 'left'), (RMconf, REconf, 'right')]:
                line, edge, side_name = side
                indexes = []
                for index in range(1, self.visLen):
                    if mapConf[edge[index]] == 0 and mapConf[line[index]] == 1:
                        indexes.append(index)

                for event_indexes in self.groupIndexes(indexes, MAX_GAP, MIN_PEAKS):
                    comment = side_name
                    changed = any([self.isLaneChanging(idx, CHANGE_LANE_DUR) for idx in event_indexes])
                    if changed: comment += '_laneChanged'
                    data.append([self.groupIndexes(event_indexes, MAX_GAP, MIN_PEAKS), 'no roadEdge', comment])

            return {'len': len(data), 'data': data}

    def ef_ConstructionArea(self, MAX_GAP=0, MIN_PEAKS=1):
        """
        EF16: Construction area detection
        EF goes through mat indexes and checks if CA flag is set. If so, index is added to indexes list.

        :param MAX_GAP: maxGap parameters of groupIndexes() (see groupIndexes info)
        :param MIN_PEAKS: minPeaks parameters of groupIndexes() (see groupIndexes info)
        :return: EF gives back dict structure with data len and data itself
        """

        if self.dat2p0:
            constArea = self.mat['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadMarkerInfo'][
                'roadMarker_ambigLinePatt_const_byte']

            data = []
            indexes = []

            for index in range(1, self.visLen):
                # If ConstructionArea flag is active at the very beggining of log
                # probably contructionArea started in previous log so this log
                # should be rejected
                if index in range(10):
                    if ('{0:03b}'.format(constArea[index])[2]):
                        break
                if ('{0:03b}'.format(constArea[index])[2]):
                    indexes.append(index)

            data.append([self.groupIndexes(indexes, MAX_GAP, MIN_PEAKS), 'Construcion Area', 'Construction Area == 1'])

            return {'len': len(data), 'data': data}

        else:
            constArea = self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['f_constructionArea']

            data = []
            indexes = []

            for index in range(1, self.visLen):
                # If ConstructionArea flag is active at the very beggining of log
                # probably contructionArea started in previous log so this log
                # should be rejected
                if index in range(10):
                    if constArea[index]:
                        break
                if constArea[index]:
                    indexes.append(index)

            data.append([self.groupIndexes(indexes, MAX_GAP, MIN_PEAKS), 'Construcion Area', 'Construction Area == 1'])

            return {'len': len(data), 'data': data}
