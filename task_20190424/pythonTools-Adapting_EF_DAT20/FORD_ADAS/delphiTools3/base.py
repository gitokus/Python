import numpy as np
import scipy.io as spio
import os
from copy import deepcopy
import pandas as pd
import time


class DotDict(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def loadmat(filename, variableName=None, sort=False, reBarrierMarge=False, dat2p0=False, dot_dict=False):
    """
    this function should be called instead of direct spio.loadmat
    as it cures the problem of not properly recovering python dictionaries
    from mat files. It calls the function check keys to cure all entries
    which are still mat-objects

    :param filename: path to .mat file
    :param variableName: Name of variables to be loaded. If None - load whole mat
    :param sort: sort system's detections
    :param reBarrierMarge: Merge LKS Barrier and RoadEdge detections into one. Supported only with CADS 3.5
    :param dat2p0: Used to load logs from DAT2.0
    :param dot_dict: Return dictionary that is also accessible as if it was Matlab struct (via dots). Array indexing
    still starts at 0, though.
    e.g. mat['mudp']['vis']['vision_function_info']['imageIndex'][0] or mat.mudp.vis.vision_function_info.imageIndex[0]
    """
    data = spio.loadmat(filename, struct_as_record=False, squeeze_me=True, variable_names=variableName)
    data = checkKeys(data)
    if sort:
        data = sortMatByID(data, dat2p0)
    if reBarrierMarge:
        data = margeReBarrier(data)
    data['__path__'] = filename

    def to_dot_dict(input_dict):
        for key in input_dict.keys():
            if isinstance(input_dict[key], dict):
                input_dict[key] = to_dot_dict(input_dict[key])
        return DotDict(input_dict)

    # Add information about project
    if dat2p0:
        data['__project__'] = 'DAT2.0'
        data = decodeDAT2p0BitFields(data)
    else:
        data['__project__'] = 'CADS3.5'

    if dot_dict:
        return to_dot_dict(data)
    else:
        return data


def decodeDAT2p0BitFields(data):
    vehicleValidityBits = {0: 'vehicleLatAccelValidity',
                           1: 'vehicleLongAccelValidity',
                           2: 'vehicleRollRateValidity',
                           3: 'vehicleVelocityValidity',
                           4: 'vehicleVerticalAccelValidity',
                           5: 'vehicleYawRateValidity',
                           6: 'steeringWheelAngleValidity',
                           7: 'accelPedPosPctValidity'
                           }
    vehStateInfo = data["mudp"]["eyeq"]["HostVeh"]["host_veh_state_info"]["vehStateInfo"]
    vehicleValidityBitField = vehStateInfo["vehicle_validity_byte"]

    data = decodeBitField(vehicleValidityBits, data, vehStateInfo, vehicleValidityBitField)

    hostVehicleStateBits = {0: 'mainBeamIndication',
                            1: 'wiperFrontCmd',
                            2: 'reverseGear',
                            3: 'brakePedalPressed'
                            }
    hostVehicleStateBitField = vehStateInfo["host_vehicle_state_byte"]
    data = decodeBitField(hostVehicleStateBits, data, vehStateInfo, hostVehicleStateBitField)

    outOfCalibTSRBits = {0: 'TSROutOfCalib',
                         1: 'TSROutOfCalib_AEB',
                         2: 'TSROutOfCalib_yaw',
                         3: 'TSROutOfCalib_horizon'
                         }
    visFailsafes = data['mudp']['eyeq']['Failsafes']['vis_failsafe_msg_info']['visFailsafes']
    outOfCalibTSRBitField = visFailsafes['outOfCalibTSR_byte']
    data = decodeBitField(outOfCalibTSRBits, data, visFailsafes, outOfCalibTSRBitField)

    roadMarkerAmbigBits = {0: 'ambiguousLinePatternLeft',
                           1: 'ambiguousLinePatternRight',
                           2: 'constructionArea'
                           }
    roadMarkerInfo = data['mudp']['eyeq']['Road']['vis_road_data_info']['roadInfo']['roadMarkerInfo']
    roadMarkerAmbigBitField = roadMarkerInfo['roadMarker_ambigLinePatt_const_byte']
    data = decodeBitField(roadMarkerAmbigBits, data, roadMarkerInfo, roadMarkerAmbigBitField)

    roadPredictionLeftBits = {0: 'roadPredictionLeftNone',
                              1: 'roadPredictionLeftOccluded',
                              2: 'roadPredictionLeftOtherSide',
                              3: 'roadPredictionLeftOverride',
                              4: 'roadPredictionLeftDistBasedExtrapolation',
                              5: 'roadPredictionLeftHeadwayOriented'
                              }
    roadPredictionLeftBitField = roadMarkerInfo['roadPredictionLeft_byte']
    data = decodeBitField(roadPredictionLeftBits, data, roadMarkerInfo, roadPredictionLeftBitField)

    roadPredictionRightBits = {0: 'roadPredictionRightNone',
                               1: 'roadPredictionRightOccluded',
                               2: 'roadPredictionRightOtherSide',
                               3: 'roadPredictionRightOverride',
                               4: 'roadPredictionRightDistBasedExtrapolation',
                               5: 'roadPredictionRightHeadwayOriented'
                               }
    roadPredictionRightBitField = roadMarkerInfo['roadPredictionRight_byte']
    data = decodeBitField(roadPredictionRightBits, data, roadMarkerInfo, roadPredictionRightBitField)

    lightSensorDetectionsBits = {0: 'fogDetected',
                                 1: 'highwayDetected',
                                 2: 'villageDetected',
                                 3: 'oncomingLaneNotDark',
                                 4: 'approachingJunction',
                                 5: 'lightNoisyScene',
                                 6: 'lightCone'
                                 }
    activeLightSensorInfo = data["mudp"]["eyeq"]["Lights"]["vis_light_sensor_data_info"]["activeLightSensorInfo"]
    lightSensorDetectionsBitField = activeLightSensorInfo["light_Sensor_Detections_byte"]
    data = decodeBitField(lightSensorDetectionsBits, data, activeLightSensorInfo, lightSensorDetectionsBitField)

    eventsDetectedBits = {0: 'noSwitchReason',
                          1: 'oncomingVehicle',
                          2: 'precedingVehicle',
                          3: 'speedLimit',
                          4: 'ambientLight',
                          5: 'villageDetection',
                          6: 'fogDetection',
                          7: 'HighwayMode',
                          8: 'delay',
                          9: 'oncomingLaneNotDark',
                          10: 'tooManyPrecedingSpots',
                          11: 'curveStatus',
                          12: 'highSpeedStatus',
                          13: 'oncomingVehicleDelay',
                          14: 'precedingVehicleDelay',
                          15: 'villageDetectionDelay'
                          }
    activeLightSensorInfo["eventsDetected"] = {}
    eventsDetectedSignals = activeLightSensorInfo["eventsDetected"]
    eventsDetectedBitField = activeLightSensorInfo["events_Detected_byte"]
    data = decodeBitField(eventsDetectedBits, data, eventsDetectedSignals, eventsDetectedBitField)

    objPredDrvAreaCloseBits = {0: 'isPredicted',
                               1: 'IsInDrivableArea',
                               2: 'isVeryClose'
                               }
    visObs = data["mudp"]["eyeq"]["Obstacles"]["vis_obstacles_msg_info"]["visObjects"]["visObs"]
    objPredDrvAreaCloseBitField = visObs["visObj_Pred_DrvArea_Close_byte"]
    data = decodeBitField(objPredDrvAreaCloseBits, data, visObs, objPredDrvAreaCloseBitField)

    lightIndicatorsBits = {0: 'valid',
                           1: 'brakeLightIndicator',
                           2: 'turnRightIndicator',
                           3: 'turnLeftIndicator'
                           }
    lightIndicators = data["mudp"]["eyeq"]["Obstacles"]["vis_obstacles_msg_info"]["visObjects"]["visObs"]["lightIndicators"]
    lightIndicatorsBitField = lightIndicators["light_indicator_byte"]
    data = decodeBitField(lightIndicatorsBits, data, lightIndicators, lightIndicatorsBitField)

    verticalEdgeBits = {0: 'isOccluded',
                        1: 'valid'
                        }
    verticalEdges = data["mudp"]["eyeq"]["Obstacles"]["vis_obstacles_msg_info"]["visObjects"]["visObs"]["imageBox"]["verticalEdges"]
    verticalEdgesBitField = verticalEdges['verticalEdge_Occulation_Validity_byte']
    data = decodeBitField(verticalEdgeBits, data, verticalEdges, verticalEdgesBitField)

    return data


def decodeBitField(bitFieldBits, data, dictToSaveIn, bitField):
    for i in range(len(bitFieldBits)):
        dictToSaveIn[bitFieldBits[i]] = get_bit(bitField, i)
    return data


def get_bit(number, bitNumberFromRight):
    return (number >> bitNumberFromRight) & 1


def translate(data_struct, mat_id):
    """
    Translate (sort) entries in mat so they match system's outputs
    :param data_struct: Data structures to be sorted (ndarray, dict, nested dict)
    :param mat_id: ndarray with IDs pattern used to sorting
    :return: Function modifies inPlace input data from mat file (returns None)
    """
    for key in data_struct.keys():
        if isinstance(data_struct[key], dict):
            translate(data_struct[key], mat_id)  # If dict entry is dict - recurse
        else:
            ndims = data_struct[key].ndim  # number of array's dimensions
            new_data = np.array(data_struct[key])
            for i in range(data_struct[key].shape[1]):  # range(number_of_cols)
                mask = np.array(mat_id == (i + 1), int)

                if ndims == 2:  # No need to expand mask
                    new_data[:, i] = np.sum(data_struct[key] * mask, axis=1)
                elif ndims == 3:  # Expand mask to 3D
                    new_data[:, i] = np.sum(data_struct[key] * np.expand_dims(mask, 2), axis=1)
                elif ndims == 4:  # Expand mask to 4D
                    new_data[:, i] = np.sum(data_struct[key] * np.expand_dims(np.expand_dims(mask, 2), 3), axis=1)

            data_struct[key] = new_data

def afl_transalate(struct, id):
    """
    Transalte (sort) AFL detections
    :param struct: structure to be sorted
    :param id: array with detection's IDs
    :return: Function modifies inPlace input data from mat file (it returns None)
    """
    prev_row = []
    for r, row in enumerate(id):
        if not len(prev_row):  # True only for 1st row
            prev_row = row
        else:
            for c, col in enumerate(row.copy()):
                if col and col in prev_row:  # id=0 is not relevant
                    i = np.argwhere(row == col)[0][0]  # col_num that detection has in current row
                    j = np.argwhere(prev_row == col)[0][0]  # col_num that detection had in prev row
                    if not i == j:  # If detection were in same column we don't need to sort
                        for key in struct.keys():
                            d = struct[key][r]
                            d[j], d[i] = d[i], d[j]  # Swap places of detections
            prev_row = row


def sortMatByID(mat, dat2p0):
    if not dat2p0:  # CADS3.5 sorting
        # tsr translate
        tsrData = mat['mudp']['vis']['vision_traffic_sign_info']['trafficSigns']
        ID = tsrData['signID']
        status = tsrData['signStatus']
        signID = ID + np.array(np.array(status, bool), int)
        for key in tsrData.keys():
            newData = np.array(tsrData[key])
            for i in range(8):
                mask = np.array(signID == (i + 1), int)
                newData[:, i] = np.sum(tsrData[key] * mask, axis=1)
            tsrData[key] = np.array(newData)

        # obj translate
        objData = mat['mudp']['vis']['vision_obstacles_info']['visObs']
        ID = np.array(objData['id'])
        for key in objData.keys():
            newData = np.array(objData[key])
            for i in range(15):
                mask = np.array(ID == (i + 1), int)
                if key in ['tlet_match', 'tlet_match_conf']:
                    newData[:, i] = np.sum(objData[key] * np.expand_dims(mask, 3), axis=1)
                else:
                    newData[:, i] = np.sum(objData[key] * mask, axis=1)
            objData[key] = newData

        # afl translate
        aflData = mat['mudp']['vis']['vision_active_light_sensor_info']['activeLightSpots']
        ID = aflData['id']
        prevRow = []
        for r, row in enumerate(ID):
            if not len(prevRow):
                prevRow = row
            else:
                for c, col in enumerate(row.copy()):
                    if col and col in prevRow:
                        i = np.argwhere(row == col)[0][0]  # col_num that detection has in current row
                        j = np.argwhere(prevRow == col)[0][0]  # col_num that detection had in prev row
                        if not i == j:  # If detection were in same column we don't need to sort
                            for key in aflData.keys():
                                d = aflData[key][r]
                                d[j], d[i] = d[i], d[j]  # Swap places of detections
                prevRow = row

        # HRS translate
        if 'reflectiveSigns' in mat['mudp']['vis']['vision_active_light_sensor_info'].keys():
            hrsData = mat['mudp']['vis']['vision_active_light_sensor_info']['reflectiveSigns']
            ID = hrsData['lightSignId']
            prevRow = []
            for r, row in enumerate(ID):
                if not len(prevRow):
                    prevRow = row
                else:
                    for c, col in enumerate(row.copy()):
                        if col and col in prevRow:
                            i = np.argwhere(row == col)[0][0]
                            j = np.argwhere(prevRow == col)[0][0]
                            if not i == j:
                                for key in hrsData.keys():
                                    d = hrsData[key][r]
                                    d[j], d[i] = d[i], d[j]
                    prevRow = row

    else:  # DAT2.0 sorting

        # TSR translate
        tsr_struct = mat['mudp']['vis']['vision_traffic_sign_info']['tsrInfo']['trafficSigns']
        sign_id = tsr_struct['signID']
        confidence = tsr_struct['signConfidence']
        sign_id = sign_id * np.array(np.array(confidence, bool), int)  # Only cells where s_conf != 0
        translate(tsr_struct, sign_id)

        # obj translate
        obj_struct = mat['mudp']['vis']['vision_obstacles_info']['visObjects']['visObs']
        obj_id = obj_struct['id']
        translate(obj_struct, obj_id)

        # AFL translate
        light_spots = mat['mudp']['vis']['vision_active_light_sensor_info']['activeLightSensorInfo']['activeLightSpots']
        light_spots_id = mat['mudp']['vis']['vision_active_light_sensor_info']['activeLightSensorInfo']\
                            ['activeLightSpots']['id']
        afl_transalate(light_spots, light_spots_id)

        # HRS translate
        refl_signs = mat['mudp']['vis']['vision_active_light_sensor_info']\
                        ['activeLightSensorInfo']['reflectiveSigns']
        refl_signs_id = mat['mudp']['vis']['vision_active_light_sensor_info']\
                           ['activeLightSensorInfo']['reflectiveSigns']['lightSignID']
        afl_transalate(refl_signs, refl_signs_id)

    return mat


def margeReBarrier(mat):
    def copyReStructure(input, output, index):
        for key in output['roadEdge'].keys():
            output['roadEdge'][key][index] = input['roadEdge'][key][index]
        for key in [key for key in output['roadEdgeConf'].keys() if not(key == 'confCMBB')]:
            output['roadEdgeConf'][key][index] = input['roadEdgeConf'][key][index]
        output['roadEdgeConf']['confCMBB'][index] = 0
        output['type'][index] = 1

    def copyBarierStructure(input, output, index):
        for key in output['roadEdge'].keys():
            output['roadEdge'][key][index] = input['visBarrier'][key][index]
        for key in [key for key in output['roadEdgeConf'].keys() if not(key == 'confDIMON') ]:
            output['roadEdgeConf'][key][index] = input['visBarrierConf'][key][index]
        output['roadEdgeConf']['confDIMON'][index] = 0
        output['type'][index] = 2

    index = mat['mudp']['vis']['vision_active_light_sensor_info']['imageIndex']
    matLen = len(index)

    LRe = mat['mudp']['vis']['vision_road_info']['roadEdgeInfo']['leftRoadEdge']
    RRe = mat['mudp']['vis']['vision_road_info']['roadEdgeInfo']['rightRoadEdge']

    LBa = mat['mudp']['vis']['vision_barrier_info']['leftVisBarrier']
    RBa = mat['mudp']['vis']['vision_barrier_info']['rightVisBarrier']

    LRe_m = deepcopy(LRe)
    LRe_m['type'] = [1 if LRe['roadEdge']['a0'][i] else 0 for i in range(matLen)]
    for key in ['a0', 'a1', 'a2', 'a3', 'range']:
        LRe_m['roadEdge'][key] = LRe_m['roadEdge'][key].astype(np.float64)
    LRe_m['roadEdgeConf']['tuneConfidence'] = LRe_m['roadEdgeConf']['tuneConfidence'].astype(np.float64)
    LRe_m['roadEdgeConf']['confCMBB'] = deepcopy(LRe_m['roadEdgeConf']['confDIMON'])
    RRe_m = deepcopy(RRe)
    RRe_m['type'] = [1 if RRe['roadEdge']['a0'][i] else 0 for i in range(matLen)]
    for key in ['a0', 'a1', 'a2', 'a3', 'range']:
        RRe_m['roadEdge'][key] = RRe_m['roadEdge'][key].astype(np.float64)
    RRe_m['roadEdgeConf']['tuneConfidence'] = RRe_m['roadEdgeConf']['tuneConfidence'].astype(np.float64)
    RRe_m['roadEdgeConf']['confCMBB'] = deepcopy(RRe_m['roadEdgeConf']['confDIMON'])

    for index in range(matLen):
        if LBa['visBarrier']['a0'][index]:
            if LRe['roadEdge']['a0'][index] and LRe['roadEdge']['a0'][index] >= LBa['visBarrier']['a0'][index]:
                copyReStructure(LRe, LRe_m, index)
            else:
                copyBarierStructure(LBa, LRe_m, index)

        if RBa['visBarrier']['a0'][index]:
            if RRe['roadEdge']['a0'][index] and RRe['roadEdge']['a0'][index] <= RBa['visBarrier']['a0'][index]:
                copyReStructure(RRe, RRe_m, index)
            else:
                copyBarierStructure(RBa, RRe_m, index)

    mat['mudp']['vis']['vision_road_info']['mergedRoadEdgeInfo'] = {'leftRoadEdge': LRe_m,
                                                                    'rightRoadEdge': RRe_m}
    return mat


def checkKeys(dict):
    """
    checks if entries in dictionary are mat-objects. If yes
    todict is called to change them to nested dictionaries
    """
    for key in dict:
        if isinstance(dict[key], spio.matlab.mio5_params.mat_struct):
            dict[key] = toDict(dict[key])
        elif isinstance(dict[key], np.ndarray):
            if len(dict[key]) > 0 and isinstance(dict[key][0], spio.matlab.mio5_params.mat_struct):
                dict[key] = toList(dict[key])
    return dict


def toDict(matobj):
    """
    A recursive function which constructs from matobjects nested dictionaries
    """
    dict = {}
    for strg in matobj._fieldnames:
        elem = matobj.__dict__[strg]
        if isinstance(elem, spio.matlab.mio5_params.mat_struct):
            dict[strg] = toDict(elem)
        elif isinstance(elem, np.ndarray):
            if len(elem)>0 and isinstance(elem[0], spio.matlab.mio5_params.mat_struct):
                dict[strg] = toList(elem)
            else:
                dict[strg] = elem
        else:
            dict[strg] = elem
    return dict


def toList(ndarray):
    """
    A recursive function which constructs lists from cellarrays
    (which are loaded as numpy ndarrays), recursing into the elements
    if they contain matobjects.
    """
    elemList = []
    for subElem in ndarray:
        if isinstance(subElem, spio.matlab.mio5_params.mat_struct):
            elemList.append(toDict(subElem))
        elif isinstance(subElem,np.ndarray):
            if len(subElem) > 0 and isinstance(subElem[0], spio.matlab.mio5_params.mat_struct):
                elemList.append(toList(subElem))
            else:
                elemList.append(subElem)
        else:
            elemList.append(subElem)
    return elemList


def printNested(d, indent=0, values=False):
    """
    Pretty print nested structures from .mat files
    """
    if isinstance(d, dict):
        for key, value in d.items():         # iteritems loops through key, value pairs
            print('\t' * indent + 'Key: ' + str(key))
            printNested(value, indent+1,values)
    elif isinstance(d,np.ndarray) and d.dtype.names is not None:  # Note: and short-circuits by default
        for n in d.dtype.names:    # This means it's a struct, it's bit of a kludge test.
            print('\t' * indent + 'Field: ' + str(n))
            printNested(d[n], indent+1)
    elif isinstance(d, list) :
        if values:
            for each in d:
                print(each)
    else:
        if values:
            print('\t' * indent + 'Value: ' + str(d))
    return


def fPrintNested(d, fileHandle, indent=0, values=False):
    if isinstance(d, dict):
        for key, value in d.items():         # iteritems loops through key, value pairs
            fileHandle.write('\t' * indent + 'Key: ' + str(key) + '\n')
            fPrintNested(value, fileHandle, indent + 1, values)
    elif isinstance(d,np.ndarray) and d.dtype.names is not None:  # Note: and short-circuits by default
        for n in d.dtype.names:    # This means it's a struct, it's bit of a kludge test.
            fileHandle.write('\t' * indent + 'Field: ' + str(n) + '\n')
            fPrintNested(d[n], fileHandle, indent + 1, values)
    elif isinstance(d, list) :
        for each in d:
            fPrintNested(each, fileHandle, indent + 1, values)
    else:
        if values:
            fileHandle.write('\t' * indent + 'Value: ' + str(d)+'\n')
    return


def readFromDvlRaw(dvlRaw, channel, message_id, message_to_signal_value):
    """
    Read data directly from dvlRaw structure.

    :param dvlRaw: dvlRaw structure in mat file
    :param channel: channel number
    :param message_id: id of a message to be read
    :param message_to_signal_value: a function which takes as argument a single message (numpy array) and returns
    a number representing a value to be extracted from the message
    :return: list of values extracted from the messages, list of timestamps of those messages

    Example:
    Read 3rd and 4th bit of 7th byte of a message as a 0-3 number. Message number is 0x3D8, it is send on channel 2.
    All .mat file data are loaded into 'mat' variable.

    message_to_value = lambda msg: ((msg[7] & 0b00001100) >> 2)
    values, timestamps = readFromDvlRaw(mat['dvlRaw'], 2, 0x3D8, message_to_value)
    """
    indexes = [
        i for i in range(len(dvlRaw['can']['msgs']['id']))
        if
        dvlRaw['can']['msgs']['id'][i] == message_id
        and
        dvlRaw['can']['msgs']['channel'][i] == channel
    ]
    signal = [message_to_signal_value(dvlRaw['can']['msgs']['data'][i]) for i in indexes]
    ctime = [dvlRaw['can']['msgs']['ctime'][i] for i in indexes]
    return signal, ctime
