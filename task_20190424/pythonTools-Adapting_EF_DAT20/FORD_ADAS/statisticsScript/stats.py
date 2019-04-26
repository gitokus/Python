import pickle
import os
import csv
import pandas as pd
from collections import defaultdict

class StatsGenerator():
    def __init__(self):
        self._metadata_list = None
        self._csvdata_list = None
        self._current_folder = None

    def load_data(self, folder_path):
        if not os.path.isdir(folder_path):
            print('Cannot find folder file!')
            self._metadata_list = None
            return

        self._current_folder = folder_path
        self._metadata_list = {}
        self._csvdata_list = []

        meta_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if
                      os.path.isfile(os.path.join(folder_path, f))
                      and os.path.splitext(f)[1] == '.meta']

        for meta in meta_files:
            with open(meta, 'rb') as f:
                name = os.path.splitext(os.path.basename(meta))[0]
                self._metadata_list[name] = pickle.load(f)
            self._csvdata_list.append(meta[:-5] + '.csv')

    def run(self):
        if self._metadata_list is None or self._csvdata_list is None:
            print('Select input folder!')
            return

        self._save_header = ['Filter name', 'Ok', 'Matched miss class', 'Matched false class', 'Matched missed',
                             'Matched false positives', 'Missed', 'False positives']
        self._save_data = defaultdict(dict)
        all_stats = dict(zip(self._save_header, ['', 0, 0, 0, 0, 0, 0, 0]))

        for log_name, log_stats in self._metadata_list.items():
            for filter_name, filter_data in log_stats.items():
                filter_data['Filter name'] = filter_name
                for stat in self._save_header:
                    if stat != 'Filter name':
                        all_stats[stat] += filter_data[stat]
                    if stat in self._save_data[filter_name].keys():
                        if stat != 'Filter name':
                            self._save_data[filter_name][stat] += filter_data[stat]
                    else:
                        self._save_data[filter_name][stat] = filter_data[stat]
        self._save_data[''] = all_stats

        self._save_report = None
        for csv in self._csvdata_list:
            self._save_report = self.generate_report(csv, self._save_report)

    def generate_report(self, filename, output_file):
        data = pd.read_csv(filename)
        sorted_data = data.sort_values(by=['_match_key', '_filter_name', '_index']).reset_index()
        series_status = sorted_data.get('_status')
        diff_status = series_status.eq(series_status.shift())
        eq_status = diff_status[diff_status == False]

        series_key = sorted_data.get('_match_key')
        diff_key = series_key.eq(series_key.shift())
        eq_key = diff_key[diff_key == False]

        series_filter = sorted_data.get('_filter_name')
        diff_filter = series_filter.eq(series_filter.shift())
        eq_filter = diff_filter[diff_filter == False]

        series_index = sorted_data.get('_index')
        diff_index = series_index.eq(series_index.shift() + 2)
        eq_index = diff_index[diff_index == False]

        merged_index = eq_status.index.union(eq_key.index).union(eq_filter.index).union(eq_index.index)

        duration = pd.Series(merged_index, index=merged_index).append(
            pd.Series([series_status.shape[0]], index=[series_status.shape[0]])).diff().shift(-1)[:-1].astype(int)

        basic_header = ['logName', 'eventFinderID', 'eventID', 'eventComment', 'eventIndex',
                        'eventDuration', 'eventColumnID', 'ME_API', 'ME_SW', 'VFP_ver', 'gtID', 'uniqueID']
        out = pd.DataFrame({
            'logName': pd.Series([os.path.basename(os.path.splitext(filename)[0])], index=merged_index),
            'eventFinderID': sorted_data['_filter_name'][merged_index],
            'eventID': pd.Series(range(1, len(merged_index) + 1), index=merged_index),
            'eventComment': series_status[merged_index],
            'eventIndex': sorted_data['_index'][merged_index],
            'eventDuration': duration,
            'eventColumnID': sorted_data['mat.col_id'][merged_index],
            'ME_API': pd.Series([''], index=merged_index),
            'ME_SW': pd.Series([''], index=merged_index),
            'VFP_ver': pd.Series([''], index=merged_index),
            'gtID': sorted_data['dat.object.id'][merged_index],
            'uniqueID': sorted_data['mat.mat_id'][merged_index]},
            index=merged_index,
            columns=basic_header)

        if output_file is None:
            output_file = out
        else:
            output_file = output_file.append(out)

        return output_file


    def save_data(self, path):
        out_name = os.path.join(path, 'STATS_summary.csv')
        with open(out_name, 'w', newline='') as outFile:
            writer = csv.DictWriter(outFile, self._save_header)
            writer.writeheader()
            writer.writerows(self._save_data.values())

        self._save_report.to_csv(os.path.join(path, 'EF_report.csv'), index=False)

