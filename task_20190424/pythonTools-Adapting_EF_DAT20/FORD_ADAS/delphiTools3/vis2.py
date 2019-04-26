import os
import readFF
import cv2
import delphiTools3.base as dtb
import numpy as np


# Define some project-specific constants at the very beginning
cads3p5_vid_width = 1280  # CADS3.5 video width = 1280 px
cads3p5_vid_height = 960  # CADS3.5 video height = 960 px
cads3p5_cam_angle = 52  # CADS3.5 video angle = 52 degrees
dat2p0_cam_angle = 100  # DAT2.0 video angle = 100 degrees

# Colors are defined in BGR (not RGB!)
colors_dict = {'w': (255, 255, 255),  # white
               'b': (255, 0, 0),  # blue
               'lb': (255, 50, 0),  # light blue
               'm': (255, 0, 255),  # magenta
               'c': (255, 255, 0),  # cyan
               'y': (0, 255, 255),  # yellow
               'r': (0, 0, 255),  # red
               'g': (0, 255, 0),  # green
               'org': (51, 153, 255),  # orange
               'k': (0, 0, 0),  # Black
               'pink': (255, 0, 255),  # Pink
               'violet': (255, 51, 153),  # Violet
               'lpink': (153, 102, 255),  # Light Pink
               'sandy': (51, 153, 255)  # Sandy (orange-ish)
               }

def loadmat(matpath, frame_shape):
    video_width = max(frame_shape)  # Vertical Videos are bad. Assume that width > height.
    if video_width == cads3p5_vid_width:
        is_dat2p0 = False
    else:
        is_dat2p0 = True
    mat_dict = dtb.loadmat(matpath, sort=True, dat2p0=is_dat2p0)
    return mat_dict


class Video:
    def __init__(self, video_path: str, is_colored=False):
        self.path = video_path
        try:
            self.video = readFF.readFF(self.path)
            self.loaded = True
        except RuntimeError as err:
            print('Could not open avi file: \n', err)
            self.loaded = False
            return

        # self.frame_no = 1
        # Parameters used to display video frame
        self.put_comment = True
        self.comment = self.video.getFrameComment()
        self.is_colored = is_colored

        self.video_len = self.video.getFrameCount()
        self.video.seek(1)
        self.video_shape = self.video.getFrame().shape
        self.video_height, self.video_width = self.video_shape[0], self.video_shape[1]
        if self.video_width == cads3p5_vid_width:
            self.is_dat2p0 = False
        else:
            self.is_dat2p0 = True

    def generate_frame(self, frame_no, by_gid=False, enhancement=None, verbose=False):
        if not self.loaded:
            return
        if by_gid:
            self.video.seek(1)  # seek 1st frame
            first_gid = self.video.getMeta()['GId']
            frame_no = ((frame_no - first_gid) % 65536) // 2 + 1  # Calculate frame difference between 1st and desired GId
        if frame_no < 1:
            frame_no = 1
        if frame_no > self.video_len:
            frame_no = self.video_len

        self.video.seek(frame_no)
        if self.is_colored:
            frame = self.video.getBGR()
            self.get_vid_shape(frame)
            # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        else:
            frame8bit = self.video.getFrame()
            frame = cv2.cvtColor(frame8bit, cv2.COLOR_GRAY2RGB)  # If frame is B&W we need to convert it to BGR
            self.get_vid_shape(frame)

        if enhancement:
            frame = self.enhance(frame, *enhancement)
        if verbose:
            meta = self.video.getMeta()
            print('frame no = {0}, grabindex = {1}'.format(meta['Frame'], meta['GId']))
        if self.put_comment:
            self.comment = self.video.getFrameComment()
            info_line = f'Frame No {frame_no}' + self.comment

            # Black background, green foreground. Comment 10 px above video's bottom edge
            cv2.putText(frame, info_line, (5, self.video_height - 10), cv2.FONT_HERSHEY_SIMPLEX, .7, (0, 0, 0), 4)
            cv2.putText(frame, info_line, (5, self.video_height - 10), cv2.FONT_HERSHEY_SIMPLEX, .7, (0, 255, 0), 1)
        return frame

    def get_vid_shape(self, frame):
        self.video_shape = frame.shape
        self.video_height, self.video_width = self.video_shape[0], self.video_shape[1]

    @staticmethod
    def enhance(img, brightness=None, contrast=None):
        if brightness:
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            h, s, v = cv2.split(hsv)
            lim = 255 - brightness
            v[v > lim] = 255
            v[v <= lim] += brightness
            img = cv2.cvtColor(cv2.merge((h, s, v)), cv2.COLOR_HSV2BGR)

        if contrast:
            lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
            l, a, b = cv2.split(lab)
            clahe = cv2.createCLAHE(clipLimit=contrast, tileGridSize=(4, 4))
            cl = clahe.apply(l)
            img = cv2.cvtColor(cv2.merge((cl, a, b)), cv2.COLOR_LAB2BGR)

        return img

    def save_to_image(self, frame, save_path, resize=None):
        if resize:
            frame = cv2.resize(frame, (0, 0), fx=resize, fy=resize,
                               interpolation=cv2.INTER_CUBIC)
        if not os.path.isdir(save_path):
            os.mkdir(save_path)
        frame_info = self.video.getMeta()['Frame'], self.video.getMeta()['GId']
        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        cv2.imwrite(
            os.path.join(save_path, os.path.basename(self.path)[:-4] + str(frame_info[0]) + '.png'),
            frame)


class Overlay:
    def __init__(self, mat_dict, frame_shape):
        self.video_width = frame_shape[1]  # Vertical Videos are bad. Assume that width > height.
        self.video_height = frame_shape[0]
        self.mat = mat_dict

        if self.video_width != cads3p5_vid_width:  # Determine configuration based on video shape
            self.is_dat2p0 = True
            self.img_index = self.mat['mudp']['vis']['vision_traffic_sign_info']['tsrInfo']['imageIndex']  # Grab Index
            self.cam_alignment = {'yaw': np.zeros_like(self.img_index),
                                  'horizon': np.zeros_like(self.img_index)}  # TODO: Camera alignment for DAT2.0 - missing in matFiles; can be found in .ffs file
            self.angle_of_view = dat2p0_cam_angle
        else:  # CADS3.5 Configuration
            self.is_dat2p0 = False

            self.img_index = self.mat['mudp']['vis']['vision_traffic_sign_info']['imageIndex']  # Grab Index
            self.cam_alignment = {'yaw': self.mat['mudp']['vis']['vision_camera_alignment_info']['cameraAlignment'][
                                        'yaw'],
                                  'horizon': self.mat['mudp']['vis']['vision_camera_alignment_info']['cameraAlignment'][
                                            'horizon']}
            self.angle_of_view = cads3p5_cam_angle

        # Pixel per radian - used to transform detections reported with angle
        self.pix_per_rad = self.video_width / np.deg2rad(self.angle_of_view)

        # Parameters used to transform detections to uniform coordinate system
        self.v_padding = 0  # vertical padding
        self.h_padding = 0  # horizontal padding

        # Coordinates placeholders. Will be overridden in child classes
        self.rectangle = {}
        self.cube_edges = {}

        # Placeholders with information about color of rectangle. Will be overridden in child classes
        self.color_enum = {}  # Color enumerations dict
        self.colors_struct = np.array([])  # Structure with conditions based on which color is chosen

        # Placeholder with information about bottom comment for detection. Will be overridden in child class
        self.comment = np.array([])

        # Placeholder with detection ID (one to put above rectangle). Will be overridden in child class
        self.detection_id = np.array([])

    # ------------------------------
    # ------ HELPER FUNCTIONS ------
    # ------------------------------
    def _get_frame_by_gid(self, grab_index):
        # TODO: This method returns first matching GID, even if more than one matching GID was found
        frame = np.argwhere(self.img_index == grab_index)
        if len(frame):  # If matching index was found
            return frame[0][0]
        else:  # If nothing was found
            return None

    def _get_rect_coords(self, row, col):
        """
        Get transformed coordinates of rectangle
        :param row: row(frame_no) for which overlay should be drawn
        :param col: column (ID) for which overlay should be drawn
        :return: tuple with 2 points
        """
        point1x = self.h_padding + self.rectangle['x_left'][row, col]  # x1 coord
        point1y = self.v_padding - self.rectangle['y_top'][row, col]  # y1 coord
        point2x = self.h_padding + self.rectangle['x_right'][row, col]  # x2 coord
        point2y = self.v_padding - self.rectangle['y_bottom'][row, col]  # y2 coord
        point1 = tuple([point1x, point1y])
        point2 = tuple([point2x, point2y])
        return point1, point2

    def _angle2rect_coords(self, row, col):
        """
        Transform detections reported with angle to pixels
        :param row: row(frame_no) for which overlay should be drawn
        :param col: column (ID) for which overlay should be drawn
        :return: tuple with 2 points
        """
        point1x = self.h_padding + (self.rectangle['x_left'][row, col] * self.pix_per_rad) +\
            self.cam_alignment['yaw'][row]
        point1y = self.v_padding - (self.rectangle['y_top'][row, col] * self.pix_per_rad) -\
            self.cam_alignment['horizon'][row]

        point2x = self.h_padding + (self.rectangle['x_right'][row, col] * self.pix_per_rad) +\
            self.cam_alignment['yaw'][row]
        point2y = self.v_padding - (self.rectangle['y_bottom'][row, col] * self.pix_per_rad) -\
            self.cam_alignment['horizon'][row]

        point1 = tuple([int(point1x), int(point1y)])
        point2 = tuple([int(point2x), int(point2y)])
        return point1, point2

    def _get_ellipse_coords(self, row, col):
        """
        Get transformed coordinates of ellipse
        :param row: row(frame_no) for which overlay should be drawn
        :param col: column (ID) for which overlay should be drawn
        :return: tuple with 2 points
        """
        h_axis = int((self.rectangle['x_right'][row, col] - self.rectangle['x_left'][row, col]) / 2)
        v_axis = int((self.rectangle['y_top'][row, col] - self.rectangle['y_bottom'][row, col]) / 2)
        axis = (h_axis, v_axis)
        center_point = (self.h_padding + self.rectangle['x_left'][row, col] + h_axis,  # X coord
                        self.v_padding - self.rectangle['y_bottom'][row, col] - v_axis)  # Y coord
        return center_point, axis

    @staticmethod
    def get_top_bot_point_coords(pt1, pt2):
        """
        Get coordinates of points where top and bottom comments will be placed
        :param pt1: Top left corner of rectangle
        :param pt2: Bottom right corner of rectangle
        :return: Tuple with two tuples (each representing point)
        """
        top_point_x = int(0.5*(pt1[0] + pt2[0]))
        top_point_y = pt1[1] - 5
        bot_point_x = top_point_x
        bot_point_y = pt2[1] + 15

        top_point = tuple([top_point_x, top_point_y])
        bot_point = tuple([bot_point_x, bot_point_y])
        return top_point, bot_point

    def _put_bottom_comment(self, frame_img, bottom_point, row, col, color=None):
        """
        Put comment at the bottom of detection
        :param np.array frame_img: Frame generated by readFF
        :param tuple bottom_point: Coordinates of bottom point (at which comment will be put)
        :param int row: Row (frame number) of np.array where comment parameters will be looked for
        :param int col: Columns number (detection ID) of np.array where comment parameters will be looked for
        :param str/tuple color: Name of comments color (from colors dict) or BGR tuple
        :return: Frame with comment
        """
        if not color:
            comment_color = color  # Comment will be same color as rectangle
        elif isinstance(color, str):
            comment_color = colors_dict[color]  # Find color in colors_dict
        else:
            comment_color = color  # If color is BGR tuple

        if not isinstance(self.comment[row, col], str):  # If comment is not string - convert it
            comment_text = str(int(self.comment[row, col]))
        else:
            comment_text = self.comment[row, col]
        # Put additional information below rectangle. Black background for better readability
        cv2.putText(frame_img, comment_text, bottom_point, cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=0.45, color=(0, 0, 0), thickness=2, lineType=cv2.LINE_AA)
        cv2.putText(frame_img, comment_text, bottom_point, cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=0.45, color=comment_color, thickness=1, lineType=cv2.LINE_AA)


