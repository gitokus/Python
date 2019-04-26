import numpy as np

from analystToolKit.lib.efsClasses import efsFrameClass


class dvlobjEFs(efsFrameClass.EFClass):
        def __init__(self):
            self.function = 'DVL'

        def appendDetails(self):
            try:
                from delphiTools3 import base
                self.dvlExt = base.loadmat(self.mat['__path__'], variableName='dvlExt')['dvlExt']
            except:
                print('error')

            self.header += ['duration[s]','time_gap', 'brake_accel', 'propulsion_accel', 'fcw_sens', 'brk_assist_sens']
            self.tselIndex = self.get_closest(self.mat['mudp']['vis']['header']['cTime'],
                                              self.dvlExt['tsel']['sys']['ctimeu'] * 1000000)
            self.dvlvisIndex = self.get_closest(self.mat['mudp']['vis']['header']['cTime'],
                                              self.dvlExt['vis']['sys']['ctimeu'] * 1000000)
            self.appendHeader()

            errorNameList = []
            for eventsDict in self.eventsDictList:
                index = int(np.where(self.visIndex == eventsDict['eventIndex'])[0][0])
                columnID = eventsDict['eventColumnID']
                try:
                    eventsDict['duration[s]'] = round(self.dvlExt['veh']['acc']['ctimeu'][index + eventsDict['eventDuration'] - 1] -
                                                 self.dvlExt['veh']['acc']['ctimeu'][index],3)
                except:
                    errorNameList.append('duration[s]')
                try:
                    eventsDict['time_gap'] = self.dvlExt['veh']['acc']['time_gap'][index]
                except:
                    errorNameList.append('time_gap')
                try:
                    eventsDict['brake_accel'] = self.dvlExt['veh']['acc']['brake_accel'][index]
                except:
                    errorNameList.append('brake_accel')
                try:
                    eventsDict['propulsion_accel'] = self.dvlExt['veh']['acc']['propulsion_accel'][index]
                except:
                    errorNameList.append('propulsion_accel')
                try:
                    eventsDict['brk_assist_sens'] = self.dvlExt['veh']['cmbb']['brk_assist_sens'][index]
                except:
                    errorNameList.append('brk_assist_sens')
                try:
                    eventsDict['fcw_sens'] = self.dvlExt['veh']['cmbb']['fcw_sens'][index]
                except:
                    errorNameList.append('fcw_sens')
                if (eventsDict['eventFinderID'] == 'ACCevents'):
                    if 'pcas' in self.dvlExt['tsel'].keys() and 'pcav' in self.dvlExt['tsel'].keys():
                        self.TselRtvDetails(eventsDict, errorNameList)
                    else:
                        self.PedsDetails(eventsDict, errorNameList)
                elif (eventsDict['eventFinderID'] == 'CMBBevents'):
                    self.TselPcasDetails(eventsDict, errorNameList)
                self.dvlVisDetails(eventsDict, errorNameList)

            return list(set(errorNameList))

        def appendHeader(self):

            self.header += ['rtv_detSens', 'rtv_trackId', 'rtv_status', 'rtv_movement', 'rtv_age', 'rtv_object_class', 'rtv_vsTrkId',
                     'rtv_long_rel_l', 'rtv_long_obj_v', 'rtv_lat_rel_l', 'rtv_lat_obj_v', 'rtv_long_obj_a', 'rtv_lat_obj_a',
                     'rtv_xohp_etsel_cmbb_fcw', 'rtv_xolc_etsel_cmbb_fcw']

            self.header += ['rts_detSens', 'rts_trackId', 'rts_status', 'rts_movement', 'rts_age', 'rts_object_class', 'rts_vsTrkId',
                     'rts_long_rel_l', 'rts_long_obj_v', 'rts_lat_rel_l', 'rts_lat_obj_v', 'rts_long_obj_a', 'rts_lat_obj_a',
                     'rts_xohp_etsel_cmbb_fcw', 'rts_xolc_etsel_cmbb_fcw']

            self.header += ['pcas_detSens', 'pcas_cmbbPriConfidence',
                     'pcas_fcwConfidence', 'pcas_Status', 'pcas_Age', 'pcas_object_class',
                    'pcas_vsTrkId', 'pcas_trackID', 'pcas_long_rel_l', 'pcas_long_obj_v', 'pcas_lat_rel_l', 'pcas_lat_obj_v',
                    'pcas_long_obj_a', 'pcas_lat_obj_a', 'pcas_movement','pcas_xohp_etsel', 'pcas_xolc_etsel']

            self.header += ['pcav_detSens', 'pcav_cmbbPriConfidence',
                     'pcav_fcwConfidence', 'pcav_Status', 'pcav_Age', 'pcav_object_class',
                    'pcav_vsTrkId', 'pcav_trackID', 'pcav_long_rel_l', 'pcav_long_obj_v', 'pcav_lat_rel_l', 'pcav_lat_obj_v',
                    'pcav_long_obj_a', 'pcav_lat_obj_a', 'pcav_movement','pcav_xohp_etsel', 'pcav_xolc_etsel']

            self.header += ['vis_vis_obs_cipv','vis_fcw_vis_veh_brake','vis_fcw_vis_vru_brake','vis_fcw_vis_veh_warn',
                            'vis_fcw_vis_vru_warn','vis_fcw_vis_veh_part_brake','vis_fcw_vis_vru_part_brake','vis_vis_veh_fce_unconf_brk',
                            'vis_vis_vru_fce_unconf_brk','vis_fcw_sense_level']

            self.header += ['peds_track_id']


        def dvlVisDetails(self, eventsDict, errorNameList):
            index = int(np.where(self.dvlvisIndex == eventsDict['eventIndex'])[0][0])
            try:
                eventsDict['vis_vis_obs_cipv'] = self.dvlExt['vis']['sys']['vis_obs_cipv'][index]
            except:
                errorNameList.append('vis_obs_cipv')
            try:
                eventsDict['vis_fcw_vis_veh_brake'] = self.dvlExt['vis']['sys']['fcw_vis_veh_brake'][index]
            except:
                errorNameList.append('fcw_vis_veh_brake')
            try:
                eventsDict['vis_fcw_vis_vru_brake'] = self.dvlExt['vis']['sys']['fcw_vis_vru_brake'][index]
            except:
                errorNameList.append('fcw_fcw_vis_vru_brake')
            try:
                eventsDict['vis_fcw_vis_veh_warn'] = self.dvlExt['vis']['sys']['fcw_vis_veh_warn'][index]
            except:
                errorNameList.append('fcw_vis_veh_warn')
            try:
                eventsDict['vis_fcw_vis_vru_warn'] = self.dvlExt['vis']['sys']['fcw_vis_vru_warn'][index]
            except:
                errorNameList.append('fcw_vis_vru_warn')
            try:
                eventsDict['vis_fcw_vis_veh_part_brake'] = self.dvlExt['vis']['sys']['fcw_vis_veh_part_brake'][index]
            except:
                errorNameList.append('fcw_vis_veh_part_brake')
            try:
                eventsDict['vis_fcw_vis_vru_part_brake'] = self.dvlExt['vis']['sys']['fcw_vis_vru_part_brake'][index]
            except:
                errorNameList.append('fcw_vis_vru_part_brake')
            try:
                eventsDict['vis_vis_veh_fce_unconf_brk'] = self.dvlExt['vis']['sys']['vis_veh_fce_unconf_brk'][index]
            except:
                errorNameList.append('vis_veh_fce_unconf_brk')
            try:
                eventsDict['vis_vis_vru_fce_unconf_brk'] = self.dvlExt['vis']['sys']['vis_vru_fce_unconf_brk'][index]
            except:
                errorNameList.append('vis_vru_fce_unconf_brk')
            try:
                eventsDict['vis_fcw_sense_level'] = self.dvlExt['vis']['sys']['fcw_sense_level'][index]
            except:
                errorNameList.append('fcw_fcw_sense_level')


        def TselRtvDetails(self,eventsDict,errorNameList):
            index = int(np.where(self.tselIndex == eventsDict['eventIndex'])[0][0])
            try:
                eventsDict['rtv_detSens'] = self.dvlExt['tsel']['rtv']['detSens'][index][0]
            except:
                errorNameList.append('rtv_detSens')
            try:
                eventsDict['rtv_trackId'] = self.dvlExt['tsel']['rtv']['trackId'][index][0]
            except:
                errorNameList.append('rtv_trackId')
            try:
                eventsDict['rtv_status'] = self.dvlExt['tsel']['rtv']['status'][index][0]
            except:
                errorNameList.append('rtv_status')
            try:
                eventsDict['rtv_movement'] = self.dvlExt['tsel']['rtv']['movement'][index][0]
            except:
                errorNameList.append('rtv_movement')
            try:
                eventsDict['rtv_age'] = self.dvlExt['tsel']['rtv']['age'][index][0]
            except:
                errorNameList.append('rtv_age')
            try:
                eventsDict['rtv_object_class'] = self.dvlExt['tsel']['rtv']['object_class'][index][0]
            except:
                errorNameList.append('rtv_object_class')
            try:
                eventsDict['rtv_vsTrkId'] = self.dvlExt['tsel']['rtv']['vsTrkId'][index][0]
            except:
                errorNameList.append('rtv_vsTrkId')
            try:
                eventsDict['rtv_long_rel_l'] = self.dvlExt['tsel']['rtv']['long_rel_l'][index][0]
            except:
                errorNameList.append('rtv_long_rel_l')
            try:
                eventsDict['rtv_long_obj_v'] = self.dvlExt['tsel']['rtv']['long_obj_v'][index][0]
            except:
                errorNameList.append('rtv_long_obj_v')
            try:
                eventsDict['rtv_lat_rel_l'] = self.dvlExt['tsel']['rtv']['lat_rel_l'][index][0]
            except:
                errorNameList.append('rtv_lat_rel_l')
            try:
                eventsDict['rtv_lat_obj_v'] = self.dvlExt['tsel']['rtv']['lat_obj_v'][index][0]
            except:
                errorNameList.append('rtv_lat_obj_v')
            try:
                eventsDict['rtv_long_obj_a'] = self.dvlExt['tsel']['rtv']['long_obj_a'][index][0]
            except:
                errorNameList.append('rtv_long_obj_a')
            try:
                eventsDict['rtv_lat_obj_a'] = self.dvlExt['tsel']['rtv']['lat_obj_a'][index][0]
            except:
                errorNameList.append('rtv_lat_obj_a')
            try:
                eventsDict['rtv_xohp_etsel_cmbb_fcw'] = self.dvlExt['tsel']['rtv']['xohp_etsel_cmbb_fcw'][index][0]
            except:
                errorNameList.append('rtv_xohp_etsel_cmbb_fcw')
            try:
                eventsDict['rtv_xolc_etsel_cmbb_fcw'] = self.dvlExt['tsel']['rtv']['xolc_etsel_cmbb_fcw'][index][0]
            except:
                errorNameList.append('rtv_xolc_etsel_cmbb_fcw')
            try:
                eventsDict['rts_detSens'] = self.dvlExt['tsel']['rts']['detSens'][index][0]
            except:
                errorNameList.append('rts_detSens')
            try:
                eventsDict['rts_trackId'] = self.dvlExt['tsel']['rts']['trackId'][index][0]
            except:
                errorNameList.append('rts_trackId')
            try:
                eventsDict['rts_status'] = self.dvlExt['tsel']['rts']['status'][index][0]
            except:
                errorNameList.append('rts_status')
            try:
                eventsDict['rts_movement'] = self.dvlExt['tsel']['rts']['movement'][index][0]
            except:
                errorNameList.append('rts_movement')
            try:
                eventsDict['rts_age'] = self.dvlExt['tsel']['rts']['age'][index][0]
            except:
                errorNameList.append('rts_age')
            try:
                eventsDict['rts_object_class'] = self.dvlExt['tsel']['rts']['object_class'][index][0]
            except:
                errorNameList.append('rts_object_class')
            try:
                eventsDict['rts_vsTrkId'] = self.dvlExt['tsel']['rts']['vsTrkId'][index][0]
            except:
                errorNameList.append('rts_vsTrkId')
            try:
                eventsDict['rts_long_rel_l'] = self.dvlExt['tsel']['rts']['long_rel_l'][index][0]
            except:
                errorNameList.append('rts_long_rel_l')
            try:
                eventsDict['rts_long_obj_v'] = self.dvlExt['tsel']['rts']['long_obj_v'][index][0]
            except:
                errorNameList.append('rts_long_obj_v')
            try:
                eventsDict['rts_lat_rel_l'] = self.dvlExt['tsel']['rts']['lat_rel_l'][index][0]
            except:
                errorNameList.append('rts_lat_rel_l')
            try:
                eventsDict['rts_lat_obj_v'] = self.dvlExt['tsel']['rts']['lat_obj_v'][index][0]
            except:
                errorNameList.append('rts_lat_obj_v')
            try:
                eventsDict['rts_long_obj_a'] = self.dvlExt['tsel']['rts']['long_obj_a'][index][0]
            except:
                errorNameList.append('rts_long_obj_a')
            try:
                eventsDict['rts_lat_obj_a'] = self.dvlExt['tsel']['rts']['lat_obj_a'][index][0]
            except:
                errorNameList.append('rts_lat_obj_a')
            try:
                eventsDict['rts_xohp_etsel_cmbb_fcw'] = self.dvlExt['tsel']['rts']['xohp_etsel_cmbb_fcw'][index][0]
            except:
                errorNameList.append('rts_xohp_etsel_cmbb_fcw')
            try:
                eventsDict['rts_xolc_etsel_cmbb_fcw'] = self.dvlExt['tsel']['rts']['xolc_etsel_cmbb_fcw'][index][0]
            except:
                errorNameList.append('rts_xolc_etsel_cmbb_fcw')


        def TselPcasDetails(self,eventsDict,errorNameList):
            index = int(np.where(self.tselIndex == eventsDict['eventIndex'])[0][0])
            try:
                eventsDict['pcas_detSens'] = self.dvlExt['tsel']['pcas']['detSens'][index]
            except:
                errorNameList.append('pcas_detSens')
            try:
                eventsDict['pcas_trackID'] = self.dvlExt['tsel']['pcas']['trackID'][index]
            except:
                errorNameList.append('pcas_trackId')
            try:
                eventsDict['pcas_Status'] = self.dvlExt['tsel']['pcas']['Status'][index]
            except:
                errorNameList.append('pcas_status')
            try:
                eventsDict['pcas_movement'] = self.dvlExt['tsel']['pcas']['movement'][index]
            except:
                errorNameList.append('pcas_movement')
            try:
                eventsDict['pcas_Age'] = self.dvlExt['tsel']['pcas']['Age'][index]
            except:
                errorNameList.append('pcas_age')
            try:
                eventsDict['pcas_object_class'] = self.dvlExt['tsel']['pcas']['object_class'][index]
            except:
                errorNameList.append('pcas_object_class')
            try:
                eventsDict['pcas_vsTrkId'] = self.dvlExt['tsel']['pcas']['visTrkId'][index]
            except:
                errorNameList.append('pcas_vsTrkId')
            try:
                eventsDict['pcas_long_rel_l'] = self.dvlExt['tsel']['pcas']['long_rel_l'][index]
            except:
                errorNameList.append('pcas_long_rel_l')
            try:
                eventsDict['pcas_long_obj_v'] = self.dvlExt['tsel']['pcas']['long_obj_v'][index]
            except:
                errorNameList.append('pcas_long_obj_v')
            try:
                eventsDict['pcas_lat_rel_l'] = self.dvlExt['tsel']['pcas']['lat_rel_l'][index]
            except:
                errorNameList.append('pcas_lat_rel_l')
            try:
                eventsDict['pcas_lat_obj_v'] = self.dvlExt['tsel']['pcas']['lat_obj_v'][index]
            except:
                errorNameList.append('pcas_lat_obj_v')
            try:
                eventsDict['pcas_long_obj_a'] = self.dvlExt['tsel']['pcas']['long_obj_a'][index]
            except:
                errorNameList.append('pcas_long_obj_a')
            try:
                eventsDict['pcas_lat_obj_a'] = self.dvlExt['tsel']['pcas']['lat_obj_a'][index]
            except:
                errorNameList.append('pcas_lat_obj_a')
            try:
                eventsDict['pcas_xohp_etsel'] = self.dvlExt['tsel']['pcas']['xohp_etsel'][index]
            except:
                errorNameList.append('pcas_xohp_etsel')
            try:
                eventsDict['pcas_xolc_etsel'] = self.dvlExt['tsel']['pcas']['xolc_etsel'][index]
            except:
                errorNameList.append('pcas_xolc_etsel')
            try:
                eventsDict['pcas_cmbbPriConfidence'] = self.dvlExt['tsel']['pcas']['cmbbPriConfidence'][index]
            except:
                errorNameList.append('pcas_cmbbPriConfidence')
            try:
                eventsDict['pcas_fcwConfidence'] = self.dvlExt['tsel']['pcas']['fcwConfidence'][index]
            except:
                errorNameList.append('pcas_fcwConfidence')
            try:
                eventsDict['pcav_detSens'] = self.dvlExt['tsel']['pcav']['detSens'][index]
            except:
                errorNameList.append('pcav_detSens')
            try:
                eventsDict['pcav_trackID'] = self.dvlExt['tsel']['pcav']['trackID'][index]
            except:
                errorNameList.append('pcav_trackId')
            try:
                eventsDict['pcav_Status'] = self.dvlExt['tsel']['pcav']['Status'][index]
            except:
                errorNameList.append('pcav_status')
            try:
                eventsDict['pcav_movement'] = self.dvlExt['tsel']['pcav']['movement'][index]
            except:
                errorNameList.append('pcav_movement')
            try:
                eventsDict['pcav_Age'] = self.dvlExt['tsel']['pcav']['Age'][index]
            except:
                errorNameList.append('pcav_age')
            try:
                eventsDict['pcav_object_class'] = self.dvlExt['tsel']['pcav']['object_class'][index]
            except:
                errorNameList.append('pcav_object_class')
            try:
                eventsDict['pcav_vsTrkId'] = self.dvlExt['tsel']['pcav']['visTrkId'][index]
            except:
                errorNameList.append('pcav_vsTrkId')
            try:
                eventsDict['pcav_long_rel_l'] = self.dvlExt['tsel']['pcav']['long_rel_l'][index]
            except:
                errorNameList.append('pcav_long_rel_l')
            try:
                eventsDict['pcav_long_obj_v'] = self.dvlExt['tsel']['pcav']['long_obj_v'][index]
            except:
                errorNameList.append('pcav_long_obj_v')
            try:
                eventsDict['pcav_lat_rel_l'] = self.dvlExt['tsel']['pcav']['lat_rel_l'][index]
            except:
                errorNameList.append('pcav_lat_rel_l')
            try:
                eventsDict['pcav_lat_obj_v'] = self.dvlExt['tsel']['pcav']['lat_obj_v'][index]
            except:
                errorNameList.append('pcav_lat_obj_v')
            try:
                eventsDict['pcav_long_obj_a'] = self.dvlExt['tsel']['pcav']['long_obj_a'][index]
            except:
                errorNameList.append('pcav_long_obj_a')
            try:
                eventsDict['pcav_lat_obj_a'] = self.dvlExt['tsel']['pcav']['lat_obj_a'][index]
            except:
                errorNameList.append('pcav_lat_obj_a')
            try:
                eventsDict['pcav_xohp_etsel'] = self.dvlExt['tsel']['pcav']['xohp_etsel'][index]
            except:
                errorNameList.append('pcav_xohp_etsel')
            try:
                eventsDict['pcav_xolc_etsel'] = self.dvlExt['tsel']['pcav']['xolc_etsel'][index]
            except:
                errorNameList.append('pcav_xolc_etsel')
            try:
                eventsDict['pcav_cmbbPriConfidence'] = self.dvlExt['tsel']['pcav']['cmbbPriConfidence'][index]
            except:
                errorNameList.append('pcav_cmbbPriConfidence')
            try:
                eventsDict['pcav_fcwConfidence'] = self.dvlExt['tsel']['pcav']['fcwConfidence'][index]
            except:
                errorNameList.append('pcav_fcwConfidence')

        def PedsDetails(self, eventsDict, errorNameList):
            index = int(np.where(self.tselIndex == eventsDict['eventIndex'])[0][0])
            try:
                for peds in self.dvlExt['tsel']['peds']['track_id'][:][index]:
                    if peds:
                        try:
                            eventsDict['peds_track_id'] = peds
                        except:
                            errorNameList.append('track_id')

            except:
                errorNameList.append('fcw_sens')



        def get_closest(self, array, values):
            # make sure array is a numpy array
            array = np.array(array)

            # get insert positions
            idxs = np.searchsorted(array, values, side="left")

            # find indexes where previous index is closer
            prev_idx_is_less = ((idxs == len(array)) | (np.fabs(values - array[np.maximum(idxs - 1, 0)]) < np.fabs(
                values - array[np.minimum(idxs, len(array) - 1)])))
            idxs[prev_idx_is_less] -= 1

            return self.mat['mudp']['vis']['vision_function_info']['imageIndex'][idxs]  # array[idx]

        def ef_dvlExt_template(self):
            """
            EF4:

            :return: EF gives back dict structure with data len and data itself
            """
            try:
                from delphiTools3 import base
                dvlExt = base.loadmat(self.mat['__path__'], variableName='dvlExt')['dvlExt']
            except:
                print('error')
                return {'len': 0, 'data': []}
            self.mat

            ### EF here
            data = []

            return {'len': len(data), 'data': data}

        def ef_ACCevents(self):
            """
            EF4: ACC Events

            :return: EF gives back dict structure with data len and data itself
            """

            try:
                from delphiTools3 import base
                dvlExt = base.loadmat(self.mat['__path__'], variableName='dvlExt')['dvlExt']
                self.visIndex = self.get_closest(self.mat['mudp']['vis']['header']['cTime'],
                                                 dvlExt['veh']['acc']['ctimeu'] * 1000000)

                self.visLen = len(self.mat['mudp']['vis']['header']['cTime'])
            except:
                print('error, missing structures')
                return {'len': 0, 'data': []}


            ACCEvents = {'stop_stat': dvlExt['veh']['acc']['stop_stat'],
                         'stop_mode': dvlExt['veh']['acc']['stop_mode'],
                         'follow_mode': dvlExt['veh']['acc']['follow_mode'],
                         'warning': dvlExt['veh']['acc']['warning'],
                         'brk_req': dvlExt['veh']['acc']['brk_req'],
                         'cc_stat': dvlExt['veh']['acc']['cc_stat']
                         }

            data = []

            for key in ACCEvents.keys():
                indexes = []
                datamatrix = ACCEvents[key]
                if (key in ('stop_mode', 'warning')):
                    for i in (1, 2, 3, 4):
                        indexes = []
                        index = (np.argwhere(datamatrix == i))
                        for each in index:
                            indexes += list(each)
                        if indexes:
                            data.append([self.groupIndexes(indexes), 'ACCevents',
                                         key + ' occured ', -1])
                elif (key == 'cc_stat'):
                    index = (np.argwhere(np.diff(datamatrix) != 0))
                    for each in index:
                        indexes += list(each)
                    if indexes:
                        data.append([self.groupIndexes(indexes), 'ACCevents',
                                     key + ' change occured ', -1])
                else:
                    index = (np.argwhere(datamatrix == 1))
                    for each in index:
                        indexes += list(each)
                    if indexes:
                        data.append([self.groupIndexes(indexes), 'ACCevents',
                                     key + ' occured ', -1])
            return {'len': len(data), 'data': data}

        def ef_CMbBevents(self):
            """
            EF6: CMbB events

            :return: EF gives back dict structure with data len and data itself
            """
            try:
                from delphiTools3 import base
                dvlExt = base.loadmat(self.mat['__path__'], variableName='dvlExt')['dvlExt']
                self.visIndex = self.get_closest(self.mat['mudp']['vis']['header']['cTime'],
                                                 dvlExt['veh']['acc']['ctimeu'] * 1000000)
                self.visLen = len(self.mat['mudp']['vis']['header']['cTime'])
            except:
                print('error, missing structures')
                return {'len': 0, 'data': []}





            CMBBEvents = {'brk_accel': dvlExt['veh']['cmbb']['brk_accel'],
                          'fcw_aud_warn': dvlExt['veh']['cmbb']['fcw_aud_warn'],
                          'fcw_denied': dvlExt['veh']['cmbb']['fcw_denied'],
                          'brk_decel_req': dvlExt['veh']['cmbb']['brk_decel_req'],
                          'cmbb_denied': dvlExt['veh']['cmbb']['cmbb_denied'],
                          'cmbb_denied_brk': dvlExt['veh']['cmbb']['cmbb_denied_brk'],
                          'cmbb_denied_prpl': dvlExt['veh']['cmbb']['cmbb_denied_prpl'],
                          'brk_precharge': dvlExt['veh']['cmbb']['brk_precharge']
                          }

            data = []

            for key in CMBBEvents.keys():
                indexes = []
                datamatrix = CMBBEvents[key]
                if (key in ('brk_accel', 'brk_precharge')):
                    index = (np.argwhere(abs(datamatrix) >= 0.1))
                    for each in index:
                        indexes += list(each)
                    if indexes:
                        data.append([self.groupIndexes(indexes), 'CMBBevents',
                                     key + ' change occured ', -1])
                else:
                    index = (np.argwhere(datamatrix == 1))
                    for each in index:
                        indexes += list(each)
                    if indexes:
                        data.append([self.groupIndexes(indexes), 'CMBBevents',
                                     key + ' occured ', -1])
            return {'len': len(data), 'data': data}
