import os
import openpyxl
import argparse
import cv2
from delphiTools3.vis import videoHandler
from tqdm import tqdm

default_template = r'excel_template.xlsx'

parser = argparse.ArgumentParser(description='Script to generate log frame in excelsheet')
parser.add_argument('avi_file', help='Path to avi file')
parser.add_argument('frame', type=int, help='Frame number')


def main(args):
    video_file = os.path.abspath(args.avi_file)
    frame = args.frame

    video_handler = videoHandler(video_file)
    img_frame = video_handler.generateFrames(frame)[0]
    img_frame = cv2.cvtColor(img_frame, cv2.COLOR_BGR2GRAY)

    wb = openpyxl.load_workbook(default_template)
    ws = wb.active
    ws.title = os.path.splitext(os.path.basename(video_file))[0] + '_frame{}'.format(frame)


    for i in tqdm(range(img_frame.shape[0]*img_frame.shape[1])):
        row = i%960 + 1
        col = i//960 + 1
        ws.cell(column=col, row=row, value=255-img_frame[row-1][col-1])

    print('Saving output...')
    wb.save(filename=os.path.join(os.path.dirname(video_file), ws.title + '.xlsx'))
    print('Done!')


if __name__ == '__main__':
    main(parser.parse_args())