class PixelOverlay(Overlay):
    def draw_rectangle(self, frame_img, grab_index, lw, bot_comment=False,
                       comment_color=None, top_color='same', angle=False):
        """
        Draw rectangular overlay in columns where detection occurred.
        OpenCv needs two points as specified below:

            pt1------------
             |             |
             |             |
             |             |
             --------------pt2

        :param np.array frame_img: BGR frame generated by readFF module
        :param int grab_index: Number of frame's grab index on which overlay needs to be drawn
        str inputs are listed in colors_dict). If color == 'same' color will be chosen based on self.colors_struct
         parameters (e.g. obstacle class)
        :param int lw: Width of the lines in pixels
        :param bool bot_comment: Put information from self.comment array at the bottom of each rectangle
        :param str or tuple comment_color: Specify color of comment below detection
        :param str/tuple top_color: Color of Comment (ID) on top of detection
        :param bool angle: If True - treat values of self.rectangle as angles, not pixels
        :return: None - function draws on frame
        """
        frame_no = self._get_frame_by_gid(grab_index)
        if frame_no is None:  # If no matching frame was found
            return

        row = frame_no
        # Draw columns that have non-zero values (i.e. have detections). Look for them only in specified row
        to_draw = np.argwhere(list(self.rectangle.values())[0][row])
        for col_num in to_draw:
            col = col_num.item()  # col_num is a single element array - need to convert to int

            condition = self.colors_struct[row, col]  # Condition based on which color is selected
            color = self.color_enum[condition]  # get color from color_enum dictionary

            # Draw rectangle marking system's detection
            if angle:  # detections reported as angle
                pt1, pt2 = self._angle2rect_coords(row, col)
            else:  # Detection reported as raw pixel values
                pt1, pt2 = self._get_rect_coords(row, col)
            cv2.rectangle(frame_img, pt1, pt2, color=color, thickness=lw)

            # Put ID of detection above rectangle. Black Background for better readability
            if top_color == 'same':
                top_color = color
            elif isinstance(top_color, str):
                top_color = colors_dict[top_color]

            top_point, bot_point = self.get_top_bot_point_coords(pt1, pt2)
            id_txt = str(self.detection_id[row, col])
            cv2.putText(frame_img, id_txt, top_point, cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.45, color=(0, 0, 0),
                        thickness=2, lineType=cv2.LINE_AA)
            cv2.putText(frame_img, id_txt, top_point, cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.45, color=top_color,
                        thickness=1, lineType=cv2.LINE_AA)

            if bot_comment:
                self._put_bottom_comment(frame_img, bot_point, row, col, color=comment_color)
        # frame_img = cv2.cvtColor(frame_img, cv2.COLOR_BGR2RGB)

    def draw_ellipse(self, frame_img, grab_index, lw):
        """
        Draw ellipse in detection spot. Ellipse id drawn based on data stored in self.rectangle since the coordinates
        are named in similar convention.

                                       'y_top'
                                    ..**** ****..
                                ..**             **..
                     'x_left' .*                     *. 'x_right'
                               *..                 ..*
                                  **..         ..**
                                      **** ****
                                     'y_bottom'

        :param np.ndarray frame_img: BGR frame generated by readFF module
        :param int grab_index: Number of frame's grab index on which overlay needs to be drawn
        :param int lw: Width of the lines in pixels
        :return: None
        """
        frame_no = self._get_frame_by_gid(grab_index)
        if frame_no is None:  # If no matching frame was found
            return

        row = frame_no
        # Draw columns that have non-zero values (i.e. have detections). Look for them only in specified row
        to_draw = np.argwhere(list(self.rectangle.values())[0][row])
        for col_num in to_draw:
            col = col_num.item()  # col_num is a single element array - need to convert to int

            color_class = self.colors_struct[row, col]  # Condition based on which color is selected
            color = self.color_enum[color_class]  # get color from color_enum dictionary

            center_point, axis = self._get_ellipse_coords(row, col)
            cv2.ellipse(frame_img, center_point, axis, angle=360.0, startAngle=0.0, endAngle=360.0, color=color,
                        thickness=lw)

    def draw_cube(self, frame_img, grab_index, color, lw):
        """
        Draw cube around detected object. ME reports coordinates in this way:
        x_coords - define straight vertical lines
        y_top - define top cube's plane
        y_bottom - define bottom cube's plane

                 x_cor[2]       x_cor[3]
                     |               |
                     |               |
            y_top[2]/---------------/| y_top[3]
                  /  |             / |
                /    |           /   |
           |  /      |      |  /     |
           |/        |      |/       |
   y_top[0]|----------------|y_tp[1] |
           |         |      |        |
           |  y_bt[2]| -----|--------|y_bot[3]
           |       / |      |       /|
           |     /   |      |     /  |
           |   /            |   /
           | /              | /
   y_bot[0]|----------------| y_bot[1]
           |                |
           |                |
      x_cor[0]           x_cor[1]

        :param np.ndarray frame_img: BGR frame generated by readFF module
        :param int grab_index: Number of frame's grab index on which overlay needs to be drawn
        :param str/tuple color: Color of shape's lines. Can ba either BGR tuple or str (available str inputs are listed
        in colors_dict)
        :param int lw: Width of the lines in pixels
        :return: None - function draws on frame
        """
        if not self.cube_edges:  # If Cube edges are not defined (i.e. function does not support them)
            return

        frame_no = self._get_frame_by_gid(grab_index)
        if frame_no is None:  # If no matching frame was found
            return

        if isinstance(color, str):
            color = colors_dict[color]

        row = frame_no
        # Draw columns that have non-zero values (i.e. have detections). Look for them only in specified row
        to_draw = np.argwhere(list(self.rectangle.values())[0][row])  # TODO Change to cube_edges not rectangle
        for col_num in to_draw:
            col = col_num.item()  # col_num is a single element array - need to convert to int

            # Create 2D np.array with [x,y] coordinates for top and bottom plane
            bottom_coords = np.stack((self.h_padding + self.cube_edges['x_coords'][row, col, :],
                                      self.v_padding - self.cube_edges['y_bottom'][row, col, :]), axis=1)
            top_coords = np.stack((self.h_padding + self.cube_edges['x_coords'][row, col, :],
                                   self.v_padding - self.cube_edges['y_top'][row, col, :]), axis=1)

            # Draw plane using polylines
            cv2.polylines(frame_img, [bottom_coords], 1, color, lw)  # Bottom plane
            cv2.polylines(frame_img, [top_coords], 1, color, lw)  # Top plane

            # Connect planes using vertical lines
            for i, j in zip(bottom_coords, top_coords):
                cv2.line(frame_img, tuple(i), tuple(j), color, lw)


class TSROverlay(PixelOverlay):
    def __init__(self, mat_dict, frame_shape):
        super().__init__(mat_dict, frame_shape)

        if self.is_dat2p0:
            self.traffic_s = self.mat['mudp']['vis']['vision_traffic_sign_info'][
                'tsrInfo']['trafficSigns']  # Traffic Signs
            self.h_padding = 0
            self.v_padding = self.video_height
        else:
            self.traffic_s = self.mat['mudp']['vis']['vision_traffic_sign_info']['trafficSigns']
            self.h_padding = 0
            self.v_padding = self.video_height

        self.mat = None  # TODO: check if it works # Free memory
        self.rectangle = {'x_left': self.traffic_s['signPositionLeft'].astype('int'),
                          'x_right': self.traffic_s['signPositionRight'].astype('int'),
                          'y_bottom': self.traffic_s['signPositionBottom'].astype('int'),
                          'y_top': self.traffic_s['signPositionTop'].astype('int')}

        # All TSR overlays should be white
        self.colors_struct = np.ones_like(self.rectangle['x_left'])
        self.color_enum = {1: colors_dict['w']}  # White for all TSR
        self.detection_id = self.traffic_s['signID'] + 1

    def draw(self, frame_img, grab_index, comment=False, lw=1,
             comment_color=None, top_color='same', angle=False):
        super().draw_rectangle(frame_img, grab_index, lw, comment, comment_color, top_color, angle)


