class __limit_len_list__(list):
    _MAX_len = None
    extend_retain: bool = False
    ignore_error: bool = False
    no_prompt: bool = False

    class OverMaxLengthError(Exception):
        def __init__(self, message):
            super().__init__(message)

    def setMAXlength(self, length: int):
        if not isinstance(length, int):
            raise TypeError("Not an int type!")
        elif length < 0:
            raise ValueError("Max_len can't be less than 0!")
        self._MAX_len = length

    def disableMAXlength(self):
        self._MAX_len = None

    def append(self, __object):
        if self._MAX_len is not None:
            if len(self) >= self._MAX_len:
                if self.ignore_error:
                    if self.no_prompt:
                        return
                    else:
                        print(f"More than MAX_len! ({self._MAX_len})")
                else:
                    raise self.OverMaxLengthError(f"More than MAX_len! ({self._MAX_len})")
            else:
                super().append(__object)
        else:
            super().append(__object)

    def insert(self, __index, __object):
        if self._MAX_len is not None:
            if len(self) >= self._MAX_len:
                if self.ignore_error:
                    if self.no_prompt:
                        return
                    else:
                        print(f"More than MAX_len! ({self._MAX_len})")
                else:
                    raise self.OverMaxLengthError(f"More than MAX_len! ({self._MAX_len})")
            else:
                super().insert(__index, __object)
        else:
            super().insert(__index, __object)

    def extend(self, __iterable):
        if not hasattr(__iterable, '__len__'):
            raise TypeError(f"{type(__iterable)} object is not iterable")

        if self._MAX_len is not None:

            if len(self) >= self._MAX_len:
                if self.ignore_error:
                    if self.no_prompt:
                        return
                    else:
                        print(f"More than MAX_len! ({self._MAX_len})")
                else:
                    raise self.OverMaxLengthError(f"More than MAX_len! ({self._MAX_len})")

            elif len(__iterable)+len(self) > self._MAX_len:
                if self.extend_retain:
                    if self.no_prompt:
                        if isinstance(__iterable, list):
                            _temp = __iterable.copy()
                            _temp = _temp[:self._MAX_len - len(self):]
                            super().extend(_temp)
                            return
                        else:
                            super().extend(__iterable[:self._MAX_len - len(self):])
                            return
                    else:
                        print(f"OverMaxLength: {self._MAX_len}, (summation: {len(self)+len(__iterable)})! elements are already reserved")
                        if isinstance(__iterable, list):
                            _temp = __iterable.copy()
                            _temp = _temp[:self._MAX_len - len(self):]
                            super().extend(_temp)
                            return
                        else:
                            super().extend(__iterable[:self._MAX_len - len(self):])
                            return
                elif self.ignore_error:
                    if self.no_prompt:
                        return
                    else:
                        print(f"The len of __iterable add the len of self is More than MAX_len! MAX_len: {self._MAX_len}, summation: {len(self)+len(__iterable)}")

            else:
                super().extend(__iterable)
        else:
            super().extend(__iterable)
