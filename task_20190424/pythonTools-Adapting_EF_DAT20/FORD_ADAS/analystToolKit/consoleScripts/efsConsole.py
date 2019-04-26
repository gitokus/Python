import os
import sys
import time
import argparse

#tymczasowo sciezka do lokalnych wersji
sys.path.insert(0, '../../')


from datetime import datetime
try:
    from delphiTools3 import base as dt
except:
    moduleSplitPath = os.path.normpath(os.path.realpath(__file__)).split(os.sep)
    projectSplitPath = moduleSplitPath[:-3]
    projectPath = os.path.normpath(os.sep.join(projectSplitPath))
    if os.path.isdir(os.path.join(projectPath, 'delphiTools3')):
        sys.path.append(projectPath)
    else:
        sys.path.append('/mnt/usinkok/users/bjzpp8/home/pythonTools/FORD_ADAS')
    from delphiTools3 import base as dt

from analystToolKit.lib.efsClasses import aflEfsClass
from analystToolKit.lib.efsClasses import lksEfsClass
from analystToolKit.lib.efsClasses import objEfsClass
from analystToolKit.lib.efsClasses import tsrEfsClass
from analystToolKit.lib.efsClasses import statsEFClass
from analystToolKit.lib.efsClasses import dvlobjEfsClass
from analystToolKit.lib.efsClasses import failsafesEfsClass
from analystToolKit.lib.efsClasses import genEFClass
from analystToolKit.lib import UDP

statsHeader = ['LogName',
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


def openMat(path, dat2p0):
    try:
        print('\nExtracting {}...'.format(os.path.basename(path)))
        print(path)
        mat = dt.loadmat(path, variableName='mudp', sort=True, reBarrierMarge=False, dat2p0=dat2p0)
        if dat2p0:
            if not (len(mat['mudp']['vis']['vision_traffic_sign_info']['tsrInfo']['imageIndex'])):
                print('Mat corrupted!')
                return
        else:
            if not len(mat['mudp']['vis']['vision_function_info']['imageIndex']):
                print('Mat corrupted!')
                return
        return mat
    except Exception as E:
        print('Error while loading {}!'.format(os.path.basename(path)), '\n', E )
        return


def main():
    aflEventFinder = aflEfsClass.aflEFs()
    lksEventFinder = lksEfsClass.lksEFs()
    objEventFinder = objEfsClass.objEFs()
    tsrEventFinder = tsrEfsClass.tsrEFs()
    dvlobjEventFinder =dvlobjEfsClass.dvlobjEFs()
    failsafesEventFinder = failsafesEfsClass.failsafesEFs()
    genEventFinder = genEFClass.genEFs()

    statsEventFinder = statsEFClass.statsEF()
    efObjects = [aflEventFinder, lksEventFinder,
                 tsrEventFinder, objEventFinder, dvlobjEventFinder,
                 failsafesEventFinder, genEventFinder, statsEventFinder]

    parser = argparse.ArgumentParser(description='Runs eventFinders on list of mat files',
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('input', help='Input path for mat list')
    parser.add_argument('port', type=int, help='UDP port to send output (0 for local save)')
    parser.add_argument('-dat', dest='OpenMat', action='store_true',
                        help='Load DAT20 logs instead of CADS3.5')
    parser.add_argument('-o', dest='output', default=os.getcwd(),
                        help='Output path for results (default is cwd)')
    parser.add_argument('-d', dest='details', action='store_true',
                        help='Save reports per function with details informations')
    parser.add_argument('-ns', dest='nostats', action='store_true',
                        help='Do not run STATS ef on given input')
    parser.add_argument('-afl', dest='aflEfs', default='',
                        help='EFs List:\n' + '\n'.join([str(i)+": "+ef for
                                                        (i, ef) in enumerate(efObjects[0].getEFsList())]))
    parser.add_argument('-lks', dest='lksEfs', default='',
                        help='EFs List:\n' + '\n'.join([str(i) + ": " + ef for
                                                        (i, ef) in enumerate(efObjects[1].getEFsList())]))
    parser.add_argument('-tsr', dest='tsrEfs', default='',
                        help='EFs List:\n' + '\n'.join([str(i) + ": " + ef for
                                                        (i, ef) in enumerate(efObjects[2].getEFsList())]))
    parser.add_argument('-obj', dest='objEfs', default='',
                        help='EFs List:\n' + '\n'.join([str(i) + ": " + ef for
                                                        (i, ef) in enumerate(efObjects[3].getEFsList())]))
    parser.add_argument('-dvl', dest='dvlEfs', default='',
                        help='EFs List:\n' + '\n'.join([str(i) + ": " + ef for
                                                        (i, ef) in enumerate(efObjects[4].getEFsList())]))
    parser.add_argument('-fs', dest='fsEfs', default='',
                        help='EFs List:\n' + '\n'.join([str(i) + ": " + ef for
                                                        (i, ef) in enumerate(efObjects[5].getEFsList())]))
    parser.add_argument('-gen', dest='genEFs', default='',
                        help='EFs List:\n' + '\n'.join([str(i) + ": " + ef for
                                                        (i, ef) in enumerate(efObjects[6].getEFsList())]))

    args = parser.parse_args()
    args.input = os.path.abspath(args.input)
    args.output = os.path.abspath(args.output)
    if not os.path.isdir(args.output):
        os.mkdir(args.output)


    efsToRun = []
    for i, arg in enumerate([args.aflEfs, args.lksEfs, args.tsrEfs, args.objEfs, args.dvlEfs, args.fsEfs, args.genEFs]):
        efsToRun.append([k for (j, k) in enumerate(efObjects[i].getEFsList()) if str(j) in arg.split(',')])
    efsToRun.append([not args.nostats])

    try:
        with open(args.input, 'r') as openFile:
            matFiles = openFile.read().splitlines()
    except:
        print('Error in reading input file')
        return
    for i, filePath in enumerate(matFiles):
        if i > 0:
            print('\n*** More work? ***')


        if args.OpenMat:
            mat = openMat(filePath, dat2p0=True)
            dat2p0 = True
        else:
            mat = openMat(filePath, dat2p0=False)
            dat2p0 = False
        if mat:
            for j, efObj in enumerate(efObjects):
                efObj.loadmat(mat, dat2p0=dat2p0)
                efObj.run(efsToRun[j], args.details)
                efObj.save(args.output, UDP.UDP_IP, args.port)
        else:
            if not args.nostats:
                stats = os.path.join(args.output, 'STATS-EF_{}.csv'.format(datetime.now().strftime("%d-%m-%y")))
                if args.port == 0:
                    if not os.path.isfile(stats):
                        with open(stats, 'w') as s:
                            s.write(','.join(statsHeader) + '\n')
                    with open(stats, 'a') as s:
                        if os.path.isfile(filePath):
                            s.write('{},Corrupted\n'.format(os.path.basename(filePath)))
                        else:
                            s.write('{},Missing\n'.format(os.path.basename(filePath)))
                else:
                    if os.path.isfile(filePath):
                        UDP.sendData(UDP.UDP_IP, args.port, ['STATS', args.output, os.path.basename(filePath),
                                      statsHeader, {'LogName': os.path.basename(filePath), 'Status': 'Corrupted'}])
                        time.sleep(0.01)
                    else:
                        UDP.sendData(UDP.UDP_IP, args.port, ['STATS', args.output, os.path.basename(filePath),
                                      statsHeader, {'LogName': os.path.basename(filePath), 'Status': 'Missing'}])
                        time.sleep(0.01)

    print('\n*** Job\'s done! ***')
    return


if __name__ == '__main__':
    main()