class TSRPlusOverlay(TSROverlay):
    def __init__(self, mat_dict, frame_shape):
        super().__init__(mat_dict, frame_shape)
        self.s_conf = self.traffic_s['signConfidence']
        self.s_type = self.traffic_s['signType']
        self.s_relevancy = self.traffic_s['signRelevantDecision']
        self.s_value = self.traffic_s['signValue']
        self.s_supp_1 = self.traffic_s['signSupplementalType1']
        self.s_supp_2 = self.traffic_s['signSupplementalType2']
        self._map_detections_to_str()

    def draw_rectangle(self, frame_img, grab_index, lw=1, bot_comment=True,
                       comment_color=None, top_color='same', angle=False, supp_info=True):
        """
        TSR Plus method has to be overridden to provide additional information
        :return:
        """
        frame_no = self._get_frame_by_gid(grab_index)
        if frame_no is None:  # If no matching frame was found
            return

        row = frame_no
        # Draw columns that have non-zero values (i.e. have detections). Look for them only in specified row
        to_draw = np.argwhere(list(self.rectangle.values())[0][row])
        for col_num in to_draw:
            col = col_num.item()  # col_num is a single element array - need to convert to int

            condition = self.colors_struct[row, col]  # Condition based on which color is selected
            color = self.color_enum[condition]  # get color from color_enum dictionary

            # Draw rectangle marking system's detection
            pt1, pt2 = self._get_rect_coords(row, col)
            cv2.rectangle(frame_img, pt1, pt2, color=color, thickness=lw)

            # Put circle at top left corner to indicate signs relevancy
            cv2.circle(frame_img, center=pt1, radius=6, color=color, thickness=self.s_relevancy[row, col])

            # Put ID of detection above rectangle and sign's type below. Black Background for better readability
            top_point, bot_point = self.get_top_bot_point_coords(pt1, pt2)
            top_point = (top_point[0] - 20, top_point[1])  # Text is wide - move point 20px to the left
            bot_point = (bot_point[0] - 30, bot_point[1])
            top_text = str(col+1) + '/' + str(np.around(self.s_conf[row, col], 2))

            # Concatenate sign type and sign value (s_val == 0 were previously replaced with empty string)
            bot_text = str(self.s_type[row, col]) + self.s_value[row, col]
            cv2.putText(frame_img, top_text, top_point, cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.45, color=(0, 0, 0),
                        thickness=2, lineType=cv2.LINE_AA)
            cv2.putText(frame_img, top_text, top_point, cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.45, color=color,
                        thickness=1, lineType=cv2.LINE_AA)
            cv2.putText(frame_img, bot_text, bot_point, cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.30, color=(0, 0, 0),
                        thickness=2, lineType=cv2.LINE_AA)
            cv2.putText(frame_img, bot_text, bot_point, cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.30, color=color,
                        thickness=1, lineType=cv2.LINE_AA)

            if supp_info:  # Supplementary type info
                supp_point = (bot_point[0] + 20, bot_point[1] + 15)
                supp_txt = self.s_supp_1[row, col] + ' ' + self.s_supp_2[row, col]
                cv2.putText(frame_img, supp_txt, supp_point, cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.30,
                            color=colors_dict['k'], thickness=2, lineType=cv2.LINE_AA)
                cv2.putText(frame_img, supp_txt, supp_point, cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.30, color=color,
                            thickness=1, lineType=cv2.LINE_AA)

    def draw(self, frame_img, grab_index, comment=True, lw=1,
             comment_color=None, top_color='same', angle=False):
        self.draw_rectangle(frame_img, grab_index)

# ----------------------------
# ----- HELPER FUNCTION ------
# -----------------------------
    def _map_detections_to_str(self):
        """
        Function used to map numerical values stored in mat into strings representing specified sign data (sing type,
        sign suppl type etc.)
        :return: None - functions replaces existing data structures
        """
        s_type_dict = {0: 'Unk', 1: 'SpdLimStrt', 2: 'SpdLimEnd', 3: 'Resrvd', 4: 'Reservd',
                       5: 'HgWayStrt', 6: 'HgWayEnd', 7: 'FreeWayStrt', 8: 'FreeWayEnd', 9: 'Reserved',
                       10: 'Yield', 11: 'TownStrt', 12: 'TwonEnd', 13: 'LowSpdArStrt', 14: 'LowSpdArEnd',
                       15: 'Stop', 16: 'NoOvrtkStrt', 17: 'NoOvrtkEnd', 18: 'NoEntrnc', 19: 'AdvSpdLimStrt',
                       20: 'NoEntrncAlrt', 21: 'Reserved', 22: 'Reserved', 23: 'Reserved', 24: 'NoOvrtkTrkStrt',
                       25: 'NoOvrtkTrkEnd', 26: 'RndAbt', 27: 'EndOfAll', 28: 'ArBlStr8', 29: 'ArBlRgt',
                       30: 'ArBlLft', 31: 'ArBlRgtAh', 32: 'ArBlLftAh', 33: 'ArBlNoLft', 34: 'ArBlNoRgt',
                       35: 'ArBlKpLft', 36: 'ArBlKpRgt', 37: 'ArBlPsEthrSid', 38: 'TwnStrt', 39: 'LimCars',
                       40: 'WarPedCrss', 41: 'WarRdAbt'
                       }
        # Transform detections from numbers to strings
        self.s_type = np.vectorize(s_type_dict.get)(self.s_type)

        s_suppl_dict = {0: '', 1: 'Generic', 2: 'Dist', 3:'DistArr', 4:'Time', 5:'Weight', 6:'School',
                        7: 'Rain', 8: 'RainCloud', 9: 'Snow', 10: 'SnowRain', 11: 'Fog', 12: 'Night',
                        13: 'Zone', 14: 'Trailer', 15: 'Truck', 16: 'Tractor', 17: 'ArrLft', 18: 'ArrRgt',
                        19: 'BendLft', 20: 'BendRgt', 21: 'End', 22: 'Ice', 23: 'DistFwd', 24: 'Trk+Trailer',
                        25: 'Ramp', 26: 'Exit', 27: 'Advisry', 28: 'Min', 29: 'RedcdAhead', 30: 'DistStop',
                        31: 'Ahead', 32: 'Area', 33: 'RdWorkAU', 34: 'ArrBidir', 35: "Rappel"
                        }
        # Transform detections from numbers to strings
        self.s_supp_1 = np.vectorize(s_suppl_dict.get)(self.s_supp_1)
        self.s_supp_2 = np.vectorize(s_suppl_dict.get)(self.s_supp_2)

        # ME reports not-relevant signs with 0 - map detection so that 1=relevant 0=not-relevant
        # Multiply by -1 since negative thickness in cv2 means that circle will be filled
        self.s_relevancy = np.array(~np.array(self.s_relevancy, dtype=bool), dtype=int) * (-1)

        # Sign value will be 255 for any non-spd limit signs. convert it to 0
        self.s_value[self.s_value == 255] = 0
        self.s_value = self.s_value.astype('str')
        # Change zeros to empty strings
        self.s_value[self.s_value == '0'] = ''


class ObjectOverlay(PixelOverlay):
    def __init__(self, mat_dict, frame_shape):
        super().__init__(mat_dict, frame_shape)

        if self.is_dat2p0:  # DAT2.0 configuration
            # Adjust image coords system. DAT2.0 - Object detections are reported in relation to image's center
            self.h_padding = int(self.video_width / 2)
            self.v_padding = int(self.video_height / 2)

            vis_obs = self.mat['mudp']['vis']['vision_obstacles_info']['visObjects']['visObs']
            # self.mat = None  # TODO: Check if 'deleting' mat is needed
            # TODO: Once ME provides good logs. Remove '4*' and ".astype('int')"
            self.rectangle = {'x_left': 4*vis_obs['imageBox']['rect']['xLeftCoord'].astype('int'),
                              'x_right': 4*vis_obs['imageBox']['rect']['xRightCoord'].astype('int'),
                              'y_bottom': 4*vis_obs['imageBox']['rect']['yBottomCoord'].astype('int'),
                              'y_top': 4*vis_obs['imageBox']['rect']['yTopCoord'].astype('int')}

            self.cube_edges = {'x_coords': 4*vis_obs['imageBox']['verticalEdges']['xCoord'].astype('int'),
                               'y_top': 4*vis_obs['imageBox']['verticalEdges']['yTopCoord'].astype('int'),
                               'y_bottom': 4*vis_obs['imageBox']['verticalEdges']['yBottomCoord'].astype('int')}

            self.detection_id = vis_obs['id']
            self.colors_struct = vis_obs['classification']
            self.comment = vis_obs['physicalState']['longDistance']  # Data to be put under the rectangle

        else:  # CADS3.5 configuration
            self.h_padding = 0
            self.v_padding = self.video_height  # CADS3.5 - overlays reported from bottom left corner
            vis_obs = self.mat['mudp']['vis']['vision_obstacles_info']['visObs']
            self.mat = None  # TODO: check if it works
            self.rectangle = {'x_left': vis_obs['pixel_left'].astype('int'),
                              'x_right': vis_obs['pixel_right'].astype('int'),
                              'y_bottom': vis_obs['pixel_bottom'].astype('int'),
                              'y_top': vis_obs['pixel_top'].astype('int')}
            self.comment = vis_obs['long_pos']
            self.colors_struct = vis_obs['obstacle_class']
            self.detection_id = vis_obs['id']

        self.color_enum = {0: colors_dict['b'],  # 'Undetermined'
                           1: colors_dict['b'],  # 'Car'
                           2: colors_dict['b'],  # 'Motorcycle'
                           3: colors_dict['lb'],  # 'Truck'
                           4: colors_dict['m'],  # 'Pedestrian'
                           5: (255, 255, 255),  # 'Pole'
                           6: (255, 255, 255),  # 'Tree'
                           7: (255, 255, 255),  # 'Animal'
                           8: (255, 255, 255),  # 'General on-road Object Detection'
                           9: colors_dict['c'],  # 'Bicycle'
                           10: (255, 255, 255)}  # 'Unidentified Vehicle'

    def draw(self, frame_img, grab_index, cube=False, lw=1, comment=True, comment_color='c',
             top_color='y', angle=False):
        if cube:
            super().draw_cube(frame_img, grab_index, color='r', lw=lw)
        else:
            super().draw_rectangle(frame_img, grab_index, lw, comment, comment_color, top_color, angle)


class AFLOverlay(PixelOverlay):
    def __init__(self, mat_dict, frame_shape):
        super().__init__(mat_dict, frame_shape)

        if self.is_dat2p0:  # DAT2.0 configuration
            self.h_padding = 0
            self.v_padding = self.video_height   # TODO clarify with ME how detections are reported
            light_spots = self.mat['mudp']['vis']['vision_active_light_sensor_info']['activeLightSensorInfo'][
                'activeLightSpots']
            self.rectangle = {'x_left': light_spots['pixelLeft'].astype('int'),
                              'x_right': light_spots['pixelRight'].astype('int'),
                              'y_bottom': light_spots['pixelBottom'].astype('int'),
                              'y_top': light_spots['pixelTop'].astype('int')}
        else:  # CAD3.5 configuration
            self.h_padding = 0
            self.v_padding = self.video_height
            light_spots = self.mat['mudp']['vis']['vision_active_light_sensor_info']['activeLightSpots']
            self.rectangle = {'x_left': light_spots['pixelLeft'].astype('int'),
                              'x_right': light_spots['pixelRight'].astype('int'),
                              'y_bottom': light_spots['pixelBottom'].astype('int'),
                              'y_top': light_spots['pixelTop'].astype('int')}
        self.colors_struct = light_spots['classification']
        self.color_enum = {0: None,  # 'None
                           1: colors_dict['b'],  # 'Headlamp
                           2: colors_dict['r'],  # 'Tail-lamp'
                           3: colors_dict['b'],  # 'Pair of Headlamps'
                           4: colors_dict['r'],  # 'Pair of Tail-lamps'
                           5: colors_dict['y'],  # 'Truck Cabin Top Lights
                           6: (255, 255, 255)}  # 'Weak oncoming pair of headlamps'

    def draw(self, frame, grab_index, lw=1):
        super().draw_ellipse(frame, grab_index, lw)


