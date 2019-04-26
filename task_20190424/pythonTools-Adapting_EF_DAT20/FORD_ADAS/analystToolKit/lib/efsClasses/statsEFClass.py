import numpy as np

from analystToolKit.lib.efsClasses import efsFrameClass


class statsEF(efsFrameClass.EFClass):
    def __init__(self):
        self.function = 'STATS'
        self.header = ['LogName',
                       'Status',
                       # general
                       'Distance',
                       'Duration',
                       'AvgSpeed',
                       'MinSpeed',
                       'MaxSpeed',
                       'AvgYrate',
                       'MinYrate',
                       'MaxYrate',
                       # lks
                       'ChngLane',
                       'AvailLRE',
                       'LREasFlat',
                       'LREasBarrier',
                       'AvailRRE',
                       'RREasFlat',
                       'RREasBarrier',
                       'AvailLL',
                       'AvailRL',
                       'SolidLL',
                       'SolidRL',
                       'DashLL',
                       'DashRL',
                       'WhiteLL',
                       'WhiteRL',
                       'YellLL',
                       'YellRL',
                       'AmbigL',
                       'AmbigR',
                       'ConstArea',
                       'SFClasL',
                       'SFClasR',
                       # tsr
                       'TSRNum',
                       # obj
                       'CarNum',
                       'MclNum',
                       'TrkNum',
                       'PedNum',
                       'AniNum',
                       'BclNum',
                       # afl
                       'Day',
                       'Dusk',
                       'Night',
                       'AmbLght',
                       'Highway',
                       'City',
                       'Tunnel',
                       'HLNum',
                       'TLNum',
                       'TrkCLNum',
                       'DarkOncL',
                       # severity levels
                       'blurSL',
                       'fogSL',
                       'smearSL',
                       'selfGSL',
                       'spotRSL',
                       'frozSL',
                       'partBSL',
                       'fullBSL',
                       # other
                       'Frames',
                       'ME_API',
                       'ME_SW',
                       'VFP_ver',
                       # diag
                       'simpFrDrop',
                       'cntError',
                       'cntFault',
                       'sFrDrop',
                       'mFrDrop',
                       'conFrDrop',
                       'decFrDrop',
                       # camera
                       'autoFixOk',
                       'cameraAlignment_horizon_min',
                       'cameraAlignment_horizon_max',
                       'cameraAlignment_yaw_min',
                       'cameraAlignment_yaw_max']
    def create_namespace(self):
        if self.dat2p0:
            # DAT2.0
            self.laneChange = self.mat['mudp']['vis']['vision_road_info']['roadInfo']['laneChange']

            self.a0_LRE = \
            self.mat['mudp']['vis']['vision_road_info']['roadInfo']['roadBorderInfo']['leftRoadBorder']['roadBorder'][
                'a0']
            self.a1_LRE = \
            self.mat['mudp']['vis']['vision_road_info']['roadInfo']['roadBorderInfo']['leftRoadBorder']['roadBorder'][
                'a1']
            self.a2_LRE = \
            self.mat['mudp']['vis']['vision_road_info']['roadInfo']['roadBorderInfo']['leftRoadBorder']['roadBorder'][
                'a2']
            self.a3_LRE = \
            self.mat['mudp']['vis']['vision_road_info']['roadInfo']['roadBorderInfo']['leftRoadBorder']['roadBorder'][
                'a3']
            self.r_LRE = self.mat['mudp']['vis']['vision_road_info']['roadInfo']['roadBorderInfo']['leftRoadBorder']['roadBorder']['endRange']
            self.start_range_LRE = self.mat['mudp']['vis']['vision_road_info']['roadInfo']['roadBorderInfo']['leftRoadBorder']['roadBorder']['startRange']
            self.type_LRE = self.mat['mudp']['vis']['vision_road_info']['roadInfo']['roadBorderInfo']['leftRoadBorder'][
                'roadBorderType']

            self.a0_RRE = \
            self.mat['mudp']['vis']['vision_road_info']['roadInfo']['roadBorderInfo']['rightRoadBorder']['roadBorder'][
                'a0']
            self.a1_RRE = \
            self.mat['mudp']['vis']['vision_road_info']['roadInfo']['roadBorderInfo']['rightRoadBorder']['roadBorder'][
                'a1']
            self.a2_RRE = \
            self.mat['mudp']['vis']['vision_road_info']['roadInfo']['roadBorderInfo']['rightRoadBorder']['roadBorder'][
                'a2']
            self.a3_RRE = \
            self.mat['mudp']['vis']['vision_road_info']['roadInfo']['roadBorderInfo']['rightRoadBorder']['roadBorder'][
                'a3']
            self.r_RLM = self.mat['mudp']['vis']['vision_road_info']['roadInfo']['roadBorderInfo']['rightRoadBorder']['roadBorder']['endRange']
            self.start_range_RLM = self.mat['mudp']['vis']['vision_road_info']['roadInfo']['roadBorderInfo']['rightRoadBorder']['roadBorder']['startRange']
            self.type_RRE = \
            self.mat['mudp']['vis']['vision_road_info']['roadInfo']['roadBorderInfo']['rightRoadBorder'][
                'roadBorderType']

            self.a0_hIndLLM = \
            self.mat['mudp']['vis']['vision_road_info']['roadInfo']['roadMarkerInfo']['hostLeftMarker']['laneMarker'][
                'a0']
            self.a1_hIndLLM = \
            self.mat['mudp']['vis']['vision_road_info']['roadInfo']['roadMarkerInfo']['hostLeftMarker']['laneMarker'][
                'a1']
            self.a2_hIndLLM = \
            self.mat['mudp']['vis']['vision_road_info']['roadInfo']['roadMarkerInfo']['hostLeftMarker']['laneMarker'][
                'a2']
            self.a3_hIndLLM = \
            self.mat['mudp']['vis']['vision_road_info']['roadInfo']['roadMarkerInfo']['hostLeftMarker']['laneMarker'][
                'a3']
            self.r_hIndLLM = self.mat['mudp']['vis']['vision_road_info']['roadInfo']['roadMarkerInfo']['hostLeftMarker']['laneMarker']['endRange']
            self.start_range_LLM = self.mat['mudp']['vis']['vision_road_info']['roadInfo']['roadMarkerInfo']['hostLeftMarker']['laneMarker']['startRange']

            self.a0_hIndRLM = \
            self.mat['mudp']['vis']['vision_road_info']['roadInfo']['roadMarkerInfo']['hostRightMarker']['laneMarker'][
                'a0']
            self.a1_hIndRLM = \
            self.mat['mudp']['vis']['vision_road_info']['roadInfo']['roadMarkerInfo']['hostRightMarker']['laneMarker'][
                'a1']
            self.a2_hIndRLM = \
            self.mat['mudp']['vis']['vision_road_info']['roadInfo']['roadMarkerInfo']['hostRightMarker']['laneMarker'][
                'a2']
            self.a3_hIndRLM = \
            self.mat['mudp']['vis']['vision_road_info']['roadInfo']['roadMarkerInfo']['hostRightMarker']['laneMarker'][
                'a3']
            self.r_hIndRLM = self.mat['mudp']['vis']['vision_road_info']['roadInfo']['roadMarkerInfo']['hostRightMarker']['laneMarker']['endRange']
            self.start_range_RLM = self.mat['mudp']['vis']['vision_road_info']['roadInfo']['roadMarkerInfo']['hostRightMarker']['laneMarker']['startRange']

            self.t_hIndLLM = \
            self.mat['mudp']['vis']['vision_road_info']['roadInfo']['roadMarkerInfo']['hostLeftMarker'][
                'laneMarkerType']
            self.t_hIndRLM = \
            self.mat['mudp']['vis']['vision_road_info']['roadInfo']['roadMarkerInfo']['hostRightMarker'][
                'laneMarkerType']
            self.col_hIndLLM = \
            self.mat['mudp']['vis']['vision_road_info']['roadInfo']['roadMarkerInfo']['hostLeftMarker'][
                'laneMarkerColor']
            self.col_hIndRLM = \
            self.mat['mudp']['vis']['vision_road_info']['roadInfo']['roadMarkerInfo']['hostRightMarker'][
                'laneMarkerColor']

            self.amb_LLM = "Bitfield"
            self.amb_RLM = "Bitfield"
            self.CA = "No info in DAT2.0"
            self.SFClasL = "Bitfield"
            self.SFClasR = "Bitfield"
            self.NTSR = self.mat['mudp']['vis']['vision_traffic_sign_info']['tsrInfo']['numberTrafficSigns']
            self.visObjClass = self.mat['mudp']['vis']['vision_obstacles_info']['visObjects']['visObs'][
                'classification'].astype(int)
            self.ahbcAvail = self.mat['mudp']['vis']['vision_active_light_sensor_info']['activeLightSensorInfo'][
                'ahbcAvailable']
            self.ahbc_events = self.mat['mudp']['vis']['vision_active_light_sensor_info']['activeLightSensorInfo'][
                'events_Detected_byte']
            self.highway = "Not supported"
            self.city = "Not supported"
            self.tunnel = "No info in DAT2.0"
            self.lsClass = \
            self.mat['mudp']['vis']['vision_active_light_sensor_info']['activeLightSensorInfo']['activeLightSpots'][
                'classification']
            self.blurSL = "No info in DAT2.0"
            self.fogSL = "No info in DAT2.0"
            self.smearSL = "No info in DAT2.0"
            self.selfGSL = "No info in DAT2.0"
            self.spotRSL = "No info in DAT2.0"
            self.frozSL = "No info in DAT2.0"
            self.partBSL = "No info in DAT2.0"
            self.fullBSL = "No info in DAT2.0"
            self.ME_API = "No info in DAT2.0"
            self.ME_SW = "No info in DAT2.0"
            self.VFP_rel_ver = "No info in DAT2.0"
            self.VFP_pro_ver = "No info in DAT2.0"
            self.grabIndex = self.mat['mudp']['vis']['vision_road_info']['roadInfo']['imageIndex']
            self.cntDrop = "No info in DAT2.0"
            self.frameIndex = self.mat['mudp']['vis']['vision_active_light_sensor_info']['activeLightSensorInfo'][
                'frameIndex']
            self.autoFixOk = "No info in DAT2.0"
            # self.dataDict['cameraAlignment_horizon_min'] = "No info in DAT2.0"
            self.cam_ali_hor_min = "No info in DAT2.0"
            self.cam_ali_hor_max = "No info in DAT2.0"
            self.cam_ali_yaw_min = "No info in DAT2.0"
            self.cam_ali_yaw_max = "No info in DAT2.0"
            self.classification = \
            self.mat['mudp']['vis']['vision_active_light_sensor_info']['activeLightSensorInfo']['activeLightSpots'][
                'classification']
            self.f_oncomingLaneNotDark = "No info in DAT2.0"
        else:
            # CADS3.5
            self.laneChange = self.mat['mudp']['vis']['vision_road_info']['laneChange']
            self.a0_LRE = self.mat['mudp']['vis']['vision_road_info']['mergedRoadEdgeInfo']['leftRoadEdge']['roadEdge'][
                'a0']
            self.a1_LRE = self.mat['mudp']['vis']['vision_road_info']['mergedRoadEdgeInfo']['leftRoadEdge']['roadEdge'][
                'a1']
            self.a2_LRE = self.mat['mudp']['vis']['vision_road_info']['mergedRoadEdgeInfo']['leftRoadEdge']['roadEdge'][
                'a2']
            self.a3_LRE = self.mat['mudp']['vis']['vision_road_info']['mergedRoadEdgeInfo']['leftRoadEdge']['roadEdge'][
                'a3']
            self.r_LRE = self.mat['mudp']['vis']['vision_road_info']['mergedRoadEdgeInfo']['leftRoadEdge']['roadEdge'][
                'range']
            self.type_LRE = self.mat['mudp']['vis']['vision_road_info']['mergedRoadEdgeInfo']['leftRoadEdge']['type']
            self.a0_RRE = \
            self.mat['mudp']['vis']['vision_road_info']['mergedRoadEdgeInfo']['rightRoadEdge']['roadEdge']['a0']
            self.a1_RRE = \
            self.mat['mudp']['vis']['vision_road_info']['mergedRoadEdgeInfo']['rightRoadEdge']['roadEdge']['a1']
            self.a2_RRE = \
            self.mat['mudp']['vis']['vision_road_info']['mergedRoadEdgeInfo']['rightRoadEdge']['roadEdge']['a2']
            self.a3_RRE = \
            self.mat['mudp']['vis']['vision_road_info']['mergedRoadEdgeInfo']['rightRoadEdge']['roadEdge']['a3']
            self.r_RRE = self.mat['mudp']['vis']['vision_road_info']['mergedRoadEdgeInfo']['rightRoadEdge']['roadEdge'][
                'range']
            self.type_RRE = self.mat['mudp']['vis']['vision_road_info']['mergedRoadEdgeInfo']['rightRoadEdge']['type']
            self.a0_hIndLLM = \
            self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostLeftIndividualMarker']['laneMarker'][
                'a0']
            self.a1_hIndLLM = \
            self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostLeftIndividualMarker']['laneMarker'][
                'a1']
            self.a2_hIndLLM = \
            self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostLeftIndividualMarker']['laneMarker'][
                'a2']
            self.a3_hIndLLM = \
            self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostLeftIndividualMarker']['laneMarker'][
                'a3']
            self.r_hIndLLM = \
            self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostLeftIndividualMarker']['laneMarker'][
                'range']
            self.a0_hIndRLM = \
            self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostRightIndividualMarker']['laneMarker'][
                'a0']
            self.a1_hIndRLM = \
            self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostRightIndividualMarker']['laneMarker'][
                'a1']
            self.a2_hIndRLM = \
            self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostRightIndividualMarker']['laneMarker'][
                'a2']
            self.a3_hIndRLM = \
            self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostRightIndividualMarker']['laneMarker'][
                'a3']
            self.r_hIndRLM = \
            self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostRightIndividualMarker']['laneMarker'][
                'range']
            self.t_hIndLLM = self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostLeftIndividualMarker'][
                'laneMarkerType']
            self.t_hIndRLM = self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostRightIndividualMarker'][
                'laneMarkerType']
            self.col_hIndLLM = \
            self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostLeftIndividualMarker']['laneMarkerColor']
            self.col_hIndRLM = \
            self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostRightIndividualMarker'][
                'laneMarkerColor']
            self.amb_LLM = self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['f_ambiguousLinePatternLeft']
            self.amb_RLM = self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['f_ambiguousLinePatternRight']
            self.CA = self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['f_constructionArea']
            # self.SFClasL = self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo'][
            #     'hostLeftIndividualSfConfShutdown']
            # self.SFClasR = self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo'][
            #     'hostRightIndividualSfConfShutdown']
            self.NTSR = self.mat['mudp']['vis']['vision_traffic_sign_info']['numberTrafficSigns']
            self.visObjClass = self.mat['mudp']['vis']['vision_obstacles_info']['visObs']['obstacle_class'].astype(int)
            self.ahbcAvail = self.mat['mudp']['vis']['vision_ahbc_info']['ahbcAvailable']
            self.ahbc_events = self.mat['mudp']['vis']['vision_ahbc_info']['eventsDetected']
            self.highway = self.mat['mudp']['vis']['vision_active_light_sensor_info']['highwayDetected']
            self.city = self.mat['mudp']['vis']['vision_active_light_sensor_info']['villageDetected']
            self.tunnel = self.mat['mudp']['vis']['vision_road_info']['f_tunnelEntryOrExit']
            self.lsClass = self.mat['mudp']['vis']['vision_active_light_sensor_info']['activeLightSpots'][
                'classification']
            self.blurSL = self.mat['mudp']['vis']['vision_failsafes']['blurredImageSeverityLevel']
            self.fogSL = self.mat['mudp']['vis']['vision_failsafes']['foggySpotsSeverityLevel']
            self.smearSL = self.mat['mudp']['vis']['vision_failsafes']['smearedSpotsSeverityLevel']
            self.selfGSL = self.mat['mudp']['vis']['vision_failsafes']['selfGlareSeverityLevel']
            self.spotRSL = self.mat['mudp']['vis']['vision_failsafes']['spotRaysSeverityLevel']
            # self.frozSL = self.mat['mudp']['vis']['vision_failsafes']['frozenWindshieldSeverityLevel']
            self.partBSL = self.mat['mudp']['vis']['vision_failsafes']['partialBlockageSeverityLevel']
            self.fullBSL = self.mat['mudp']['vis']['vision_failsafes']['fullBlockageSeverityLevel']
            self.ME_API = self.mat['mudp']['vfpState']['versions']['vision_version_info']['apiVer'][0]
            self.ME_SW = self.mat['mudp']['vfpState']['versions']['vision_version_info']['swVer'][0]
            self.VFP_rel_ver = self.mat['mudp']['vfpState']['versions']['release_revision'][0]
            self.VFP_pro_ver = self.mat['mudp']['vfpState']['versions']['promote_revision'][0]
            self.grabIndex = self.mat['mudp']['vis']['vision_road_info']['imageIndex']
            try:
                self.cntDrop = self.mat['mudp']['vfpDiag']['vision_video_diag_info']['ctrDropError']
            except:
                print("WARNING: mat['mudp']['vfpDiag']['vision_video_diag_info']['ctrDropError'] not found.")
            self.frameIndex = self.mat['mudp']['vis']['vision_active_light_sensor_info']['frameIndex']
            self.autoFixOk = self.mat['mudp']['vis']['vision_camera_alignment_info']['autoFixOk']
            # self.dataDict['cameraAlignment_horizon_min'] = min(
            # self.mat['mudp']['vis']['vision_camera_alignment_info']['cameraAlignment']['horizon'])
            self.cam_ali_hor_min = self.mat['mudp']['vis']['vision_camera_alignment_info']['cameraAlignment']['horizon']
            self.cam_ali_hor_max = self.mat['mudp']['vis']['vision_camera_alignment_info']['cameraAlignment']['horizon']
            self.cam_ali_yaw_min = self.mat['mudp']['vis']['vision_camera_alignment_info']['cameraAlignment']['yaw']
            self.cam_ali_yaw_max = self.mat['mudp']['vis']['vision_camera_alignment_info']['cameraAlignment']['yaw']
            self.classification = self.mat['mudp']['vis']['vision_active_light_sensor_info']['activeLightSpots'][
                'classification']
            self.f_oncomingLaneNotDark = self.mat['mudp']['vis']['vision_active_light_sensor_info'][
                'f_oncomingLaneNotDark']



    def run(self, runParam, uselessParam, refreshFunction=None):
        self.create_namespace()
        if not runParam[0]:
            return

        if self.dat2p0:
            time = self.mat['mudp']['vis']['header']['cTime'] / 1000000.0
            #v_veh = self.mat['mudp']['vfpState']['vse_out']['vcs_long_velocity'] * 3.6
            #v_yaw = self.mat['mudp']['vfpState']['vse_out']['raw_yaw_rate_rps'] * 180 / 3.1416
            v_veh = self.mat['mudp']['VSE']['vse_out']['vcs_long_velocity'] * 3.6
            v_yaw = self.mat['mudp']['VSE']['vse_out']['raw_yaw_rate_rps'] * 180 / 3.1416
        else:
            # time in log
            time = self.mat['mudp']['vis']['header']['cTime'] / 1000000.0
            v_veh = self.mat['mudp']['vis']['vision_vehicle_info']['vehicleVelocity'] * 3.6
            v_yaw = self.mat['mudp']['vis']['vision_vehicle_info']['vehicleYawRate'] * 180 / 3.1416
        print('Running {} script...'.format(self.function))

        dataDict = {}
        errorNameList = []

        try:
            # 1 - filename
            dataDict['LogName'] = self.matName
        except:
            errorNameList.append('LogName')
        try:
            # 2 - file status
            dataDict['Status'] = 'Available'
        except:
            errorNameList.append('Status')


        nsample = float(self.visLen)

        # General info
        try:
            # 3 - distance [km]
            dataDict['Distance'] = self.distanceCalculation()
        except:
            errorNameList.append('Distance')
        try:
            # 4 - duration [s]
            time_sum = 0
            for i in range(self.visLen - 1):
                dt = time[i + 1] - time[i]
                if dt >= 0:
                    time_sum += dt
                else:
                    time_sum += 0.0556
            dataDict['Duration'] = time_sum
        except:
            errorNameList.append('Duration')



        try:
            # 5 - vehicle average speed [km/h]
            dataDict['AvgSpeed'] = np.mean(v_veh)
        except:
            errorNameList.append('AvgSpeed')
        try:
            # 6 - vehicle min speed [km/h]
            dataDict['MinSpeed'] = min(v_veh)
        except:
            errorNameList.append('MinSpeed')
        try:
            # 7 - vehicle max speed [km/h]
            dataDict['MaxSpeed'] = max(v_veh)
        except:
            errorNameList.append('MaxSpeed')
        try:
            # 8 - vehicle average yaw rate [deg/s]
            dataDict['AvgYrate'] = np.mean(v_yaw)
        except:
            errorNameList.append('AvgYrate')
        try:
            # 9 - vehicle min yaw rate [deg/s]
            dataDict['MinYrate'] = min(v_yaw)
        except:
            errorNameList.append('MinYrate')
        try:
            # 10 - vehicle max yaw rate [deg/s]
            dataDict['MaxYrate'] = max(v_yaw)
        except:
            errorNameList.append('MaxYrate')

        if refreshFunction is not None:
            refreshFunction()

