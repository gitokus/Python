import argparse
from argparse import RawTextHelpFormatter
import os
import read_det


def main():
    parser = argparse.ArgumentParser(
        description='''Parse dtf logs. Saving to pickle file.
        Example usage:
            python3 read_det_console.py test\GrabIndex_mess.rtf test
            python3 read_det_console.py -d test\GrabIndex_mess.rtf .''',
        formatter_class=RawTextHelpFormatter
    )

    parser.add_argument('input', help='Input log file path')
    parser.add_argument('output', help='Output path to write result files.')
    parser.add_argument('-m', dest='map', default='memory_map.csv', help=
    '''Memory map file. Supported memory types: float32, int16. Memory map file is csv file. Default file is memory_map.csv.''')
    parser.add_argument('-d', dest='details', action='store_true',
                        help='Save reports with details informations. ')

    args = parser.parse_args()
    args.input = os.path.abspath(args.input)
    args.output = os.path.abspath(args.output)
    args.map = os.path.abspath(args.map)

    basename = os.path.basename(args.input)
    file_name, _ = os.path.splitext(basename)

    output_file = os.path.join(args.output, file_name)

    read_det.to_pickle(args.input, output_file, args.map, args.details)


if __name__ == '__main__':
    main()