class HRSOverlay(PixelOverlay):
    def __init__(self, mat_dict, frame_shape):
        super().__init__(mat_dict, frame_shape)

        if self.is_dat2p0:  # DAT2.0 configuration
            self.h_padding = int(self.video_width/2)
            self.v_padding = int(self.video_height/2)   # TODO clarify with ME how detections are reported
            reflective_sgs = self.mat['mudp']['vis']['vision_active_light_sensor_info']['activeLightSensorInfo'][
                'reflectiveSigns']
            self.rectangle = {'x_left': reflective_sgs['lightSignLeftAngle'],
                              'x_right': reflective_sgs['lightSignRightAngle'],
                              'y_bottom': reflective_sgs['lightSignBottomAngle'],
                              'y_top': reflective_sgs['lightSignTopAngle']}
            self.detection_id = reflective_sgs['lightSignID']
            self.angle_of_view = dat2p0_cam_angle

        else:  # CAD3.5 configuration
            self.h_padding = int(self.video_width/2)
            self.v_padding = int(self.video_height/2)
            if 'reflectiveSigns' not in self.mat['mudp']['vis']['vision_active_light_sensor_info']:
                return  # Some older SWs don't have this feature
            reflective_sgs = self.mat['mudp']['vis']['vision_active_light_sensor_info']['reflectiveSigns']
            self.rectangle = {'x_left': reflective_sgs['lightSignLeftAngle'],
                              'x_right': reflective_sgs['lightSignRightAngle'],
                              'y_bottom': reflective_sgs['lightSignBottomAngle'],
                              'y_top': reflective_sgs['lightSignTopAngle']}
            self.detection_id = reflective_sgs['lightSignId']

            # HRS are reported at 48 degrees, not 52. Not sure why...
            self.angle_of_view = 48
        self.pix_per_rad = self.video_width / np.deg2rad(self.angle_of_view)

        # All HRS should have same color (white)
        self.colors_struct = np.zeros_like(self.rectangle['x_left'])
        self.color_enum = {0: colors_dict['org']}

        # Merge current glare level with max glare level and put as comment below overlay
        # Use np.array with strings
        glare_current = reflective_sgs['lightSignGlareLevelCurrent'].astype('str')
        slash_arr = np.full_like(glare_current, '/')
        glare_max = reflective_sgs['lightSignGlareLevelMax'].astype('str')

        # Add three arrays to form comment
        self.comment = np.core.defchararray.add(np.core.defchararray.add(glare_current, slash_arr),
                                                glare_max)

    def draw(self, frame_img, grab_index, lw=1, comment=True,
             comment_color='org', top_color='same', angle=True):
        super().draw_rectangle(frame_img, grab_index, lw, comment, comment_color, top_color, angle)


class SystemOverlay(Overlay):
    def __init__(self, mat_dict, frame_shape):
        super().__init__(mat_dict, frame_shape)


        if self.is_dat2p0:
            # TODO: Provide camera calibration when good logs are available
            self.pitch_ang = 20 / self.pix_per_rad #from ffs
            self.yaw_ang = 16 / self.pix_per_rad #from ffs
            self.roll_ang = 0 / self.pix_per_rad #from ffs
            self.focal_len = 1504 # from ffs
            self.cam_height = 1.257 #from ffs
            self.vcs_cam_long = 1.689 #from ffs
        else:  # CADS3.5 configuration
            # Distance from vehicle coordinate system (usually front bumper) to camera
            self.focal_len = self.mat['mudp']['vfpState']['cals']['vision_params']['vehIndependentParam'][
                'focalLength'][-1]
            self.cam_height = self.mat['mudp']['vfpState']['cals']['vision_params']['vehDependentParam'][
                                  'cameraHeight_mm'][-1].astype('int') / 1000  # Camera height should be in meters
            self.vcs_cam_long = -1 * self.mat['mudp']['vfpState']['cals']['corse_sensor_cals'][
                'camera_mounting']['vcs_camera_long'][-1]

            # Pitch, yaw and roll are reported as pixels. Convert to radians
            self.pitch_ang = -1 * self.mat['mudp']['vis']['vision_camera_alignment_info'][
                'cameraAlignment']['horizon'][-1] / self.pix_per_rad
            self.yaw_ang = self.mat['mudp']['vis']['vision_camera_alignment_info'][
                'cameraAlignment']['yaw'][-1] / self.pix_per_rad
            self.roll_ang = self.mat['mudp']['vis']['vision_camera_alignment_info'][
                'cameraAlignment']['rollAngle'][-1] / self.pix_per_rad

    def draw_line(self, frame_img, grab_index, data_dict, color, style=None, lw=1):
        """
        Draw line on image (frame)
        :param np.array frame_img: Frame (image) generated by readFF module
        :param int grab_index: Number of grabIndex of current frame
        :param data_dict: Dictionary with values of factors and range. Dict has to have structure:
        {'left': left_line_data, 'right': right_line_data}
        :param tuple color: BGR color of line
        :param style:
        :param int lw: width of the drawn line
        :return: None
        """

        left_data = data_dict['left']
        right_data = data_dict['right']
        frame_no = self._get_frame_by_gid(grab_index)
        for side in [left_data, right_data]:
            line = self.poly2points(frame_no, side)
            if not np.any(line):  # If all points are zero
                continue
            if style is None:  # Use style defined by some structure
                style = side['style'][frame_no].item()

            # Solid line
            if style == 'solid':
                for row in range(1, len(line)):  # Iterate over rows with [x,y] coordinates
                    p1 = tuple(line[row - 1])  # 1st point
                    p2 = tuple(line[row])  # 2nd point
                    cv2.line(frame_img, p1, p2, color, lw, cv2.LINE_AA)
            # Road Edge
            if style == 're':
                for row in range(1, len(line)):  # Iterate over rows with [x,y] coordinates
                    p1 = tuple(line[row - 1])  # 1st point
                    p2 = tuple(line[row])  # 2nd point
                    cv2.line(frame_img, p1, p2, color, lw, cv2.LINE_AA)

                    # Add horizontal lines to distinguish REs
                    if p1[0] < self.h_padding:  # RE is on the left
                        p3 = np.array(p2) - [30, 0]  # Horizontal line 30px long
                        p3 = tuple(p3)
                        cv2.line(frame_img, p2, p3, color, lw, cv2.LINE_AA)
                    else:
                        p3 = np.array(p2)
                        p3 = p3 + [30, 0]  # Horizontal line 30px long
                        p3 = tuple(p3)
                        cv2.line(frame_img, p2, p3, color, lw, cv2.LINE_AA)
            # Barrier
            if style == 'bar':
                for row in range(1, len(line)):  # Iterate over rows with [x,y] coordinates
                    p1 = tuple(line[row - 1])  # 1st point
                    p2 = tuple(line[row])  # 2nd point
                    cv2.line(frame_img, p1, p2, color, lw, cv2.LINE_AA)
                    # Add vertical lines to distinguish barriers
                    p3 = np.array(p2) - [0, 30]  # Vertical line 30px long
                    p3 = tuple(p3)
                    cv2.line(frame_img, p2, p3, color, lw, cv2.LINE_AA)
            # Curb
            if style == 'curb':
                for row in range(1, len(line)):  # Iterate over rows with [x,y] coordinates
                    p1 = tuple(line[row - 1])  # 1st point
                    p2 = tuple(line[row])  # 2nd point
                    cv2.line(frame_img, p1, p2, color, lw, cv2.LINE_AA)
                    # Add vertical lines
                    p3 = np.array(p2) - [0, 30]  # Vertical line 30px long
                    p3 = tuple(p3)
                    cv2.line(frame_img, p2, p3, color, lw, cv2.LINE_AA)
                    if p1[0] < self.h_padding:  # curb is on the left
                        p4 = np.array(p3) - [30, 0]
                    else:  # Curb is on the right
                        p4 = np.array(p3) + [30, 0]
                    p4 = tuple(p4)
                    cv2.line(frame_img, p3, p4, color, lw, cv2.LINE_AA)
            # Cones/poles
            if style == 'cones' or style == 'poles':
                for row in range(1, len(line)):  # Iterate over rows with [x,y] coordinates
                    p1 = tuple(line[row - 1])  # 1st point
                    p2 = tuple(line[row])  # 2nd point
                    cv2.line(frame_img, p1, p2, color, lw, cv2.LINE_AA)
                    # Add vertical lines
                    p3 = np.array(p2) - [0, 30]  # Vertical line 30px long
                    p3 = tuple(p3)
                    cv2.line(frame_img, p2, p3, color, lw, cv2.LINE_AA)
                    # Put circular "point" at the top of vertical line
                    cv2.circle(frame_img, p3, 3, color, thickness=3)
            # Parked cars
            if style == 'cars':
                for row in range(1, len(line)):  # Iterate over rows with [x,y] coordinates
                    p1 = tuple(line[row - 1])  # 1st point
                    p2 = tuple(line[row])  # 2nd point
                    cv2.line(frame_img, p1, p2, color, lw, cv2.LINE_AA)
                    # Add vertical arrows on the line
                    p3 = np.array(p2) - [0, 40]  # Vertical line 30px long
                    p3 = tuple(p3)
                    cv2.arrowedLine(frame_img, p2, p3, color, lw, cv2.LINE_AA, tipLength=0.3)


