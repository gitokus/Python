'''
this program iterates over mat files and plots signals which determine
whether delayed sign confidence on highway-exit speed limits has impact
on system or nota
'''

import delphiTools3.base as dtb
import os
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

path = r"D:\dev\python\Zuzia\task5"
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
logsData = pd.read_csv(r'D:\dev\python\Zuzia\task5\data.csv', sep=';')
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
    log1= logsData['matPath1'].iloc[row]
    log2= logsData['matPath2'].iloc[row]
    beg = logsData['startEvent'].iloc[row]
    end = logsData['endEvent'].iloc[row]
    logName = logsData['matName'].iloc[row]
    log1 = dtb.loadmat(log1, sort=True, variableName='mudp')
    log2 = dtb.loadmat(log2, sort=True, variableName='mudp')
    data1 = SignData(log1)
    data2 = SignData(log2)
    print(f"***** Processing: {logName} ****")

    #rozmiar obrazka w calach = A4, rodzielczosc=100dpi
    #plt.figure( figsize=(8.27, 11.69), dpi=100 )
    plt.figure( figsize=(9, 9) )
    #tytul wykresu, zkres wspolrzednych 0,0=bottom-left 1,1=top-right
    plt.suptitle( logName )

    for i in range(8):
        #kolumna i w tablicy sType
        sType1 = data1.sType[:, i]
        sType2 = data2.sType[:, i]

        # wybierz z sType indeksy niezerowych elementow z obu plików i wstaw do macierzy indexes
        indexes1 = np.argwhere(sType1 == 1)
        indexes2 = np.argwhere(sType2 == 1)
        #indexes = np.union1d( (indexes1), (indexes2) )

        # print(indexes)
        # Filter indexes so that we take into account only indexes regarding our event
        indexes1 = np.intersect1d(indexes1, np.arange(beg, end))
        indexes2 = np.intersect1d(indexes2, np.arange(beg, end))
        
        # try:
        #     sType = data.sType[indexes, i]
        # except IndexError:
        #     continue
        sType1 = data1.sType[indexes1, i]
        sConf1 = data1.sConf[indexes1, i]
        sSupType1 = data1.sSupType[indexes1, i]
        sValue1 = data1.sValue[indexes1, i]
        sRelDec1 = data1.sRelDec[indexes1, i]
        imageIndex1 = data1.imageIndex[indexes1]

        sType2 = data2.sType[indexes2, i]
        sConf2 = data2.sConf[indexes2, i]
        sSupType2 = data2.sSupType[indexes2, i]
        sValue2 = data2.sValue[indexes2, i]
        sRelDec2 = data2.sRelDec[indexes2, i]
        imageIndex2 = data2.imageIndex[indexes2]

        minorLocator = matplotlib.ticker.AutoMinorLocator()

        # Plot singValue vs. x_values
        p1 = plt.subplot(411)
        # domyslnie wykres dla wszystkich wartosci rysowany jest jednym przylozeniem "pisaka"
        # dlatego marker='.' i linestyle='none' zeby bylo widac nieciaglasci miedzy fragmentami
        # p1.plot(imageIndex, sValue, color=colorsDict[i], marker='.', markersize=3, linestyle='none')
        # p1.plot(x_values, sValue, color=colorsDict[i], lw=2, linestyle='-')
        p1.set_title('Sign Value')
        p1.plot(imageIndex1, sValue1, color='b', marker=',', markersize=1, linestyle='none')
        p1.plot(imageIndex2, sValue2, color='r', marker='.', markersize=0.5,  linestyle='none')

        # Plot singConfidence vs. imageIndex
        p2 = plt.subplot(412)
        p2.set_title('Sign Confidence')
        p2.plot(imageIndex1, sConf1, color='b', marker=',', markersize=1, linestyle='none')
        p2.plot(imageIndex2, sConf2, color='r', marker='.', markersize=0.5, linestyle='none')
        plt.ylim(0.4, 1.05)
        # plt.grid(True, which='both', alpha=0.5)

        # Plot signSuppl vs. imageIndex
        p3 = plt.subplot(413)
        p3.set_title('Supplementary Type')
        p3.plot(imageIndex1, sSupType1, color='b', marker=',', markersize=1, linestyle='none')
        p3.plot(imageIndex2, sSupType2, color='r', marker='.', markersize=0.5, linestyle='none')

        # Plot signRelevantDecision vs. imageIndex
        p4 = plt.subplot(414)
        p4.set_title('Relevant Decision')
        p4.plot(imageIndex1, sRelDec1, color='b', marker=',', markersize=1, linestyle='none')
        p4.plot(imageIndex2, sRelDec2, color='b', marker='.', markersize=0.5, linestyle='none')

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig(os.path.join(path, f'{row+1}_{logName}' +'.png'))
    # plt.show()
    print("\n Finished \n")
    plt.close()