##########################################################################################################
        # LKS

        # 11 - changing lane
        try:
            dataDict['ChngLane'] = np.array(self.laneChange != 0).sum()
        except:
            errorNameList.append('ChngLane')
        try:

            avail = []
            isBarrier = 0
            isFlat = 0
            for i in range(self.visLen):
                if self.a0_LRE[i] == 0 and self.a1_LRE[i] == 0 and self.a2_LRE[i] == 0 and self.a3_LRE[i] == 0 and self.r_LRE[i] == 0:
                    avail.append(0)
                else:
                    avail.append(1)
                    if self.type_LRE[i] == 1:
                        isFlat += 1
                    else:
                        isBarrier += 1
            dataDict['AvailLRE'] = sum(avail) / nsample
            if isFlat:
                dataDict['LREasFlat'] = isFlat / float(isFlat + isBarrier)
            else:
                dataDict['LREasFlat'] = 0
            if isBarrier:
                dataDict['LREasBarrier'] = isBarrier / float(isFlat + isBarrier)
            else:
                dataDict['LREasBarrier'] = 0
        except:
            errorNameList.append('AvailLRE')
        try:
            avail = []
            isBarrier = 0
            isFlat = 0
            for i in range(self.visLen):
                if self.a0_RRE[i] == 0 and self.a1_RRE[i] == 0 and self.a2_RRE[i] == 0 and self.a3_RRE[i] == 0 and self.r_RRE[i] == 0:
                    avail.append(0)
                else:
                    avail.append(1)
                    if type[i] == 1:
                        isFlat += 1
                    else:
                        isBarrier += 1
            dataDict['AvailRRE'] = sum(avail) / nsample
            if isFlat:
                dataDict['RREasFlat'] = isFlat / float(isFlat + isBarrier)
            else:
                dataDict['RREasFlat'] = 0
            if isBarrier:
                dataDict['RREasBarrier'] = isBarrier / float(isFlat + isBarrier)
            else:
                dataDict['RREasBarrier'] = 0
        except:
            errorNameList.append('AvailRRE')
        try:
            # 14 - left lane avail [%]
            avail = []
            for i in range(self.visLen):
                if self.a0_hIndLLM[i] == 0 and self.a1_hIndLLM[i] == 0 and self.a2_hIndLLM[i] == 0 and self.a3_hIndLLM[i] == 0 and self.r_hIndLLM[i] == 0:
                    avail.append(0)
                else:
                    avail.append(1)
            dataDict['AvailLL'] = sum(avail) / nsample
        except:
            errorNameList.append('AvailLL')
        try:
            # 15 - right lane avail [%]
            avail = []
            for i in range(self.visLen):
                if self.a0_hIndRLM[i] == 0 and self.a1_hIndRLM[i] == 0 and self.a2_hIndRLM[i] == 0 and self.a3_hIndRLM[i] == 0 and self.r_hIndRLM[i] == 0:
                    avail.append(0)
                else:
                    avail.append(1)
            dataDict['AvailRL'] = sum(avail) / nsample
        except:
            errorNameList.append('AvailRL')
        try:
            # 16 - left lane solid [%]

            s = 0
            for i in range(self.visLen):
                if self.t_hIndLLM[i] == 1:
                    s += 1
            dataDict['SolidLL'] = s / nsample
        except:
            errorNameList.append('SolidLL')
        try:
            # 17 - right lane solid [%]
            s = 0
            for i in range(self.visLen):
                if self.t_hIndRLM[i] == 1:
                    s += 1
            dataDict['SolidRL'] = s / nsample
        except:
            errorNameList.append('SolidRL')
        try:
            # 18 - left lane dashed [%]
            s = 0
            for i in range(self.visLen):
                if self.t_hIndLLM[i] == 2:
                    s += 1
            dataDict['DashLL'] = s / nsample
        except:
            errorNameList.append('DashLL')
        try:
            # 19 - right lane dashed [%]
            s = 0
            for i in range(self.visLen):
                if self.t_hIndRLM[i] == 2:
                    s += 1
            dataDict['DashRL'] = s / nsample
        except:
            errorNameList.append('DashRL')
        try:
            # 20 - left lane white [%]
            s = 0
            for i in range(self.visLen):
                if self.col_hIndLLM[i] == 2:
                    s += 1
            dataDict['WhiteLL'] = s / nsample
        except:
            errorNameList.append('WhiteLL')
        try:
            # 21 - right lane white [%]
            s = 0
            for i in range(self.visLen):
                if self.col_hIndRLM[i] == 2:
                    s += 1
            dataDict['WhiteRL'] = s / nsample
        except:
            errorNameList.append('WhiteRL')
        try:
            # 22 - left lane yellow [%]
            s = 0
            for i in range(self.visLen):
                if self.col_hIndLLM[i] == 1:
                    s += 1
            dataDict['YellLL'] = s / nsample
        except:
            errorNameList.append('YellLL')
        try:
            # 23 - right lane yellow [%]
            s = 0
            for i in range(self.visLen):
                if self.col_hIndRLM[i] == 1:
                    s += 1
            dataDict['YellRL'] = s / nsample
        except:
            errorNameList.append('YellRL')
        try:
            # 24 - left lane ambiguous [%]
            s = 0
            for i in range(self.visLen):
                if self.amb_LLM[i] == 1:
                    s += 1
            dataDict['AmbigL'] = s / nsample
        except:
            errorNameList.append('AmbigL')
        try:
            # 25 - right lane ambiguous [%]

            s = 0
            for i in range(self.visLen):
                if self.amb_RLM[i] == 1:
                    s += 1
            dataDict['AmbigR'] = s / nsample
        except:
            errorNameList.append('AmbigR')
        try:
            # 26 - construction area [%]
            s = 0
            for i in range(self.visLen):
                if self.CA[i] == 1:
                    s += 1
            dataDict['ConstArea'] = s / nsample
        except:
            errorNameList.append('ConstArea')
        try:
            # 27 - Single Frame Classifier Left [%]
            s = 0
            for i in range(self.visLen):
                if self.SFClasL[i] == 1:
                    s += 1
            dataDict['SFClasL'] = s / nsample
        except:
            errorNameList.append('SFClasL')
        try:
            # 28 - Single Frame Classifier Right [%]
            s = 0
            for i in range(self.visLen):
                if self.SFClasR[i] == 1:
                    s += 1
            dataDict['SFClasR'] = s / nsample
        except:
            errorNameList.append('SFClasR')

        if refreshFunction is not None:
            refreshFunction()