# --------------------------------------
# ---------- HELPER FUNCTIONS ----------
# --------------------------------------
    def system2image(self, lat_pos, long_pos):
        """
        Map system detection to image - used for mapping lanes and objects that are not reported in pixels e.g. TSEL
        or PCA
        :param np.array long_pos: Longitudinal position (for lanes - X coordinates)
        :param np.array lat_pos: Lateral position (for lanes - Y coordinates)
        :return: Tuple with two np.arrays of points mapped on image
        """
        if not len(long_pos) or not len(lat_pos):  # If arrays are empty
            return
        cam_x = lat_pos
        cam_y = long_pos
        cam_z = -self.cam_height

        # Rotate coordinate system adjusting for yaw_angle
        cam_x2 = cam_x * np.cos(self.yaw_ang) + cam_y * np.sin(self.yaw_ang)
        cam_y2 = cam_y * np.cos(self.yaw_ang) - cam_x * np.sin(self.yaw_ang)
        cam_z2 = cam_z

        # Rotate coordinate system adjusting for pitch_angle
        cam_x3 = cam_x2
        cam_y3 = cam_y2 * np.cos(self.pitch_ang) + cam_z2 * np.sin(self.pitch_ang)
        cam_z3 = cam_z2 * np.cos(self.pitch_ang) - cam_y2 * np.sin(self.pitch_ang)

        # Coordinates on image
        img_x = (self.focal_len / cam_y3) * cam_x3
        img_y = (self.focal_len / cam_y3) * cam_z3

        # Adjust for roll angle
        rolled_img_x = img_x * np.cos(self.roll_ang) + img_y * np.sin(self.roll_ang)
        rolled_img_y = img_y * np.cos(self.roll_ang) - img_x * np.sin(self.roll_ang)

        # Pad detections to coordinates system used by openCV
        rolled_img_x = self.h_padding + rolled_img_x
        rolled_img_y = self.v_padding - rolled_img_y
        return rolled_img_x.astype('int'), rolled_img_y.astype('int')

    def poly2points(self, frame_no, poly_info, min_line_range=3):
        """
        Transform 3rd degree polynomial to points on the screen
        :param frame_no: number of frame
        :param poly_info: Dictionary with factors and range of polynomial. Dict has to have structure:
        dict = {'a0': , 'a1': , 'a2': , 'a3': , 'endRange', 'startRange'}
        :param min_line_range: Minimum range value of line (point of line which is closest to the camera) - recommended
        values: 3 or higher
        :return: 2D numpy array with [x,y] coords of points
        """
        if frame_no is None:  # Just fixing DAT2.0 issues. Same sh... different line
            return

        a0 = poly_info['a0'][frame_no]
        a1 = poly_info['a1'][frame_no]
        a2 = poly_info['a2'][frame_no]
        a3 = poly_info['a3'][frame_no]
        max_line_range = poly_info['endRange'][frame_no]
        # Since DAT2.0 are not perfect - sometimes drops in log cause max_line_range to be multiple element array
        if max_line_range is None:
            return
        if len(np.array([max_line_range])) > 1:
            max_line_range = max_line_range[0]

        if 'startRange' in poly_info.keys():  # If data has startRange - assign as min_line_range
            min_line_range = poly_info['startRange'][frame_no]
            # TODO Find out how minRange signal works in practice - it's seems like a weird signal
            if len(np.array([min_line_range])) > 1:
                min_line_range = min_line_range[0]
            if min_line_range < 3:
                min_line_range = 3

        factors = [a3, a2, a1, a0]
        # If all factors are 0 or line range is smaller than minimum - return matrix full of zeros
        if not np.any(factors) or max_line_range <= min_line_range:
            return np.zeros((5, 2), dtype=int)

        # Estimate polynomial value with 5 points;
        y_cords = np.linspace(min_line_range, max_line_range, 5)
        x_cords = np.polyval(factors, y_cords)

        img_x, img_y = self.system2image(x_cords, y_cords)
        out = np.array((img_x, img_y)).transpose()  # return array of [x,y] values - 5 rows, 2 cols
        return out


class LKSOverlay(SystemOverlay):
    def __init__(self, mat_dict, frame_shape):
        super().__init__(mat_dict, frame_shape)
        # Adjust padding
        self.h_padding = int(self.video_width / 2)
        self.v_padding = int(self.video_height / 2)

        if self.is_dat2p0:  # DAT2.0 configuration
            # ------ Host lane marker
            host_marker_left = self.mat['mudp']['vis']['vision_road_info']['roadInfo']['roadMarkerInfo'][
                'hostLeftMarker']['laneMarker']
            host_marker_right = self.mat['mudp']['vis']['vision_road_info']['roadInfo']['roadMarkerInfo'][
                'hostRightMarker']['laneMarker']
            # Add color to host_marker dictionary (concatenate two dicts)
            self.host_marker = dict({'left': host_marker_left, 'right': host_marker_right},
                                    **{'color': colors_dict['org']})

            # ------ Next lane markers - left lane
            next_left_marker_l = self.mat['mudp']['vis']['vision_road_info']['roadInfo']['roadMarkerInfo'][
                'nextLeftLeftMarker']['laneMarker']
            next_left_marker_r = self.mat['mudp']['vis']['vision_road_info']['roadInfo']['roadMarkerInfo'][
                'nextLeftRightMarker']['laneMarker']
            # Add color to host_marker dictionary (concatenate two dicts)
            self.next_left = dict({'left': next_left_marker_l, 'right': next_left_marker_r},
                                  **{'color': colors_dict['y']})

            # ------ Next lane markers - right lane
            next_right_marker_l = self.mat['mudp']['vis']['vision_road_info']['roadInfo']['roadMarkerInfo'][
                'nextRightLeftMarker']['laneMarker']
            next_right_marker_r = self.mat['mudp']['vis']['vision_road_info']['roadInfo']['roadMarkerInfo'][
                'nextRightRightMarker']['laneMarker']
            # Add color to host_marker dictionary (concatenate two dicts)
            self.next_right = dict({'left': next_right_marker_l, 'right': next_right_marker_r},
                                   **{'color': colors_dict['y']})

            # ------ Borders
            border_left = self.mat['mudp']['vis']['vision_road_info']['roadInfo']['roadBorderInfo'][
                'leftRoadBorder']['roadBorder']
            border_left_type = self.mat['mudp']['vis']['vision_road_info']['roadInfo']['roadBorderInfo'][
                'leftRoadBorder']['roadBorderType']

            border_right = self.mat['mudp']['vis']['vision_road_info']['roadInfo']['roadBorderInfo'][
                'rightRoadBorder']['roadBorder']
            border_right_type = self.mat['mudp']['vis']['vision_road_info']['roadInfo']['roadBorderInfo'][
                'rightRoadBorder']['roadBorderType']

            # Dict for translation of edge types in DAT2.0
            border_dict = {0: 're', 1: 'curb', 2: 'bar', 3: 'cones', 4: 'cars'}

            # Map types of borders using border_dict
            border_left_type = np.vectorize(border_dict.get)(border_left_type)
            border_right_type = np.vectorize(border_dict.get)(border_right_type)

            # Concatenate all dicts into one
            self.border = {'left': dict(border_left, **{'style': border_left_type}),
                           'right': dict(border_right, **{'style': border_right_type}),
                           'color': colors_dict['org']}

        else:  # CADS3.5 configuration

            # Individual lane model
            ind_left = self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo'][
                'hostLeftIndividualMarker']['laneMarker']
            ind_right = self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo'][
                'hostRightIndividualMarker']['laneMarker']
            self.data_ind = {'left': {'a0': ind_left['a0'], 'a1': ind_left['a1'], 'a2': ind_left['a2'],
                                      'a3': ind_left['a3'], 'endRange': ind_left['range']},
                             'right': {'a0': ind_right['a0'], 'a1': ind_right['a1'], 'a2': ind_right['a2'],
                                       'a3': ind_right['a3'], 'endRange': ind_right['range']},
                             'color': colors_dict['org']}

            # Parallel Model
            par_left = self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo'][
                'hostLeftParallellMarker']['laneMarker']
            par_right = self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo'][
                'hostRightParallellMarker']['laneMarker']
            self.data_par = {'left': {'a0': par_left['a0'], 'a1': par_left['a1'], 'a2': par_left['a2'],
                                      'a3': par_left['a3'], 'endRange': par_left['range']},
                             'right': {'a0': par_right['a0'], 'a1': par_right['a1'], 'a2': par_right['a2'],
                                       'a3': par_right['a3'], 'endRange': par_right['range']},
                             'color': colors_dict['g']}

            # High speed prediction
            hsp_left = self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo'][
                'hostLeftWithHighSpeedPredMarker']['laneMarker']
            hsp_right = self.mat['mudp']['vis']['vision_road_info']['roadMarkerInfo'][
                'hostRightWithHighSpeedPredMarker']['laneMarker']
            self.data_hsp = {'left': {'a0': hsp_left['a0'], 'a1': hsp_left['a1'], 'a2': hsp_left['a2'],
                                      'a3': hsp_left['a3'], 'endRange': hsp_left['range']},
                             'right': {'a0': hsp_right['a0'], 'a1': hsp_right['a1'], 'a2': hsp_right['a2'],
                                       'a3': hsp_right['a3'], 'endRange': hsp_right['range']},
                             'color': colors_dict['r']}

            # Road edge
            re_left = self.mat['mudp']['vis']['vision_road_info']['roadEdgeInfo']['leftRoadEdge']['roadEdge']
            re_right = self.mat['mudp']['vis']['vision_road_info']['roadEdgeInfo']['rightRoadEdge']['roadEdge']
            self.data_re = {'left': {'a0': re_left['a0'], 'a1': re_left['a1'], 'a2': re_left['a2'],
                                     'a3': re_left['a3'], 'endRange': re_left['range']},
                            'right': {'a0': re_right['a0'], 'a1': re_right['a1'], 'a2': re_right['a2'],
                                      'a3': re_right['a3'], 'endRange': re_right['range']},
                            'color': colors_dict['org']}

            # Barrier
            if 'vision_barrier_info' not in self.mat['mudp']['vis'].keys():
                return  # Old SWs did not detect barriers
            bar_left = self.mat['mudp']['vis']['vision_barrier_info']['leftVisBarrier']['visBarrier']
            bar_right = self.mat['mudp']['vis']['vision_barrier_info']['rightVisBarrier']['visBarrier']
            self.data_bar = {'left': {'a0': bar_left['a0'], 'a1': bar_left['a1'], 'a2': bar_left['a2'],
                                      'a3': bar_left['a3'], 'endRange': bar_left['range']},
                             'right': {'a0': bar_right['a0'], 'a1': bar_right['a1'], 'a2': bar_right['a2'],
                                       'a3': bar_right['a3'], 'endRange': bar_right['range']},
                             'color': colors_dict['org']}

    def draw(self, frame, grab_index, data_dict, style):
            super().draw_line(frame, grab_index, data_dict, data_dict['color'],  style, lw=1)


