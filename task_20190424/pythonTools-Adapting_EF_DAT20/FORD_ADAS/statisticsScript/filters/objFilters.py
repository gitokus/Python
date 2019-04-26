class ObjFilters():
    def __init__(self):
        self._filters = []

    def prepare_filters(self, filter_list=None):
        self._filters = []
        methods_list = dir(self)
        i = 1
        names_dict = {}
        for m in methods_list:
            if m.startswith('_append_filter_') and (filter_list is None or int(m[15:]) in filter_list):
                names = eval('self.{}()'.format(m))
                names_dict[i] = names
        return names_dict

    def get_filters(self):
        return self._filters

    def get_filters_list(self):
        return self.prepare_filters()

    def _APPEND_TEMPLATE(self):
        """
        copy this function to create custom filters
        remember to change name to _append_filter_<no.>
        :return: list of filters (functions)
        """

        def template(*args):
            """
            args are single value conditions
            :param args:
            :return:
            """

            ### START YOUR CODE HERE ###
            # unroll arguments
            list, of, values, some_value= args
            ### END YOUR CODE HERE ###

            def f(dat, mat, index, mat_index, id, unique_id):
                ### START YOUR CODE HERE ###
                # general conditions
                general_info = [obj for obj in dat[index] if obj['objType'] == 'general'][0]
                if general_info != some_value:
                    return False, False, False, False
                ### END YOUR CODE HERE ###


                if id is not None:
                    dat_obj = [obj for obj in dat[index] if obj['objID'] == id]
                    is_id = bool(len(dat_obj))
                    if is_id:
                        dat_obj = dat_obj[0]
                else:
                    is_id = False

                if unique_id is not None:
                    mat_ids = mat['mudp']['vis']['vision_obstacles_info']['visObs']['uniqueID'][mat_index]
                    is_unique_id = unique_id in mat_ids
                    if is_unique_id:
                        mat_col = list(mat_ids).index(unique_id)
                else:
                    is_unique_id = False

                if is_id:
                    ### START YOUR CODE HERE ###
                    # dat conditions
                    c1 = dat_obj['some_value'] == some_value
                    ### END YOUR CODE HERE ###
                else:
                    c1 = False

                if is_unique_id:
                    ### START YOUR CODE HERE ###
                    # mat conditions
                    c2 = mat['mudp']['vis']['vision_function_info'] == some_value
                    ### END YOUR CODE HERE ###
                else:
                    c2 = False

                return is_id, is_unique_id, c1, c2
            f.__name__ = '{}_{}_{}-{}'.format(list, of, values, some_value)
            return f

        ### START YOUR CODE HERE ###
        values_list_1 = ['Full Day', 'Early Morning / Evening', 'Night']
        values_list_2 = ['Car', 'Motocycle', 'Truck', 'Pedestrian', 'Cycle']
        ### END YOUR CODE HERE ###

        names_list = []
        for dt in values_list_1:
            for ot in values_list_2:
                f = template(dt, ot)
                self._filters.append(f)
                names_list.append(f.__name__)
        return names_list

    def _append_filter_1(self):
        """
        filters to cover forward in path object stats
        :return:
        """
        def template(*args):

            day_time, obj_type, mat_obj_type, dist_low, dist_high = args

            def f(dat, mat, index, mat_index, id, unique_id):
                # general conditions
                general_info = [obj for obj in dat[index] if obj['objType'] == 'general'][0]
                if general_info['infoDict']['timeOfDay'] != day_time:
                    return False, False, False, False

                if id is not None:
                    dat_obj = [obj for obj in dat[index] if obj['objID'] == id]
                    is_id = bool(len(dat_obj))
                    if is_id:
                        dat_obj = dat_obj[0]
                else:
                    is_id = False

                if unique_id is not None:
                    mat_ids = mat['mudp']['vis']['vision_obstacles_info']['visObs']['uniqueID'][mat_index]
                    is_unique_id = unique_id in mat_ids
                    if is_unique_id:
                        mat_col = list(mat_ids).index(unique_id)
                else:
                    is_unique_id = False

                if is_id:
                    # dat conditions
                    type = dat_obj['infoDict']['type'] == obj_type
                    visibility = dat_obj['infoDict']['visibility'] == '100%'
                    try:
                        delayed_visibility = [obj for obj in dat[index - 24] if obj['objID'] == id][0][
                                                 'infoDict']['visibility'] == '100%'
                    except:
                        delayed_visibility = False
                    if is_unique_id:
                        distance = dist_low < mat['mudp']['vis']['vision_obstacles_info']['visObs']['long_pos'][
                            mat_index][mat_col] < dist_high
                    else:
                        distance = dist_low < dat_obj['infoDict']['distance'] < dist_high
                    relevancy = dat_obj['infoDict']['relevancy'] == 'Main Object'
                    c1 = visibility and delayed_visibility and type and distance and relevancy
                else:
                    c1 = False

                if is_unique_id:
                    # mat conditions
                    type = mat['mudp']['vis']['vision_obstacles_info']['visObs']['obstacle_class'][mat_index][
                               mat_col] == mat_obj_type
                    long_pos = dist_low < \
                               mat['mudp']['vis']['vision_obstacles_info']['visObs']['long_pos'][mat_index][
                                   mat_col] < dist_high
                    vis_id = mat['mudp']['vis']['vision_obstacles_info']['visObs']['id'][mat_index][mat_col]
                    cipo = mat['mudp']['vis']['vision_function_info']['visOnlyVehCIPO'][mat_index]
                    c2 = type and long_pos and vis_id == cipo
                    if is_id:
                        c2 = c2 and visibility and delayed_visibility
                    elif id is None:
                        c2 = False
                else:
                    c2 = False

                return is_id, is_unique_id, c1, c2
            f.__name__ = '{}_{}_{}-{}'.format(day_time, obj_type, dist_low, dist_high)
            return f

        day_time_list = ['Full Day', 'Early Morning / Evening', 'Night']
        obj_type_list = ['Car', 'Motocycle', 'Truck']
        mat_obj_type_list = [1, 2, 3]
        dists = [0, 10, 30, 60]

        names_list = []
        for dt in day_time_list:
            for ot, m_ot in zip(obj_type_list, mat_obj_type_list):
                for i in range(len(dists) - 1):
                    f = template(dt, ot, m_ot, dists[i], dists[i+1])
                    self._filters.append(f)
                    names_list.append(f.__name__)
        return names_list

    # def _append_filter_2(self):
    #     """
    #     filters to cover pedestrians
    #     :return:
    #     """
    #     def template(*args):
    #         day_time, obj_type, mat_obj_type, dist_low, dist_high = args
    #         def f(dat, mat, index, mat_index, id, unique_id):
    #             # general conditions
    #             general_info = [obj for obj in dat[index] if obj['objType'] == 'general'][0]
    #             if general_info['infoDict']['timeOfDay'] != day_time:
    #                 return False, False, False, False
    #
    #             if id is not None:
    #                 dat_obj = [obj for obj in dat[index] if obj['objID'] == id]
    #                 is_id = bool(len(dat_obj))
    #                 if is_id:
    #                     dat_obj = dat_obj[0]
    #             else:
    #                 is_id = False
    #
    #             if unique_id is not None:
    #                 mat_ids = mat['mudp']['vis']['vision_obstacles_info']['visObs']['uniqueID'][mat_index]
    #                 is_unique_id = unique_id in mat_ids
    #                 if is_unique_id:
    #                     mat_col = list(mat_ids).index(unique_id)
    #             else:
    #                 is_unique_id = False
    #
    #             if is_id:
    #                 # dat conditions
    #                 type = dat_obj['infoDict']['type'] == obj_type
    #                 if is_unique_id:
    #                     distance = dist_low < mat['mudp']['vis']['vision_obstacles_info']['visObs']['long_pos'][
    #                         mat_index][mat_col] < dist_high
    #                 else:
    #                     distance = dist_low < dat_obj['infoDict']['distance'] < dist_high
    #                 relevancy = dat_obj['infoDict']['relevancy'] == 'Main Object'
    #                 c1 = type and distance and relevancy
    #             else:
    #                 c1 = False
    #
    #             if is_unique_id:
    #                 # mat conditions
    #                 type = mat['mudp']['vis']['vision_obstacles_info']['visObs']['obstacle_class'][mat_index][
    #                            mat_col] == mat_obj_type
    #                 long_pos = dist_low < \
    #                            mat['mudp']['vis']['vision_obstacles_info']['visObs']['long_pos'][mat_index][
    #                                mat_col] < dist_high
    #                 id = mat['mudp']['vis']['vision_obstacles_info']['visObs']['id'][mat_index][mat_col]
    #                 cipo = mat['mudp']['vis']['vision_function_info']['visOnlyVehCIPO'][mat_index]
    #                 c2 = type and long_pos and id == cipo
    #             else:
    #                 c2 = False
    #
    #             return is_id, is_unique_id, c1, c2
    #         f.__name__ = '{}_{}_{}-{}'.format(day_time, obj_type, dist_low, dist_high)
    #         return f
    #
    #     day_time_list = ['Full Day', 'Early Morning / Evening', 'Night']
    #     obj_type_list = ['Car', 'Motocycle', 'Truck']
    #     mat_obj_type_list = [1, 2, 3]
    #     dists = [0, 10, 30, 60]
    #
    #     names_list = []
    #     for dt in day_time_list:
    #         for ot, m_ot in zip(obj_type_list, mat_obj_type_list):
    #             for i in range(len(dists) - 1):
    #                 f = template(dt, ot, m_ot, dists[i], dists[i+1])
    #                 self._filters.append(f)
    #                 names_list.append(f.__name__)
    #     return names_list
