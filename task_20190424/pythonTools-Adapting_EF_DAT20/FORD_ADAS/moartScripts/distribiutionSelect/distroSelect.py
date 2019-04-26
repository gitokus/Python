import csv
import os
import sys
import math

from datetime import datetime
from random import randint


def main():
    config = openConfig()

    statsCsvName = input('Enter path to STATS-EF.csv file:\n')
    logList = openStats(statsCsvName, config['header'])

    totalLen = calculateLen(logList, config['lenMode'])
    print('Total length is {} {}.'.format(totalLen, config['lenMode']))
    print('Desired distribution length: {} {}'.format(config['len'], config['lenMode']))

    if config['len'] > totalLen:
        print('WARNING: Desirable distribiution length ({}) is greater then total lenght!'
              '\n\t\t Overwriting config...'.format(config['len']))
        config['len'] = totalLen


    if config['dayTimeCondition'] == 'On':
        dayTimeKeys = ['Day', 'Dusk', 'Night']
        dayTimeRatio = [config['dayTimeDay'], config['dayTimeDusk'], config['dayTimeNight']]
        if not sum(dayTimeRatio) == 1:
            sys.exit('ERROR: Wrong dayTime split, must sum to 1.')
    else:
        dayTimeKeys = [None]
        dayTimeRatio = [1.]

    if  config['roadTypeCondition'] == 'On':
        roadTypeKeys = ['Highway', 'City', 'OtherRoadType']
        roadTypeRatio = [config['roadTypeCity'], config['roadTypeHighway'], config['roadTypeOther']]
        if not sum(roadTypeRatio) == 1:
            sys.exit('ERROR: Wrong dayTime split, must sum to 1.')
    else:
        roadTypeKeys = [None]
        roadTypeRatio = [1.]

    print('Generating distribiution...')
    distribiution = []

    info = [('Origin file: {}\n'
             'Total length is {} {}.\n'
             'Desired distribution length: {} {}').format(statsCsvName,
                                                       totalLen, config['lenMode'],
                                                       config['len'], config['lenMode'])]

    for dayTimeKey, dayTimeRat in zip(dayTimeKeys, dayTimeRatio):
        for roadTypeKey, roadTypeRat in zip(roadTypeKeys, roadTypeRatio):
            subList = logList
            if dayTimeKey is not None:
                subList = subListFromCondition(subList, dayTimeKey, 0.01, 1)
            if roadTypeKey is not None:
                subList = subListFromCondition(subList, roadTypeKey, 0.01, 1)

            conditionsKeys = [c.strip('cc_') for c in config.keys() if 'cc_' in c]
            for conditionKey in conditionsKeys:
                subList = subListFromCondition(subList, conditionKey,
                                               config['cc_' + conditionKey]['minVal'],
                                               config['cc_' + conditionKey]['maxVal'])

            subDistribiution = []
            while calculateLen(subDistribiution, config['lenMode']) < math.ceil(config['len'] * dayTimeRat * roadTypeRat):
                if len(subList):
                    subDistribiution.append(subList.pop(randint(0, len(subList)-1)))
                else:
                    break

            subInfo = """Subdistribiution for
\tDayTime: {}
\tRoadType: {}
\tCustom conditions:\n{}
\tFound: {}/{} {}""".format(dayTimeKey, roadTypeKey,
                '\n'.join(['\t\t{}: {}-{}'.format(conditionKey, config['cc_' + conditionKey]['minVal'],
                    config['cc_' + conditionKey]['maxVal']) for conditionKey in conditionsKeys]),
                calculateLen(subDistribiution, config['lenMode']), math.ceil(config['len'] * dayTimeRat * roadTypeRat),
                    config['lenMode'])

            print(subInfo)
            info.append(subInfo)

            distribiution += subDistribiution

    print('Saving results...')

    nowStr = datetime.strftime(datetime.now(), '%d-%m-%y_%H-%M')
    config['header'].insert(config['header'].index('City') + 1, 'OtherRoadType')
    with open(statsCsvName[:-4] + '-subDist-{}.csv'.format(nowStr), 'w', newline='') as outputFile:
        writer = csv.DictWriter(outputFile, config['header'], extrasaction='ignore', dialect='excel')
        writer.writeheader()
        writer.writerows(distribiution)
    with open(statsCsvName[:-4] + '-subDist-{}.txt'.format(nowStr), 'w', newline='') as outputTxt:
        outputTxt.writelines('\n'.join(info))


def openConfig(configPath='config'):
    if os.path.isfile(configPath):
        try:
            with open(configPath, 'r') as configFile:
                configLines = configFile.read().splitlines()

            config = {}
            for line in configLines:
                if line.startswith('#') or line == '':
                    continue
                else:
                    key = line.split('=')[0].strip(' ')
                    value = line.split('=')[1].strip(' ')
                    config[key] = value

            config['header'] = config['header'].split(',')
            for key in config.keys():
                if key.startswith('cc_'):
                    minVal, maxVal = [float(v.strip(' ')) for v in config[key].split(',')]
                    config[key] = {'minVal': minVal,
                                   'maxVal': maxVal}
                else:
                    try:
                        config[key] = float(config[key])
                    except:
                        pass

            return config
        except:
            sys.exit('ERROR: Cannot read config file')

    else:
        configPath = input('Enter path to config file:\n')
        openConfig(configPath)


def openStats(filePath, header):
    print('Loading .csv file data...')
    logList = []
    with open(filePath) as csvfile:
        reader = csv.DictReader(csvfile, header)
        for row in reader:
            if row['Status'] == 'Available':
                for key in row.keys():
                    try:
                        row[key] = round(float(row[key]), 4)
                    except:
                        pass
                row['OtherRoadType'] = min((max(0., 1. - (row['Highway'] + row['City'])), 1.))
                logList.append(row)
    return logList


def calculateLen(iterable, mode):
    distance = 0
    for i in iterable:
        if isinstance(i, dict):
            if mode=='km':
                distance += i['Distance']
            elif mode=='logs':
                distance += 1
            elif mode=='minutes':
                distance += i['Duration']/60
            else:
                raise Exception('Unknown len mode')

        elif isinstance(i, list):
            distance += i[1]
    return round(distance, 4)


def subListFromCondition(logList, key, lowerLimit, upperLimit):
    subList = []
    for log in logList:
        if lowerLimit <= log[key] <= upperLimit:
            subList.append(log)
    return subList


if __name__ == '__main__':
    main()