class FusionOverlay(SystemOverlay):
    def __init__(self, mat_dict, frame_shape):
        super().__init__(mat_dict, frame_shape)

        if self.is_dat2p0:
            self.v_padding = int(self.video_height / 2)
            self.h_padding = int(self.video_width / 2)
            if not isinstance(self.mat['mudp']['fus'], dict):
                return
            self.grb_idx_fus = self.mat['mudp']['fus']['log_data_fusion_tracker']['status']['grabIndex']
            self.fused_dict = {  # Adjust longitudinal position for camera mounting
                               'long_pos': np.copy(self.mat['mudp']['fus']['log_data_fusion_tracker']['Fus'][
                                                    'fusTracks']['vcs_long_posn']) + self.vcs_cam_long,
                               'lat_pos': np.copy(self.mat['mudp']['fus']['log_data_fusion_tracker']['Fus'][
                                                   'fusTracks']['vcs_lat_posn'])
                               }
            self.fused_peds = self.mat['mudp']['fus']['fused_ped_ind_vec']

            self.veh_dict = self.fused_dict.copy()
            self.ped_dict = {}
            self.filter_detections()
        else:
            self.v_padding = int(self.video_height / 2)
            self.h_padding = int(self.video_width / 2)
            if not isinstance(self.mat['mudp']['fus'], dict):
                return
            self.grb_idx_fus = self.mat['mudp']['fus']['log_data_fusion_tracker']['status']['grabIndex']
            self.fused_dict = {  # Adjust longitudinal position for camera mounting
                               'long_pos': np.copy(self.mat['mudp']['fus']['log_data_fusion_tracker']['Fus'][
                                                    'fusTracks']['vcs_long_posn']) + self.vcs_cam_long,
                               'lat_pos': np.copy(self.mat['mudp']['fus']['log_data_fusion_tracker']['Fus'][
                                                   'fusTracks']['vcs_lat_posn'])
                               }
            self.fused_peds = self.mat['mudp']['fus']['fused_ped_ind_vec']

            self.veh_dict = self.fused_dict.copy()
            self.ped_dict = {}
            self.filter_detections()

    def draw_rectangle(self, frame_img, grab_index, data_dict, lw=1, top_color='same'):
        """
        Draw rectangular overlay in columns where detection occurred.
        OpenCv needs two points as specified below:

            pt1------------
             |             |
             |             |
             |             |
             --------------pt2

        :param np.array frame_img: BGR frame generated by readFF module
        :param int grab_index: Number of frame's grab index on which overlay needs to be drawn
        str inputs are listed in colors_dict). If color == 'own' color will be chosen based on self.colors_struct
         parameters (e.g. obstacle class)
        :param dict data_dict: Dictionary with data to plot
        :param int lw: Width of the lines in pixels
        :param str/tuple top_color: Color of Comment (ID) on top of detection
        :return: None - function draws on frame
        """
        fus_idx = self.map_fus2vis_idx(grab_index)
        if fus_idx is None:  # If no matching fus_idx was found
            return
        row = fus_idx
        if 'color' not in data_dict.keys():  # If not defined - assume overlay color should be white
            color = colors_dict['w']
        else:
            color = data_dict['color']

        to_draw = np.argwhere(data_dict['long_pos'][fus_idx] != self.vcs_cam_long)
        if not len(to_draw):  # If nothing should be drawn
            return

        # Put ID of detection above rectangle. Black Background for better readability
        if top_color == 'same':
            top_color = color
        elif isinstance(top_color, str):
            top_color = colors_dict[top_color]

        for col_num in to_draw:
            col = col_num.item()  # col_num is a single element array - convert to int

            long_pos = data_dict['long_pos'][row, col]
            lat_pos = data_dict['lat_pos'][row, col]
            pt1, pt2 = self.system2rect_coords(long_pos, lat_pos)
            cv2.rectangle(frame_img, pt1, pt2, color=color, thickness=lw)

            top_point, bot_point = self.get_top_bot_point_coords(pt1, pt2)
            id_txt = str(col + 1)
            cv2.putText(frame_img, id_txt, top_point, cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.35, color=(0, 0, 0),
                        thickness=2, lineType=cv2.LINE_AA)
            cv2.putText(frame_img, id_txt, top_point, cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.35, color=top_color,
                        thickness=1, lineType=cv2.LINE_AA)

    def draw_ellipse(self, frame_img, grab_index, data_dict, lw=1, comment=True):
        """
        Draw ellipse in detection spot. Ellipse id drawn based on data stored in self.rectangle since the coordinates
        are named in similar convention.

                                       'y_top'
                                    ..**** ****..
                                ..**             **..
                     'x_left' .*                     *. 'x_right'
                               *..                 ..*
                                  **..         ..**
                                      **** ****
                                     'y_bottom'

        :param np.ndarray frame_img: BGR frame generated by readFF module
        :param dict data_dict: Dictionary with data to plot
        :param int grab_index: Number of frame's grab index on which overlay needs to be drawn
        :param int lw: Width of the lines in pixels
        :param bool comment: Put top and bottom comment (detection ID + long_pos)
        :return: None
        """
        fus_idx = self.map_fus2vis_idx(grab_index)
        if fus_idx is None:  # If no matching fus_idx was found
            return
        row = fus_idx
        if 'color' not in data_dict.keys():  # If not defined - assume overlay color should be white
            color = colors_dict['w']
        else:
            color = data_dict['color']

        # Draw columns that have non-zero values (i.e. have detections). Look for them only in specified row
        to_draw = np.argwhere(data_dict['long_pos'][fus_idx])
        if not len(to_draw):  # If nothing should be drawn
            return

        for col_num in to_draw:
            col = col_num.item()  # col_num is a single element array - need to convert to int
            long_pos = data_dict['long_pos'][row, col]
            lat_pos = data_dict['lat_pos'][row, col]

            center_point, axis = self.system2ellipse_coords(long_pos, lat_pos)
            cv2.ellipse(frame_img, center_point, axis, angle=360.0, startAngle=0.0, endAngle=360.0, color=color,
                        thickness=lw)
            if comment:
                top_point = center_point[0] - 5, center_point[1] - axis[1] - 5
                bot_point = center_point[0] - 5, center_point[1] + axis[1] + 15

                id_txt = str(col + 1)
                cv2.putText(frame_img, id_txt, top_point, cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.45, color=(0, 0, 0),
                            thickness=2, lineType=cv2.LINE_AA)
                cv2.putText(frame_img, id_txt, top_point, cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.45, color=color,
                            thickness=1, lineType=cv2.LINE_AA)

                lg_pos_txt = str(int(data_dict['long_pos'][fus_idx, col_num]))
                cv2.putText(frame_img, lg_pos_txt, bot_point, cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.45, color=(0, 0, 0),
                            thickness=2, lineType=cv2.LINE_AA)
                cv2.putText(frame_img, lg_pos_txt, bot_point, cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.45, color=color,
                            thickness=1, lineType=cv2.LINE_AA)

    def filter_detections(self):
        """
        Filter detections based on self.fused_peds. Values equal to 255 indicate that detection IS NOT a ped
        :return: None
        """

        # Prepare pedestrian data for drawing
        for key, val in self.veh_dict.items():
            new_val = np.zeros_like(self.fused_peds, dtype='float')
            for i in range(new_val.shape[1]):  # Iterate over columns
                row_nums = np.argwhere(self.fused_peds[:, i] != 255)  # Get rows indices of pedestrian detections
                col_nums = self.fused_peds[row_nums, i] - 1  # Get column numbers where pedestrian detections are stored

                # Copy lat/long pos values of cells where pedestrian was detected
                new_val[row_nums, i] = val[row_nums, col_nums]
                # Remove fused detections that were peds - only non-ped detections will remain
                val[row_nums, col_nums] = 0
            self.ped_dict[key] = new_val

    def map_fus2vis_idx(self, img_idx):
        """
        Get index of fusion detection in mat (i.e. row number)
        :param int img_idx: image_index
        :return: int fus_idx or None (if nothing was found)
        """
        fus_idx = np.argwhere(self.grb_idx_fus == img_idx)
        max_fus_idx = len(self.grb_idx_fus)
        if len(fus_idx):
            fus_idx = fus_idx[0][0]
            if fus_idx > max_fus_idx:
                fus_idx = max_fus_idx
            return fus_idx
        else:
            return None

    def map_length_top2vis(self, long_pos, real_height=1.6):
        if np.isclose(long_pos, 0.):  # If object is very close
            return 100
        # cam_real_height = 1
        long_pos_mm = long_pos * 1000
        img_height = (self.focal_len * real_height * self.video_height) / long_pos_mm
        return int(img_height)

    def system2rect_coords(self, long_pos, lat_pos):
        """
        Get coordinates of rectangle for Fusion detections
        :param np.array/float long_pos: Longitudinal position of the detection
        :param np.array/float lat_pos: Lateral position of the detection
        :return: Tuple with two tuples (points coordinates)
        """
        if not isinstance(lat_pos, np.ndarray):
            lat_pos = np.array([lat_pos])
        if not isinstance(long_pos, np.ndarray):
            long_pos = np.array([long_pos])

        # System2Image treats detection as single point and will result in 2 points at same height
        # Use map_length_top2vis to get objects height on image
        detection_point = self.system2image(lat_pos, long_pos)
        img_height = self.map_length_top2vis(long_pos, real_height=1.2)

        # For better visualisation make detections that are further from host narrower than the close ones
        # Values are completely arbitrary and may require some tuning #ArbitraryValue
        width = 25 - 0.2*long_pos
        if width <= 2:
            width = 3

        p1 = (int(detection_point[0] - width), int(detection_point[1]))
        p2 = (int(detection_point[0] + width), int(detection_point[1] - img_height))
        return p2, p1

    def system2ellipse_coords(self, long_pos, lat_pos):
        if not isinstance(lat_pos, np.ndarray):
            lat_pos = np.array([lat_pos])
        if not isinstance(long_pos, np.ndarray):
            long_pos = np.array([long_pos])

        # System2Image treats detection as single point and will result in 2 points at same height
        # Use map_length_top2vis to get objects height on image
        detection_point = self.system2image(lat_pos, long_pos)
        height_on_img = self.map_length_top2vis(long_pos, real_height=1.2)

        # Move ellipse up by 0.25 of its height so that it matches the way DVTool draws it #ArbitraryValue
        # detection_point = detection_point[0], detection_point[1] - 0.25*height_on_img

        v_axis = int(height_on_img / 2)  # vertical axis
        # Assume horizontal axis is 30 px, subtract half of long pos for better visualisation #ArbitraryValue
        h_axis = int(30 - 0.5*long_pos)
        if h_axis < 1:
            h_axis = 1  # Axis length cannot be negative

        # Taking 0.25 of height_on_img works well #ArbitraryValue
        center_point = (int(detection_point[0]), int(detection_point[1] - 0.25*height_on_img))

        axis = (h_axis, v_axis)
        return center_point, axis

    def draw(self, frame_img, grab_index, data_dict):
        if data_dict == self.veh_dict:
            self.draw_rectangle(frame_img, grab_index, data_dict)
        elif data_dict == self.ped_dict:
            self.draw_ellipse(frame_img, grab_index, data_dict)
        else:
            print("Incorrect Data passed to Fusion Overlay drawing function")
            return


