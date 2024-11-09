from .other_method_part import other_method_part


class reservation_part(other_method_part):

    def __repr__(self):
        if not self.normal_print and self._reservation_dic and self.reservation:
            original = super().__repr__()
            original = original[:len(original) - 1] + ', '
            original += str(self._reservation_dic)[1:]
            return original[:len(original) - 1] + ']'
        else:
            return super().__repr__()

    def __str__(self):
        if not self.normal_print and self._reservation_dic and self.reservation:
            original = super().__str__()
            original = original[:len(original) - 1] + ', '
            original += str(self._reservation_dic)[1:]
            return original[:len(original) - 1] + ']'
        else:
            return super().__str__()

    def append(self, item):
        if self.reservation and self._reservation_dic:
            _temp = min(self._reservation_dic.keys())
            if len(self) == _temp:
                super().append(self._reservation_dic.get(_temp))
                self._reservation_dic.pop(_temp)
                self.append(item)
                return

        super().append(item)

    def insert(self, __index: int, __object):
        if self.reservation:
            _temp = min(self._reservation_dic.keys())
            if len(self) == _temp:
                super().append(self._reservation_dic.get(_temp))
                if __index >= len(self):
                    super().append(__object)
                else:
                    super().insert(__index, __object)
                self._reservation_dic.pop(_temp)
                return

        super().insert(__index, __object)

    def extend(self, iterable):
        if self.reservation:
            def find_keys_less_than(num: int, my_dict: dict) -> list:
                return [key for key in my_dict if isinstance(key, int) and key < num]

            sum_len = len(self)+len(iterable)-1
            conform_lst = find_keys_less_than(sum_len, self._reservation_dic)
            if not conform_lst:
                super().extend(iterable)
            else:
                for item in iterable:
                    self.append(item)
        else:
            super().extend(iterable)
