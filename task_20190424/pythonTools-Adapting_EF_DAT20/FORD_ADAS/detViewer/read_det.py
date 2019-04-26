import pandas as pd
import numpy as np
import pickle
import re
import struct
import os


def read_log(file_name: str) -> pd.DataFrame:
    print('[INFO]    Opening log file: %s' % file_name)
    with open(file_name, 'r') as file:
        # standard log pattern. Cleaning lines
        re_pattern = r'[0-9]+[\.,][0-9]+  \(..\)  .*\\par'
        lines = file.readlines()
        lines_log = [re.findall(re_pattern, l[:-1]) for l in lines]
        lines_log = [g[0][:-4] for g in lines_log if len(g) > 0]

        if len(lines_log) < 1 or len(lines_log[0]) < 1:
            raise Exception('EMPTY log - wrong file format')

        logs = pd.DataFrame({'log': lines_log})
        # extract data to columns time, action, channel, log; data and message in one column - log
        logs = logs.log.str.extract(
            '^(?P<time>[0-9]+[\.,][0-9]+)  (?P<action>.{4})  (?P<channel>.{5})  (?P<log>.*)',
            expand=True)
        logs.time = logs.time.str.replace(',', '.')

        # split value and message on '  ---  '
        value_message = logs.log.str.split('  ---  ', expand=True)
        value_message.columns = ['value', 'message']

        return pd.concat([logs, value_message], axis=1).drop('log', axis=1)


def _decode_int16(series: pd.Series) -> pd.Series:
    def decode(x):
        v = x.replace(' ', '')[6:-6]
        return struct.unpack('<H', bytes.fromhex(v))[0]
    return series.map(decode)


def _decode_float32(series: pd.Series) -> pd.Series:
    def decode(x):
        v = x.replace(' ', '')[4:-4]
        return struct.unpack('f', bytes.fromhex(v))[0]
    return series.map(decode)


def _decode_1(series: pd.Series) -> pd.Series:
    decode_dict = {
        'F0': 0,
        '69': 2,
        '96': 3
    }

    def decode(x):
        v = x.split('  ')[2]
        return decode_dict[v if v in decode_dict else 'F0']

    return series.map(decode)


_decode_functions = {
    'int16': _decode_int16,
    'float32': _decode_float32,
    'confLKA': _decode_1,
}


def get_dictionary(df: pd.DataFrame, memory_map: pd.DataFrame) -> dict:
    result_dict = {}
    for key, indexes in df.groupby('address').groups.items():
        if key in memory_map.index:
            memory_row = memory_map.loc[key]
            # print(key, ' ', memory_row['directory'])
            if memory_row['type'] in _decode_functions:
                to_save = df.loc[indexes]
                r = _decode_functions[memory_row['type']](to_save.value)
                result_dict[memory_row['directory']] = pd.DataFrame({'time': pd.to_numeric(to_save.time), 'value': r})
            else:
                print('[WARNING] Type %s is not supported. Variable %s' % (memory_row['type'], memory_row['directory']))
        else:
            print('[WARNING] Memory address %s not found in memory map file.' % key)
    return result_dict


def to_tree_dict(in_dict: dict) -> dict:
    result_dict = {}
    for key, values in in_dict.items():
        p = result_dict
        memory_map = key.split('.')
        for d in memory_map[:-1]:
            p = p.setdefault(d, {})
        p.setdefault(memory_map[-1], values.values)
    return result_dict


def save_pickle(df_dict: dict, filename: str):
    with open(filename, 'wb') as file:
        pickle.dump(df_dict, file)


def _extract_address_size(message_series: pd.Series) -> pd.DataFrame:
    # Mask - True value when message is request, false otherwise
    response_mask = message_series.str.contains('Request to Read').fillna(False).astype(bool)
    # set None when message is not response
    message_series.loc[~response_mask] = None

    # fill forward and backward messages when they describe the same memory and size
    message_series = message_series.fillna(method='ffill', limit=1)
    return message_series.str.extract(
        '^Request to Read Memory By Address (?P<address>[0-9A-F]x[0-9A-F]{8}), Size: (?P<size>[0-9A-F]x[0-9A-F]{4})',
        expand=True)


def get_response(df: pd.DataFrame):
    # assuming that response one log after request message
    request_array = df.message.fillna('').str.contains('Request to Read').values
    request_array_shifted = np.concatenate([[False], request_array[:-1]])
    address_size = _extract_address_size(df.message)[request_array_shifted]
    return pd.concat([df[request_array_shifted], address_size], axis=1)


def to_pickle(input_file: str, output_file_prefix: str, map_file: str, details: bool):
    map = pd.read_csv(map_file, index_col='memory')
    df = read_log(input_file)

    if details:
        print('[INFO]    Saving file: %s ' % (output_file_prefix + '_1.csv'))
        df.to_csv(output_file_prefix + '_1.csv')

    df = get_response(df).drop(['message', 'channel', 'action', 'size'], axis=1)

    if details:
        print('[INFO]    Saving file: %s ' % (output_file_prefix + '_2.csv'))
        df.to_csv(output_file_prefix + '_2.csv')

    df_dict = get_dictionary(df, map)
    df_dict = to_tree_dict(df_dict)

    print('[INFO]    Saving file: %s ' % (output_file_prefix + '.p'))
    save_pickle(df_dict, output_file_prefix + '.p')


if __name__ == "__main__":
    # WRITE EXAMPLE
    files = [
        os.path.join('test', 'log13_ME_N_a0.rtf'),
        os.path.join('test', 'log12_ME_N_a0.rtf'),
        os.path.join('test', 'log11_FORD_H_a0-FORD_N_a0-ME_N_a0-ME_H_a0.rtf'),
        os.path.join('test', 'log10_FORD_H_a0-FORD_N_a0-ME_NL_a0-ME_H_a0.rtf'),
        os.path.join('test', 'log9_FORD_N_a0.rtf'),
        os.path.join('test', 'log8_FORD_N_a0.rtf'),
        os.path.join('test', 'log7_FORD_N_a0-ME_N-a0.rtf'),
        os.path.join('test', 'log6_FORD_N_a0-FORD_N_conf-ME_N_a0.rtf'),
        os.path.join('test', 'log5_FORD_N_a0-FORD_N_conf-ME_N_a0.rtf'),
        os.path.join('test', 'log4_FORD_N_a0-ME_N_a0.rtf'),
        os.path.join('test', 'log3_FORD_N_a0-ME_N_a0.rtf'),
        os.path.join('test', 'log2_ME_N_a0.rtf'),
        os.path.join('test', 'log1_FORD_N_a0-ME_N_a0.rtf'),
        os.path.join('test', 'GrabIndex_mess.rtf')
    ]

    memory_map_file = 'memory_map.csv'
    memory_map = pd.read_csv(memory_map_file, index_col='memory')

    for f in files:
        to_pickle(f, f[:-4], memory_map_file, True)

    # READ EXAMPLE
    tests_files = [f[:-4] + '.p' for f in files]

    for f in tests_files:
        print('LOAD FILE: ', f)
        with open(f, 'rb') as file:
            log_dict = pickle.load(file)
            print(type(log_dict))