class TSELOverlay(FusionOverlay):
    def __init__(self, mat_dict, frame_shape):
        super().__init__(mat_dict, frame_shape)

        if self.is_dat2p0:
            # Adjust long_pos for camera mounting
            if not isinstance(self.mat['mudp']['tsel'], dict):
                return
            self.acc_stationary_dict = {'long_pos': self.mat['mudp']['tsel']['accStationaryTracks']['vcs_long_posn'] +
                                                    self.vcs_cam_long,
                                        'lat_pos': self.mat['mudp']['tsel']['accStationaryTracks']['vcs_lat_posn'],
                                        'color': {1: colors_dict['lpink'],  # TODO: What colors should be RTS 2-6?
                                                  2: colors_dict['sandy'],
                                                  3: colors_dict['b'],
                                                  4: colors_dict['pink'],
                                                  5: colors_dict['lb'],
                                                  6: colors_dict['violet']}
                                        }
            self.acc_moving_dict = {'long_pos': self.mat['mudp']['tsel']['accMovingTracks']['vcs_long_posn'] +
                                                self.vcs_cam_long,
                                    'lat_pos': self.mat['mudp']['tsel']['accMovingTracks']['vcs_lat_posn'],
                                    'color': {1: colors_dict['r'],
                                              2: colors_dict['sandy'],
                                              3: colors_dict['b'],
                                              4: colors_dict['pink'],
                                              5: colors_dict['lb'],
                                              6: colors_dict['violet']}
                                    }
            self.pca_moving_dict = {'long_pos': self.mat['mudp']['tsel']['pcaMovingTrack']['vcs_long_posn'] +
                                                self.vcs_cam_long,
                                    'lat_pos': self.mat['mudp']['tsel']['pcaMovingTrack']['vcs_lat_posn'],
                                    'color': {1: colors_dict['w']},
                                    'comment': 'PCA'}
            self.pca_stationary_dict = {'long_pos': self.mat['mudp']['tsel']['pcaStationaryTrack']['vcs_long_posn'] +
                                                    self.vcs_cam_long,
                                    'lat_pos': self.mat['mudp']['tsel']['pcaStationaryTrack']['vcs_lat_posn'],
                                    'color': {1: colors_dict['w']},
                                    'comment': 'PCA-S'}
        else:
            # Adjust long_pos for camera mounting
            if not isinstance(self.mat['mudp']['tsel'], dict):
                return
            self.acc_stationary_dict = {'long_pos': self.mat['mudp']['tsel']['accStationaryTracks']['vcs_long_posn'] +
                                                    self.vcs_cam_long,
                                        'lat_pos': self.mat['mudp']['tsel']['accStationaryTracks']['vcs_lat_posn'],
                                        'color': {1: colors_dict['lpink'],  # TODO: What colors should be RTS 2-6?
                                                  2: colors_dict['sandy'],
                                                  3: colors_dict['b'],
                                                  4: colors_dict['pink'],
                                                  5: colors_dict['lb'],
                                                  6: colors_dict['violet']}
                                        }
            self.acc_moving_dict = {'long_pos': self.mat['mudp']['tsel']['accMovingTracks']['vcs_long_posn'] +
                                                self.vcs_cam_long,
                                    'lat_pos': self.mat['mudp']['tsel']['accMovingTracks']['vcs_lat_posn'],
                                    'color': {1: colors_dict['r'],
                                              2: colors_dict['sandy'],
                                              3: colors_dict['b'],
                                              4: colors_dict['pink'],
                                              5: colors_dict['lb'],
                                              6: colors_dict['violet']}
                                    }
            self.pca_moving_dict = {'long_pos': self.mat['mudp']['tsel']['pcaMovingTrack']['vcs_long_posn'] +
                                                self.vcs_cam_long,
                                    'lat_pos': self.mat['mudp']['tsel']['pcaMovingTrack']['vcs_lat_posn'],
                                    'color': {1: colors_dict['w']},
                                    'comment': 'PCA'}
            self.pca_stationary_dict = {'long_pos': self.mat['mudp']['tsel']['pcaStationaryTrack']['vcs_long_posn'] +
                                                    self.vcs_cam_long,
                                    'lat_pos': self.mat['mudp']['tsel']['pcaStationaryTrack']['vcs_lat_posn'],
                                    'color': {1: colors_dict['w']},
                                    'comment': 'PCA-S'}

    def draw_rectangle(self, frame_img, grab_index, data_dict, lw=1, bot_comment=False, is_pca=False):
        fus_idx = self.map_fus2vis_idx(grab_index)
        if fus_idx is None:  # If no matching fus_idx was found
            return

        color_enum = data_dict['color']
        row = fus_idx
        to_draw = np.argwhere(data_dict['long_pos'][fus_idx] != self.vcs_cam_long)
        if not len(to_draw):  # If nothing should be drawn
            return

        for col_num in to_draw:
            col = col_num.item()  # col_num is a single element array - convert to int
            if is_pca:
                long_pos = data_dict['long_pos'][row]
                lat_pos = data_dict['lat_pos'][row]
            else:
                long_pos = data_dict['long_pos'][row, col]
                lat_pos = data_dict['lat_pos'][row, col]
            pt1, pt2 = self.system2rect_coords(long_pos, lat_pos)
            color = color_enum[col + 1]
            cv2.rectangle(frame_img, pt1, pt2, color=color, thickness=lw)
            # top_point, bot_point = self.get_top_bot_point_coords(pt2, pt1)
            top_point = (pt1[0] - 15, pt1[1] - 5)
            bot_point = (pt1[0] - 15, pt2[1] + 10)

            if is_pca:  # PCA
                # Get additional points to draw X mark
                pt3 = pt1[0], pt2[1]
                pt4 = pt2[0], pt1[1]
                cv2.line(frame_img, pt1, pt2, color, lw, cv2.LINE_AA)
                cv2.line(frame_img, pt3, pt4, color, lw, cv2.LINE_AA)

                cv2.putText(frame_img, data_dict['comment'], top_point, cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.35,
                            color=(0, 0, 0), thickness=2, lineType=cv2.LINE_AA)
                cv2.putText(frame_img, data_dict['comment'], top_point, cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.35,
                            color=color, thickness=1, lineType=cv2.LINE_AA)

                pos_txt = str(int(round(long_pos)))
                cv2.putText(frame_img, pos_txt, bot_point, cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.35, color=(0, 0, 0),
                            thickness=2, lineType=cv2.LINE_AA)
                cv2.putText(frame_img, pos_txt, bot_point, cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.35, color=color,
                            thickness=1, lineType=cv2.LINE_AA)
            else:  # TSEL detections
                id_txt = str(col + 1)
                cv2.putText(frame_img, id_txt, top_point, cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.35, color=(0, 0, 0),
                            thickness=2, lineType=cv2.LINE_AA)
                cv2.putText(frame_img, id_txt, top_point, cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.35, color=color,
                            thickness=1, lineType=cv2.LINE_AA)

                pos_txt = str(int(round(long_pos)))
                cv2.putText(frame_img, pos_txt, bot_point, cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.35, color=(0, 0, 0),
                            thickness=2, lineType=cv2.LINE_AA)
                cv2.putText(frame_img, pos_txt, bot_point, cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.35, color=color,
                            thickness=1, lineType=cv2.LINE_AA)

    def draw(self, frame_img, grab_index, data_dict):
        if data_dict in [self.pca_moving_dict, self.pca_stationary_dict]:
            self.draw_rectangle(frame_img, grab_index, self.pca_moving_dict, is_pca=True)
            self.draw_rectangle(frame_img, grab_index, self.pca_stationary_dict, is_pca=True)
        elif data_dict in [self.acc_moving_dict, self.acc_stationary_dict]:
            self.draw_rectangle(frame_img, grab_index, self.acc_moving_dict, is_pca=False)
            self.draw_rectangle(frame_img, grab_index, self.acc_stationary_dict, is_pca=False)
        else:
            print("Incorrect Data passed to Fusion Overlay drawing function")
            return


class TSELPathOverlay(FusionOverlay):
    def __init__(self, mat_dict, frame_shape):
        super().__init__(mat_dict, frame_shape)
        if self.is_dat2p0:
            return   # TODO: add support for DAT2.0
        else:
            if not isinstance(self.mat['mudp']['tsel'], dict):
                return
            self.path_data = {'offset': self.mat['mudp']['tsel']['commonETSELInfo'][
                                               'predictedPath']['predicted_path_lane_center_offset'],
                              'a1': np.tan(self.mat['mudp']['tsel']['commonETSELInfo'][
                                               'predictedPath']['predicted_path_coef_k']),
                              'a2': self.mat['mudp']['tsel']['commonETSELInfo'][
                                        'predictedPath']['predicted_path_coef_c0'] / 2,
                              'a3': self.mat['mudp']['tsel']['commonETSELInfo'][
                                        'predictedPath']['predicted_path_coef_c1'] / 6,
                              'endRange': self.mat['mudp']['tsel']['commonETSELInfo'][
                                  'predictedPath']['predicted_path_valid_length'],
                              'width': self.mat['mudp']['tsel']['commonETSELInfo'][
                                  'predictedPath']['predicted_path_lane_width']}

    def draw_line(self, frame_img, grab_index, data_dict, color=colors_dict['c'], style='solid', lw=1):
        """
        Draw line on image (frame)
        :param np.array frame_img: Frame (image) generated by readFF module
        :param int grab_index: Number of grabIndex of current frame
        :param data_dict: Dictionary with values of factors and range. Dict has to have structure:
        {'left': left_line_data, 'right': right_line_data}
        :param tuple color: BGR color of line
        :param style:
        :param int lw: width of the drawn line
        :return: None
        """
        fus_idx = self.map_fus2vis_idx(grab_index)
        if fus_idx is None:  # If no matching fus_idx was found
            return

        # All coefficients except for a0 will be the same for both sides - make copies of dicts
        left_data = data_dict.copy()
        right_data = data_dict.copy()

        # TSEL reports path as centerline. To plot it as two lines we need to take into account path's offset
        left_data['a0'] = -left_data['width']/2 + left_data['offset']  # Left line should have negative a0
        right_data['a0'] = right_data['width']/2 + right_data['offset']

        for side in [left_data, right_data]:
            line = self.poly2points(fus_idx, side)
            if not np.any(line):  # If all points are zero
                continue
            for row in range(1, len(line)):  # Iterate over rows with [x,y] coordinates
                p1 = tuple(line[row - 1])  # 1st point
                p2 = tuple(line[row])  # 2nd point
                cv2.line(frame_img, p1, p2, color, lw, cv2.LINE_AA)

    def draw(self, frame_img, grab_index, data_dict):
        self.draw_line(frame_img, grab_index, data_dict)


