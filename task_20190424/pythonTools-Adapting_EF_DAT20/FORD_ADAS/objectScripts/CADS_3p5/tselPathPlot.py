import numpy as np
import delphiTools3.base as dtb
import matplotlib.pyplot as plt
import traceback
import signalClasses as signal
from matplotlib.ticker import AutoMinorLocator
import os
import glob
plt.rcParams['axes.grid'] = True


class Path(signal.FusSignal):
    def __init__(self, mat):
        super().__init__(mat)
        self.mat = mat
        self.path_signals = {
            'offset': mat['mudp']['tsel']['commonETSELInfo']['predictedPath']['predicted_path_lane_center_offset'],
            'angle': mat['mudp']['tsel']['commonETSELInfo']['predictedPath']['predicted_path_coef_k'],
            'c0': mat['mudp']['tsel']['commonETSELInfo']['predictedPath']['predicted_path_coef_c0'],
            'c1': mat['mudp']['tsel']['commonETSELInfo']['predictedPath']['predicted_path_coef_c1']}
        self.synchronize_path()
        self.get_synchronized(self.path_signals)

    def synchronize_path(self):
        return super().get_synchronized(self.path_signals)

    def get_path(self, frame, path_range=None):
        """ Get value of path's polynomial at desired frame.

         :param frame: Vision frame (index in mat)
         :param path_range: Range of path polynomial. Can be either single number or list(range). If not specified, path
                            will be calculated for range from TSEL valid length.
        :returns: tuple (path_range, path polynomial value) """
        fus_index = self.combined[frame, 0]

        # Get path coefficients and path range (if not specified)
        a0 = self.path_signals['offset'][fus_index]  # Lateral offset
        a1 = np.tan(self.path_signals['angle'][fus_index])  # heading angle
        a2 = self.path_signals['c0'][fus_index] / 2
        a3 = self.path_signals['c1'][fus_index] / 6
        if path_range is None:
            path_range = np.arange(0, self.path_signals['range'][fus_index], 0.5)

        # Calculate path as 3rd order polynomial
        path_poly = a0 + a1 * path_range + a2 * np.power(path_range, 2) + a3 * np.power(path_range, 3)
        return path_range, path_poly

    def get_distance_from_path(self, tgt_id, frame_range, long_pos='vis', lat_pos='vis'):
        """
        Get the distance between centerline of path and target.
        :param tgt_id: ID of object (either fusion or vision)
        :param frame_range: range of frames for which distance has to calculated (either vision of fusion)
        :param long_pos: target's longitudinal position. Default - vision pos
        :param lat_pos: target's lateral position. Default - vision pos

        :return: np.array with VRU's distance from path (with correct sign)
        """
        if lat_pos == 'vis':
            lat_pos = self.mat['mudp']['vis']['vision_obstacles_info']['visObs']['lat_pos'][:, tgt_id]
        if long_pos == 'vis':
            long_pos = self.mat['mudp']['vis']['vision_obstacles_info']['visObs']['long_pos'][:, tgt_id]
        out = []
        for frame in frame_range:
            _, path_poly = self.get_path(frame, long_pos[frame])  # get the value of path at VRU's long_pos
            dist_from_path = -lat_pos[frame] - path_poly  # Mind the signs (both values should be negative)
            out.append(dist_from_path)
        return np.array(out)


class VFPSignal(signal.VFPSignal):
    def __init__(self, mat):
        super().__init__(mat)
        self.brake_pedal = mat['mudp']['vfpState']['cmd_msg']['veh_state_info']['brakePedalPressed'][self.vfp_index]
        self.ref_X_point = mat['mudp']['vfpState']['cals']['vision_params']['vehDependentParam']['referencePointX_mm'][-1] /1000
        self.l_wheel = mat['mudp']['vfpState']['cals']['vision_params']['vehDependentParam']['leftWheel_mm'][-1] / 1000
        self.r_wheel = (-1)*mat['mudp']['vfpState']['cals']['vision_params']['vehDependentParam']['rightWheel_mm'][-1] / 1000