##########################################################################################################
        # TSR
        try:
            # 29 - number of TS
            num_TSR = np.insert(self.N_TSR.astype(int), 0, 0)
            s = (np.diff(num_TSR) * np.array(np.diff(num_TSR) > 0, int)).sum()
            dataDict['TSRNum'] = s
        except:
            errorNameList.append('TSRNum')

        if refreshFunction is not None:
            refreshFunction()

##########################################################################################################
        # OBJ


        s = []
        for i in [1, 2, 3, 4, 7, 9]:
            total = np.insert(np.array(self.visObjClass == i).sum(axis=1), 0, 0)
            s.append((np.diff(total) * np.array(np.diff(total) > 0, int)).sum())

        try:
            # 30 - number of car
            dataDict['CarNum'] = s[0]
        except:
            errorNameList.append('CarNum')
        try:
            # 31 - number of motocycle
            dataDict['MclNum'] = s[1]
        except:
            errorNameList.append('MclNum')
        try:
            # 32 - number of truck
            dataDict['TrkNum'] = s[2]
        except:
            errorNameList.append('TrkNum')
        try:
            # 33 - number of pedestrian
            dataDict['PedNum'] = s[3]
        except:
            errorNameList.append('PedNum')
        try:

            # 34 - number of animal
            dataDict['AniNum'] = s[4]
        except:
            errorNameList.append('AniNum')
        try:
            # 35 - number of bicycle
            dataDict['BclNum'] = s[5]
        except:
            errorNameList.append('BclNum')

        if refreshFunction is not None:
            refreshFunction()

