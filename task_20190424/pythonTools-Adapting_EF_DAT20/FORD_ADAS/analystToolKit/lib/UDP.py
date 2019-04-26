import csv
import os
import sys
import pickle
import select
import socket
import subprocess
import argparse

from threading import Thread, Timer
from time import strftime


def validate_UDP_PORT(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setblocking(False)
        sock.bind((ip, port))
        sock.close()
        return True
    except:
        return False


class dataBuffers:
    def __init__(self, outputPath):
        self.buffers = {}
        self.timers = {}

        self.outputPath = outputPath

    def appendData(self, data):
        func = data[0]
        bufferName = func

        if bufferName in self.timers.keys():
            self.timers[bufferName].cancel()
            self.timers[bufferName].join()
        if bufferName in self.buffers.keys():
            self.buffers[bufferName].append(data)
            self.timers[bufferName] = Timer(BUFFER_TIMEOUT, self.flushData, (bufferName,))
            self.timers[bufferName].start()
            if len(self.buffers[bufferName]) >= BUFFER_MEMORY_SIZE:
                self.flushData(bufferName)
        else:
            self.buffers[bufferName] = [data]
            self.timers[bufferName] = Timer(BUFFER_TIMEOUT, self.flushData, (bufferName,))
            self.timers[bufferName].start()

    def flushData(self, bufferName):
        os.system('module load openblas/dynamic/0.2.14')
        os.system('module load python/2.7.11')

        if bufferName in self.buffers.keys():
            func = self.buffers[bufferName][0][0]
            header = self.buffers[bufferName][0][3]

            if not os.path.isdir(self.outputPath):
                os.mkdir(self.outputPath)

            outCsvName = os.path.join(self.outputPath, func + '-EF_{}.csv'.format(strftime("%d-%m-%Y")))

            if not os.path.isfile(outCsvName):
                csvfile = open(outCsvName, 'w')
                fcsvwriter = csv.DictWriter(csvfile, header, extrasaction='ignore', dialect='excel')
                fcsvwriter.writeheader()
            else:
                csvfile = open(outCsvName, 'a')
                fcsvwriter = csv.DictWriter(csvfile, header, extrasaction='ignore', dialect='excel')

            for data in self.buffers[bufferName]:
                dataDict = data[4]
                fcsvwriter.writerow(dataDict)

            csvfile.close()
            self.buffers.pop(bufferName, None)

        if bufferName in self.buffers.keys():
            t = self.timers.pop(bufferName, None)
            t.cancel()
            t.join()

    def flushAllData(self):
        keys = self.buffers.copy().keys()
        for buffer in keys:
            self.flushData(buffer)


class serverUDP():
    def __init__(self, outputPath ,UDP_PORT):
        self.rawData = []
        self.buffers = dataBuffers(outputPath)
        self.outputPath = outputPath

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setblocking(False)
        self.sock.bind((UDP_IP, UDP_PORT))

        print('*** Starting UDP server. ***')
        print('\tIP: ' + UDP_IP)
        print('\tPORT: ' + str(UDP_PORT))
        print('\tListening...\n')

        self.runFlag = True
        self.run = Thread(target=self.reciveLoop, args=())
        self.run.start()

        self.runAppendData = True

        self.watchdogTimer = Timer(BUFFER_TIMEOUT, self.watchDog)
        self.watchdogTimer.start()

        try:
            while self.runAppendData:
                if self.rawData:
                    data = pickle.loads(self.rawData.pop(0))
                    try:
                        self.buffers.appendData(data)
                    except:
                        print('Error while appending ' + data[0] + 'data',  sys.exc_info()[0])
        except KeyboardInterrupt:
            self.stopServer()

    def reciveLoop(self):
        os.system('module load openblas/dynamic/0.2.14')
        os.system('module load python/2.7.11')

        while self.runFlag:
            dataReady = select.select([self.sock], [], [], 10)
            if dataReady[0]:
                rawData, addr = self.sock.recvfrom(UDP_BUFFER_SIZE)
                self.rawData.append(rawData)

    def stopServer(self):
        print('\n*** Stopping UDP server ***\n\tPlease wait...')
        self.runFlag = False
        self.run.join()
        self.runAppendData = False
        self.sock.close()
        self.buffers.flushAllData()
        print('*** UDP server down ***')


    def watchDog(self):
        os.system('module load slurm')
        status, output = subprocess.getstatusoutput('squeue -rh -u $(id -un) | wc -l')
        if output == '0':
            self.stopServer()
        else:
            self.watchdogTimer = Timer(BUFFER_TIMEOUT, self.watchDog)
            self.watchdogTimer.start()



def sendData(ip, port, data):
    rawData = pickle.dumps(data)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(rawData, (ip, port))


UDP_IP = '10.195.186.39'  # pedro
# UDP_IP = '127.0.0.1' #local
UDP_BUFFER_SIZE = 8192

BUFFER_MEMORY_SIZE = 1000
BUFFER_TIMEOUT = 30


def cancelJobs():
    os.system('module load slurm')
    while 1:
        status, output = subprocess.getstatusoutput('squeue -rht R -u $(id -un)')
        jobid= output[8:16]
        if input('Cancel jobs..id: ' + jobid + '? (y/n)\n') == 'y':
            os.system('scancel ' + jobid)
            break


def main():
    parser = argparse.ArgumentParser(description='UDP server to recive efs output.')
    parser.add_argument('output', help='Output path to save')
    parser.add_argument('port', type=int, help='Soft version to resim with')


    args = parser.parse_args()
    args.output = os.path.join(os.path.abspath(args.output))
    if not validate_UDP_PORT(UDP_IP, args.port):
        print('Error: Port not valid.')
        cancelJobs()
        return


    if args.port:
        serverUDP(args.output, args.port)
    else:
        print('Port 0, local save.')

if __name__ == '__main__':
    main()