class VisSignals:
    def __init__(self, mat):
        self.vru_flags = {
            'VRUPartBrake': mat['mudp']['vis']['vision_function_info']['visOnlyVRUPartialBrake'].astype('float32'),
            'VRUBrakeUnconf': mat['mudp']['vis']['vision_function_info']['visOnlyVRUBrakeUnconfirmed'].astype(
                'float32'),
            'VRUWarning': mat['mudp']['vis']['vision_function_info']['visOnlyVRUWarning'].astype('float32'),
            'VRUBrakeFull': mat['mudp']['vis']['vision_function_info']['visOnlyVRUBrake'].astype('float32')}
        self.veh_flags = {'VehWarn': mat['mudp']['vis']['vision_function_info']['visOnlyVehWarning'].astype('float32'),
                          'VehPartBrake': mat['mudp']['vis']['vision_function_info']['visOnlyVehPartialBrake'].astype(
                              'float32'),
                          'VehBrakeUnconf': mat['mudp']['vis']['vision_function_info'][
                              'visOnlyVehBrakeUnconfirmed'].astype('float32'),
                          'VehBrakeFull': mat['mudp']['vis']['vision_function_info']['visOnlyVehBrake'].astype(
                              'float32')}
        self.obj_signals = {'lat_pos': mat['mudp']['vis']['vision_obstacles_info']['visObs']['lat_pos'],
                            'long_pos': mat['mudp']['vis']['vision_obstacles_info']['visObs']['long_pos'],
                            'lat_vel': mat['mudp']['vis']['vision_obstacles_info']['visObs']['lat_vel'],
                            'long_vel': mat['mudp']['vis']['vision_obstacles_info']['visObs']['long_vel'],
                            'obstacle_class': mat['mudp']['vis']['vision_obstacles_info']['visObs']['obstacle_class'],
                            'ttcAccel': mat['mudp']['vis']['vision_obstacles_info']['visObs']['ttc_const_accel'],
                            'ttcVel': mat['mudp']['vis']['vision_obstacles_info']['visObs']['ttc_const_vel'],
                            'tlet_conf': mat['mudp']['vis']['vision_obstacles_info']['visObs']['tlet_match_conf']}
        self.host_signals = {'vehYawRate': mat['mudp']['vis']['vision_vehicle_info']['vehicleYawRate'],
                             'vehSpeed': mat['mudp']['vis']['vision_vehicle_info']['vehicleVelocity']}

        self.image_index = mat['mudp']['vis']['vision_obstacles_info']['imageIndex']
        self.start_event = len(self.vru_flags['VRUWarning'])
        self.end_event = 0
        self.find_event(self.vru_flags)
        self.obj_id = self.find_obj_id(self.vru_flags)
        self._separate_warnings(self.vru_flags)

    @staticmethod
    def find_obj_id(signals_dict):
        if not np.any([np.any(np.nonzero(a)) for a in signals_dict.values()]):
            print('*********\nNo active flags in the log - Nothing to plot \n**********')
            return False
        obj_id = []
        for warning in signals_dict.values():
            try:
                warning_obj_ID = warning[np.nonzero(warning)[-1][-1]]
                obj_id.append(warning_obj_ID)
            except IndexError:
                continue
        obj_id = obj_id[-1]
        return int(obj_id - 1)

    @staticmethod
    def _separate_warnings(signals_dict):
        """ Separate signals to make them more readable"""
        i = 0.5
        for warning in signals_dict.values():
            warning[np.nonzero(warning)] = i
            i += 0.25

    def find_event(self, signals_dict):
        for warning in signals_dict.values():
            warning_duration = np.argwhere(warning != 0).flatten()
            # If argwhere finds nothing an IndexError will occur
            try:
                if warning_duration[0] < self.start_event:
                    self.start_event = warning_duration[0]
                if warning_duration[-1] > self.end_event:
                    self.end_event = warning_duration[-1]
            except IndexError:
                continue
        # Extend event range
        if self.start_event - 20 > 0:
            self.start_event = self.start_event - 20
        if self.end_event + 20 < len(signals_dict['VRUWarning']):
            self.end_event = self.end_event + 20
        # return start_event, end_event