##########################################################################################################
        # AFL

        try:
            # 36 - day [%]
            s = 0
            for i in range(self.visLen):
                if self.ahbcAvail[i] == 0:
                    s += 1
            dataDict['Day'] = s / nsample
        except:
            errorNameList.append('Day')
        try:
            # 37 - twilight [%]
            s = 0
            for i in range(self.visLen):
                if self.ahbcAvail[i] == 1:
                    s += 1
            dataDict['Dusk'] = s / nsample
        except:
            errorNameList.append('Dusk')
        try:
            # 38 - night [%]
            s = 0
            for i in range(self.visLen):
                if self.ahbcAvail[i] == 2:
                    s += 1
            dataDict['Night'] = s / nsample
        except:
            errorNameList.append('Night')
        try:
            # 39 - ambient light [%]

            s = 0
            for i in range(self.visLen):
                if self.bitget(self.ahbc_events[i], 5) == 1:
                    s += 1
            dataDict['AmbLght'] = s / nsample
        except:
            errorNameList.append('AmbLght')
        try:
            # 40 - highway [%]

            dataDict['Highway'] = sum(self.highway) / nsample
        except:
            errorNameList.append('Highway')
        try:
            # 41 - city [%]

            dataDict['City'] = sum(self.city) / nsample
        except:
            errorNameList.append('City')
        try:
            # 42 - tunnel [%]

            dataDict['Tunnel'] = sum(self.tunnel) / nsample
        except:
            errorNameList.append('Tunnel')


        try:
            # 43 - number of headlamp lightspots
            total = np.insert(np.array(self.lsClass == 1).sum(axis=1), 0, 0) + \
                    np.insert(np.array(self.lsClass == 3).sum(axis=1), 0, 0)
            s = (np.diff(total) * np.array(np.diff(total) > 0, int)).sum()
            dataDict['HLNum'] = s
        except:
            errorNameList.append('HLNum')
        try:
            # 44 - number of taillamp lightspots
            total = np.insert(np.array(self.lsClass == 2).sum(axis=1), 0, 0) + \
                    np.insert(np.array(self.lsClass == 4).sum(axis=1), 0, 0)
            s = (np.diff(total) * np.array(np.diff(total) > 0, int)).sum()
            dataDict['TLNum'] = s
        except:
            errorNameList.append('TLNum')
        try:
            # 45 - number of truck cabin lightspots
            total = np.insert(np.array(self.lsClass == 5).sum(axis=1), 0, 0)
            s = (np.diff(total) * np.array(np.diff(total) > 0, int)).sum()
            dataDict['TrkCLNum'] = s
        except:
            errorNameList.append('TrkCLNum')
        try:
            # 46 - dark oncoming lane (HOST) [%]
            DarkOncL = self.f_oncomingLaneNotDark_To_dark_oncoming_lane()
            s = 0
            for i in range(self.visLen):
                if DarkOncL[i] == 1:
                    s += 1
            dataDict['DarkOncL'] = s / nsample
        except:
            errorNameList.append('DarkOncL')

        if refreshFunction is not None:
            refreshFunction()

