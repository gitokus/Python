import os
import sys
import numpy as np
import operator
import configparser
import csv
import pickle
from tqdm import tqdm
from delphiTools3 import base
from itertools import product
from functools import reduce

from statisticsScript.filters import aflFilters, lksFilters, tsrFilters, objFilters

class Comperator():
    def __init__(self):
        self._mat = None
        self._dat = None
        self._out_def = None
        self._filters_classes = {
            'afl': aflFilters.AflFilters(),
            'lks': lksFilters.LksFilters(),
            'tsr': tsrFilters.TsrFilters(),
            'obj': objFilters.ObjFilters()
        }

    def load_mat(self, file_path):
        if not os.path.isfile(file_path):
            print('Cannot find .mat file!')
            self._mat = None
            return

        try:
            self._mat = base.loadmat(file_path, 'mudp', True, True)
            if not len(self._mat['mudp']['vis']['vision_function_info']['imageIndex']):
                print('Mat file corrupted!')
                self._mat = None
        except:
            print('Error while loading .mat file!')
            self._mat = None

    def load_dat(self, file_path):
        if not os.path.isfile(file_path):
            print('Cannot find .dat file!')
            self._dat = None
            return

        with open(file_path, 'rb') as f:
            dat_data = pickle.load(f)

        parsed_data = {}
        for frame in dat_data.keys():
            gid = None
            for obj in dat_data[frame]:
                if obj['objType'] == 'general':
                    gid = obj['frameGId']
                else:
                    pixel_height = obj['cords'][1][0] - obj['cords'][0][0]
                    if obj['infoDict']['height'] != '-':
                        obj_height = float(obj['infoDict']['height'][:4]) * 1000
                    else:
                        obj_height = 1650
                    try:
                        field = (5.47 * obj_height * 960) / (pixel_height * 4) / 1000
                    except:
                        field = 0
                    obj['infoDict']['distance'] = field
            if gid is not None:
                parsed_data[gid] = dat_data[frame]
            else:
                print('Gid prasing failed for frame {}'.format(frame))

        self._dat = parsed_data

    def load_config(self, config_file='out_definitions'):
        self._out_def = configparser.ConfigParser()
        self._out_def.optionxform = str
        self._out_def.read(config_file)

    def get_filters_list(self, func, format_output=False):
        filters_list = self._filters_classes[func].get_filters_list()
        if format_output:
            out = '{} filters:\n'.format(func.upper())
            for key, value in filters_list.items():
                out += str(key).zfill(3)
                for i, v in enumerate(value):
                    out += '\t{}\n'.format(v)
                out += '\n'
            return out
        else:
            return filters_list

    def _get_matching(self, threshold=0.3, print_info=False):
        mat_gids = list(self._mat['mudp']['vis']['vision_obstacles_info']['imageIndex'])
        common_gids = sorted(list(set(self._dat.keys()) & set(mat_gids)))

        matching = {}
        all_ids = set()
        all_unique_ids = set()

        for gid in common_gids:
            ids = np.zeros((len(self._dat[gid]) - 1), int)
            boxes = np.zeros((len(self._dat[gid]) - 1, 4))
            for i, each in enumerate(self._dat[gid]):
                if not each['objType'] == 'general':
                    ids[i] = each['objID']
                    boxes[i] = (each['cords'][2][0], each['cords'][2][1],
                                each['cords'][1][0], each['cords'][1][1])
            all_ids = all_ids | set(ids.tolist())

            mat_index = mat_gids.index(gid)
            mat_objs_data = self._mat['mudp']['vis']['vision_obstacles_info']['visObs']
            mat_ids = mat_objs_data['uniqueID'][mat_index]
            all_unique_ids = all_unique_ids | set(mat_ids.tolist())
            mat_ids = np.expand_dims(mat_ids, 1)
            mat_boxes = np.stack([mat_objs_data['pixel_left'][mat_index],
                                  960 - mat_objs_data['pixel_top'][mat_index],
                                  mat_objs_data['pixel_right'][mat_index],
                                  960 - mat_objs_data['pixel_bottom'][mat_index]], 1)
            mat_boxes *= mat_ids > 0

            if not len(boxes) or not len(mat_boxes):
                continue

            boxes_permutations = list(product(boxes, mat_boxes))
            ids_map = np.array(list(product(ids, mat_ids)), int)
            compare = np.array(list(map(self._iou, boxes_permutations)))

            idx = np.where(compare > 0)

            match_ids = ['-'.join(map(str, e)) for e in ids_map[idx].tolist()]
            match_prob = compare[idx].tolist()

            for i in range(len(match_ids)):
                if match_ids[i] in matching.keys():
                    matching[match_ids[i]].append(match_prob[i])
                else:
                    matching[match_ids[i]] = [match_prob[i]]
        all_unique_ids -= {0}
        all_ids, all_unique_ids = sorted(all_ids), sorted(all_unique_ids)

        matching_sum = {}
        for key, val in matching.items():
            prob_sum = sum(val) / len(val)
            if prob_sum > threshold:
                already_matched = [k for k in matching_sum.keys() if
                                   '{}-{}'.format(key.split('-')[0], key.split('-')[1]) in k]
                if already_matched:
                    if prob_sum > matching_sum[already_matched[0]]:
                        matching_sum.pop(already_matched[0])
                    else:
                        continue
                matching_sum[key] = prob_sum

        if len(matching_sum):
            matched_ids, matched_unique_ids = zip(*[map(int, match.split('-')) for match in matching_sum.keys()])
            unmatched_ids = sorted(list(set(all_ids) - set(matched_ids)))
            unmatched_unique_ids = sorted(list(set(all_unique_ids) - set(matched_unique_ids)))
        else:
            matched_ids, matched_unique_ids, unmatched_ids, unmatched_unique_ids = [], [], all_ids, all_unique_ids

        if print_info:
            print('Labeled objects: no. {}\n{}'.format(len(all_ids), all_ids))
            print('System output: no. {}\n{}'.format(len(all_unique_ids), all_unique_ids))
            print('\nMatching:')
            no = 1
            for key, value in [i for _, i in sorted(zip(matched_ids, matching_sum.items()))]:
                print('{}. {}: \t{}'.format(str(no).zfill(3), key, value))
                no += 1

        return matching_sum, matched_ids, matched_unique_ids, unmatched_ids, unmatched_unique_ids, common_gids

    def _iou(self, boxes):
        """
        box = (x1, y1, x2, y2) where 1 is top-left and 2 is bottom-right corner
        """
        box1, box2 = boxes
        box1 = box1.astype(int)
        box2 = box2.astype(int)
        box1_area = (box1[2] - box1[0]) * (box1[3] - box1[1])
        box2_area = (box2[2] - box2[0]) * (box2[3] - box2[1])
        if box1_area == 0 or box2_area == 0:
            return 0

        xi1 = max(box1[0], box2[0])
        yi1 = max(box1[1], box2[1])
        xi2 = min(box1[2], box2[2])
        yi2 = min(box1[3], box2[3])
        if xi1 > xi2 or yi1 > yi2:
            return 0
        inter_area = (xi2 - xi1) * (yi2 - yi1)
        union_area = (box1_area + box2_area) - inter_area
        iou = inter_area / union_area
        return iou

    def run(self, func, to_run, print_results=False):
        if self._mat is None or self._dat is None or self._out_def is None:
            print('Load .mat and .dat files and config also!')
            return
        else:
            print('\n\n********************************************************************\n'
                  'Processing {}...\n'
                  '********************************************************************'.format(
                os.path.splitext(os.path.basename(self._mat['__path__']))[0]))
        iou_score, matched_ids, matched_unique_ids, \
        unmatched_ids, unmatched_unique_ids, common_gids = self._get_matching(print_info=print_results)

        self._function = func
        self._filters_classes[func].prepare_filters(to_run)
        filters = self._filters_classes[func].get_filters()

        self._header = []
        self._data = []
        self._get_header()
        self._metadata = {}

        for f in tqdm(filters, desc='Filters'):
            ok = 0
            matched_miss_class = 0
            matched_fp_class = 0
            matched_missed = 0
            matched_fp = 0
            missed = 0
            fp = 0

            filter_name = f.__name__
            for index in common_gids:
                mat_index = list(self._mat['mudp']['vis']['vision_obstacles_info']['imageIndex']).index(index)

                # matched objects
                for i, id in enumerate(set(matched_ids)):
                    all_matched_for_id = [matched_unique_ids[j] for j, _ in enumerate(matched_ids) if _ == id]
                    unique_id_present = [uid for uid in all_matched_for_id if uid in
                                         self._mat['mudp']['vis']['vision_obstacles_info']['visObs']['uniqueID'][mat_index]]
                    if len(unique_id_present) > 0:
                        unique_id = unique_id_present[0]
                    else:
                        unique_id = all_matched_for_id[0]

                    all_matched_for_unique_id = [matched_ids[j] for j, _ in enumerate(matched_unique_ids) if _ == unique_id]
                    id_present = [p_id for p_id in all_matched_for_unique_id if p_id in
                                  [obj['objID'] for obj in self._dat[index]]]
                    if len(id_present) > 0 and id not in id_present:
                        continue

                    is_id, is_unique_id, c1, c2 = f(self._dat, self._mat, index, mat_index, id, unique_id)

                    if is_id and is_unique_id:
                        if c1 and c2:
                            ok += 1
                            self._append_data(index, mat_index, id, unique_id, 'ok', filter_name)
                        elif c1:
                            matched_miss_class += 1
                            self._append_data(index, mat_index, id, unique_id, 'matched_miss_class', filter_name)
                        elif c2:
                            matched_fp_class += 1
                            self._append_data(index, mat_index, id, unique_id, 'matched_fp_class', filter_name)
                    elif is_id:
                        if c1:
                            matched_missed += 1
                            self._append_data(index, mat_index, id, None, 'matched_missed', filter_name)
                    elif is_unique_id:
                        if c2:
                            matched_fp += 1
                            self._append_data(index, mat_index, None, unique_id, 'matched_fp', filter_name)
                    else:
                        continue

                # objects only in labeling
                for id in unmatched_ids:
                    is_id, is_unique_id, c1, c2 = f(self._dat, self._mat, index, mat_index, id, None)
                    if is_id and c1:
                        missed += 1
                        self._append_data(index, mat_index, id, None, 'missed', filter_name)

                # objects only in system
                for unique_id in unmatched_unique_ids:
                    is_id, is_unique_id, c1, c2 = f(self._dat, self._mat, index, mat_index, None, (unique_id, index))
                    if is_unique_id and c2:
                        fp += 1
                        self._append_data(index, mat_index, None, unique_id, 'fp', filter_name)

                self._metadata[filter_name] = {
                    'Ok': ok,
                    'Matched miss class': matched_miss_class,
                    'Matched false class': matched_fp_class,
                    'Matched missed': matched_missed,
                    'Matched false positives': matched_fp,
                    'Missed': missed,
                    'False positives': fp,
                }
            if print_results and ok + matched_miss_class + matched_fp_class + matched_missed + matched_fp + missed + fp > 0:
                print('\nFilter {}:'.format(filter_name))
                print('STATS:')
                print('\tOK: {}'.format(ok))
                print('\tMatched miss class: {}'.format(matched_miss_class))
                print('\tMatched false class: {}'.format(matched_fp_class))
                print('\tMatched missed: {}'.format(matched_missed))
                print('\tMatched false positives: {}'.format(matched_fp))
                print('\tMissed: {}'.format(missed))
                print('\tFalse positives: {}\n'.format(fp))

        self.save_data()

    def _get_header(self):
        for key, item in self._out_def[self._function.upper()].items():
            self._header.append(key)

    def _append_data(self, index, mat_index, id, unique_id, status, filter_name):
        record = dict()
        record['_filter_name'] = filter_name
        record['_from_dat'] = id is not None
        record['_from_mat'] = unique_id is not None
        record['_index'] = index
        record['_match_key'] = id if id is not None else unique_id
        record['_status'] = status

        dat_temp = {'general': [obj for obj in self._dat[index] if obj['objType'] == 'general'][0]}
        if id is not None:
            dat_temp['obj'] = [obj for obj in self._dat[index] if obj['objID'] == id][0]
        if unique_id is not None:
            mat_col = list(reduce(operator.getitem, self._out_def[self._function.upper()]['mat.mat_id'].split('.'),
                                  self._mat)[mat_index]).index(unique_id)
            record['mat.col_id'] = mat_col
        else:
            record['mat.col_id'] = -1

        for key, item in self._out_def[self._function.upper()].items():
            if key.startswith('dat.'):
                try:
                    record[key] = reduce(operator.getitem, item.split('.'), dat_temp)
                except:
                    # print('Cannot append "{}" data.'.format(key))
                    pass

            if key.startswith('mat.'):
                try:
                    f = reduce(operator.getitem, item.split('.'), self._mat)
                    if isinstance(f, dict):
                        for item_key, item_value in f.items():
                            if not '.'.join([key, item_key]) in self._header:
                                self._header.append('.'.join([key, item_key]))
                            record['.'.join([key, item_key])] = item_value[mat_index][mat_col]

                    elif isinstance(f, np.ndarray) and len(f.shape) > 1:
                        record[key] = f[mat_index][mat_col]
                    else:
                        record[key] = f[mat_index]
                except:
                    # print('Cannot append "{}" data.'.format(key))
                    pass

        if record:
            self._data.append(record)

    def save_data(self):
        out_name = os.path.splitext(self._mat['__path__'])[0]
        with open(out_name + '.meta', 'wb') as outFile1:
            pickle.dump(self._metadata, outFile1)
        self._header.sort()
        with open(out_name + '.csv', 'w', newline='') as outFile2:
            writer = csv.DictWriter(outFile2, self._header, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(self._data)
