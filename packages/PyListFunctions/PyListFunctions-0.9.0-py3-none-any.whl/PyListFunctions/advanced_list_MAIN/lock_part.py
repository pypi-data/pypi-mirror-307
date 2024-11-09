from .type_part import type_part
__all__ = ['lock_part']


class lock_part(type_part):
    def __setitem__(self, index, value):
        if self._lock_all:
            if self.ignore_error:
                if not self.no_prompt:
                    print("All element is locked!, method: __setitem__")
            else:
                raise self.LockError("All element is locked!, method: __setitem__")

        if index in self._lock_lst:
            if self.ignore_error:
                if not self.no_prompt:
                    print("This element is locked!, method: __setitem__")
            else:
                raise self.LockError("This element is locked!, method: __setitem__")

        super().__setitem__(index, value)

    def append(self, item):
        if not self.writable:
            if self.ignore_error:
                if not self.no_prompt:
                    print("Not writable!, method: append")
                return
            else:
                raise self.LockError("Not writable!, method: append")
        super().append(item)

    def extend(self, iterable):
        if not self.writable:
            if self.ignore_error:
                if not self.no_prompt:
                    print("Not writable!, method: extend")
                return
            else:
                raise self.LockError("Not writable!, method: extend")
        super().extend(iterable)

    def insert(self, __index: int, __object):
        if not self.writable:
            if self.ignore_error:
                if not self.no_prompt:
                    print("Not writable!, method: insert")
                return
            else:
                raise self.LockError("Not writable!, method: insert")

        super().insert(__index, __object)
        if len(self._lock_lst) != 0:
            if 0 <= __index < self._lock_lst[0]:
                self._lock_check2()
            elif __index > self._lock_lst[0]:
                self._lock_check(__index)

    def pop(self, __index=None):
        if self._lock_all:
            if self.ignore_error:
                if not self.no_prompt:
                    print("All element is locked!, method: pop")
                return
            else:
                raise self.LockError("All element is locked!, method: pop")
        if __index in self._lock_lst:
            if self.ignore_error:
                if not self.no_prompt:
                    print("This element is locked!, method: pop")
            else:
                raise self.LockError("This element is locked!, method: pop")
        else:
            if __index is None:
                return super().pop()
            else:
                super().pop(__index)
            if len(self._lock_lst) != 0:
                if 0 <= int(__index) < self._lock_lst[0]:
                    self._lock_check2()
                elif __index > self._lock_lst[0]:
                    self._lock_check(int(__index))

    def remove(self, __value):
        if self._lock_all:
            if self.ignore_error:
                if not self.no_prompt:
                    print("All element is locked!, method: remove")
                return
            else:
                raise self.LockError("All element is locked!, method: remove")
        self._tmp_find_int = super().index(__value)
        if self._tmp_find_int in self._lock_lst:
            if self._tmp_find_int in self._lock_lst:
                if self.ignore_error:
                    if not self.no_prompt:
                        print("This element is locked!, method: remove")
                else:
                    raise self.LockError("This element is locked!, method: remove")
        else:
            super().remove(__value)
            if len(self._lock_lst) != 0:
                if self._tmp_find_int == 0:
                    self._lock_check2()
                elif self._tmp_find_int > self._lock_lst[0]:
                    self._lock_check(self._tmp_find_int)
                else:
                    self._lock_check2()

    def clear(self):
        if self._lock_all:
            if self.ignore_error:
                if not self.no_prompt:
                    print("All element is locked!, method: clear")
                return
            else:
                raise self.LockError("All element is locked!, method: clear")
        if len(self._lock_lst) == 0:
            super().clear()
            return
        else:
            self._lck_tmp_lst = []
            self._lck_tmp_lst2 = [_ for _ in range(len(self._lock_lst))]
            for self._i in range(len(self._lock_lst)):
                self._lck_tmp_lst.append(super().__getitem__(self._lock_lst[self._i]))
            super().clear()
            for self._i in range(len(self._lck_tmp_lst)):
                self.append(self._lck_tmp_lst[self._i])
            for self._i in range(len(self._lock_lst)):
                self._lock_lst[self._i] = self._lck_tmp_lst2[self._i]
            if not self.no_prompt:
                print("The locked element is already retained!")

    def sort(self, *, key=..., reverse=...):
        if len(self._lock_lst) != 0 or self._lock_all:
            if self.ignore_error:
                if not self.no_prompt:
                    print("Some elements is locked, The sort function cannot be called")
            else:
                raise self.LockError("Some elements is locked, The sort function cannot be called")
        else:
            super().sort(key=key, reverse=reverse)

    def reverse(self):
        if len(self._lock_lst) != 0 or self._lock_all:
            if self.ignore_error:
                if not self.no_prompt:
                    print("Some elements is locked, The reverse function cannot be called")
            else:
                raise self.LockError("Some elements is locked, The reverse function cannot be called")
        else:
            super().reverse()
