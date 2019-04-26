# TSR
def hintType(number, reverse = False):
    template = {70: 'UNKNOWN',
                71: 'Speed Limit Sign',
                72: 'City Entry/Exit Sign',
                73: 'Speed Zone Sign',
                74: 'Overtaking Sign',
                75: 'Electronic Sign',
                76: 'Supplementary Sign',
                77: 'Road signs',
                78: 'All wrong way signs',
                79: 'Many signs'}
    if reverse:
        template = {v: k for k, v in template.items()}
    if number in template.keys():
        return template[number]
    else:
        return 'UNKNOWN'


def signType(signType, reverse = False):
    template = {0: '-',
                1: 'SPEED_LIMIT_START',
                2: 'SPEED_LIMIT_END',
                5: 'HIGHWAY_START',
                6: 'HIGHWAY_END',
                7: 'FREEWAY_START',
                8: 'FREEWAY_END',
                10: 'YIELD',
                11: 'TOWN_START',
                12: 'TOWN_END',
                13: 'LOW_SPEED_AREA_START',
                14: 'LOW_SPEED_AREA_END',
                15: 'STOP',
                16: 'NO_OVERTAKING_START',
                17: 'NO_OVERTAKING_END',
                18: 'NO_ENTRANCE',
                19: 'ADVISORY_SPEED_LIMIT_START',
                20: 'NO_ENTRANCE_ALERT',
                24: 'NO_OVERTAKING_TRUCK_START',
                25: 'NO_OVERTAKING_TRUCK_END',
                26: 'ROUND_ABOUT',
                27: 'END_OF_ALL',
                28: 'ARROW_BLUE_STRAIGHT',
                29: 'ARROW_BLUE_RIGHT',
                30: 'ARROW_BLUE_LEFT',
                31: 'ARROW_BLUE_RIGHT_AHEAD',
                32: 'ARROW_BLUE_LEFT_AHEAD',
                33: 'ARROW_BLUE_NO_LEFT',
                34: 'ARROW_BLUE_NO_RIGHT',
                35: 'ARROW_BLUE_KEEP_LEFT',
                36: 'ARROW_BLUE_KEEP_RIGHT',
                37: 'ARROW_BLUE_PASS_EITHER_SIDE',
                38: 'TOWN_START_DARK_BG',
                39: 'LIMIT_CARS',
                40: 'WARNING_PEDESTRIAN_CROSSING'}
    if reverse:
        template = {v: k for k, v in template.items()}
    if signType in template.keys():
        return template[signType]
    else:
        return '-'

def signValue(signValue, reverse = False):
    if not reverse:
        if int(signValue)== 255:
            return '-'
        else:
            return str((int(signValue)/5)*5)
    else:
        if str(signValue)== '-':
            return 255
        else:
            return float(signValue)

def f_signEmbedded(signEmbedded, reverse = False):
    template = {0: '-',
                1: 'EMBEDDED'}
    if reverse:
        template = {v: k for k, v in template.items()}
    if signEmbedded in template.keys():
        return template[signEmbedded]
    else:
        return '-'


def f_signElectronic(signElectronic, reverse = False):
    template = {0: '-',
                1: 'ELECTRONIC'}
    if reverse:
        template = {v: k for k, v in template.items()}
    if signElectronic in template.keys():
        return template[signElectronic]
    else:
        return '-'


def signLocation(signLocation, reverse = False):
    template = {0: 'Unknown',
                1: 'Above Road',
                2: '-'}
    if reverse:
        template = {v: k for k, v in template.items()}
    if signLocation in template.keys():
        return template[signLocation]
    else:
        return '-'


