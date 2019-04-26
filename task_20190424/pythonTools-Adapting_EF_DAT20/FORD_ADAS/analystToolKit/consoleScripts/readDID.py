import delphiTools3.base as dtb
import numpy as np
import argparse


class Did:
    def __init__(self, name):
        self._name = name
        self._missing_messages = None
        self._did_array = None
        self._status = None

    def _get_DID_from_mat(self, mat, channel):
        """
        :param mat: loaded .mat file (dict)
        :param channel: INST-CAN channel (int)
        :return:
            * True if the DID was read correctly, otherwise False,
            * numpy array of integers,
            * set of IDs of missing messages (if the DID could not be read correctly due to missing messages on the
            specified channel.
        """
        raise Exception("Method _get_DID_from_mat must be implemented in inheriting class.")

    def read_DID_from_mat(self, mat, channel):
        self._status, self._did_array, self._missing_messages = self._get_DID_from_mat(mat, channel)

    def get_name(self):
        return self._name

    def get_result(self):
        return self._status, self._did_array, self._missing_messages
    
    
class DidDe00(Did):
    def __init__(self):
        super().__init__(name='DE00')

    def _get_DID_from_mat(self, mat, channel):
        missing_messages = set([])
        try:
            byte_0_to_7 = dtb.readFromDvlRaw(mat['dvlRaw'], channel, 0x7B0, lambda msg: msg[:8])[0][0]
        except IndexError:
            missing_messages.add(0x7B0)
        try:
            byte_8_to_15 = dtb.readFromDvlRaw(mat['dvlRaw'], channel, 0x7B1, lambda msg: msg[:8])[0][0]
        except IndexError:
            missing_messages.add(0x7B1)
        if len(missing_messages) == 0:
            byte_16_to_22 = np.uint8([0, 0, 0, 0, 0, 0, 0])
            byte_0_to_22 = np.concatenate((
                byte_0_to_7,
                byte_8_to_15,
                byte_16_to_22
            ))
            return True, byte_0_to_22, missing_messages
        else:
            return False, None, missing_messages


class DidDe04(Did):
    def __init__(self):
        super().__init__(name='DE04')

    def _get_DID_from_mat(self, mat, channel):
        missing_messages = set([])
        try:
            byte_0_to_7 = dtb.readFromDvlRaw(mat['dvlRaw'], channel, 0x7BD, lambda msg: msg[:8])[0][0]
        except IndexError:
            missing_messages.add(0x7BD)
        if len(missing_messages) == 0:
            return True, byte_0_to_7, missing_messages
        else:
            return False, None, missing_messages


class DIDReader:
    def __init__(self, uppercase):
        self._dids = []
        self._uppercase = uppercase

    def add_did(self, did):
        self._dids.append(did)

    def read_dids(self, mat, channel):
        for did in self._dids:
            print("reading " + did.get_name() + " ...")
            did.read_DID_from_mat(mat, channel)
            status, array, missing_messages = did.get_result()
            if status:
                print(self._array_to_hex_string(array))
            elif (not status) and len(missing_messages) > 0:
                print("Failed to read DID. Reason: the following messages are missing: " + self._set_to_hex_string(missing_messages))
            else:
                print("Failed to read DID. Reason unknown.")

    def _array_to_hex_string(self, array):
        out = ''
        for (index, value) in enumerate(array):
            if index == 0:
                out += self._int_to_hex_string(value)
            else:
                out += " " + self._int_to_hex_string(value)
        return out

    def _set_to_hex_string(self, set):
        out = ''
        for (index, value) in enumerate(sorted(set)):
            if index == 0:
                out += '0x' + self._int_to_hex_string(value)
            else:
                out += ', 0x' + self._int_to_hex_string(value)
        return out

    def _int_to_hex_string(self, number):
        if self._uppercase:
            return format(number, '02X')
        else:
            return format(number, '02x')


def get_CAN_channels(mat):
    return list(mat['dvlRaw']['can']['channels_present'])


def get_INST_CAN_version(mat):
    version_string = ''
    version_string += str(mat['dvlExt']['inst']['version']['host_instcan_ver_major'])
    version_string += '.'
    version_string += str(mat['dvlExt']['inst']['version']['host_instcan_ver_minor'])
    return version_string


def main():
    parser = argparse.ArgumentParser(description="Read DIDs from a .mat file. Currently supported DIDs: DE00, DE04. Checked with INST-CAN versions: v05.16.")
    parser.add_argument('input', help='Input .mat file.')

    parser.add_argument('-ch', dest='channel', default='all',
                        help='INST-CAN channel. Default value: "all" (the script checks all CAN channels searching for messages with required IDs).')
    parser.add_argument('-lwc', dest='lowercase', action='store_true',
                        help='Print in lowercase (e.g. "f7 f2 0a ..." instead of "F7 F2 0A ..."')
    args = parser.parse_args()

    mat = dtb.loadmat(args.input)
    reader = DIDReader(uppercase=(not args.lowercase))
    reader.add_did(DidDe00())
    reader.add_did(DidDe04())

    channels_to_check = []
    if args.channel == 'all':
        print("WARNING: all CAN channels are being checked. Please note that the results might not be correct.")
        channels_to_check = get_CAN_channels(mat)
    else:
        try:
            channels_to_check = [int(args.channel)]
        except ValueError:
            raise ValueError('channel must be an integer or "all"')

    for channel in channels_to_check:
        print("-" * 10)
        print("Checking channel " + str(channel))
        reader.read_dids(mat, channel)


if __name__ == "__main__":
    main()
