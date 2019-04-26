import numpy as np
from itertools import product
import collections

from analystToolKit.lib.efsClasses import efsFrameClass


class failsafesEFs(efsFrameClass.EFClass):


        def __init__(self):
            self.function = 'FS'

        """
        try:
            eventsDict[] = \
            
        except:
            errorNameList.append()
        """

        def appendDetails(self):
            try:
                from delphiTools3 import base
                self.dvlExt = base.loadmat(self.mat['__path__'], variableName='dvlExt')['dvlExt']
            except:
                print('error')
            mapDayNight = {0: 'day', 1: 'dusk', 2: 'night'}
            mapLaneConf = {240: 0, 150: 2, 105: 1}
            car_id_list = ['KQW3213', 'KQW3211', 'KQW3215', 'KQW3210', 'KQW6524', 'KQZ7442', 'KQZ7441', 'EU64FVF',
                           '564W756', '517W750', '516W341', '565W051', '565W081', '565W696', '565W697',
                           '565W698', 'AH359H', 'AH555G', 'AG628D', 'GA62099', 'GA62048', 'A0H1C9','STELIAN']

            self.header += ['severity_level','carID','day/night','detected_vru','detected_veh','detected_obj','detected_signs',
                            'leftlaneMarkerConf2 duration','leftlaneMarkerConf3 duration','rightlaneMarkerConf2 duration',
                            'rightlaneMarkerConf3 duration','f_ambiguousLinePatternRight duration','f_ambiguousLinePatternLeft duration',
                            'roadPredictionLeft','roadPredictionRight','activeLightSpots',
                            'camera_dist_lwheel_mm','camera_dist_rwheel_mm','vcs_camera_height','vcs_camera_lat',
                            'vcs_camera_long','f_tunnelEntryOrExit duration','f_constructionArea duration','urban_area duration','leftWheel_mm',
                            'rightWheel_mm','amb_air_tempMax','amb_air_tempMin','villageDetected','imagerTemperatureMin',
                            'imagerTemperatureMax','mipsTemperatureMin',
                            'mipsTemperatureMax','vmpTemperatureMin','vmpTemperatureMax','ddrTemperatureMin',
                             'ddrTemperatureMax','imagerChipVersion','imagerFuseID','hardwareRevision','vehicle_type',
                            'vehicle_region', 'vehicle_country','horizonKA','yawKA','rollAngleKA','cameraAlignmentValidKA',
                             'drivingSideKA','currentMarketKA','tsrMarketKA','PercentRamUsage','autoFixOk',
                             'horizon','yaw','rollAngle','washerFrontcmd','wiperFrontCmd','wiperSpeedInfo']

            errorNameList = []
            for eventsDict in self.eventsDictList:
                index = int(np.where(self.visIndex == eventsDict['eventIndex'])[0][0])
                columnID = eventsDict['eventColumnID']
                try:
                    eventsDict['day/night'] = \
                        mapDayNight[int(round(np.mean(self.mat['mudp']['vis']['vision_ahbc_info']['ahbcAvailable'])))]
                except:
                    errorNameList.append('day/night')
                try:
                    eventsDict['severity_level'] = \
                        self.mat['mudp']['vis']['vision_failsafes'][eventsDict['eventComment']][index]
                except:
                    errorNameList.append('severity_level')
                try:
                    eventsDict['carID'] = \
                        [x for x in car_id_list if x in eventsDict['logName'].upper()][0]
                except:
                    errorNameList.append('carID')
                try:
                    eventsDict['detected_vru'] = \
                        self.object_counter(index, eventsDict['eventDuration'], 4,9)
                except:
                    errorNameList.append('detected_vru')
                try:
                    eventsDict['detected_veh'] = \
                        self.object_counter(index,eventsDict['eventDuration'],1,3)
                except:
                    errorNameList.append('detected_veh')
                try:
                    eventsDict['detected_obj'] = \
                        (self.mat['mudp']['vis']['vision_obstacles_info']['visObs']['detection_status']
                         [index:index + eventsDict['eventDuration']] == 1).sum()
                except:
                    errorNameList.append('detected_obj')
                try:
                    eventsDict['detected_signs'] = \
                        (self.mat['mudp']['vis']['vision_traffic_sign_info']['trafficSigns']['signStatus']
                        [index:index + eventsDict['eventDuration']] == 2).sum()
                except:
                    errorNameList.append('detected_signs')
                try:
                    eventsDict['leftlaneMarkerConf2 duration'] = \
                        (self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostLeftIndividualMarker'][
                            'laneMarkerConf']['confLKA'][index:index+eventsDict['eventDuration']] == 105).sum()
                except:
                    errorNameList.append('leftlaneMarkerConf2 duration')
                try:
                    eventsDict['rightlaneMarkerConf2 duration'] = \
                        (self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostRightIndividualMarker'][
                            'laneMarkerConf']['confLKA'][index:index+eventsDict['eventDuration']] == 105).sum()
                except:
                    errorNameList.append('rightlaneMarkerConf2 duration')
                try:
                    eventsDict['leftlaneMarkerConf3 duration'] = \
                        (self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostLeftIndividualMarker'][
                            'laneMarkerConf']['confLKA'][index:index+eventsDict['eventDuration']] == 150).sum()
                except:
                    errorNameList.append('leftlaneMarkerConf3 duration')
                try:
                    eventsDict['rightlaneMarkerConf3 duration'] = \
                        (self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostRightIndividualMarker'][
                            'laneMarkerConf']['confLKA'][index:index+eventsDict['eventDuration']] == 150).sum()
                except:
                    errorNameList.append('rightlaneMarkerConf3 duration')
                try:
                    eventsDict['f_ambiguousLinePatternLeft duration'] = \
                        (self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['f_ambiguousLinePatternLeft'][
                            index:index+eventsDict['eventDuration']] == 1).sum()
                except:
                    errorNameList.append('f_ambiguousLinePatternLeft duration')
                try:
                    eventsDict['f_ambiguousLinePatternRight duration'] = \
                        (self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['f_ambiguousLinePatternRight'][
                            index:index+eventsDict['eventDuration']] == 1).sum()
                except:
                    errorNameList.append('f_ambiguousLinePatternRight duration')
                try:
                    eventsDict['roadPredictionLeft'] = \
                        dict(collections.Counter(self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['roadPredictionLeft'][
                            index:index+eventsDict['eventDuration']]))
                except:
                    errorNameList.append('roadPredictionLeft')
                try:
                    eventsDict['roadPredictionRight'] = \
                        dict(collections.Counter(self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['roadPredictionRight'][
                            index:index+eventsDict['eventDuration']]))
                except:
                    errorNameList.append('roadPredictionRight')
                try:
                    eventsDict['activeLightSpots'] = \
                        (np.unique(self.mat['mudp']['vis']['vision_active_light_sensor_info']['activeLightSpots']['id']
                                  [index:index+eventsDict['eventDuration']]) > 0).sum()
                except:
                    errorNameList.append('activeLightSpots')
                try:
                    eventsDict['camera_dist_lwheel_mm'] = \
                        self.mat['mudp']['vfpState']['cals']['corse_sensor_cals']['camera_mounting']['camera_dist_lwheel_mm'][index]
                except:
                    errorNameList.append('camera_dist_lwheel_mm')
                try:
                    eventsDict['camera_dist_rwheel_mm'] = \
                        self.mat['mudp']['vfpState']['cals']['corse_sensor_cals']['camera_mounting']['camera_dist_rwheel_mm'][index]
                except:
                    errorNameList.append('camera_dist_rwheel_mm')
                try:
                    eventsDict['vcs_camera_height'] = \
                        self.mat['mudp']['vfpState']['cals']['corse_sensor_cals']['camera_mounting']['vcs_camera_height'][index]
                except:
                    errorNameList.append('vcs_camera_height')
                try:
                    eventsDict['vcs_camera_lat'] = \
                        self.mat['mudp']['vfpState']['cals']['corse_sensor_cals']['camera_mounting']['vcs_camera_lat'][index]
                except:
                    errorNameList.append('vcs_camera_lat')
                try:
                    eventsDict['vcs_camera_long'] = \
                        self.mat['mudp']['vfpState']['cals']['corse_sensor_cals']['camera_mounting']['vcs_camera_long'][index]
                except:
                    errorNameList.append('vcs_camera_long')
                try:
                    eventsDict['f_tunnelEntryOrExit duration'] = \
                        (self.mat['mudp']['vis']['vision_road_info']['f_tunnelEntryOrExit']
                         [index:index + eventsDict['eventDuration']] != 0).sum()
                except:
                    errorNameList.append('f_tunnelEntryOrExit duration')
                try:
                    eventsDict['f_constructionArea duration'] = \
                        (self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['f_constructionArea']
                         [index:index + eventsDict['eventDuration']] != 0).sum()
                except:
                    errorNameList.append('f_constructionArea duration')
                try:
                    eventsDict['urban_area duration'] = \
                        (self.dvlExt['vis']['ahbc']['urban_area'][index:index + eventsDict['eventDuration']] != 0).sum()
                except:
                    errorNameList.append('urban_area duration')
                try:
                    eventsDict['leftWheel_mm'] = \
                        self.mat['mudp']['vfpState']['cals']['vision_params']['vehDependentParam']['leftWheel_mm'][index]
                except:
                    errorNameList.append('leftWheel_mm')
                try:
                    eventsDict['rightWheel_mm'] = \
                        self.mat['mudp']['vfpState']['cals']['vision_params']['vehDependentParam']['rightWheel_mm'][index]
                except:
                    errorNameList.append('rightWheel_mm')
                try:
                    eventsDict['amb_air_tempMax'] = \
                        max(self.dvlExt['veh']['ahbc']['amb_air_temp'])
                except:
                    errorNameList.append('amb_air_tempMax')
                try:
                    eventsDict['amb_air_tempMin'] = \
                        min(self.dvlExt['veh']['ahbc']['amb_air_temp'])
                except:
                    errorNameList.append('amb_air_tempMin')
                try:
                    eventsDict['villageDetected'] = \
                        self.mat['mudp']['vis']['vision_active_light_sensor_info']['villageDetected'][index]
                except:
                    errorNameList.append('villageDetected')
                try:
                    eventsDict['imagerTemperatureMin'] = \
                        min(self.mat['mudp']['vfpDiag']['vision_temperature_info']['imagerTemperature'])
                except:
                    errorNameList.append('imagerTemperatureMin')
                try:
                    eventsDict['mipsTemperatureMin'] = \
                        min(self.mat['mudp']['vfpDiag']['vision_temperature_info']['mipsTemperature'])
                except:
                    errorNameList.append('mipsTemperatureMin')
                try:
                    eventsDict['vmpTemperatureMin'] = \
                        min(self.mat['mudp']['vfpDiag']['vision_temperature_info']['vmpTemperature'])
                except:
                    errorNameList.append('vmpTemperatureMin')
                try:
                    eventsDict['ddrTemperatureMin'] = \
                        min(self.mat['mudp']['vfpDiag']['vision_temperature_info']['ddrTemperature'])
                except:
                    errorNameList.append('ddrTemperatureMin')
                try:
                    eventsDict['imagerTemperatureMax'] = \
                        max(self.mat['mudp']['vfpDiag']['vision_temperature_info']['imagerTemperature'])
                except:
                    errorNameList.append('imagerTemperatureMax')
                try:
                    eventsDict['mipsTemperatureMax'] = \
                        max(self.mat['mudp']['vfpDiag']['vision_temperature_info']['mipsTemperature'])
                except:
                    errorNameList.append('mipsTemperatureMax')
                try:
                    eventsDict['vmpTemperatureMax'] = \
                        max(self.mat['mudp']['vfpDiag']['vision_temperature_info']['vmpTemperature'])
                except:
                    errorNameList.append('vmpTemperatureMax')
                try:
                    eventsDict['ddrTemperatureMax'] = \
                        max(self.mat['mudp']['vfpDiag']['vision_temperature_info']['ddrTemperature'])
                except:
                    errorNameList.append('ddrTemperaturMaxe')
                try:
                    eventsDict['imagerChipVersion'] = \
                        max(self.mat['mudp']['vfpDiag']['vision_app_init_info']['imagerChipVersion'])
                except:
                    errorNameList.append('imagerChipVersion')
                try:
                    eventsDict['imagerFuseID'] = \
                        self.mat['mudp']['vfpDiag']['vision_app_init_info']['imagerFuseID'][round(index/9)]
                except:
                    errorNameList.append('imagerFuseID')
                try:
                    eventsDict['hardwareRevision'] = \
                        self.mat['mudp']['vfpDiag']['vision_app_init_info']['hardwareRevision'][round(index/9)]
                except:
                    errorNameList.append('hardwareRevision')
                try:
                    eventsDict['vehicle_type'] = \
                        self.mat['mudp']['vfpState']['cals']['delphi_sw_params']['vehicle_type'][index]
                except:
                    errorNameList.append('vehicle_type')
                try:
                    eventsDict['vehicle_region'] = \
                        self.mat['mudp']['vfpState']['cals']['delphi_sw_params']['vehicle_region'][index]
                except:
                    errorNameList.append('vehicle_region')
                try:
                    eventsDict['vehicle_country'] = \
                        self.mat['mudp']['vfpState']['cals']['delphi_sw_params']['vehicle_country'][index]
                except:
                    errorNameList.append('vehicle_country')
                try:
                    eventsDict['horizonKA'] = \
                        self.mat['mudp']['vfpState']['cals']['vision_params']['driveCycleParam']['horizonKA'][index]
                except:
                    errorNameList.append('horizonKA')
                try:
                    eventsDict['yawKA'] = \
                        self.mat['mudp']['vfpState']['cals']['vision_params']['driveCycleParam']['yawKA'][index]
                except:
                    errorNameList.append('yawKA')
                try:
                    eventsDict['rollAngleKA'] = \
                        self.mat['mudp']['vfpState']['cals']['vision_params']['driveCycleParam']['rollAngleKA'][index]
                except:
                    errorNameList.append('rollAngleKA')
                try:
                    eventsDict['cameraAlignmentValidKA'] = \
                        self.mat['mudp']['vfpState']['cals']['vision_params']['driveCycleParam'][
                            'cameraAlignmentValidKA'][index]
                except:
                    errorNameList.append('cameraAlignmentValidKA')
                try:
                    eventsDict['drivingSideKA'] = \
                        self.mat['mudp']['vfpState']['cals']['vision_params']['driveCycleParam']['drivingSideKA'][index]
                except:
                    errorNameList.append('drivingSideKA')
                try:
                    eventsDict['currentMarketKA'] = \
                        self.mat['mudp']['vfpState']['cals']['vision_params']['driveCycleParam']['currentMarketKA'][index]
                except:
                    errorNameList.append('currentMarketKA')
                try:
                    eventsDict['tsrMarketKA'] = \
                        self.mat['mudp']['vfpState']['cals']['vision_params']['driveCycleParam']['tsrMarketKA'][index]
                except:
                    errorNameList.append('tsrMarketKA')
                try:
                    eventsDict['PercentRamUsage'] = \
                        max(self.mat['mudp']['vfpDiag']['PercentRamUsage'])
                except:
                    errorNameList.append('PercentRamUsage')
                try:
                    eventsDict['autoFixOk'] = \
                        self.mat['mudp']['vis']['vision_camera_alignment_info']['autoFixOk'][index]
                except:
                    errorNameList.append('autoFixOk')
                try:
                    eventsDict['horizon'] = \
                        self.mat['mudp']['vis']['vision_camera_alignment_info']['cameraAlignment']['horizon'][index]
                except:
                    errorNameList.append('horizon')
                try:
                    eventsDict['yaw'] = \
                        self.mat['mudp']['vis']['vision_camera_alignment_info']['cameraAlignment']['yaw'][index]
                except:
                    errorNameList.append('yaw')
                try:
                    eventsDict['rollAngle'] = \
                        self.mat['mudp']['vis']['vision_camera_alignment_info']['cameraAlignment']['rollAngle'][index]
                except:
                    errorNameList.append('rollAngle')
                try:
                    eventsDict['washerFrontcmd'] = \
                        round((self.mat['mudp']['vfpState']['cmd_msg']['veh_state_info']['washerFrontcmd']
                         [round(index*3.7):round((index + eventsDict['eventDuration'])*3.7)] > 0).sum()/3.6)
                except:
                    errorNameList.append('washerFrontcmd')
                try:
                    eventsDict['wiperFrontCmd'] = \
                        round((self.mat['mudp']['vfpState']['cmd_msg']['veh_state_info']['wiperFrontCmd']
                         [round(index*3.6):round((index + eventsDict['eventDuration'])*3.6)] > 0).sum()/3.6)
                except:
                    errorNameList.append('wiperFrontCmd')
                try:
                    eventsDict['wiperSpeedInfo'] = \
                        round((self.mat['mudp']['vfpState']['cmd_msg']['veh_state_info']['wiperSpeedInfo']
                         [round(index*3.7):round((index + eventsDict['eventDuration'])*3.6)] > 0).sum()/3.6)
                except:
                    errorNameList.append('rollAngle')

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
            imageIndex = self.mat['mudp']['vis']['vision_function_info']['imageIndex']

            data = []
            indexes = []
            for index in range(self.visLen):
                if index % 2 == 0:
                    indexes.append(index)

            data.append(
                [self.groupIndexes(indexes), 'EF_template(ID)', 'This is template event finder(Comment)', '-1'])
            return {'len': len(data), 'data': data}

        def ef_SeverityLevelFailSafes(self, MAX_GAP=0, MIN_PEAKS=1):
            """
            EF1 SeverityLevelFailSafes: Looking for each of severity level > 0.

            :param MAX_GAP:
            :param MIN_PEAKS:
            :return:
            """

            excluded_types = ['ddrRamCrcFailure', 'frameIndex', 'imageIndex', 'pllFailure', 'radarCommErrorCounter']
            failSafeTypes = [key for key in (self.mat['mudp']['vis']['vision_failsafes']).keys()
                             if key not in excluded_types and key.endswith('SeverityLevel')]
            failSafeFlags = {failSafeType: self.mat['mudp']['vis']['vision_failsafes'][failSafeType]
                             for failSafeType in failSafeTypes}

            data = []

            for key in failSafeFlags.keys():
                indexes = []
                datamatrix = self.mat['mudp']['vis']['vision_failsafes'][key]
                for severityLevel in [1, 2, 3]:
                    indexes = []
                    index = (np.argwhere(datamatrix == severityLevel))
                    for each in index:
                        indexes += list(each)
                    if indexes:
                        data.append([self.groupIndexes(indexes), 'Failsafe severity level',
                                        key + " == " + str(severityLevel), -1])

            return {'len': len(data), 'data': data}

        def ef_NonZeroFailsafes(self, MAX_GAP=0, MIN_PEAKS=0, CONF_THRESHOLD=1):
            """
            EF2 simple failsafes: searches for any failSafes except from 'excluded_types'

            :param MAX_GAP: maxGap parameters of groupIndexes() (see groupIndexes info)
            :param MIN_PEAKS: minPeaks parameters of groupIndexes() (see groupIndexes info)
            :return:
            """

            excluded_types = ['ddrRamCrcFailure', 'frameIndex', 'imageIndex', 'pllFailure', 'radarCommErrorCounter']
            failSafeTypes = [key for key in (self.mat['mudp']['vis']['vision_failsafes']).keys()
                             if key not in excluded_types]
            failSafeFlags = {failSafeType: self.mat['mudp']['vis']['vision_failsafes'][failSafeType]
                             for failSafeType in failSafeTypes}

            data =[]

            for key in failSafeFlags.keys():
                indexes = []
                datamatrix = self.mat['mudp']['vis']['vision_failsafes'][key]
                indexes = []
                index = (np.argwhere(datamatrix != 0))
                for each in index:
                    indexes += list(each)
                if indexes:
                    data.append([self.groupIndexes(indexes), 'Non zero failsafe',
                                    key, -1])

            return {'len': len(data), 'data': data}

        def ef_FailsafesFlickering(self, MAX_GAP=40, MIN_PEAKS=2):
            """
            EF3: Flickering failsafes detection
            EF goes through mat indexes and check if failsafe change compering to previous index.
            If so, index is added to indexes list.

            :param MAX_GAP: maxGap parameters of groupIndexes() (see groupIndexes info)
            :param MIN_PEAKS: minPeaks parameters of groupIndexes() (see groupIndexes info)
            :return: EF gives back dict structure with data len and data itself
            """
            excluded_types = ['ddrRamCrcFailure', 'frameIndex', 'imageIndex', 'pllFailure', 'radarCommErrorCounter']
            failSafeTypes = [key for key in (self.mat['mudp']['vis']['vision_failsafes']).keys()
                             if key not in excluded_types]
            failSafeFlags = {failSafeType: self.mat['mudp']['vis']['vision_failsafes'][failSafeType]
                             for failSafeType in failSafeTypes}

            data = []

            for key in failSafeFlags.keys():
                indexes = []
                datamatrix = self.mat['mudp']['vis']['vision_failsafes'][key]
                for index in range(1, self.visLen):
                    if not datamatrix[index - 1] and datamatrix[index] or \
                            datamatrix[index - 1] and not datamatrix[index]:
                        indexes.append(index)
                data.append([self.groupIndexes(indexes, MAX_GAP, MIN_PEAKS), 'Failsafe flickering', key ,-1])

            return {'len': len(data), 'data': data}

        # helper function

        def object_counter(self, index, duration, *args):
            """
            Object counter:
            """
            count = 0
            for i in args:
                count += sum([np.array_equal(x, y) for x, y in product(np.argwhere(
                    self.mat['mudp']['vis']['vision_obstacles_info']['visObs']['detection_status'][
                    index:index + duration] == 1), np.argwhere(
                    self.mat['mudp']['vis']['vision_obstacles_info']['visObs']['obstacle_class']
                    [index:index + duration] == i))])
            return count



