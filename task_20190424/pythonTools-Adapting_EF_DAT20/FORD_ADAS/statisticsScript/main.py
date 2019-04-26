import os
import argparse

from tqdm import tqdm
from statisticsScript.comperator import Comperator
from statisticsScript.stats import StatsGenerator

def main():
    comp = Comperator()
    comp.load_config()

    stats = StatsGenerator()

    parser = argparse.ArgumentParser(description='Runs statistics on list of files (mat+dat)',
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('input', help='Input path for files list or folder')
    parser.add_argument('-o', dest='output', default='',
                        help='Output path for results (default is input)')
    parser.add_argument('-afl', dest='afl_filters', default='',
                        help=comp.get_filters_list('afl', True))
    parser.add_argument('-lks', dest='lks_filters', default='',
                        help=comp.get_filters_list('lks', True))
    parser.add_argument('-tsr', dest='tsr_filters', default='',
                        help=comp.get_filters_list('tsr', True))
    parser.add_argument('-obj', dest='obj_filters', default='',
                        help=comp.get_filters_list('obj', True))
    parser.add_argument('-d', dest='debug', action='store_true',
                        help='Add debug option')

    args = parser.parse_args()
    args.input = os.path.abspath(args.input)
    if args.output == '':
        args.output = os.path.dirname(args.input)
    else:
        args.output = os.path.abspath(args.output)
    if not os.path.isdir(args.output):
        os.mkdir(args.output)

    if os.path.isdir(args.input):
        files_paths = {os.path.join(args.input, os.path.splitext(file)[0]) for file in os.listdir(args.input)}
    else:
        with open(args.input, 'r') as in_file:
            files_paths = in_file.read().splitlines()

    print('\nRunning comparison script...')
    root_paths = set()
    for file_path in tqdm(files_paths, desc='Files'):
        if os.path.isfile(file_path + '.dat') and os.path.isfile(file_path + '.mat'):
            root_paths.add(os.path.dirname(file_path))
            comp.load_dat(file_path + '.dat')
            comp.load_mat(file_path + '.mat')
            for func in ['afl', 'lks', 'tsr', 'obj']:
                s = eval('args.{}_filters'.format(func))
                if s != '':
                    comp.run(func, [int(f) for f in s.split(',')], print_results=args.debug)

    print('\nRunning summary stats...')
    for root in tqdm(root_paths):
        stats.load_data(root)
        stats.run()
        stats.save_data(args.output)
    print('Job done!')


if __name__ == '__main__':
    main()
