import argparse
import json
import os
import matChecker.matwrapper as mw
import pandas as pd


def checkMatPath(mat_path, schema_path):
    return _checkMat(mw.MatWrapper.fromFile(mat_path), schema_path)


def checkMatDict(mat, schema_path):
    return _checkMat(mw.MatWrapper(mat), schema_path)


def _checkMat(mat, schema_path):
    schema = pd.read_csv(schema_path)

    dict_schema = {}
    for _, row in schema.iterrows():
        acc = dict_schema
        path_splited = row.path.split('.')
        for field in path_splited[:-1]:
            if field not in acc:
                acc[field] = {}
            acc = acc[field]
        acc[path_splited[-1]] = list(row[1:].iteritems())

    result = mat.checkSchema(dict_schema)
    df = pd.DataFrame(result)
    return df


def main():
    parser = argparse.ArgumentParser(
        description=''' ''',
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument('mat', help='Input mat file')
    parser.add_argument('schema', help='Input schema file')
    args = parser.parse_args()

    args.mat = os.path.abspath(args.mat)
    args.schema = os.path.abspath(args.schema)

    df = checkMatPath(args.mat, args.schema)

    result_path = os.path.splitext(args.mat)[0] + '_res.csv'
    df.to_csv(result_path)


if __name__ == '__main__':
    main()
