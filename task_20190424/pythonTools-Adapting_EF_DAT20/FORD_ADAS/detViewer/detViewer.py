import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import QIcon
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import os
import pandas as pd
import traceback

import read_det
import seaborn as sns
sns.set()
sns.set_style("ticks")


def show_error(exception):
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Critical)
    msg.setText("Error: %s" % str(exception))
    msg.setInformativeText("This is additional information")
    msg.setWindowTitle("Error")
    msg.setDetailedText("The details are as follows: " + traceback.format_exc())
    msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
    retval = msg.exec_()
    print("value of pressed message box button:", retval)


class RawLogViewer(QtWidgets.QMainWindow):

    def __init__(self, parent):
        super(RawLogViewer, self).__init__(parent)
        self.df = None
        self.initUI()

    def initUI(self):
        self.setGeometry(320, 320, 400, 600)
        self.setWindowTitle('raw logs')

        self.central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.vertical_layout = QtWidgets.QVBoxLayout(self.central_widget)
        self.vertical_layout.setStretch(1, 1)

        # csv tab view
        self.csv_table = QtWidgets.QTableWidget(self.central_widget)
        self.csv_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.csv_table.horizontalHeader().setStretchLastSection(False)
        self.csv_table.verticalHeader().setVisible(False)
        self.csv_table.verticalHeader().setStretchLastSection(False)
        self.vertical_layout.addWidget(self.csv_table)

        # buttons
        self.horizontal = QtWidgets.QHBoxLayout(self.central_widget)
        self.action_save_to_csv = QtWidgets.QPushButton('Save to csv', self.central_widget)
        self.action_save_to_csv.clicked.connect(self.on_save_to_csv)
        self.horizontal.addWidget(self.action_save_to_csv)
        self.vertical_layout.addLayout(self.horizontal)

    def set_df(self, df, directory):
        self.df = df
        self.directory = directory
        self.csv_table.setRowCount(df.shape[0])
        self.csv_table.setColumnCount(df.shape[1])
        self.csv_table.setHorizontalHeaderLabels(['Time', 'Value', 'Address'])
        for i, (_, row) in enumerate(df.iterrows()):
            self.csv_table.setItem(i, 0, QtWidgets.QTableWidgetItem(row['time']))
            self.csv_table.setItem(i, 1, QtWidgets.QTableWidgetItem(row['value']))
            self.csv_table.setItem(i, 2, QtWidgets.QTableWidgetItem(row['address']))
        self.csv_table.resizeColumnsToContents()

    def on_save_to_csv(self):
        directory, basename = os.path.split(self.directory)
        file_name, _ = os.path.splitext(basename)
        output_file = os.path.join(directory, file_name + '.csv')

        f, x = QtWidgets.QFileDialog.getSaveFileName(self, directory=output_file, filter='*.csv')
        if f is not None and f != '':
            print('[VIEWER][INFO] Saving raw data to csv: ', f)
            self.df.to_csv(f)