class Fusion(signal.FusSignal):
    def __init__(self, mat):
        super().__init__(mat)
        self.cmbb_signals = {'cmbb_conf': mat['mudp']['fus']['log_data_fusion_tracker']['Fus']['fusTracks']['cmbbPrimaryConfidence'],
                             'ped_id': mat['mudp']['fus']['fused_ped_ind_vec'],
                             'visTrkID': mat['mudp']['fus']['log_data_fusion_tracker']['Fus']['fusTracks']['visTrkID'],
                             'fus_source': mat['mudp']['fus']['log_data_fusion_tracker']['Fus']['fusTracks']['fusion_source'],
                             'fcw_conf': mat['mudp']['fus']['log_data_fusion_tracker']['Fus']['fusTracks']['fcwConfidence']}
        self.cmbb_signals = self.get_synchronized(self.cmbb_signals)


def has_changed(signal):
    """ Find where signal status has changed (turn on or off). it's recommended to pass full signal """
    turned_on = []
    turned_off = []
    for i in range(1, len(signal)):
        if signal[i - 1] != 0 and signal[i] == 0:
            turned_off.append(i)
        if signal[i - 1] == 0 and signal[i] != 0:
            turned_on.append(i)
    return turned_on, turned_off


def plot_brake_pedal(ax, turned_on, turned_off):
    if turned_on.tolist():
        for i, event in enumerate(turned_on.tolist()):
            if i == 0:
                ax.axvline(event, C='k', ls='--', label='Brake pedal pressed', marker='^')
            else:
                ax.axvline(event, C='k', ls='--', marker='^')
    if turned_off.tolist():
        for i, event in enumerate(turned_off.tolist()):
            if i == 0:
                ax.axvline(event, C='k', ls='--', label='Brake pedal released', marker='v')
            else:
                ax.axvline(event, C='k', ls='--', marker='v')