##########################################################################################################
        # Severity levels

        try:
            # 47 - blurredImageSeverityLevel

            s = 0
            for i in range(self.visLen):
                if self.blurSL[i] > 0:
                    s += 1
            dataDict['blurSL'] = s / nsample
        except:
            errorNameList.append('blurSL')

        try:
            # 48 - foggySpotsSeverityLevel

            s = 0
            for i in range(self.visLen):
                if self.fogSL[i] > 0:
                    s += 1
            dataDict['fogSL'] = s / nsample
        except:
            errorNameList.append('fogSL')

        try:
            # 49 - smearedSpotsSeverityLevel

            s = 0
            for i in range(self.visLen):
                if self.smearSL[i] > 0:
                    s += 1
            dataDict['smearSL'] = s / nsample
        except:
            errorNameList.append('smearSL')

        try:
            # 50 - selfGlareSeverityLevel

            s = 0
            for i in range(self.visLen):
                if self.selfGSL[i] > 0:
                    s += 1
            dataDict['selfGSL'] = s / nsample
        except:
            errorNameList.append('selfGSL')

        try:
            # 51 - spotRaySeverityLevel

            s = 0
            for i in range(self.visLen):
                if self.spotRSL[i] > 0:
                    s += 1
            dataDict['spotRSL'] = s / nsample
        except:
            errorNameList.append('spotRSL')

        try:
            # 52 - frozenWindshieldSeverityLevel

            s = 0
            for i in range(self.visLen):
                if self.frozSL[i] > 0:
                    s += 1
            dataDict['frozSL'] = s / nsample
        except:
            errorNameList.append('frozSL')

        try:
            # 53 - partialBlockageSeverityLevel

            s = 0
            for i in range(self.visLen):
                if self.partBSL[i] > 0:
                    s += 1
            dataDict['partBSL'] = s / nsample
        except:
            errorNameList.append('partBSL')

        try:
            # 54 - fullBlockageSeverityLevel

            s = 0
            for i in range(self.visLen):
                if self.fullBSL[i] > 0:
                    s += 1
            dataDict['fullBSL'] = s / nsample
        except:
            errorNameList.append('fullBSL')

        if refreshFunction is not None:
            refreshFunction()