class MemoryMap(QtWidgets.QMainWindow):

    def __init__(self, memory_df, parent):
        super(MemoryMap, self).__init__(parent)
        self.df = memory_df
        self.initUI()
        self.set_df()

    def initUI(self):
        self.setGeometry(320, 320, 1050, 600)
        self.setWindowTitle('Memory map')

        self.central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.outer_layout = QtWidgets.QHBoxLayout(self.central_widget)
        self.outer_layout.setStretch(1, 1)

        # csv tab view
        self.csv_table = QtWidgets.QTableWidget(self.central_widget)
        self.csv_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.csv_table.horizontalHeader().setStretchLastSection(False)
        self.csv_table.verticalHeader().setVisible(False)
        self.csv_table.verticalHeader().setStretchLastSection(False)
        self.outer_layout.addWidget(self.csv_table)

        # buttons
        self.inner_layout = QtWidgets.QVBoxLayout(self.central_widget)

        self.action_import_csv = QtWidgets.QPushButton('Import csv', self.central_widget)
        self.action_import_csv.clicked.connect(self.on_import_csv)
        self.inner_layout.addWidget(self.action_import_csv)

        self.action_save_to_csv = QtWidgets.QPushButton('Export to csv', self.central_widget)
        self.action_save_to_csv.clicked.connect(self.on_save_to_csv)
        self.inner_layout.addWidget(self.action_save_to_csv)

        self.outer_layout.addLayout(self.inner_layout)

    def set_df(self):

        self.csv_table.setRowCount(self.df.shape[0])
        self.csv_table.setColumnCount(3)
        self.csv_table.setHorizontalHeaderLabels(['Memory', 'Directory', 'Type'])
        for i, (memory, row) in enumerate(self.df.iterrows()):
            self.csv_table.setItem(i, 0, QtWidgets.QTableWidgetItem(memory))
            self.csv_table.setItem(i, 1, QtWidgets.QTableWidgetItem(row['directory']))
            memory_type = 'NaN' if pd.isnull(row['type']) else row['type']
            self.csv_table.setItem(i, 2, QtWidgets.QTableWidgetItem(memory_type))
        self.csv_table.resizeColumnsToContents()

    def on_save_to_csv(self):
        output_file = 'memory_map.csv'
        f, x = QtWidgets.QFileDialog.getSaveFileName(self, directory=output_file, filter='*.csv')
        if f is not None and f != '':
            print('[VIEWER][INFO] Saving memory map to csv: ', f)
            self.df.to_csv(f)

    def on_import_csv(self):
        dir_name = 'memory_map.csv'
        f, x = QtWidgets.QFileDialog.getOpenFileName(self, directory=dir_name, filter='*.csv')
        if f is not None and f != '':
            print('[VIEWER][INFO] Reading memory map from csv: ', f)
            self.df = pd.read_csv(f, index_col='memory')
            self.set_df()