def plot_in_current_path(mat, logname, out_path, vru_type):
    """ Plots for longitudinal tests.

    :return Two subplots: #1: TTC and warning activation
                          #2: VRU position in relation to current host path"""

    target = VisSignals(mat)
    max_speed = np.max(target.host_signals["vehSpeed"])
    print(f'\nMax speed for test: {max_speed}\n')
    if max_speed > 22.22:
        print('####### WARNING! Approaching speed higher than max for warning! #########')

    event_range = np.arange(target.start_event, target.end_event)
    vfp_state = VFPSignal(mat)
    pressed, released = has_changed(vfp_state.brake_pedal[event_range])
    target_id = target.obj_id

    # Get data for path plotting
    my_path = Path(mat)
    path_to_vru_dist = my_path.get_distance_from_path(target_id, event_range)
    ttc = target.obj_signals['ttcAccel'][event_range, target_id]
    ttc[ttc > 5] = 5
    img_index = target.image_index[event_range]

    f1, ax = plt.subplots(2, 1, figsize=(14, 9))
    plt.suptitle(logname)
    # -------------------- First Plot ----------------------------
    ax1 = ax[0]
    ax1.plot(img_index, ttc, label='Time To Collision')
    ax1.set_ylabel('TTC[s]')
    ax1.set_xlabel('GrabIndex')
    ax1.set_title('TTC vs Flag activation')
    plot_brake_pedal(ax1, img_index[pressed], img_index[released])
    if vru_type == 'ped':
        thresholds = {'Warning': 2.15, 'Unconfirmed/PartBrake': 1.5, 'FullBrake': 1.4}
    elif vru_type == 'bic':
        thresholds = {'Warning': 2., 'Unconfirmed/PartBrake': 1.4, 'FullBrake': 1.3}
    else:
        raise ValueError('incorrect VRU type')

    for name, flag in target.vru_flags.items():
        active_at_ttc = 0
        try:
            active_at_ttc = ttc[np.nonzero(flag[event_range])[0][0]]  # Get the ttc at 1st occurance of the flag
            active_at_ttc = np.around(active_at_ttc, 2)
        except IndexError:
            pass
        ax1.plot(img_index, flag[event_range], ls='--', label=name + f' TTC:{active_at_ttc}')

    # Find index where TTC value dropped below threshold and append to value of dict
    temp_ttc = ttc
    temp_ttc[temp_ttc == 0] = np.nan  # Temporary TTC; Prevents from putting thresholds when object was not detected yet
    for name, thresh_value in thresholds.items():
        try:
            index = np.argwhere(temp_ttc < thresh_value)[0][0]
        except IndexError:  # In case np.argwhere finds nothing
            index = np.nan
        thresholds[name] = [index, thresh_value]
    # Draw vertical lines at the points where flag should light up
    taken_idx=[]
    for name, values in thresholds.items():
        if np.isnan(values[0]):
            continue
        ax1.axvline(img_index[values[0]], lw=1.5, ls=':', C='k')
        if values[0] in taken_idx:  # If place (index) on the plot is already taken, move text to prevent overlay
            values[0] = values[0] - 2
        taken_idx.append(values[0])

        y_pos = ax1.get_yticks()[-1]*0.9 / 2  # Set y_pos of text to be in the middle of plot
        ax1.text(img_index[values[0]], y_pos, f'\n{name} threshold: {values[1]}s', rotation='vertical', fontsize=10,
                 va='center', bbox=dict(facecolor='r', alpha=0.4), linespacing=0.3)

    # Adjust subplot position
    box1 = ax1.get_position()
    ax1.set_position([box1.x0, box1.y0 + box1.height * 0.12, box1.width, box1.height])

    # Adjust grid, add legend
    minor_locator = AutoMinorLocator(5)
    ax1.yaxis.set_minor_locator(minor_locator)
    ax1.grid(which='minor', color='k', alpha=0.2)
    ax1.legend(fontsize=9)

    # ----------------------- Second Plot ------------------------------------
    ax2 = ax[1]
    ax2.plot(img_index, np.ones_like(path_to_vru_dist) * 1.13, ls='-.', C='r',
             label='FullBrake - predicted path')
    ax2.plot(img_index, np.ones_like(path_to_vru_dist) * (-1.13), ls='-.', C='r')

    ax2.plot(img_index, np.ones_like(path_to_vru_dist) * 1.43, ls='--', C='k',
             label='Warning/Unconf/PartBrake - predicted path')
    ax2.plot(img_index, np.ones_like(path_to_vru_dist) * (-1.43), ls='--', C='k')
    ax2.plot(img_index, path_to_vru_dist, label='VRU distance from path')
    plot_brake_pedal(ax2, img_index[pressed], img_index[released])

    # Add vertical lines at events where flags were turned on and off with comment regarding TTC at event
    colors_dict = {1: 'g', 2: 'b', 3: 'm', 4: 'c'}
    it = 1
    for name, flag in target.vru_flags.items():
        flag = flag[event_range]
        on, off = has_changed(flag)
        linewidth = 1
        if name == 'VRUWarning':
            linewidth = 2
        i_on, i_off = 0, 0  # Iterables used to remove duplicates from legend (when flags were flickering)
        for event_on in on:
            ax2.axvline(img_index[event_on], ls='-', C=colors_dict[it], lw=linewidth,
                        label=name + ' ON' if i_on == 0 else '')
            plt.text(img_index[event_on], 0, f'\nTTC= {np.around(ttc[event_on], 2)}s', rotation='vertical', fontsize=10,
                     bbox=dict(facecolor='gray', alpha=0.3), linespacing=0.3)
            i_on += 1
        for event_off in off:
            ax2.axvline(img_index[event_off], dashes=[5,5,5,5], C=colors_dict[it], lw=linewidth,
                        label=name + ' OFF' if i_off == 0 else '')
            plt.text(img_index[event_off], 0, f'\nTTC= {np.around(ttc[event_off], 2)}s', rotation='vertical',
                     fontsize=10, bbox=dict(facecolor='gray', alpha=0.3), linespacing=0.3)
            i_off += 1
        it += 1

    # Adjust subplot position
    box2 = ax2.get_position()
    ax2.set_position([box2.x0, box2.y0 + box2.height * 0.12, box2.width, box2.height*0.95])
    ax2.legend(fontsize=10, loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=4)
    ax2.set_xlabel('GrabIndex')
    ax2.set_ylabel('Distance [m]')
    ax2.set_title('VRU Distance from path')

    # plt.tight_layout(rect=(0, 0, 1, 0.95))
    # plt.savefig(os.path.join(out_path, logname + '.png'))
    print(f'Saving {logname}.png')
    # plt.close('all')
    plt.show()


