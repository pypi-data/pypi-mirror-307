"""def replace_scrapped(self, __o_obj=None, __n_obj: Any = None, start: int = 0, end: int = None, step: int = 1, None_mode: bool = False):
        """'''Replace the elements in list.

        (When the __o_obj is None, all elements in the start to end range are replaced (locked elements are not deleted))

        (When the __n_obj is None, the original element is deleted)

        (If the element is locked, it is retained)
        :param __o_obj: original element
        :param __n_obj: new element
        :param start: the index of start
        :param end: the index of end
        :param step: the step of range
        :param None_mode: if you want to replace the none to other, please open this mode'''"""

        if self._lock_all:
            if self.ignore_error:
                if not self.no_prompt:
                    print("All elements is locked, The replace function cannot be called")
            else:
                raise self.LockError("All elements is locked, The replace function cannot be called")

        if step < 1:
            raise ValueError("step cannot less than 1")

        if end is None:
            end = len(self)
        elif not isinstance(end, int) or end > len(self):
            end = len(self)

        if start > end:
            raise ValueError("start cannot more than end")
        self._scope_of_impact = []
        self._scope_of_impact_element = 0
        self._i2 = start
        try:
            if __o_obj is None and not None_mode:
                for self._i in range(start, end, step):
                    if __n_obj is None:
                        if self._i2 not in self._lock_lst:
                            super().pop(self._i2)
                            self._scope_of_impact.append(self._i2)
                            self._scope_of_impact_element += 1
                            self._i2 -= step
                    else:
                        if self._i2 not in self._lock_lst:
                            super().__setitem__(self._i2, __n_obj)
                    self._i2 += step
            else:
                for self._i in range(start, end, step):
                    if super().__getitem__(self._i2) is __o_obj:
                        if __n_obj is None:
                            if self._i2 not in self._lock_lst:
                                super().pop(self._i2)
                                self._scope_of_impact.append(self._i2)
                                self._scope_of_impact_element += 1
                                self._i2 -= step
                        else:
                            if self._i2 not in self._lock_lst:
                                super().__setitem__(self._i2, __n_obj)
                    self._i2 += step
            if len(self._scope_of_impact) != 0 and len(self._lock_lst) != 0:
                self._i = 0
                while self._scope_of_impact[0] > self._lock_lst.__getitem__(self._i):
                    self._i += 1
                self._i2 = len(self._lock_lst) - 1
                while self._scope_of_impact[len(self._scope_of_impact) - 1] > self._lock_lst.__getitem__(self._i2):
                    self._i2 -= 1
                for self._i3 in range(self._i, self._i2):
                    self._lock_lst[self._i3] -= self._scope_of_impact_element
        except IndexError:
            pass"""