class DetViewer(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.det_dict_df = None
        self.det_raw_df = None
        self.det_filename = None

        self.plot_pin_memory = set()
        self.plot_path = None

        memory_map = pd.read_csv('memory_map.csv', index_col='memory')
        self.memory_map = MemoryMap(memory_map, self)
        self.raw_log_viewer = RawLogViewer(self)

        self.initUI()
        self.show()

    def initUI(self):
        self.setGeometry(250, 150, 1000, 700)
        self.setWindowTitle('detViewer')
        self.setAcceptDrops(True)

        self.central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.vertical_layout = QtWidgets.QVBoxLayout(self.central_widget)
        self.vertical_layout.setStretch(1, 1)

        # Load log line
        self.load_line = QtWidgets.QHBoxLayout()
        self.load_det_edit = QtWidgets.QLineEdit(self.central_widget)
        self.load_det_edit.setText("")
        self.load_det_edit.setReadOnly(True)
        self.load_line.addWidget(self.load_det_edit)
        self.load_det_btn = QtWidgets.QPushButton('Load DET log', self.central_widget)
        self.load_det_btn.clicked.connect(self.on_load_det_log)
        self.load_line.addWidget(self.load_det_btn)
        self.save_det_btn = QtWidgets.QPushButton('Save to pickle', self.central_widget)
        self.save_det_btn.setDisabled(True)
        self.save_det_btn.clicked.connect(self.on_save_to_pickle)
        self.load_line.addWidget(self.save_det_btn)
        self.vertical_layout.addLayout(self.load_line)

        # Log view line
        self.outer_splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal, self.central_widget)
        self.vertical_layout.addWidget(self.outer_splitter)

        # Left - tree view
        self.fields_tree = QtWidgets.QTreeWidget(self.outer_splitter)
        self.fields_tree.setHeaderLabels(['DetFields', 'Save to csv', 'Pin plot'])
        self.fields_tree.header().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        self.fields_tree.setColumnWidth(1, 1)
        self.fields_tree.setColumnWidth(2, 1)
        self.fields_tree.currentItemChanged.connect(self.on_tree_item_change)
        self.fields_tree.itemChanged.connect(self.on_tree_clicked)
        self.outer_splitter.addWidget(self.fields_tree)

        # Right splitter
        self.inner_splitter = QtWidgets.QSplitter(QtCore.Qt.Vertical, self.outer_splitter)
        self.outer_splitter.addWidget(self.inner_splitter)

        # Values Table
        self.values_table = QtWidgets.QTableWidget(self.inner_splitter)
        self.values_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.values_table.setColumnCount(0)
        self.values_table.setRowCount(0)
        self.values_table.horizontalHeader().setStretchLastSection(False)
        self.values_table.verticalHeader().setVisible(False)
        self.values_table.verticalHeader().setStretchLastSection(False)
        self.inner_splitter.addWidget(self.values_table)

        # Plot layout
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.plot_layout = QtWidgets.QVBoxLayout(self.inner_splitter)
        self.plot_layout.addWidget(self.canvas)
        self.plot_layout.addWidget(self.toolbar)
        self.plot_layout.setContentsMargins(0, 0, 0, 0)

        # Menu
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu('&File')

        # Load DET action
        self.action_load_det = QtWidgets.QAction('&Load DET', self)
        self.action_load_det.setShortcut('Ctrl+L')
        self.action_load_det.triggered.connect(self.on_load_det_log)
        self.file_menu.addAction(self.action_load_det)

        # Save to pickle
        self.action_save_to_pickle = QtWidgets.QAction('&Save to pickle', self)
        self.action_save_to_pickle.setShortcut('Ctrl+S')
        self.action_save_to_pickle.setDisabled(True)
        self.action_save_to_pickle.triggered.connect(self.on_save_to_pickle)
        self.file_menu.addAction(self.action_save_to_pickle)
        self.file_menu.addSeparator()

        # Show raw logs
        self.action_show_raw_logs = QtWidgets.QAction('&Show raw logs', self)
        self.action_show_raw_logs.setDisabled(True)
        self.action_show_raw_logs.triggered.connect(self.on_show_raw_logs)
        self.file_menu.addAction(self.action_show_raw_logs)

        # Edit memory mapper
        self.action_edit_memory_mapper = QtWidgets.QAction('&Edit memory mapper', self)
        self.file_menu.addAction(self.action_edit_memory_mapper)
        self.action_edit_memory_mapper.triggered.connect(self.on_edit_memory_mapper)
        self.file_menu.addSeparator()

        # Exit
        self.action_exit = QtWidgets.QAction('&Exit', self)
        self.action_exit.setShortcut('Ctrl+Q')
        self.action_exit.setStatusTip('Exit application')
        self.action_exit.triggered.connect(QtWidgets.qApp.quit)
        self.file_menu.addAction(self.action_exit)

    def on_load_det_log(self):
        path = str(self.load_det_edit.text())
        if path == '':
            path = os.getcwd()
        f, x = QtWidgets.QFileDialog.getOpenFileName(self, directory=path, filter='*.rtf')
        if f is not None and f != "":
            print("[VIEWER][INFO] Selected log: ", f)
            try:
                self.load_det_file(f)
                self.save_det_btn.setDisabled(False)
                self.action_save_to_pickle.setDisabled(False)
                self.action_show_raw_logs.setDisabled(False)
                self.load_det_edit.setText(f)
                self.setWindowTitle('detViewer - %s' % f)
            except Exception as e:
                print('[VIEWER][ERROR] Fatal exception during loading det log: ', e)
                show_error(e)
                traceback.print_exc()
        else:
            print("[VIEWER][INFO] Log not selected.")

    def load_det_file(self, det_filename):
        self.plot_pin_memory = set()
        self.plot_path = None
        self.det_filename = det_filename
        df = read_det.read_log(det_filename)
        self.det_raw_df = read_det.get_response(df).drop(['message', 'channel', 'action', 'size'], axis=1)
        self.det_dict_df = read_det.get_dictionary(self.det_raw_df, self.memory_map.df)
        self.det_dict_df = read_det.to_tree_dict(self.det_dict_df)
        self.plot_reload()
        self.fill_tree()

    def fill_tree(self):
        def save_data(data, name):
            def inner_listener():
                directory, basename = os.path.split(self.det_filename)
                file_name, _ = os.path.splitext(basename)
                output_file = os.path.join(directory, '%s-%s.csv' % (file_name, name))
                f, x = QtWidgets.QFileDialog.getSaveFileName(self, directory=output_file, filter='*.csv')
                if f is not None and f != '':
                    pd.DataFrame({'value': data[:, 1]}, index=data[:, 0]).to_csv(f)
            return inner_listener

        def rec_fill(item, value):
            if isinstance(value, dict):
                for key, val in sorted(value.items()):
                    child = QtWidgets.QTreeWidgetItem()
                    child.setText(0, key)
                    item.addChild(child)
                    rec_fill(child, val)
            else:
                button = QtWidgets.QPushButton('csv')
                button.clicked.connect(save_data(value, item.text(0)))
                self.fields_tree.setItemWidget(item, 1, button)
                item.setCheckState(2, QtCore.Qt.Unchecked)
        self.fields_tree.clear()
        rec_fill(self.fields_tree.invisibleRootItem(), self.det_dict_df)
        self.fields_tree.expandAll()

    def table_reload(self, name, value):
        self.values_table.setRowCount(value.shape[0])
        self.values_table.setColumnCount(2)
        self.values_table.setHorizontalHeaderLabels(['Time', name])
        for i, v in enumerate(value):
            self.values_table.setItem(i, 0, QtWidgets.QTableWidgetItem(str(v[0])))
            self.values_table.setItem(i, 1, QtWidgets.QTableWidgetItem(str(v[1])))
        self.values_table.resizeColumnsToContents()

    def plot_reload(self):
        self.figure.clf()
        ax = self.figure.add_subplot(111)
        r = self.plot_pin_memory

        if self.plot_path is not None and self.plot_path not in r:
            r = r.union({self.plot_path})

        for path in r:
            value = self.det_dict_df
            for e in list(path):
                value = value[e]
            ax.plot(value[:, 0], value[:, 1])  # drawstyle='steps-post'
        ax.grid()

        len_r = len(r)

        if len_r > 1:
            common_path_elements = set.intersection(*[set(path) for path in r])
            legend_labels = ['.'.join([elem for elem in path if elem not in common_path_elements]) for path in r]
            ax.legend(legend_labels)  # , loc='upper center', bbox_to_anchor=bbox)
        elif len_r == 1:
            legend_labels = [list(r)[0][-1]]
            ax.legend(legend_labels)  #, loc='upper center', bbox_to_anchor=bbox)

        ax.set_xlabel('Time')
        self.figure.tight_layout()
        self.canvas.draw()

    def get_full_tree_path(self, it):
        path_list = [str(it.text(0))]
        while it.parent():
            it = it.parent()
            path_list.append(str(it.text(0)))
        return list(reversed(path_list))

    def on_tree_item_change(self, item):
        if item is not None and item.childCount() == 0:
            value = self.det_dict_df
            path = self.get_full_tree_path(item)
            for e in path:
                value = value[e]
            self.table_reload(path[-1], value)
            self.plot_path = tuple(path)
            self.plot_reload()
        else:
            self.plot_path = None

    def on_tree_clicked(self, item, column):
        if item is not None and column == 2:
            key = tuple(self.get_full_tree_path(item))
            if item.checkState(2) == 2 and key not in self.plot_pin_memory:
                self.plot_pin_memory.add(key)
                self.plot_reload()
            elif key in self.plot_pin_memory:
                self.plot_pin_memory.remove(key)
                self.plot_reload()

    def on_save_to_pickle(self):
        print("[VIEWER][INFO] Saving to pickle.")
        if self.det_dict_df is not None:
            directory, basename = os.path.split(self.det_filename)
            file_name, _ = os.path.splitext(basename)
            output_file = os.path.join(directory, file_name + '.p')
            f, x = QtWidgets.QFileDialog.getSaveFileName(self, directory=output_file, filter='*.p')
            if f is not None and f != '':
                read_det.save_pickle(self.det_dict_df, f)

    def on_show_raw_logs(self):
        self.raw_log_viewer.set_df(self.det_raw_df, self.det_filename)
        self.raw_log_viewer.show()
        print("[VIEWER][INFO] Show raw logs.")

    def on_edit_memory_mapper(self):
        self.memory_map.show()
        if self.det_filename is not None:
            self.load_det_file(self.det_filename)
        print("[VIEWER][INFO] Edit memory mapper.")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = DetViewer()
    sys.exit(app.exec_())