def signSupplementalType1(signSuppType, reverse = False):
    template = {0: 'None',
                1: 'Generic',
                2: 'Distance',
                3: 'Distance Arrow',
                4: 'Time',
                5: 'Weight',
                6: 'School',
                7: 'Rain',
                8: 'Rain Cloud',
                9: 'Snow',
                10: 'Snow Rain',
                11: 'Fog',
                12: 'Night',
                13: 'Zone',
                14: 'Trailer',
                15: 'Truck',
                16: 'Tractor',
                17: 'Arrow Left',
                18: 'Arrow Right',
                19: 'Bend Left',
                20: 'Bend Right',
                21: 'End',
                22: 'Ice',
                23: 'Distance For AND In',
                24: 'Truck & Trailer (Not Supported)',
                25: 'Ramp',
                26: 'Exit',
                27: 'Advisory',
                28: 'Minimum',
                29: 'Reduced_ahead',
                30: 'Distance_stop',
                31: 'Ahead',
                32: 'Area',
                33: 'Road_work_au',
                34: 'Arrow_bidirectional',
                35: 'Rappel'
                }
    if reverse:
        template = {v: k for k, v in template.items()}
    if signSuppType in template.keys():
        return template[signSuppType]
    else:
        return 'None'
signSupplementalType2 = signSupplementalType1


def signRelevantDecision(signRelevant, reverse = False):
    template = {0: 'Relevant Sign',
                1: 'Highway Exit',
                2: 'Lane Assignment Sign',
                3: 'Parallel Road Sign',
                4: 'Sign On Turn',
                5: 'Far Irrelevant Sign',
                6: 'Internal Sign Contradiction',
                7: 'Other Filtering Reason'}
    if reverse:
        template = {v: k for k, v in template.items()}
    if signRelevant in template.keys():
        return template[signRelevant]
    else:
        return 'Other Filtering Reason'


def currentMarket(currenMarket, reverse = False):
    template = {0: 'Init',
                1: 'Default',
                2: 'UK',
                3: 'Ireland / South Africa',
                4: 'Canada',
                5: 'China',
                6: 'Japan',
                7: 'Europe',
                8: 'USA',
                9: 'Arab',
                10: 'Korea',
                11: 'Australia',
                12: 'Reserved',
                13: 'Reserved',
                14: 'Reserved',
                15: 'Reserved',
                16: '-'}
    if reverse:
        template = {v: k for k, v in template.items()}
    if currenMarket in template.keys():
        return template[currenMarket]
    else:
        return '-'


# AFL
def ahbcAvailable(available, reverse = False):
    template = {0: 'OFF',
                1: 'Partially',
                2: 'Full',
                3: '-'}
    if reverse:
        template = {v: k for k, v in template.items()}
    if available in template.keys():
        return template[available]
    else:
        return '-'


def adaptiveRequest(request, reverse = False):
    template = {0: 'OFF',
                1: 'ON',
                2: 'Not Used',
                3: 'FROZEN ON',
                4: '-'}
    if reverse:
        template = {v: k for k, v in template.items()}
    if request in template.keys():
        return template[request]
    else:
        return '-'


def beamRequest(request, reverse = False):
    template = {0: 'High Beam OFF',
                1: 'High Beam ON',
                2: '-'}
    if reverse:
        template = {v: k for k, v in template.items()}
    if request in template.keys():
        return template[request]
    else:
        return '-'


def classification(classification, reverse = False):
    template = {0: 'None',
                1: 'Head lamp',
                2: 'Tail lamp',
                3: 'Head lamp pair',
                4: 'Tail lamp pair',
                5: 'Truck cabin top lights',
                6: 'Weak Head Pair',
                7: '-'}
    if reverse:
        template = {v: k for k, v in template.items()}
    if classification in template.keys():
        return template[classification]
    else:
        return '-'