##########################################################################################################
        # Other
        try:
            # 55 - frames
            dataDict['Frames'] = self.visLen
        except:
            errorNameList.append('Frames')
        try:
            # 56 - meAPI
            dataDict['ME_API'] = str(self.ME_API)
        except:
            errorNameList.append('ME_API')
        try:
            # 57 - meSW
            dataDict['ME_SW'] = str(self.ME_SW)
        except:
            errorNameList.append('ME_SW')
        try:
            # 58 - vfpVer
            dataDict['VFP_ver'] = str(self.VFP_rel_ver) + '.' + \
                                 str(self.VFP_pro_ver)
        except:
            errorNameList.append('VFP_ver')

        if refreshFunction is not None:
            refreshFunction()

##########################################################################################################
        # Diag
        try:
            # 59 - simple Frame Drop [num]

            s = 0
            for i in range(self.visLen - 1):
                delta = self.grabIndex[i + 1] - self.grabIndex[i]
                if delta != 2 and delta >= 0:
                    s += 1
            dataDict['simpFrDrop'] = s
        except:
            errorNameList.append('simpFrDrop')
        try:
            # 60 - Error counter [num]
            # 61 - Error fault counter [num]

            cntError = 0
            cntFault = 0

            for i in range(len(self.cntDrop) - 1):
                delta = self.cntDrop[i + 1] - self.cntDrop[i]
                if delta == 1:
                    cntError += 1
                elif delta > 1:
                    cntFault += 1
            dataDict['cntError'] = cntError
            dataDict['cntFault'] = cntFault
        except:
            errorNameList.append('cntError')
            errorNameList.append('cntFault')
        try:
            # 62 - single Frame Drop [num]
            # 63 - multiple Frame Drop [num]
            # 64 - continuous Frame Drop [num]
            # 65 - decrease Frame Drop [num]

            sFrDrop = 0
            mFrDrop = 0
            conFrDrop = 0
            decFrDrop = 0
            singleFrameDropEvent = 0
            for i in range(self.visLen - 1):
                delta = self.frameIndex[i + 1] - self.frameIndex[i]
                if delta == 0:
                    conFrDrop += 1
                elif delta == 1:
                    singleFrameDropEvent += 1
                elif delta == 2:
                    if singleFrameDropEvent > 0:
                        if singleFrameDropEvent > 1:
                            mFrDrop += 1
                        else:
                            sFrDrop += 1
                        singleFrameDropEvent = 0
                elif delta < 0:
                    decFrDrop += 1
            dataDict['sFrDrop'] = sFrDrop
            dataDict['mFrDrop'] = mFrDrop
            dataDict['conFrDrop'] = conFrDrop
            dataDict['decFrDrop'] = decFrDrop
        except:
            errorNameList.append('sFrDrop')
            errorNameList.append('mFrDrop')
            errorNameList.append('conFrDrop')
            errorNameList.append('decFrDrop')

        if refreshFunction is not None:
            refreshFunction()