class FailSafeOverlay(Overlay):
    def __init__(self, mat_dict, frame_shape):
        super().__init__(mat_dict, frame_shape)
        if self.is_dat2p0:
            return  # TODO: add support for DAT2.0
        else:
            fs_data = self.mat['mudp']['vis']['vision_failsafes']
            # Filter dictionaries
            self.severity_level = {struct_name: fs_data[struct_name] for struct_name in fs_data.keys() if
                                   'SeverityLevel' in struct_name}
            self.fail_safes = {struct_name: fs_data[struct_name] for struct_name in fs_data.keys() if
                               'Failsafe' in struct_name}

            # Add AEB shutdown as FailSafe
            self.fail_safes['aeb_shutdown'] = self.mat['mudp']['vis']['vision_function_info']['aeb_shutdown']

    # Helper function
    def get_text(self, grab_index):
        frame_no = self._get_frame_by_gid(grab_index)
        if frame_no is None:  # If no matching frame was found
            return {'severity': {'color': colors_dict['w'], 'text': 'No data'},
                    'fail_safe': {'color': colors_dict['w'], 'text': 'No data'}}

        is_severity = np.any([sever[frame_no] for sever in self.severity_level.values()])
        is_failsafe = np.any([fail_s[frame_no] for fail_s in self.fail_safes.values()])

        if is_severity:
            sever_color = colors_dict['r']
            severity_txt = []
            for key, val in self.severity_level.items():
                if val[frame_no] != 0:
                    severity_txt.append(": ".join([str(key), str(val[frame_no])]))
            severity_txt = 'Non-zero severity lvl: ' + ", ".join(severity_txt)
        else:
            sever_color = colors_dict['g']
            severity_txt = ": ".join(['Non-zero severity lvl', str(None)])

        if is_failsafe:
            fails_color = colors_dict['r']
            failsafe_txt = []
            for key, val in self.fail_safes.items():
                if val[frame_no] != 0:
                    failsafe_txt.append(': '.join([str(key), str(val[frame_no])]))
            failsafe_txt = 'Failsafes active: ' + ", ".join(failsafe_txt)
        else:
            fails_color = colors_dict['g']
            failsafe_txt = ': '.join(['Failsafe active', str(None)])

        return {'severity': {'color': sever_color, 'text': severity_txt},
                'fail_safe': {'color': fails_color, 'text': failsafe_txt}}

    def draw(self, frame_img, grab_index):
        text_data = self.get_text(grab_index)
        severity = text_data['severity']
        fail_safe = text_data['fail_safe']

        # Severity levels
        cv2.putText(frame_img, severity['text'], (10, 20), cv2.FONT_HERSHEY_SIMPLEX, .7,
                    colors_dict['k'], 4)
        cv2.putText(frame_img, severity['text'], (10, 20), cv2.FONT_HERSHEY_SIMPLEX, .7,
                    severity['color'], 1)

        # Fail safes
        cv2.putText(frame_img, fail_safe['text'], (10, 45), cv2.FONT_HERSHEY_SIMPLEX, .7,
                    colors_dict['k'], 4)
        cv2.putText(frame_img, fail_safe['text'], (10, 45), cv2.FONT_HERSHEY_SIMPLEX, .7,
                    fail_safe['color'], 1)


def main(video):
    title = 'Test video'
    cv2.namedWindow(title)
    cv2.moveWindow(title, 0, 0)

    # mat_path = r"Z:\DAT2 Logs\Stage D\20181018_FTP804\20181018_131233_FTP804_F150_A25_StageD_1__Time__001.mat"
    # mat_path = r"Z:\DAT2 Logs\Stage D\20181018_FTP804\20181018_132628_FTP804_F150_A25_StageD_1__Time__003.mat"
    # mat_path = r"Z:\DAT2 Logs\Stage D\20181018_FTP804\20181018_AHBC_FTP804_StageD.1\20181018_AHBC_StageD_1_FTP804_210121__Time__004.mat"
    # mat_path = r"E:/CAD3p5_tickets/ADAS-1280/PW_files/ADAS__Date_KQW3210_PRA_PRA_BK_PG_140917_032.mat"
    # mat_path = r"Z:/CHECKOUTS/U625TT_checkout_AFL_20180809/U625TT_AFL_checkout_20180809_205644_045.mat"
    # mat_path = r"Z:\CHECKOUTS\U625TT_checkout_AFL_20180809\U625TT_AFL_checkout_20180809_205644_002.mat"
    mat_path = r"C:/Users/fj7nmq/Documents/!JIRA/BNJ-42/canlog_20190107_193001_012.mat"
    # mat_path = r"Z:\JIRA\ADAS-1166\Test\ADAS_20160909_KQW3215_WAW_WAW_JB_LK_190610_029.mat"
    mat_dict = loadmat(mat_path, video.video_shape)
    obj_test = ObjectOverlay(mat_dict, video.video_shape)
    # tsr = TSROverlay(mat_dict, video.video_shape)
    tsr_plus = TSRPlusOverlay(mat_dict, video.video_shape)
    afl = AFLOverlay(mat_dict, video.video_shape)
    # hrs = HRSOverlay(mat_dict, video.video_shape)
    lks = LKSOverlay(mat_dict, video.video_shape)
    fs = FailSafeOverlay(mat_dict, video.video_shape)
    tsel = TSELOverlay(mat_dict, video.video_shape)
    fus = FusionOverlay(mat_dict, video.video_shape)
    path = TSELPathOverlay(mat_dict, video.video_shape)

    def nothing(x):
        pass

    cv2.createTrackbar('Frame', title, 1, video.video_len, nothing)

    last_frame = 0
    while cv2.getWindowProperty(title, 0) >= 0:
        iframe = cv2.getTrackbarPos('Frame', title)
        iframe = min(max(1, iframe), video.video_len)
        if iframe != last_frame:
            last_frame = iframe
            # curr_frame = video.generate_frame(iframe, by_gid=True)
            curr_frame = video.generate_frame(iframe, verbose=False)
            curr_gid = video.video.getMeta()['GId']
            # obj_test.draw(curr_frame, curr_gid, cube=False)
            # path.draw_line(curr_frame, curr_gid, path.path_data)
            # obj_test.draw(curr_frame, curr_gid, cube=True)
            # video.save_to_image(curr_frame, r"C:\Users\qj3x4n\Pictures\temp")
            # tsr.draw(curr_frame, curr_gid)
            # tsr_plus.draw(curr_frame, curr_gid)
            # fs.draw(curr_frame, curr_gid)
            # fus.draw_rectangle(curr_frame, curr_gid, fus.veh_dict)
            fus.draw_ellipse(curr_frame, curr_gid, fus.ped_dict)
            # tsr.draw_rectangle(curr_frame, curr_gid)
            # hrs.draw_rectangle(curr_frame, curr_gid)
            # afl.draw_ellipse(curr_frame, curr_gid, lw=1)
            tsel.draw_rectangle(curr_frame, curr_gid, tsel.acc_moving_dict)
            tsel.draw_rectangle(curr_frame, curr_gid, tsel.pca_moving_dict, is_pca=True)
            # lks.draw_line(curr_frame, curr_gid, lks.data_ind['color'], lks.data_ind)
            # lks.draw_line(curr_frame, curr_gid, lks.data_hsp['color'], lks.data_hsp)
            # lks.draw_line(curr_frame, curr_gid, lks.data_par, lks.data_par['color'], style='solid')
            # lks.draw_line(curr_frame, curr_gid, lks.data_re['color'], lks.data_re, style='cars')
            # lks.draw_line(curr_frame, curr_gid, lks.data_bar['color'], lks.data_bar, style='bar')
            # lks.draw_line(curr_frame, curr_gid, lks.host_marker, lks.host_marker['color'], style='solid')
            # lks.draw_line(curr_frame, curr_gid, lks.next_left['color'], lks.next_left, style='solid')
            # lks.draw_line(curr_frame, curr_gid, lks.next_right['color'], lks.next_right, style='solid')
            # lks.draw_line(curr_frame, curr_gid, lks.border['color'], lks.border, style=None)

            # display frame
            cv2.imshow(title, curr_frame)
            # curr_video.put_comment(iframe)
        # draw image and check key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # close window
    cv2.destroyWindow(title)


if __name__ == '__main__':
    # vid_path = r"Z:/CHECKOUTS/U625TT_checkout_AFL_20180809/U625TT_AFL_checkout_20180809_205644_045.avi"
    vid_path = r"Z:\CHECKOUTS\U625TT_checkout_AFL_20180809\U625TT_AFL_checkout_20180809_205644_002.avi"
    # vid_path = r"Z:\JIRA\ADAS-1166\Test\ADAS_20160909_KQW3215_WAW_WAW_JB_LK_190610_029.avi"
    # vid_path = r"Z:/CHECKOUTS/U625TT_checkout_AFL_20180809/U625TT_AFL_checkout_20180809_205644_045.avi"
    # vid_path = r"Z:\DAT2 Logs\Stage D\20181018_FTP804\20181018_132628_FTP804_F150_A25_StageD_1__Time__003.avi"
    # vid_path = r'Z:/JIRA/ADAS-1166/Test\\ADAS_20160909_KQW3215_WAW_WAW_JB_LK_190610_029.avi'
    # vid_path = r"Z:\DAT2 Logs\Stage D\20181018_FTP804\20181018_AHBC_FTP804_StageD.1\20181018_AHBC_StageD_1_FTP804_210121__Time__004.avi"
    # vid_path = r"Z:\DAT2 Logs\Stage D\20181018_FTP804\20181018_131233_FTP804_F150_A25_StageD_1__Time__001.avi"
    sample_vid = Video(vid_path, is_colored=True)
    main(sample_vid)
