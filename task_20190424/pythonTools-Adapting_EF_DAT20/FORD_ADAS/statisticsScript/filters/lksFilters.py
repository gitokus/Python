class LksFilters():
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

    def get_filters_list(self, print_filters=False):
        names = self.prepare_filters()
        if print_filters:
            for key, value in names.items():
                print(key, end='')
                for i, v in enumerate(value):
                    print('\t', v)
        return names