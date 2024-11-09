from typing import Any
__all__ = ['__type_list__']


class __type_list__(list):

    @staticmethod
    def __get_type_lst(lst) -> list:
        """
        Get the types of elements in this list
        :param lst:
        :return:
        """
        if not isinstance(lst, list):
            return [type(lst)]

        result_lst: list = []

        if len(lst) == 0:
            return [Any]

        for _i in range(len(lst)):
            if type(lst[_i]) is type:
                result_lst.append(lst[_i])
            else:
                result_lst.append(type(lst[_i]))
        return list(set(result_lst))

    def _check(self) -> None:
        self._i2: int = 0
        try:
            for self._i in range(0, len(self)):
                if type(self[self._i2]) not in self.type_lst:
                    self.remove(self[self._i2])
                    self._i2 -= 1
                self._i2 += 1
        except IndexError:
            pass

    def __init__(self, *args, **kwargs):
        self._i = None
        self._type_dic = {}
        self.type_lst = []
        self.ignore_error: bool = bool(kwargs.get("ignore_error"))
        self.no_prompt: bool = bool(kwargs.get("no_prompt"))
        self.retain: bool = False
        if kwargs.get("retain"):
            self.retain = True
        _t = kwargs.get("type")
        self._None_t = False
        self._B_T_arg = False

        if args != () and len(args) == 1 and isinstance(list(args)[0], list):
            super().__init__(list(args)[0])
            self._B_T_arg = True
            self._T_arg = list(args)[0]
        else:
            super().__init__(args)

        if _t is None:
            self._None_t = True
        if isinstance(_t, list):
            if len(_t) > 0:
                for _i in range(len(_t)):
                    if not (type(_t[_i]) is type):
                        self._type_dic[_i] = type(_t[_i])
                    else:
                        self._type_dic[_i] = _t[_i]
            else:
                self._type_dic[0] = Any
        else:
            if self._B_T_arg:
                self.type_lst = self.__get_type_lst(self._T_arg)
            else:
                self.type_lst = self.__get_type_lst(list(args))
        if not self._None_t:
            for _i in range(len(self._type_dic)):
                self.type_lst.append(self._type_dic[_i])

        if not self.retain:
            self._check()

    def type(self, _t):
        if _t is None:
            _t = self
        self.type_lst = self.__get_type_lst(_t)

        if not self.retain:
            self._check()

    def __class_getitem__(cls, item):
        """
        Only use for define function\n
        for example:\n
        def func() -> type_list[type1, type2, ..., typeN]: pass
        """
        pass

    def __setitem__(self, index, value):
        if type(value) not in self.type_lst and self.type_lst != [Any]:
            if not self.ignore_error:
                raise TypeError(
                    f"The types of elements in this list is: {self.type_lst}, The value you want to change: {repr(value)}, type of value: {type(value)}, method: __setitem__")
            elif self.ignore_error and not self.no_prompt:
                print(
                    f"The types of elements in this list is: {self.type_lst}, The value you want to change: {repr(value)}, type of value: {type(value)}, method: __setitem__")
            elif self.ignore_error and self.no_prompt:
                pass
        else:
            super().__setitem__(index, value)

    def append(self, item):
        if type(item) not in self.type_lst and self.type_lst != [Any]:
            if not self.ignore_error:
                raise TypeError(
                    f"The types of elements in this list is: {self.type_lst}, The value you want to change: {repr(item)}, type of value: {type(item)}, method: append")
            elif self.ignore_error and not self.no_prompt:
                print(
                    f"The types of elements in this list is: {self.type_lst}, The value you want to change: {repr(item)}, type of value: {type(item)}, method: append")
            elif self.ignore_error and self.no_prompt:
                pass
        else:
            super().append(item)

    def extend(self, iterable):
        if type(iterable) not in self.type_lst and self.type_lst != [Any]:
            if not self.ignore_error:
                raise TypeError(
                    f"The types of elements in this list is: {self.type_lst}, The value you want to change: {repr(iterable)}, type of value: {type(iterable)}, method: extend")
            elif self.ignore_error and not self.no_prompt:
                print(
                    f"The types of elements in this list is: {self.type_lst}, The value you want to change: {repr(iterable)}, type of value: {type(iterable)}, method: extend")
            elif self.ignore_error and self.no_prompt:
                pass
        else:
            super().extend(iterable)