def eventsDetected(events, reverse = False):
    ans = []
    template = {0: 'No switch reason',
                1: 'Oncoming Vehicle',
                2: 'Preceding Vehicle',
                3: 'Speed Limit',
                4: 'Ambient Light',
                5: 'Village Detection',
                6: 'Fog Detection',
                7: 'Highway Mode',
                8: 'Delay',
                9: 'Too Many Oncoming Spots',
                10: 'Too Many Preceding Spots',
                11: 'Curve Status',
                12: 'High Speed Status',
                13: 'Oncoming Vehicle Delay',
                14: 'Preceding Vehicle Delay',
                15: 'Village Detection Delay',
                16: '-'}
    if reverse:
        template = {v: k for k, v in template.items()}
        ans = 0
        for bit in events.split('/\n'):
            ans += 2**template[bit]
    else:
        for id, bit in enumerate(str(bin(int(events))[2:]).zfill(16)[::-1]):
            if bit == '1':
                ans.append(template[id])
    if isinstance(ans, list):
        if len(ans) == 0:
            return '-'
        else:
            return '/\n'.join(ans)
    else:
        return ans


def clearFieldOfView(fov, reverse = False):
    template = {0: 'Unknown',
                1: 'No Clear FOV',
                2: 'Clear FOV',
                3: '-'}
    if reverse:
        template = {v: k for k, v in template.items()}
    if fov in template.keys():
        return template[fov]
    else:
        return '-'


def highwayDetected(hd, reverse = False):
    template = {0: 'No Highway',
                1: 'Highway',
                2: '-'}
    if reverse:
        template = {v: k for k, v in template.items()}
    if hd in template.keys():
        return template[hd]
    else:
        return '-'


def villageDetected(vd, reverse = False):
    template = {0: 'No Urban Area',
                1: 'City',
                2: '-'}
    if reverse:
        template = {v: k for k, v in template.items()}
    if vd in template.keys():
        return template[vd]
    else:
        return '-'


def f_oncomingLineLotDark(dk, reverse = False):
    template = {0: 'Dark',
                1: 'Not Dark',
                2: '-'}
    if reverse:
        template = {v: k for k, v in template.items()}
    if dk in template.keys():
        return template[dk]
    else:
        return '-'


# LKS
def roadPrediction(events, reverse = False):
    ans = []
    template = {0: 'Diverging lane-marks',
                1: 'Other Side based',
                2: 'Merge',
                3: 'Extrapolation',
                4: 'Occluded Lane-Mark',
                5: 'Headway Oriented',
                6: 'Highway Exit Spain',
                7: '-'}
    if reverse:
        template = {v: k for k, v in template.items()}
        ans = 0
        for bit in events.split('/\n'):
            ans += 2**template[bit]
    else:
        for id, bit in enumerate(str(bin(int(events))[2:]).zfill(7)[::-1]):
            if bit == '1':
                ans.append(template[id])
    if isinstance(ans, list):
        if len(ans) == 0:
            return '-'
        else:
            return '/\n'.join(ans)
    else:
        return ans
roadPredictionLeft = roadPredictionRight = roadPrediction

def laneMarkerColor(color, reverse = False):
    template = {0: 'Unknown',
                1: 'Yellow',
                2: 'White',
                3: 'Blue',
                4: '-'}
    if reverse:
        template = {v: k for k, v in template.items()}
    if color in template.keys():
        return template[color]
    else:
        return '-'


def laneMarkerType(type, reverse = False):
    template = {0: 'None',
                1: 'Solid',
                2: 'Dashed',
                3: 'Reserved',
                4: 'Botts Dots',
                5: 'Reserved',
                6: 'Invalid',
                7: 'Undecided',
                8: 'Double',
                9: '-'}
    if reverse:
        template = {v: k for k, v in template.items()}
    if type in template.keys():
        return template[type]
    else:
        return '-'

def type(type, reverse = False):
    template = {0: '-',
                1: 'Flat',
                2: 'Barrier'}
    if reverse:
        template = {v: k for k, v in template.items()}
    if type in template.keys():
        return template[type]
    else:
        return '-'

def status(status, reverse = False):
    template = {0: 'Invalid',
                1: 'Reserved',
                2: 'New',
                3: 'Reserved',
                4: 'Reserved',
                5: 'Updated',
                6: 'Coasted',
                7: 'Reserved',
                8: '-'}
    if reverse:
        template = {v: k for k, v in template.items()}
    if status in template.keys():
        return template[status]
    else:
        return '-'

