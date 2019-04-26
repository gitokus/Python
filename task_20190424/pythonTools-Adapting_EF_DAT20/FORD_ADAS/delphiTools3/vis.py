import os

import cv2
import readAVI
import numpy as np
import sys, traceback

from delphiTools3.base import loadmat


class videoHandler():
    def __init__(self, videoPath, data=None):
        self.videoPath = videoPath
        self.videoName = os.path.splitext(os.path.basename(videoPath))[0]

        try:
            self.video = readAVI.readAVI(videoPath)
            self.status = True
        except RuntimeError as err:
            print('Could not open video file: {}\n'.format(videoPath), err)
            self.status = False
            return

        self.videoSize = (self.video.getFrame().shape[1], self.video.getFrame().shape[0])
        self.videoLen = self.video.getFrameCount()
        self.videoMeta = self.calcMetaData()

        self.data = self.openData(data)
        self.layers = [False, False, False, False, False, False]

    def generateFrames(self, firstFrame, lastFrame=None, byGId=False, saveFolder=None, layerIDs=True,
                       enchancement=None, resize=0, colored=False):
        if self.status:
            if lastFrame is None:
                print('Generating frame: {}...'.format(firstFrame))
            else:
                print('Generating frames: {} - {}...'.format(firstFrame, lastFrame))

            if byGId:
                try:
                    firstFrame = self.videoMeta.index(firstFrame) + 1
                except:
                    print('Index {} out of range {} - {}'.format(firstFrame, self.videoMeta[0], self.videoMeta[-1]))
                    return [None]
            firstFrame = min(max(1, firstFrame), self.videoLen)
            if lastFrame is None:
                lastFrame = firstFrame
            else:
                if byGId:
                    try:
                        lastFrame = self.videoMeta.index(lastFrame) + 1
                    except:
                        print('Index {} out of range {} - {}'.format(lastFrame, self.videoMeta[0], self.videoMeta[-1]))
                        return [None]
                lastFrame = min(max(firstFrame, lastFrame), self.videoLen)

            generatedFrames = []

            self.video.seek(firstFrame)
            while True:
                try:
                    if colored:
                        frame = self.video.getBGR()
                        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    else:
                        frame = self.video.getFrame()
                        frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
                    meta = self.video.getMeta()
                    frameName = self.videoName + '_frame' + str(meta['Frame']) + '_gid' + str(meta['GId'])
                    if enchancement:
                        frame = self.enchance(frame, *enchancement)
                    frame = self.generateLayer(meta['GId'], frame, layerIDs)
                    if resize:
                        frame = cv2.resize(frame, (0, 0), fx=resize, fy=resize, interpolation=cv2.INTER_CUBIC)
                    if saveFolder:
                        if not os.path.isdir(saveFolder):
                            os.mkdir(saveFolder)
                        cv2.imwrite(os.path.join(saveFolder, frameName + '.png'),
                                    cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                        generatedFrames.append(frameName + '.png')
                    else:
                        generatedFrames.append(frame)
                except:
                    print('Skipping frame: {}'.format(self.video.getFrameNumber()))

                if self.video.getFrameNumber() == lastFrame:
                    break
                else:
                    self.video.seek(self.video.getFrameNumber() + 1)

            return generatedFrames

    def enchance(self, img, brightness=None, contrast=None):
        if brightness:
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            h, s, v = cv2.split(hsv)
            lim = 255 - brightness
            v[v > lim] = 255
            v[v <= lim] += brightness
            img = cv2.cvtColor(cv2.merge((h, s, v)), cv2.COLOR_HSV2BGR)

        if contrast:
            lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
            l, a, b = cv2.split(lab)
            clahe = cv2.createCLAHE(clipLimit=contrast, tileGridSize=(4, 4))
            cl = clahe.apply(l)
            img = cv2.cvtColor(cv2.merge((cl, a, b)), cv2.COLOR_LAB2BGR)

        return img

    ## PROJECT SPECIFIC SETTINGS
    def openData(self, data):
        if data and isinstance(data, dict):
            return data
        elif data and os.path.isfile(data):
            return loadmat(data, variableName='mudp', reBarrierMarge=True, sort=True)
        else:
            print('Cannot open data file!')
            return None

    def getFrameGId(self, frame=None):
        if frame:
            self.video.seek(frame)
        return self.video.getMeta()['GId']

    def calcMetaData(self):
        self.video.seek(1)
        first = self.video.getMeta()['GId']
        self.video.seek(self.videoLen)
        last = self.video.getMeta()['GId']
        if first < last:
            meta = list(range(first, last + 2, 2))
        else:
            meta = list(range(first, 65535 + 2, 2)) + list(range(1, last + 2, 2))
        return meta

    def showLayer(self, number, state):
        if self.status:
            translate = {'afl': 0,
                         'lks': 1,
                         'obj': 2,
                         'tsr': 3,
                         'rad': 4,
                         'gtl': 5}
            if isinstance(number, str):
                number = translate[number]

            self.layers[number] = state

    def generateLayer(self, GId, frame=None, layerIDs=True):
        try:
            imageIndex = list(self.data['mudp']['vis']['vision_traffic_sign_info']['imageIndex'])
            index = imageIndex.index(GId)
            if any(self.layers):
                if frame is None:
                    frame = np.zeros((self.videoSize[1], self.videoSize[0], 4))
                if self.data:
                    if self.layers[0]:
                        # afl
                        afl = self.data['mudp']['vis']['vision_active_light_sensor_info']['activeLightSpots']
                        # (R, G, B)
                        colorDict = {0: (255, 255, 255),  # 'None'
                                     1: (0, 0, 255),  # 'Headlamp'
                                     2: (255, 0, 0),  # 'Tail-lamp'
                                     3: (0, 0, 255),  # 'Pair of Headlamps'
                                     4: (255, 0, 0),  # 'Pair of Tail-lamps'
                                     5: (255, 128, 0),  # 'Truck Cabin Top Lights'
                                     6: (0, 255, 0),  # 'Weak Onciming or Weak TCL'
                                     7: (255, 0, 255)}  # 'Cluster'
                        for col in range(afl['classification'].shape[1]):
                            if afl['classification'][index][col] > 0:
                                color = colorDict[afl['classification'][index][col]]
                                cv2.rectangle(frame,
                                              (afl['pixelLeft'][index][col], 960 - afl['pixelTop'][index][col]),
                                              (afl['pixelRight'][index][col], 960 - afl['pixelBottom'][index][col]),
                                              color,
                                              2)
                                if layerIDs:
                                    point = ((afl['pixelLeft'][index][col] + afl['pixelRight'][index][col]) // 2,
                                             (960 - afl['pixelTop'][index][col]))
                                    cv2.putText(frame, str(afl['id'][index][col]), point, cv2.FONT_HERSHEY_COMPLEX,
                                                0.45,
                                                color, thickness=1, lineType=cv2.LINE_AA)
                        # afl-HRS
                        if 'reflectiveSigns' in self.data['mudp']['vis']['vision_active_light_sensor_info'].keys():
                            hrs = self.data['mudp']['vis']['vision_active_light_sensor_info']['reflectiveSigns']
                            rectangleColor = (255, 255, 0)
                            textColor = (255, 0, 255)
                            pixelPerRadian = 1280 / (52 * 2 * np.pi / 360)
                            for col in range(12):
                                if hrs['lightSignId'][index][col] > 0:
                                    pixelTop = 960 // 2 - \
                                               int(hrs['lightSignTopAngle'][index][col] * pixelPerRadian) - \
                                               self.data['mudp']['vis']['vision_camera_alignment_info'][
                                                   'cameraAlignment']['horizon'][index]
                                    pixelBottom = 960 // 2 - \
                                                  int(hrs['lightSignBottomAngle'][index][col] * pixelPerRadian) - \
                                                  self.data['mudp']['vis']['vision_camera_alignment_info'][
                                                      'cameraAlignment']['horizon'][index]
                                    pixelLeft = 1280 // 2 + \
                                                int(hrs['lightSignLeftAngle'][index][col] * pixelPerRadian) + \
                                                self.data['mudp']['vis']['vision_camera_alignment_info'][
                                                    'cameraAlignment']['yaw'][index]
                                    pixelRight = 1280 // 2 + \
                                                 int(hrs['lightSignRightAngle'][index][col] * pixelPerRadian) + \
                                                 self.data['mudp']['vis']['vision_camera_alignment_info'][
                                                     'cameraAlignment']['yaw'][index]
                                    cv2.rectangle(frame,
                                                  (pixelLeft, pixelTop),
                                                  (pixelRight, pixelBottom),
                                                  rectangleColor,
                                                  2)
                                    if layerIDs:
                                        point = ((pixelLeft + pixelRight) // 2, pixelBottom + 20)
                                        cv2.putText(frame, str(hrs['lightSignId'][index][col]), point,
                                                    cv2.FONT_HERSHEY_COMPLEX,
                                                    0.45,
                                                    textColor, thickness=1, lineType=cv2.LINE_AA)
                    if self.layers[1]:
                        # lks
                        lanesData = {
                            'LLn': self.data['mudp']['vis']['vision_road_info']['roadMarkerInfo'][
                                'hostLeftIndividualMarker'],
                            'RLn': self.data['mudp']['vis']['vision_road_info']['roadMarkerInfo'][
                                'hostRightIndividualMarker'],
                            'LRe': self.data['mudp']['vis']['vision_road_info']['mergedRoadEdgeInfo']['leftRoadEdge'],
                            'RRe': self.data['mudp']['vis']['vision_road_info']['mergedRoadEdgeInfo']['rightRoadEdge']
                        }
                        lanes = ['LRe', 'RRe', 'LLn', 'RLn']
                        for lane in lanes:
                            if lane == 'LRe' or lane == 'RRe':
                                colorDict = {0: (255, 255, 255),
                                             1: (100, 100, 255),
                                             2: (255, 200, 55)}
                                color = colorDict[lanesData[lane]['type'][index]]
                            else:
                                colorDict = {0: (255, 155, 155),
                                             1: (255, 255, 0),
                                             2: (255, 255, 255),
                                             3: (0, 200, 255)}
                                color = colorDict[lanesData[lane]['laneMarkerColor'][index]]
                            points = polyToPoints(self.data, index)
                            for l in range(4):
                                x1 = int(points[lane]['x'][l])
                                x2 = int(points[lane]['x'][l + 1])
                                y1 = int(points[lane]['y'][l])
                                y2 = int(points[lane]['y'][l + 1])
                                if lane == 'LLn' or lane == 'RLn':
                                    frame = drawCustomLine(frame, x1, y1, x2, y2, color, 1,
                                                           lanesData[lane]['laneMarkerType'][index])
                                else:
                                    frame = drawCustomLine(frame, x1, y1, x2, y2, color, 1)
                    if self.layers[2]:
                        # obj
                        obj = self.data['mudp']['vis']['vision_obstacles_info']['visObs']
                        for col in range(15):
                            if obj['detection_status'][index][col] == 0:
                                continue
                            else:
                                colorDict = {0: (255, 255, 255),  # 'Undetermined'
                                             1: (255, 255, 255),  # 'Car'
                                             2: (255, 255, 255),  # 'Motorcycle'
                                             3: (255, 255, 255),  # 'Truck'
                                             4: (255, 255, 255),  # 'Pedestrian'
                                             5: (255, 255, 255),  # 'Pole'
                                             6: (255, 255, 255),  # 'Tree'
                                             7: (255, 255, 255),  # 'Animal'
                                             8: (255, 255, 255),  # 'General on-road Object Detection'
                                             9: (255, 255, 255),  # 'Bicycle'
                                             10: (255, 255, 255)}  # 'Unidentified Vehicle'
                                color = colorDict[obj['obstacle_class'][index][col]]
                                cv2.rectangle(frame,
                                              (obj['pixel_left'][index][col], 960 - obj['pixel_top'][index][col]),
                                              (obj['pixel_right'][index][col], 960 - obj['pixel_bottom'][index][col]),
                                              color)
                                if layerIDs:
                                    point = ((obj['pixel_left'][index][col] + obj['pixel_right'][index][col]) // 2,
                                             (960 - obj['pixel_top'][index][col]))
                                    cv2.putText(frame, str(col + 1), point, cv2.FONT_HERSHEY_COMPLEX, 0.45,
                                                color, thickness=1, lineType=cv2.LINE_AA)
                    if self.layers[3]:
                        # tsr
                        tsr = self.data['mudp']['vis']['vision_traffic_sign_info']['trafficSigns']
                        for sign in range(8):
                            if tsr['signStatus'][index][sign] == 0:
                                continue
                            else:
                                color = (255, 255, 0, 255)
                                cv2.rectangle(frame,
                                              (tsr['signPositionLeft'][index][sign],
                                               960 - tsr['signPositionTop'][index][sign]),
                                              (tsr['signPositionRight'][index][sign],
                                               960 - tsr['signPositionBottom'][index][sign]),
                                              color, 1)
                                if layerIDs:
                                    point = (((tsr['signPositionLeft'][index][sign] + tsr['signPositionRight'][index][
                                        sign]) // 2),
                                             (960 - tsr['signPositionTop'][index][sign]))
                                    cv2.putText(frame, str(sign + 1), point, cv2.FONT_HERSHEY_COMPLEX, 0.45,
                                                color, thickness=1, lineType=cv2.LINE_AA)
                    if self.layers[4]:
                        fus_index = self.mapVisIndex2FusIndex(index)

                        # ACC STATIONARY RT1(RTS1)
                        rts1 = self.data['mudp']['tsel']['accStationaryTracks']

                        long_posn = rts1['vcs_long_posn'][fus_index, 0]
                        lat_posn = rts1['vcs_lat_posn'][fus_index, 0]
                        # track_id = rts1['track_id'][fus_index, 0]

                        top_left, right_bottom = self.mapLongLat2Box(long_posn, lat_posn, index)
                        top_right, left_bottom = (right_bottom[0], top_left[1]), (top_left[0], right_bottom[1])
                        color = (128, 128, 128, 255)

                        cv2.rectangle(frame, top_left, right_bottom, color, 1)
                        cv2.line(frame, top_left, right_bottom, color, 1)
                        cv2.line(frame, top_right, left_bottom, color, 1)

                        text_pos = top_left[0], right_bottom[1] - 5
                        cv2.putText(frame, 'RTS1', text_pos, cv2.FONT_HERSHEY_COMPLEX, 0.45,
                                    color, thickness=1, lineType=cv2.LINE_AA)

                        # PCA STATIONARY(PCAS)
                        pcas = self.data['mudp']['tsel']['pcaStationaryTrack']
                        long_posn = pcas['vcs_long_posn'][fus_index]
                        lat_posn = pcas['vcs_lat_posn'][fus_index]
                        # track_id = pcas['track_id'][fus_index]

                        top_left, right_bottom = self.mapLongLat2Box(long_posn, lat_posn, index)
                        color = (0, 255, 0, 255)
                        cv2.rectangle(frame, top_left, right_bottom, color, 1)

                        text_pos = right_bottom[0], top_left[1] + 5
                        cv2.putText(frame, 'PCAS', text_pos, cv2.FONT_HERSHEY_COMPLEX, 0.45,
                                    color, thickness=1, lineType=cv2.LINE_AA)

                        # PCA MOVING: (PCAV)
                        pcav = self.data['mudp']['tsel']['pcaMovingTrack']
                        long_posn = pcav['vcs_long_posn'][fus_index]
                        lat_posn = pcav['vcs_lat_posn'][fus_index]
                        # track_id = pcav['track_id'][fus_index]

                        top_left, right_bottom = self.mapLongLat2Box(long_posn, lat_posn, index)
                        top_right, left_bottom = (right_bottom[0], top_left[1]), (top_left[0], right_bottom[1])
                        color = (255, 0, 0, 255)

                        cv2.rectangle(frame, top_left, right_bottom, color, 1)
                        cv2.line(frame, top_left, right_bottom, color, 1)
                        cv2.line(frame, top_right, left_bottom, color, 1)

                        text_pos = top_left[0], right_bottom[1] - 5
                        cv2.putText(frame, 'PCAV', text_pos, cv2.FONT_HERSHEY_COMPLEX, 0.45,
                                    color, thickness=1, lineType=cv2.LINE_AA)

                        # ACC MOVING RT1(RTV1)
                        rtv1 = self.data['mudp']['tsel']['accMovingTracks']
                        long_posn = rtv1['vcs_long_posn'][fus_index, 0]
                        lat_posn = rtv1['vcs_lat_posn'][fus_index, 0]
                        # track_id = rtv1['track_id'][fus_index, 0]

                        top_left, right_bottom = self.mapLongLat2Box(long_posn, lat_posn, index)
                        color = (100, 0, 255, 255)

                        cv2.rectangle(frame, top_left, right_bottom, color, 1)

                        text_pos = top_left[0], right_bottom[1] + 5
                        cv2.putText(frame, 'RTV1', text_pos, cv2.FONT_HERSHEY_COMPLEX, 0.45,
                                    color, thickness=1, lineType=cv2.LINE_AA)

                        # Fused Pedestrian
                        fused = self.data['mudp']['fus']['log_data_fusion_tracker']['Fus']['fusTracks']
                        filter = self.data['mudp']['fus']['fused_ped_ind_vec'][fus_index, :]
                        filter_indexes = np.where(filter != 255)
                        indexes = fused['id'][fus_index, :]

                        for obj_id in filter[filter_indexes]:
                            obj_index = np.where(indexes == obj_id)[0][0]
                            long_posn = fused['vcs_long_posn'][fus_index, obj_index]
                            lat_posn = fused['vcs_lat_posn'][fus_index, obj_index]

                            center, radius = self.mapLongLat2Ellipse(long_posn, lat_posn, index)
                            text_pos = center[0], center[1] - radius[1] - 5
                            color = (255, 255, 0, 255)

                            cv2.ellipse(frame, center, radius, 0, 0, 360, color, 1)
                            cv2.putText(frame, str(obj_id), text_pos, cv2.FONT_HERSHEY_COMPLEX, 0.45,
                                        color, thickness=1, lineType=cv2.LINE_AA)
                    if self.layers[5] and 'groundtruth' in self.data.keys():
                        # GT
                        frame_data = self.data['groundtruth'][GId]
                        for obj in frame_data.values():
                            if obj['objType'] == '2DObj':
                                color = (255, 0, 0)
                                bottom_right, top_left = obj['cords'][1:3]
                                cv2.rectangle(frame, top_left, bottom_right, color, thickness=2)
                                if layerIDs:
                                    point = (top_left[0], top_left[1])
                                    cv2.putText(frame, str(obj['objID']), point, cv2.FONT_HERSHEY_COMPLEX, 0.45,
                                                color, thickness=1, lineType=cv2.LINE_AA)


        except Exception as e:
            print(f'Exception: {e}')
            print('No data for index {} in data file.'.format(GId))
        return frame

    def mapVisIndex2FusIndex(self, visIndex):
        imageIndex = self.data['mudp']['vis']['vision_obstacles_info']['imageIndex'][visIndex]
        grabIndex = self.data['mudp']['fus']['log_data_fusion_tracker']['status']['grabIndex']
        whereResult = np.where(grabIndex == imageIndex)[0]
        return whereResult[0]

    def mapLongLat2Box(self, long_posn, lat_posn, index):
        vis_cords = topView2Vis(np.array([[lat_posn], [long_posn]]), self.data, index)
        vis_height = int(mapLengthT2V(1.6, long_posn, self.data, index))
        return (int(vis_cords[0, 0]) + 10, int(vis_cords[1, 0])),\
               (int(vis_cords[0, 0]) - 10, int(vis_cords[1, 0]) - vis_height)

    def mapLongLat2Ellipse(self, long_posn, lat_posn, index):
        vis_cords = topView2Vis(np.array([[lat_posn], [long_posn]]), self.data, index)
        vis_height = int(mapLengthT2V(1.6, long_posn, self.data, index))
        center = int(vis_cords[0, 0]), int(vis_cords[1, 0]) - int(vis_height / 2)
        radius = 10, int(vis_height / 2)
        return center, radius


## HELPERS
def drawCustomLine(img, x1, y1, x2, y2, color, width, style=1):
    if style == 1:  # solid
        img = cv2.line(img, (x1, y1), (x2, y2), color, width, cv2.LINE_AA)
    elif style == 2:  # dashed
        closerRange = min(abs(x2 - x1), abs(y2 - y1))
        x = np.linspace(x1, x2, closerRange)
        y = np.linspace(y1, y2, closerRange)
        i = 0
        j = 0
        draw = True
        while i < closerRange:
            if (x[i] - x[j]) ** 2 + (y[i] - y[j]) ** 2 > 100:
                if draw:
                    img = cv2.line(img, (int(x[j]), int(y[j])), (int(x[i]), int(y[i])), color, width, cv2.LINE_AA)
                draw = not draw
                j = i
            i += 1
    elif style == 4:  # dot
        closerRange = min(abs(x2 - x1), abs(y2 - y1))
        x = np.linspace(x1, x2, closerRange)
        y = np.linspace(y1, y2, closerRange)
        i = 0
        j = 0
        draw = True
        while i < closerRange:
            if (x[i] - x[j]) ** 2 + (y[i] - y[j]) ** 2 > 9:
                if draw:
                    img = cv2.line(img, (int(x[j]), int(y[j])), (int(x[i]), int(y[i])), color, width, cv2.LINE_AA)
                draw = not draw
                j = i
            i += 1
    elif style == 8:  # double
        img = cv2.line(img, (x1, y1), (x2, y2), color, width, cv2.LINE_AA)
        img = cv2.line(img, (x1 - 20, y1), (x2 - 20, y2), color, width, cv2.LINE_AA)
    else:  # solid with width 1
        img = cv2.line(img, (x1, y1), (x2, y2), color, 1, cv2.LINE_AA)
    return img


def polyToPoints(mat, index):
    """
    Translate poly factors of given lane into points to be drawn on frame from video.

    :param index: index in mat file where data should be extracted
    :param factors: array of factors for given line
    :param hRange: array of range of given line
    :return: returns two 5 element lists with x and y cords
    """

    focalLength = float(
        mat['mudp']['vfpState']['cals']['vision_params']['vehIndependentParam']['focalLength'][index])
    pixelsPerDegree = float(
        mat['mudp']['vfpState']['cals']['vision_params']['vehIndependentParam']['pixelsPerDegree'][index])
    cameraHeight = float(
        mat['mudp']['vfpState']['cals']['vision_params']['vehDependentParam']['cameraHeight_mm'][index]) / 1000
    pitch = -1 * float(
        mat['mudp']['vis']['vision_camera_alignment_info']['cameraAlignment']['horizon'][
            index] / pixelsPerDegree)
    yaw = float(mat['mudp']['vis']['vision_camera_alignment_info']['cameraAlignment'][
                    'yaw'][index] / pixelsPerDegree)
    roll = float(
        mat['mudp']['vis']['vision_camera_alignment_info']['cameraAlignment']['rollAngle'][
            index] / pixelsPerDegree)

    imagerWidth = 1280
    imagerHeight = 960

    lanes = {
        'LLn': mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostLeftIndividualMarker']['laneMarker'],
        'RLn': mat['mudp']['vis']['vision_road_info']['roadMarkerInfo']['hostRightIndividualMarker']['laneMarker'],
        'LRe': mat['mudp']['vis']['vision_road_info']['mergedRoadEdgeInfo']['leftRoadEdge']['roadEdge'],
        'RRe': mat['mudp']['vis']['vision_road_info']['mergedRoadEdgeInfo']['rightRoadEdge']['roadEdge']
    }

    lanesPoints = {
        'LLn': {'x': [], 'y': []},
        'RLn': {'x': [], 'y': []},
        'LRe': {'x': [], 'y': []},
        'RRe': {'x': [], 'y': []},
    }

    ls = ['LRe', 'RRe', 'LLn', 'RLn']
    for lane in ls:
        hRange = lanes[lane]['range'][index]
        factors = [lanes[lane]['a3'][index], lanes[lane]['a2'][index],
                   lanes[lane]['a1'][index], lanes[lane]['a0'][index]]

        Y = list(np.linspace(0, hRange, 5))
        X = list(np.polyval(factors, Y))

        for j in range(5):
            camX = X[j]
            camY = Y[j]
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

            lanesPoints[lane]['x'].append((imagerWidth / 2) + imageX)
            lanesPoints[lane]['y'].append((imagerHeight / 2) - imageY)

    return lanesPoints


def mapLengthT2V(realHeight, lenghtY, mat, index) -> int:
    if np.isclose(lenghtY, 0.):
        return 100
    sensorPhysicalHeight = 1
    focalLength = float(
        mat['mudp']['vfpState']['cals']['vision_params']['vehIndependentParam']['focalLength'][index])
    return int((focalLength * realHeight * 960) / (sensorPhysicalHeight * lenghtY * 1000))


def topView2Vis(topView, mat, index):
    """

    :param topView:
    :param mat:
    :param index: current index
    :return:
    """

    focalLength = float(
        mat['mudp']['vfpState']['cals']['vision_params']['vehIndependentParam']['focalLength'][index])
    pixelsPerDegree = float(
        mat['mudp']['vfpState']['cals']['vision_params']['vehIndependentParam']['pixelsPerDegree'][index])
    cameraHeight = float(
        mat['mudp']['vfpState']['cals']['vision_params']['vehDependentParam']['cameraHeight_mm'][index]) / 1000
    pitch = -1 * float(
        mat['mudp']['vis']['vision_camera_alignment_info']['cameraAlignment']['horizon'][
            index] / pixelsPerDegree)
    yaw = float(mat['mudp']['vis']['vision_camera_alignment_info']['cameraAlignment'][
                    'yaw'][index] / pixelsPerDegree)
    roll = float(
        mat['mudp']['vis']['vision_camera_alignment_info']['cameraAlignment']['rollAngle'][
            index] / pixelsPerDegree)

    imagerWidth = 1280
    imagerHeight = 960

    camX = topView[0]
    camY = topView[1]
    camZ = -cameraHeight

    yaw_angle = np.deg2rad(yaw)
    cam2X = camX * np.cos(yaw_angle) + camY * np.sin(yaw_angle)
    cam2Y = camY * np.cos(yaw_angle) - camX * np.sin(yaw_angle)
    cam2Z = camZ

    pitch_angle = np.deg2rad(pitch)
    cam3X = cam2X
    cam3Y = cam2Y * np.cos(pitch_angle) + cam2Z * np.sin(pitch_angle)
    cam3Z = cam2Z * np.cos(pitch_angle) - cam2Y * np.sin(pitch_angle)

    p = (focalLength / cam3Y) * cam3X
    q = (focalLength / cam3Y) * cam3Z

    roll_angle = np.deg2rad(roll)
    image_x = (p * np.cos(roll_angle)) + (q * np.sin(roll_angle))
    image_y = (q * np.cos(roll_angle)) - (p * np.sin(roll_angle))

    x = (imagerWidth / 2) + image_x
    y = (imagerHeight / 2) - image_y

    return np.array([x, y])


if __name__ == '__main__':
    tavi = r"D:\tickets\test\Cx483_checkout_20180222_20180222_180923_001.tavi"
    avi = r"D:\tickets\test\Cx483_checkout_20180222_20180222_180923_001.avi"
    mat = r"D:\tickets\test\Cx483_checkout_20180222_20180222_180923_001.mat"

    vH = videoHandler(tavi, mat)
    vH.layers = [1, 1, 1, 1, 0]

    vH.generateFrames(14181, 16339, byGId=True, saveFolder='C:/Users/wj5y0m/Desktop/out')  # 49749-52003

    vH = videoHandler(avi, mat)
    vH.layers = [1, 1, 1, 1, 0]

    vH.generateFrames(14181, 16339, byGId=True, saveFolder='C:/Users/wj5y0m/Desktop/out2')  # 49749-52003
