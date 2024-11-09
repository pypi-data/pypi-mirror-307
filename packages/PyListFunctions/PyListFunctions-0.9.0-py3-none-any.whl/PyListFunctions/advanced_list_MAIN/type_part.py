from .. import advanced_list_EXTRA
from typing import Any
__all__ = ['type_part']


class type_part(advanced_list_EXTRA.reservation_part):

    def __setitem__(self, index, value):
        if type(value) not in self.type_lst and self.type_lst != [Any] and self.use_type:
            if not self.ignore_error:
                raise TypeError(
                    f"The types of elements in this list is: {self.type_lst}, The value you want to change: {repr(value)}, type of value: {type(value)}, method: __setitem__")
            elif self.ignore_error and not self.no_prompt:
                print(f"The types of elements in this list is: {self.type_lst}, The value you want to change: {repr(value)}, type of value: {type(value)}, method: __setitem__")
                return
        super().__setitem__(index, value)

    def append(self, item):
        if type(item) not in self.type_lst and self.type_lst != [Any] and self.use_type:
            if not self.ignore_error:
                raise TypeError(
                    f"The types of elements in this list is: {self.type_lst}, The value you want to change: {repr(item)}, type of value: {type(item)}, method: append")
            elif self.ignore_error and not self.no_prompt:
                print(f"The types of elements in this list is: {self.type_lst}, The value you want to change: {repr(item)}, type of value: {type(item)}, method: append")
            elif self.ignore_error and self.no_prompt:
                pass
        else:
            super().append(item)

    def extend(self, iterable):
        if not self.use_type:
            super().extend(iterable)
            return
        for self._i in range(len(iterable)):
            if type(list(iterable)[self._i]) not in self.type_lst and self.type_lst != [Any]:
                if not self.ignore_error:
                    raise TypeError(
                        f"The types of elements in this list is: {self.type_lst}, The value you want to change: {repr(iterable)}, type of value: {type(iterable)}, method: extend")
                elif self.ignore_error and not self.no_prompt:
                    print(
                        f"The types of elements in this list is: {self.type_lst}, The value you want to change: {repr(iterable)}, type of value: {type(iterable)}, method: extend")
                    return
                elif self.ignore_error and self.no_prompt:
                    pass
        super().extend(iterable)

    def insert(self, __index: int, __object):
        if type(__object) not in self.type_lst and self.type_lst != [Any] and self.use_type:
            if not self.ignore_error:
                raise TypeError(
                    f"The types of elements in this list is: {self.type_lst}, The value you want to change: {repr(__object)}, type of value: {type(__object)}, method: insert")
            elif self.ignore_error and not self.no_prompt:
                print(f"The types of elements in this list is: {self.type_lst}, The value you want to change: {repr(__object)}, type of value: {type(__object)}, method: insert")
            elif self.ignore_error and self.no_prompt:
                pass
        else:
            super().insert(__index, __object)