def plot_in_predicted_path(mat, log_path, out_path=None, conf_plot=False):
    """
    Create subplots for test with crossing scenarios.\n
    Returns two subplots:
    \n#1 TTC and flags activation
    \n#2: VRU position in relation to host predicted path (ME: currSide, predSide)

    :param mat: mat file
    :param log_path: full path to mat file
    :param out_path: (Optional) path to directory where figures will be saved. If not specified, figure will be saved in
                      directory with mat file
    :return: matplotlib figure
    """
    vis = VisSignals(mat)
    if vis.obj_id == False and isinstance(vis.obj_id, bool):  # Two conditions. Obj_id may be 0 and still be valid!
        return  # No point doing anything else if no event was found
    vfp = VFPSignal(mat)
    my_path = Path(mat)
    event_range = np.arange(vis.start_event, vis.end_event)
    pressed, released = has_changed(vfp.brake_pedal[event_range])
    tgt_id = vis.obj_id

    # Get data for path plotting. Assume host is driving straight, and ideally perpendicular to target
    vru_lat_vel = vis.obj_signals['lat_vel'][event_range, tgt_id]
    vru_lat_pos = vis.obj_signals['lat_pos'][event_range, tgt_id]
    host_vel = vis.host_signals['vehSpeed'][event_range]
    vru_long_pos = vis.obj_signals['long_pos'][event_range][:,tgt_id] - vfp.ref_X_point  # Mind camera offset
    host_ttpoc = np.divide(vru_long_pos, host_vel,
                           out=np.full_like(host_vel, np.nan), where=host_vel!=0)  # TTPOC = Time To Point Of Collision
    vru_dist_to_travel = -vru_lat_vel * host_ttpoc

    vru_dist_from_path = my_path.get_distance_from_path(tgt_id, event_range)
    vru_pred_pos = vru_dist_to_travel + vru_dist_from_path

    ttc = vis.obj_signals['ttcAccel'][event_range, tgt_id]
    ttc[ttc > 5] = 5
    def get_ttc_from_ffs():
        # ////////////////// TO DO/////////////////////////
        pass

    img_index = vis.image_index[event_range]

    # ----------------- First Subplot --------------------
    f1, ax = plt.subplots(2, 1, figsize=(14, 9))
    ax1, ax2 = ax

    plt.suptitle(os.path.basename(log_path)[:-4])
    ax1.plot(img_index, ttc, label='Time To Collision')
    ax1.set_ylabel('TTC[s]')
    ax1.set_xlabel('GrabIndex')
    ax1.set_title('TTC vs Flag activation')
    plot_brake_pedal(ax1, img_index[pressed], img_index[released])

    for name, flag in vis.vru_flags.items():
        try:
            active_at_ttc = ttc[np.nonzero(flag[event_range])[0][0]]  # Get the ttc at 1st occurance of the flag
            active_at_ttc = np.around(active_at_ttc, 2)
        except IndexError:
            active_at_ttc = 0
        ax1.plot(img_index, flag[event_range], ls='--', label=name + f' TTC:{active_at_ttc}')

    # Adjust subplot position
    # box1 = ax1.get_position()
    # ax1.set_position([box1.x0, box1.y0 + box1.height * 0.12, box1.width, box1.height])

    # Adjust grid, add legend
    minor_locator_y = AutoMinorLocator(5)
    ax1.yaxis.set_minor_locator(minor_locator_y)
    minor_locator_x = AutoMinorLocator(2)
    ax1.xaxis.set_minor_locator(minor_locator_x)
    ax1.grid(which='minor', color='k', alpha=0.2)
    ax1.legend(fontsize=9)

    # --------------- Second Subplot ---------------
    ax2.plot(img_index, np.ones_like(vru_pred_pos) * (vfp.l_wheel + 0.2), ls='-.', C='b', label='Current Side(fullBrk)')
    ax2.plot(img_index, np.ones_like(vru_pred_pos) * (vfp.r_wheel - 0.2), ls='-.', C='b',)
    ax2.plot(img_index, np.ones_like(vru_pred_pos) * (vfp.l_wheel + 0.5), ls='-.', C='r', label='Current Side(other)')
    ax2.plot(img_index, np.ones_like(vru_pred_pos) * (vfp.r_wheel - 0.5), ls='-.', C='r')
    ax2.plot(img_index, np.ones_like(vru_pred_pos) * (vfp.r_wheel + 3.5), ls='-.', C='0.5',
             label='Crossing expand (fullBrk')
    ax2.plot(img_index, np.ones_like(vru_pred_pos) * (vfp.r_wheel - 3.5), ls='-.', C='0.5')
    ax2.plot(img_index, np.ones_like(vru_pred_pos) * (vfp.r_wheel + 5.5), ls='-.', C='m', label='Crossing expand(other)')
    ax2.plot(img_index, np.ones_like(vru_pred_pos) * (vfp.r_wheel - 5.5), ls='-.', C='m')
    ax2.scatter(img_index, vru_pred_pos, c='g', label='VRU predicted position', s=12)

    # Adjust y_limits and grid
    ax2.set_ylim(bottom=-6.5, top=6.5)
    ax2.xaxis.set_minor_locator(minor_locator_x)
    ax2.grid(which='minor', color='k', alpha=0.1)

    ax2.set_ylabel('Distance[m]')
    ax2.set_xlabel('GrabIndex')
    ax2.set_title('VRU position in relation to predicted path')
    ax2.legend()

    plt.tight_layout(h_pad=0.5, w_pad=1, rect=(0, 0, 1, 0.97))
    if out_path:
        plt.savefig(os.path.join(out_path, os.path.basename(log_path)[:-4] + '_conf.png'))
    else:
        plt.savefig(log_path[:-4] + '_conf.png')
    plt.show()

    plt.close('all')


