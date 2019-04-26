'''
this program iterates over mat files and plots signals which determine
whether delayed sign confidence on highway-exit speed limits has impact
on system or not
'''

import delphiTools3.base as dtb
import os
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import glob
import time

path = r"D:\dev\python\Zuzia\task4"
# testMat = dtb.loadmat(os.path.join(path, 'mats',
#                                    'ADAS_20160527_KQW3211_PAR_PAR_BK_PG_20160528_000609_036_rM8641055.mat'),
#                       sort=True)
# mat = testMat


# matPaths = pd.Series(glob.glob(os.path.join(path, 'mats', '*.mat')), name='matPaths')
# # get only names, without paths
# matNames = pd.Series([os.path.split(matPath)[1][:-4] for matPath in matPaths], name = 'matNames')

# # Create df from series
# logsData = pd.concat([matPaths, matNames], axis=1)
# logsData = logsData.sort_values(by='matNames')
# logsData.to_csv(os.path.join(path, 'data.csv'))

# Read csv file. Extend range of start/end of event by 50 frames,
# if startEvent < 0, change it to 0
logsData = pd.read_csv(r'D:\dev\python\PycharmProjects\Zuzia\Python\task04\data.csv', sep=';')
logsData.columns
logsData['startEvent'] = logsData['startEvent'] - 50
logsData['endEvent'] = logsData['endEvent'] + 50
logsData.loc[logsData['startEvent'] < 0, 'startEvent'] = 0


class SignData():
    def __init__(self, mat):
        self.signs = mat['mudp']['vis']['vision_traffic_sign_info']['trafficSigns']
        self.grabIndex = mat['mudp']['tsel']['commonETSELInfo']['grab_index']
        self.imageIndex = mat['mudp']['vis']['vision_traffic_sign_info']['imageIndex']
        self.sType = self.signs['signType']
        self.sConf = self.signs['signConfidence']
        self.sSupType = self.signs['signSupplementalType1']
        self.sValue = self.signs['signValue']
        self.longPos = self.signs['signLongPosition']
        self.sRelDec = self.signs['signRelevantDecision']
    #     self.changeConfidence()

    # def changeConfidence(self):
    #     # For better visualisation if conf==0.99 assume it's 0.5
    #     self.sConf[self.sConf < 0.5,:] = 0
    #     self.sConf[0.5 <= self.sConf <= 0.99,:] = 0.5


for row in range(len(logsData)):
# for row in range(1):
    log = logsData['matPath'].iloc[row]
    beg = logsData['startEvent'].iloc[row]
    end = logsData['endEvent'].iloc[row]
    logName = logsData['matName'].iloc[row]
    log = dtb.loadmat(log, sort=True, variableName='mudp')
    data = SignData(log)
    print(f"***** Processing: {logName} ****")

    #rozmiar obrazka w calach = A4, rodzielczosc=100dpi
    #plt.figure( figsize=(8.27, 11.69), dpi=100 )
    plt.figure( figsize=(9, 9) )
    #tytul wykresu, zkres wspolrzednych 0,0=bottom-left 1,1=top-right
    plt.suptitle( logName+f':range [{beg}:{end}]', fontsize=10, ha='left', x=0.03, y=0.97)

    colorsDict = {0: 'b', 1: 'g', 2: 'r', 3: 'c',4: 'm', 5: 'y', 6: 'k', 7: 'b'}

    print(len(data.sType))

    for i in range(8):
        #kolumna i w tablicy sType
        sType = data.sType[:, i]
        # wybierz z sType indeksy elementow spelniajacych warunki index >= beg i index < end
        if len(sType) < end:
            end = len(sType)
        # wybierz z sType indeksy niezerowych elementow i wstaw do macierzy indexex
        indexes = np.argwhere(sType == 1)
        # print(indexes)
        # Filter indexes so that we take into account only indexes regarding
        # our event
        indexes = np.intersect1d(indexes, np.arange(beg, end))

        # try:
        #     sType = data.sType[indexes, i]
        # except IndexError:
        #     continue
        sType = data.sType[indexes, i]
        sConf = data.sConf[indexes, i]
        sSupType = data.sSupType[indexes, i]
        sValue = data.sValue[indexes, i]
        sRelDec = data.sRelDec[indexes, i]
        imageIndex = data.imageIndex[indexes]

        minorLocator = matplotlib.ticker.AutoMinorLocator()

        # Plot singValue vs. grabIndex
        p1 = plt.subplot(411)
        # domyslnie wykres dla wszystkich wartosci rysowany jest jednym przylozeniem "pisaka" 
        # dlatego marker='.' i linestyle='none' zeby bylo widac nieciaglasci miedzy fragmentami
        p1.plot(indexes, sValue, color=colorsDict[i], marker='.', markersize=3, linestyle='none')
        #p1.plot(imageIndex, sValue, color=colorsDict[i], lw=2, linestyle='-')
        p1.set_title('Sign Value')
        p1.xaxis.set_minor_locator(minorLocator)
        plt.grid(True, which='both')

        # Plot singConfidence vs. imageIndex
        p2 = plt.subplot(412)
        p2.plot(imageIndex, sConf, color=colorsDict[i], marker='.', markersize=2, linestyle='none')
        #p2.plot(imageIndex, sConf, color=colorsDict[i], lw=1.5, linestyle='--')
        p2.set_title('Sign Confidence')
        p2.xaxis.set_minor_locator(minorLocator)
        plt.grid(True, which='both')
        plt.ylim(0.4, 1.05)
        # plt.grid(True, which='both', alpha=0.5)

        # Plot signSuppl vs. imageIndex
        p3 = plt.subplot(413)
        p3.plot(imageIndex, sSupType, color=colorsDict[i], marker='.', markersize=2, linestyle='none')
        #p3.plot(imageIndex, sSupType, color=colorsDict[i], lw=1.5, linestyle='--')
        p3.set_title('Supplementary Type')
        p3.xaxis.set_minor_locator(minorLocator)
        plt.grid(True, which='both')

        # Plot signRelevantDecision vs. imageIndex
        p4 = plt.subplot(414)
        p4.plot(imageIndex, sRelDec, color=colorsDict[i], marker='.', markersize=2, linestyle='none')
        #p4.plot(imageIndex, sRelDec, color=colorsDict[i], lw=1.5, linestyle='--')
        p4.set_title('Relevant Decision')
        p4.xaxis.set_minor_locator(minorLocator)
        plt.grid(True, which='both')

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig(os.path.join(path, f'{row+1}_{logName}' +'.png'))
    # plt.show()
    print("\n Finished \n")
    plt.close()