import os
import argparse

from shutil import copyfile


def finder(inputTxt, inputReference, outputPath, exts, mode, hist):
    logs = []
    with open(inputTxt, 'r') as txtFile:
        text = txtFile.read()
    for log in text.split('\n'):
        if len(log) > 0:
            logs.append(str(log).translate({ord(c):'' for c in ' \n\t\r'}))
    logs = list(set(logs))

    logsHist = []
    for log in logs:
        no = int(log[-3:])
        for i in [j for j in range(no - hist, no + 1) if j > 0]:
            newLog = log[:-3] + str(i).zfill(3)
            if newLog not in logsHist:
                logsHist.append(newLog)
    logs = logsHist

    logsExts = []
    for log in logs:
        for ext in exts:
            newLog = os.path.splitext(log)[0] + ext
            if newLog not in logsExts:
                logsExts.append(newLog)
    logs = logsExts

    filesToSearchCount = len(logs)
    checkedFiles = 0
    foundFiles = 0

    with open(os.path.join(outputPath, 'searchReport.txt'), 'w') as reportFile:
        reportFile.write('***Found files:***\n\n')

    try:
        if os.path.isfile(inputReference):
            with open(inputReference, 'r') as referenceFile:
                for line in referenceFile:
                    refPath = os.path.abspath(line.strip('\n'))
                    refName = os.path.basename(refPath)
                    checkedFiles += 1
                    if refName in logs:
                        try:
                            foundFiles += 1
                            if mode == 'report':
                                print('Saving path: ' + refName)
                            if mode == 'link':
                                print('Linking: ' + refName)
                                os.link(refPath, os.path.join(outputPath, refName))
                            if mode == 'copy':
                                print('Copying: ' + refName)
                                copyfile(refPath, os.path.join(outputPath, refName))
                            with open(os.path.join(outputPath, 'searchReport.txt'), 'a') as reportFile:
                                reportFile.write('{}\n'.format(refPath))
                            logs.remove(refName)
                        except:
                            print('Error handaling match!')
                    print('Checked files: ' + str(checkedFiles) +
                          '\tFound: ' + str(foundFiles) + '/' + str(filesToSearchCount))
                    if len(logs) == 0:
                        print('All files found.')
                        break
        else:
            for root, dirnames, filenames in os.walk(inputReference):
                matches = list(set(logs) & set(filenames))
                checkedFiles += len(filenames)
                for match in matches:
                    try:
                        foundFiles += 1
                        if mode == 'report':
                            print('Saving path: ' + match)
                        if mode == 'link':
                            print('Linking: ' + match)
                            os.link(os.path.join(root, match), os.path.join(outputPath, match))
                        if mode == 'copy':
                            print('Copying: ' + match)
                            copyfile(os.path.join(root, match), os.path.join(outputPath, match))
                        with open(outputPath + os.sep + 'searchReport.txt', 'a') as reportFile:
                            reportFile.write('{}\n'.format(os.path.join(root, match)))
                        logs.remove(match)
                    except:
                        print('Error handaling match!')
                print('Checked files: ' + str(checkedFiles) +
                      '\tFound: ' + str(foundFiles) + '/' + str(filesToSearchCount))
                if len(logs) == 0:
                    print('All files found.')
                    break
    except KeyboardInterrupt:
        print('Abroting search')
    finally:
        if len(logs) > 0:
            with open(os.path.join(outputPath, 'searchReport.txt'), 'a') as reportFile:
                reportFile.write('\n\n***Missing files:***\n\n')
                for log in sorted(logs):
                    reportFile.write(log + '\n')


def main():
    parser = argparse.ArgumentParser(description='Search for files in input list.\nOutput could be report, copy or link.\n'
                                                 'User need to specify root for search.\nAlso specified extensions can be used.')
    parser.add_argument('inputList', help='Input file path for files list')
    parser.add_argument('mode', default='report', help='Mode of output\nreport, link or copy')
    parser.add_argument('reference', help='Input list or root for recursive search')

    parser.add_argument('-e', dest='extensions', default='.dvl,.mudp,.ffs,.tapi,.avi', help='Extensions to search for (full logs by default)')
    parser.add_argument('-o', dest='output', default=os.getcwd(), help='Output path to write to (cwd by default)')
    parser.add_argument('-hi', dest='history',type=int, default=0, help='History of given logs to find')

    args = parser.parse_args()
    args.inputList = os.path.abspath(args.inputList)
    args.reference = os.path.abspath(args.reference)
    args.output = os.path.abspath(args.output)
    args.extensions = args.extensions.split(',')

    if '.avi' in args.extensions:
        args.extensions.append('_alt.avi')

    if not os.path.isdir(args.output):
        os.mkdir(args.output)

    finder(args.inputList, args.reference, args.output, args.extensions, args.mode, args.history)


if __name__ == '__main__':
    main()