##########################################################################################################
        # Camera
        try:
            dataDict['autoFixOk'] = sum(self.autoFixOk) / float(nsample)
        except:
            errorNameList.append('autoFixOk')
        try:
            dataDict['cameraAlignment_horizon_min'] = min(self.cam_ali_hor_min)
        except:
            errorNameList.append('cameraAlignment_horizon_min')
        try:
            dataDict['cameraAlignment_horizon_max'] = max(self.cam_ali_hor_max )
        except:
            errorNameList.append('cameraAlignment_horizon_max')
        try:
            dataDict['cameraAlignment_yaw_min'] = min(self.cam_ali_hor_min)
        except:
            errorNameList.append('cameraAlignment_yaw_min')
        try:
            dataDict['cameraAlignment_yaw_max'] = max(cam_ali_yaw_max)
        except:
            errorNameList.append('cameraAlignment_yaw_max')

        self.eventsDictList.append(dataDict)
        if errorNameList:
            print('\tCannot read: ', str(list(set(errorNameList)))[1:-1])

    def distanceCalculation(self):
        if self.dat2p0:
            v_veh = self.mat['mudp']['vfpState']['vse_out']['vcs_long_velocity']
            time = self.mat['mudp']['vis']['header']['cTime'] / 1000000.0
        else:
            v_veh = self.mat['mudp']['vis']['vision_vehicle_info']['vehicleVelocity']
            time = self.mat['mudp']['vis']['header']['cTime'] / 1000000.0
        # calculating distance in the log

        meter_sum = 0
        for i in range(self.visLen - 1):
            dt = time[i + 1] - time[i]
            if dt >= 0:
                meter_sum += v_veh[i] * dt
            else:
                meter_sum += v_veh[i] * 0.0556
        return meter_sum / 1000.0

    def bitget(self, x, nbit):
        x >>= nbit - 1
        return x % 2

    def f_oncomingLaneNotDark_To_dark_oncoming_lane(self):

        dark_oncoming_lane = np.empty(self.f_oncomingLaneNotDark.shape[0], dtype=np.int64)
        for i in range(self.f_oncomingLaneNotDark.shape[0]):
            if self.f_oncomingLaneNotDark[i] == 1:
                dark_oncoming_lane[i] = 0
            else:
                for j in range(self.classification.shape[1]):
                    condition = self.classification[i][j] == 1 or self.classification[i][j] == 3
                    if condition:
                        dark_oncoming_lane[i] = 0
                        break
                    else:
                        dark_oncoming_lane[i] = 1
        return dark_oncoming_lane
