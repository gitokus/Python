import re
from collections import defaultdict

import pandas as pd
import numpy as np

import delphiTools3.base as dtb


def _construct_df(sub_mat, fields):
    if fields is None:
        dfs = {key: pd.DataFrame(item) for key, item in sub_mat.items()
               if not isinstance(item, dict)}
    else:
        dfs = {key: pd.DataFrame(sub_mat[key]) for key in fields
               if key in sub_mat and not isinstance(sub_mat[key], dict)}

    return pd.concat(dfs, axis=1).stack(level=0).unstack(level=1)


def checkGt(arr, cond):
    max_value = np.max(arr)
    return 'ok' if max_value <= cond else 'error' + ', %.02f >= %.02f' % (max_value, cond)


def checkLt(arr, cond):
    min_value = np.min(arr)
    return 'ok' if min_value >= cond else 'error' + ', %.02f <= %.02f' % (min_value, cond)


def checkDGt(arr, cond):
    max_value = np.max(np.diff(arr))
    return 'ok' if max_value <= cond else 'error' + ', %.02f >= %.02f' % (max_value, cond)


def checkDLt(arr, cond):
    min_value = np.min(np.diff(arr))
    return 'ok' if min_value >= cond else 'error' + ', %.02f <= %.02f' % (min_value, cond)


_checkDictionary = {
    "max": checkGt,
    "min": checkLt,
    "max_change_rate": checkDGt,
    "min_change_rate": checkDLt
}


class MatWrapper(object):

    def df(self, schema):
        def rec(data, sc):
            acc = dict()
            for key, item in sc.items():
                if isinstance(item, dict):
                    if key in data:
                        acc.update(rec(data[key], item))
                else:
                    acc[item] = data[key]
            return acc

        r = rec(self.mat, schema)
        dfs = {key: pd.DataFrame(data) for key, data in r.items()}
        return pd.concat(dfs, axis=1).stack(level=0).unstack(level=1)

    def find(self, pattern):
        name_dict = defaultdict(int)

        def rec(data):
            acc = dict()
            for key, item in data.items():
                if isinstance(item, dict):
                    rec_result = rec(item)
                    if re.match(pattern, key) is not None or len(rec_result) > 0:
                        acc[key] = rec_result
                elif re.match(pattern, key) is not None:
                    if key in name_dict:
                        name_dict[key] += 1
                    else:
                        name_dict[key] = 0
                    acc[key] = key + '_' + str(name_dict[key])
            return acc
        return rec(self.mat)

    def checkSchema(self, schema):
        def rec(data, sc, path=''):
            if len(path) > 0:
                path += '.'
            acc = defaultdict(dict)
            for key, item in sc.items():
                if isinstance(item, dict):
                    if key in data:
                        acc.update(rec(data[key], item, path + key))
                elif isinstance(item, list):
                    for name, cond in item:
                        if not np.isnan(cond):
                            result = _checkDictionary[name](data[key], cond)
                            acc[name][path + key] = result
                        else:
                            acc[name][path + key] = 'none'

            return acc

        r = rec(self.mat, schema)
        return r

    def compare_tree(self, other):
        def rec(ltree, rtree):
            lacc, racc = dict(), dict()
            for lkey, litem in ltree.items():
                if lkey in rtree:
                    if isinstance(litem, dict):
                        lres, rres = rec(litem, rtree[lkey])
                        if len(lres) > 0:
                            lacc[lkey] = lres
                        if len(rres) > 0:
                            racc[lkey] = rres
                else:
                    lacc[lkey] = lkey
            for rkey, ritem in rtree.items():
                if rkey in ltree:
                    if isinstance(ritem, dict):
                        lres, rres = rec(ltree[rkey], ritem)
                        if len(lres) > 0:
                            lacc[rkey] = lres
                        if len(rres) > 0:
                            racc[rkey] = rres
                else:
                    racc[rkey] = rkey
            return lacc, racc
        return rec(self.mat, other.mat)

    def __init__(self, mat):
        self.mat = mat

    @classmethod
    def fromFile(self, mat_file):
        self.mat = dtb.loadmat(mat_file)

    def __getitem__(self, item):
        return self.mat[item]