def confidence_plot(mat, log_path, out_path=None):
    vis = VisSignals(mat)
    if vis.obj_id == False and isinstance(vis.obj_id, bool):  # Two conditions. Obj_id may be 0 and still be valid!
        return  # No point doing anything else if no event was found
    vfp = VFPSignal(mat)
    fus_data = Fusion(mat)
    event_range = np.arange(vis.start_event, vis.end_event)
    pressed, released = has_changed(vfp.brake_pedal[event_range])
    tgt_id = vis.obj_id
    img_index = vis.image_index[event_range]

    f1, ax = plt.subplots(4, 1, figsize=(14, 9))
    ax1, ax2, ax3, ax4 = ax
    plt.suptitle(os.path.basename(log_path)[:-4])

    # -------------First plot --------------------------
    try:
        fus_det = np.argwhere(fus_data.cmbb_signals['visTrkID'] == tgt_id+1)  # fusion detection
        grab_index = fus_data.grabIndex[fus_det[:,0]]
        ax1.plot(grab_index, fus_data.cmbb_signals['fus_source'][fus_det[:,0], fus_det[:,1]], label='fusion_source')
    except Exception as err:
        print('Fusion_ID not found\n', err)
    ax1.set_title('Fusion Source')
    ax1.set_xlabel('GrabIndex')

    # ------------- Second plot -------------------------
    try:
        fus_det = np.argwhere(fus_data.cmbb_signals['visTrkID'] == tgt_id+1)  # fusion detection
        grab_index = fus_data.grabIndex[fus_det[:,0]]
        ax2.plot(grab_index, fus_data.cmbb_signals['cmbb_conf'][fus_det[:,0], fus_det[:,1]], label='CMbB Oonfidence')
    except Exception as err:
        print('Fusion_ID not found\n', err)
    ax2.set_title('CMbB Confidence')
    ax2.set_ylabel('Confidence')
    ax2.set_xlabel('GrabIndex')

    # ------------ Third plot -----------------------
    for i in range(5):
        ax3.plot(img_index, vis.obj_signals['tlet_conf'][event_range, tgt_id, i], label=f'FlrId: {str(i+1)}')
    ax3.legend(loc=1, prop={'size':8})
    ax3.set_yticks(range(6))
    ax3.set_ylabel('confidence')
    ax3.set_title('Tracklet confidence')
    ax3.set_xlabel('GrabIndex')

    # ------------- Fourth plot -------------------------
    try:
        fus_det = np.argwhere(fus_data.cmbb_signals['visTrkID'] == tgt_id+1)  # fusion detection
        grab_index = fus_data.grabIndex[fus_det[:,0]]
        ax4.plot(grab_index, fus_data.cmbb_signals['fcw_conf'][fus_det[:,0], fus_det[:,1]], label='FCW Oonfidence')
    except Exception as err:
        print('Fusion_ID not found\n', err)
    ax4.set_title('FCW Confidence')
    ax4.set_ylabel('Confidence')
    ax4.set_xlabel('GrabIndex')

    plt.tight_layout(h_pad=1.2, w_pad=1.1, rect=(0, 0, 1, 0.97))
    if out_path:
        plt.savefig(os.path.join(out_path, os.path.basename(log_path)[:-4] + '_conf2.png'))
    else:
        plt.savefig(log_path[:-4] + '_conf2.png')
    # plt.show()
    print('\n/// DONE///\n')
    plt.close('all')
