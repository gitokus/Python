import numpy as np
import os

def compareSignal(mat1, mat2, signalPath, column, output = False):
    try:
        result = []
        mat1Indexes = mat1['mudp']['vis']['vision_road_info']['imageIndex']
        mat2Indexes = mat2['mudp']['vis']['vision_road_info']['imageIndex']

        tempPath = signalPath[:]
        signal1 = mat1
        signal2 = mat2
        while tempPath:
            subName = tempPath.pop(0)
            if type(subName) == int:
                signal1 = signal1[:,subName]
                signal2 = signal2[:,subName]
            else:
                signal1 = signal1[subName]
                signal2 = signal2[subName]

        if type(signal1) == np.ndarray and len(signal1.shape) == 2:
            result = compareSignal(mat1, mat2, signalPath + [column], column, output)
        else:
            minIndex = min(mat1Indexes[0], mat2Indexes[0])
            maxIndex = max(mat1Indexes[-1], mat2Indexes[-1])

            if maxIndex < minIndex:
                maxIndex += 65535
                indexRange = range(minIndex, maxIndex + 1, 2)
                indexRange = [i if i <65537 else i - 65535 for i in indexRange]
            else:
                indexRange = range(minIndex, maxIndex + 1, 2)

            s1 = np.ma.masked_array(indexRange, [0 if x in mat1Indexes else 1 for x in indexRange])
            s1[~s1.mask] = signal1

            s2 = np.ma.masked_array(indexRange, [0 if x in mat2Indexes else 1 for x in indexRange])
            s2[~s2.mask] = signal2

            if output:
                name= os.path.splitext(mat1['mudp']['bfname'])[0] + '_' + '-'.join([str(e) for e in signalPath])
                with open(name + '.csv', 'w') as output:
                    output.write('General info:\n')
                    output.write('signal:,' + '-'.join([str(e) for e in signalPath]) + '\n')
                    output.write('name:,,' + os.path.splitext(mat1['mudp']['bfname'])[0] + ',,'
                                 + os.path.splitext(mat2['mudp']['bfname'])[0] + '\n')
                    output.write('range:,' + str(len(indexRange)) + '\n')
                    output.write('mat1 drops:,' + str(len(s1[s1.mask])) + '\n')
                    output.write('mat2 drops:,' + str(len(s2[s2.mask])) + '\n')
                    compare = (s1 == s2)
                    output.write('matches:,' + str(len(np.where(compare[~compare.mask] == True)[0])) + '\n')
                    output.write('mismatches:,' + str(len(np.where(compare[~compare.mask] == False)[0])) + '\n')
                    output.write('\nDetail info:\n')
                    for i in range(len(indexRange)):
                        output.write('index:,' + str(indexRange[i]) + ',mat1:,' + str(s1[i]) + ',mat2:,' + str(s2[i]) +
                                     ',match:,' + str((compare)[i]) + '\n')
            result = (s1, s2)

        return result
    except:
        return None