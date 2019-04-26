import sys
#tymczasowo sciezka do lokalnych wersji
sys.path.insert(0, '../../')

from analystToolKit.lib.efsClasses import aflEfsClass
from analystToolKit.lib.efsClasses import lksEfsClass


class genEFs(aflEfsClass.aflEFs):
    def __init__(self):
        self.function = 'GEN'

    def ef_HighwayDetection(self, MAX_GAP=100, MIN_PEAKS=1):
        """
        HighwayDetection
        EF goes through mat indexes and check if HighwayDetection flag change comparing to previous index.
        If so, index is added to indexes list. EF finds only changes in HighwayDetection signal, so only frequent
        flickering is reported, constant detection is discarded (depends on groupIndexes params)

        :param MAX_GAP: maxGap parameters of groupIndexes() (see groupIndexes info)
        :param MIN_PEAKS: minPeaks parameters of groupIndexes() (see groupIndexes info)
        :return: EF gives back dict structure with data len and data itself
        """
        if self.dat2p0:
            highwayDetection = self.get_bit(
                self.mat["mudp"]["eyeq"]["Lights"]["vis_light_sensor_data_info"]["activeLightSensorInfo"]["light_Sensor_Detections_byte"],
                bit_number_from_right=1)
        else:
            highwayDetection = self.mat['mudp']['vis']['vision_active_light_sensor_info']['highwayDetected']

        data = []
        indexes = []
        for index in range(1, self.visLen):
            if not highwayDetection[index - 1] and highwayDetection[index] or \
                            highwayDetection[index - 1] and not highwayDetection[index]:
                indexes.append(index)

        data.append([self.groupIndexes(indexes, MAX_GAP, MIN_PEAKS), 'Highway detected', 'HD flag changed', -1])

        return {'len': len(data), 'data': data}

    def ef_UrbanArea(self, MAX_GAP=100, MIN_PEAKS=1):
        return super(genEFs, self).ef_UrbanArea()

    def ef_ApproachingJunction(self, MAX_GAP=0, MIN_PEAKS=1):
        return super(genEFs, self).ef_ApproachingJunction()

    def ef_ConstructionArea(self, MAX_GAP=0, MIN_PEAKS=1):
        return lksEfsClass.lksEFs.ef_ConstructionArea(self)

    def getEFsList(self):
        return sorted([f[3:] for f in dir(self) if f[:3] == 'ef_'
                       and not 'template' in f
                       and f in ['ef_HighwayDetection','ef_UrbanArea','ef_ApproachingJunction','ef_ConstructionArea']])