# ----------- Current path ----------

# matlist=glob.glob("Z:\JIRA\Crossing\*mat")
# for matfile in matlist:
#     in_path = r"Z:\EuNCAP\s412_EuNCAP\s412_long_ncap"
#     out_path = r"F:\ADAS-1901\figures"
#     mat = dtb.loadmat(os.path.join(in_path, matfile + '.mat'), sort=True)
#     # mat = dtb.loadmat(matfile, sort=True)
#     print('-------------------------------------------------')
#     print(f'Processing {matfile}')
#     # plot_signals(mat, matfile, out_path)
#     try:
#         # plot_signals(mat, matfile, out_path)
#         plot_in_current_path(mat, matfile, out_path, vru_type='ped')
#     except Exception as err:
#         print(err)

# matfile = "KR6N086_FTP112_TC9_20180709_164506_022"
# # matfile = "KR6N086_FTP112_TC9_20180709_164506_019"
# in_path = r"Z:\EuNCAP\s412_EuNCAP\s412_long_ncap"
# out_path = r"F:\ADAS-1901\figures"
# mat = dtb.loadmat(os.path.join(in_path, matfile + '.mat'), sort=True)
# plot_in_current_path(mat, matfile, out_path, vru_type='bic')


# ----------------------------- PREDICTED PATH -------------------------

# mat_name = "KR6N086_FTP112_TC8_20180710_105309_002"
# in_path = r"Z:\JIRA\Crossing"
# mat_path = os.path.join(in_path, mat_name + '.mat')
# out_path = r"F:\ADAS-1901\figures"
# mat = dtb.loadmat(mat_path, sort=True)
# plot_in_predicted_path(mat, mat_path, out_path)

matlist=glob.glob(r"E:\EuNCAP_s414\NCAP_20180917\*mat")

output_dir = os.path.join(r'E:\EuNCAP_s414\NCAP_20180917', 'plots_ped')
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
for matfile in matlist:
    # out_path = r"F:\ADAS-1901\figures"
    # mat = dtb.loadmat(os.path.join(in_path, matfile + '.mat'), sort=True)

    print('-------------------------------------------------')
    print(f'Processing {matfile}')
    # plot_signals(mat, matfile, out_path)
    try:
        mat = dtb.loadmat(matfile, sort=True)
        confidence_plot(mat, matfile, output_dir)
        # plot_in_predicted_path(mat, matfile, output_dir)
    except Exception as err:
        # print(err)
        traceback.print_exc()
        continue
