import argparse
import os
import time
import subprocess


def main():
    try:
        os.system('module load slurm')
        os.system('module load projects/ford-adas')
    except:
        pass
    parser = argparse.ArgumentParser(description='Automatically start continuous resim on as many logs as possible.')
    parser.add_argument('input', help='Input path for dvls list or folder with dvls')
    parser.add_argument('soft', help='Soft version to resim with')

    parser.add_argument('-o', dest='output', default=os.getcwd(),
                        help='Output path for resim (default is cwd)')
    parser.add_argument('-s', dest='step', type=int, default=2, help='Resim step (2 by default)')
    parser.add_argument('-hi', dest='history', type=int, default=0,
                        help='History to find if input is list of logs (0 by default)\n'
                             'Available when resimulating list of files')
    parser.add_argument('-t', dest='tracklets', action='store_true',
                        help='Add -notracklets option to resim step 2')
    parser.add_argument('-cf', dest='iters', type=int, default=0,
                        help='Check output dir for complete resim and rerun if neccessery (0 by default)')
    parser.add_argument('-n', dest='nFiles', default='', help='Resim nfiles parameter (empty by default)')
    parser.add_argument('-ovr', dest='overrideCalFile', action='store_true',
                        help='Use parameters stored in override.cal file' +
                             ' (the .cal file must be placed in the working directory)')

    args = parser.parse_args()
    args.input = os.path.abspath(args.input)
    args.output = os.path.abspath(args.output)

    logList = []
    if os.path.isdir(args.input):
        content = os.listdir(args.input)
        onlyfiles = set([os.path.splitext(f)[0] for f in content
                         if os.path.isfile(os.path.join(args.input, f))])
        for each in onlyfiles:
            if args.step != 2:
                extList = ['.mudp', '.dvl']
            else:
                extList = ['_alt.avi', '.avi', '.mudp', '.tapi', '.ffs', '.dvl']
            for ext in extList:
                if not each + ext in content:
                    break
            else:
                logList.append(os.path.join(args.input, each + '.dvl'))
    else:
        with open(args.input, 'r') as inputFile:
            logList = sorted(inputFile.read().splitlines())

        if args.history:
            logListHist = []
            param = args.history
            for log in logList:
                for i in range(-param, 1):
                    newLog = log[:-7] + str(int(log[-7:-4]) + i).zfill(3) + '.dvl'
                    if newLog not in logListHist:
                        logListHist.append(newLog)
            logList = logListHist

        logListFileCheck = []
        for log in logList:
            if not os.path.isfile(log) or log in logListFileCheck:
                continue
            logName = os.path.splitext(os.path.basename(log))[0]
            logDir = os.path.dirname(log)
            if args.step != 2:
                extList = ['.mudp', '.dvl']
            else:
                extList = ['_alt.avi', '.avi', '.mudp', '.tapi', '.ffs', '.dvl']
            for ext in extList:
                if not os.path.isfile(os.path.join(logDir, logName + ext)):
                    break
            else:
                logListFileCheck.append(log)
        logList = logListFileCheck

    logList = checkResimOutput(logList, args)

    if logList:
        autoResimListName = writeAutoResimList(logList)
        submitResim(autoResimListName, args)

        if args.iters:
            print('Entering check file state\nIn this state, status of files in output dir\n'
                  'as well as slurm jobs will be monitored.')
        while args.iters:
            status, output = subprocess.getstatusoutput('squeue -rh -u $(id -un) | wc -l')
            print('Remaining slurm jobs: {}'.format(output))
            if output == '0':
                logList = checkResimOutput(logList, args)
                if logList:
                    autoResimListName = writeAutoResimList(logList)
                    submitResim(autoResimListName, args)
                else:
                    print('All files present\nFinishing...')
                    break
                args.iters -= 1
            time.sleep(300)
    else:
        print('All files present\nFinishing...')


def getFirst(logList):
    firstLogs = []
    for log in logList:
        prev = log[:-7] + str(int(log[-7:-4]) - 1).zfill(3) + '.dvl'
        if not prev in logList:
            firstLogs.append(log)
    return firstLogs


def writeAutoResimList(logList):
    logList = getFirst(logList)
    folder = os.path.join(os.getcwd(), 'autoResimList')
    if not os.path.isdir(folder):
        os.mkdir(folder)
    name = 'autoResimList_1'
    while name in os.listdir(folder):
        name = name.split('_')[0] + '_' + str(int(name.split('_')[1]) + 1)
    print('Creating new list...({})'.format(name.split("_")[1]))
    with open(os.path.join(folder, name), 'w') as autoList:
        for log in logList:
            autoList.write(os.path.abspath(log + os.linesep))
    return os.path.join(folder, name)


def submitResim(autoResimListName, args):
    opts = ''
    if args.tracklets:
        opts += ' -T'
    if args.overrideCalFile:
        opts += ' -O'
    if args.nFiles != '':
        opts += ' -c ' + args.nFiles
    opts += ' -N'

    command = 'submit_list.sh -l {} -s {} -o {} -C {}{}'.format(
        autoResimListName, args.step, args.output, args.soft, opts
    )
    print('executing: {}'.format(command))
    os.system(command)


def checkResimOutput(logList, args):
    try:
        versions = '/mnt/usinkok/projects/FORD-ADAS/7-Tools/ford-adas-scripts/resim/etc/configs'
        if args.step == 2:
            with open(os.path.join(versions, args.soft)) as configFile:
                config = configFile.read().splitlines()
                for line in config:
                    if 'vistag' in line:
                        folderName = line.split('=')[1]

        folderPath = os.path.join(args.output, folderName)
        if os.path.isdir(folderPath):
            resimFiles = os.listdir(folderPath)

            notDoneLogs = []
            for log in logList:
                name = os.path.splitext(os.path.basename(log))[0] + '_' + folderName
                if not (name + '.dvl' in resimFiles
                        and os.stat(os.path.join(folderPath, name + '.dvl')).st_size > 1000
                        and name + '.mudp' in resimFiles
                        and os.stat(os.path.join(folderPath, name + '.mudp')).st_size > 1000):
                    notDoneLogs.append(log)
        else:
            notDoneLogs = logList

        print('Number of missing resim files: {}'.format(len(notDoneLogs)))
        return notDoneLogs
    except:
        print('Cannot check files')
        return logList


if __name__ == '__main__':
    main()
