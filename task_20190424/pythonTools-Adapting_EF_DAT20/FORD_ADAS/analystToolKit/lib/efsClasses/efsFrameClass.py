import csv
import os
import sys
import time
import re
import numpy as np
import traceback

from itertools import groupby, count
from datetime import datetime

from analystToolKit.lib import UDP
SEND_DELAY = 0.01


class EFClass():
    def loadmat(self, mat, dat2p0):
        self.dat2p0 = dat2p0
        if dat2p0:
            self.mat = mat
            self.visIndex = self.mat["mudp"]["eyeq"]["Lights"]["vis_light_sensor_data_info"]["activeLightSensorInfo"]["imageIndex"]
            self.visLen = len(self.visIndex)
            self.matName = os.path.splitext(self.mat['mudp']['bfname'])[0]
            self.ME_API = ""
            self.ME_SW = ""
            self.VFP = ""
            self.eventIDCounter = 1
            self.eventsDictList = []

        else:
            self.mat = mat
            self.visIndex = mat['mudp']['vis']['vision_function_info']['imageIndex']
            self.visLen = len(self.visIndex)
            self.matName = os.path.splitext(self.mat['mudp']['bfname'])[0]
            self.ME_API = mat['mudp']['vfpState']['versions']['vision_version_info']['apiVer'][0]
            self.ME_SW = mat['mudp']['vfpState']['versions']['vision_version_info']['swVer'][0]
            self.VFP = str(mat['mudp']['vfpState']['versions']['release_revision'][0]) + '.' + \
                               str(mat['mudp']['vfpState']['versions']['promote_revision'][0])

            self.eventIDCounter = 1
            self.eventsDictList = []


    def getEFsList(self):
        return sorted([f[3:] for f in dir(self) if f[:3] == 'ef_' and not 'template' in f])


    def run(self, EFsToRun, details=False, refreshFunction=None):
        if not EFsToRun:
            return

        print('Running ' + self.function + ' event finders...')
        for ef in EFsToRun:
            try:
                print('\tEF {}:'.format(ef))
                efResults = eval('self.ef_{}()'.format(ef))
                errorNameList = []
                numberOfEvents = 0
                for i in range(efResults['len']):
                    if refreshFunction is not None:
                        refreshFunction()
                    events, errors = self.appendEvents(efResults['data'][i], details)
                    numberOfEvents += events
                    errorNameList += errors
                if numberOfEvents:
                    print('\tFound events: {}'.format(numberOfEvents))
                    if errorNameList:
                        print('\tCannot read: {}'.format(str(list(set(errorNameList)))[1:-1]))
                print('\tDone')
            except:
                print('\tEvent finder failed: ', traceback.format_exc())
                continue


    def appendEvents(self, data, details):
        self.header = ['logName', 'eventFinderID', 'eventID',
                       'eventComment', 'eventIndex', 'eventDuration',
                       'ME_API', 'ME_SW', 'VFP_ver']
        if len(data) == 4:
            self.header.insert(6, 'eventColumnID')
        try:
            indexes = data[0]
            ID = data[1]
            Comment = data[2]
            if len(data) == 4:
                ColumnID = data[3]
            else:
                ColumnID = -1

            eventsDictList = []

            for event in indexes:
                newEventDict = dict()
                newEventDict['logName'] = self.matName
                newEventDict['eventFinderID'] = ID
                newEventDict['eventID'] = self.eventIDCounter
                newEventDict['eventComment'] = Comment
                newEventDict['eventIndex'] = self.visIndex[event[0]]
                newEventDict['eventDuration'] = len(event)
                newEventDict['eventColumnID'] = ColumnID
                try:
                    newEventDict['ME_API'] = self.ME_API

                    newEventDict['ME_SW'] = self.ME_SW
                    newEventDict['VFP_ver'] = self.VFP
                except TypeError:
                    rM_resim_tag = re.search('_rM(\d{2})(\d{3})\d{2}', self.matName)
                    if rM_resim_tag:
                        newEventDict['ME_API'] = rM_resim_tag.group(1) + ' (resim)'
                        newEventDict['ME_SW'] = rM_resim_tag.group(2) + ' (resim)'
                        newEventDict['VFP_ver'] = ''
                    else:
                        newEventDict['ME_API'] = ''
                        newEventDict['ME_SW'] = ''
                        newEventDict['VFP_ver'] = ''
                eventsDictList.append(newEventDict)
                self.eventIDCounter += 1
            self.eventsDictList += eventsDictList

            errors = []
            if details:
                errors = self.appendDetails(dat2p0=self.dat2p0)

            return len(eventsDictList), errors
        except:
            print('\tUnable to read core event data')
            raise


    def save(self, outputPath, ip='', port=0):
        try:
            if self.eventsDictList:
                print('Saving results...')

                outCsvName = os.path.join(outputPath, '{}-EF_{}.csv'.format(self.function, datetime.now().strftime("%d-%m-%y")))

                if ip == '' or port == 0:
                    if not os.path.isfile(outCsvName):
                        with open(outCsvName, 'w', newline='') as csvfile:
                            fcsvwriter = csv.DictWriter(csvfile, self.header, extrasaction='ignore', dialect='excel')
                            fcsvwriter.writeheader()
                    with open(outCsvName, 'a', newline='') as csvfile:
                        fcsvwriter = csv.DictWriter(csvfile, self.header, extrasaction='ignore', dialect='excel')
                        fcsvwriter.writerows(self.eventsDictList)
                else:
                    for event in self.eventsDictList:
                        UDP.sendData(ip, port, [self.function, outputPath, self.matName, self.header, event])
                        time.sleep(SEND_DELAY)

                print('Saving complete.')
        except:
            print('Error while saving results!')


    def dictFormatter(self, dict):
        for key in dict.keys():
            if isinstance(dict[key], np.ndarray):
                dict[key] = dict[key].tolist()
        return dict


    def groupIndexes(self, signal, maxGap=0, minPeaks=0):
        if not signal:
            return []
        newSignal = [signal[0]]
        for index in signal[1:]:
            diff = index - newSignal[-1]
            if diff < maxGap:
                for newIndex in range(newSignal[-1] + 1, newSignal[-1] + 1 + diff):
                    newSignal.append(newIndex)
            else:
                newSignal.append(index)

        seperatedSignal = [list(g) for _, g in groupby(newSignal, key=lambda n, c=count(): n - next(c))]

        peaksFilteredSignal = []
        for event in seperatedSignal:
            peaksCounter = 0
            for i in event:
                if i in signal:
                    peaksCounter += 1
                if peaksCounter >= minPeaks:
                    peaksFilteredSignal.append(event)
                    break

        return peaksFilteredSignal