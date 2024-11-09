from typing import Any, Dict, List, Optional, overload


# classes

class advanced_list(list):
    def __init__(self, *args, ignore_error: bool = False, no_prompt: bool = False, use_type: bool = False, type: list = List[type], lock_all: bool = False, writable: bool = False, reservation: bool = False,
                 reservation_dict: Dict[int: Any] = {int: Any}):
        """
        **This class inherits all the features of list !**

        Parameters:\n
        args: The value you want to assign a value to a list\n

        KeyWords:\n
        use_type (bool)\n
        (If the use_type is not True, the type parameter is invalid.)\n
        type [type1, type2..., typeN]\n
        ignore_error (bool)\n
        no_prompt (bool)\n
        lock_all (bool)\n
        writable (bool)\n
        reservation (bool)\n
        reservation_dict (dict)
        """

        self._i = None
        self._i2 = None
        self._copy_self = None
        self._lock_lst = None
        self._lock_all: bool = bool(lock_all)
        self._tmp_lock_lst = None
        self._tmp_reservation_dic = None
        self._slice_lst = None
        if reservation_dict:
            self._reservation_dic = dict(reservation_dict)
        else:
            self._reservation_dic = {}

        self.type_lst: list = []
        self.writable: bool = bool(writable)
        self.use_type: bool = bool(use_type)
        self.reservation = bool(reservation)
        self.normal_print: bool = False
        self.ignore_error: bool = bool(ignore_error)
        self.no_prompt: bool = bool(no_prompt)

    def __getitem__(self, item) -> advanced_list | Any: ...

    # Type part

    def type(self, _t: list | Any = None) -> None:
        """
        ENG(translator):Re-determine the list of allowed variable types based on the types within the given parameters\n
        ZH CN：根据此形参（内）的类型来重新决定允许的变量类型的列表
        :param _t:
        :return:
        """
        pass

    # Lock part

    def lock(self, __index: int | List[int] = None, writable: bool = True) -> None:
        """
        ENG(translator): This Function will lock element in the list, if __index is None, all element will lock. Warning! sort function cannot use when locked.\n
        ZH CN：这个函数会把列表内__index下标的元素"上锁", 无法更改（如果__index为None，则上锁所有元素），当上锁时,sort将不能使用！
        :param __index: Ths subscript of element you want to lock
        :param writable: if False, then the append,insert,extend cannot work.
        :return:
        """
        pass

    class LockError(Exception):
        """The LockError Class."""
        pass

    def view_lock_list(self) -> list:
        """
        Return lock_list
        :return:
        """
        pass

    def unlock(self, __index: int | List[int] = None, writable: bool = True) -> None:
        """
        Unlock element.
        :param __index: Ths subscript of element you want to unlock
        :param writable: if False, then the append,insert,extend cannot work.
        :return:
        """
        pass

    # Reservation part

    @overload
    def modifyReservationElement(self, ReservationElementDict: Dict[int: Any] = {int: Any}) -> None:
        """
        Create or update the reservation element.
        :param ReservationElementDict:
        :return:
        """
        pass

    @overload
    def modifyReservationElement(self, _subscript: int, _obj: Any) -> None:
        """
        Create or update the reservation element.
        :param _subscript:
        :param _obj:
        :return:
        """
        pass

    def delReservationElement(self, _subscript: int) -> None:
        """
        delete the reservation element.
        :param _subscript:
        :return:
        """
        pass

    def clearReservationElement(self) -> None:
        """
        clear all the reservation elements.
        :return:
        """

    def view_reservation_dict(self) -> dict:
        """
        Return reservation_dict
        :return:
        """
        pass

    # Extra func

    def replace(self, __o_obj: Any = None, __n_obj: Any = None, start: int = 0, end: int = None, step: int = 1, None_mode_original: bool = False, None_mode_new_value: bool = False) -> None:
        """
        Replace the elements in list.

        (if all params are None, it will clear all elements!!!)

        (When the __o_obj is None, all elements in the start to end range are replaced (locked elements are not deleted))

        (When the __n_obj is None, the original element is deleted)

        (If the element is locked, it is retained)

        :param __o_obj: original element
        :param __n_obj: new element
        :param start: the index of start
        :param end: the index of end
        :param step: the step of range
        :param None_mode_original: if you want to replace the None to other, please open this mode
        :param None_mode_new_value: if you want to replace the value to None, please open this mode

        """
        pass

    def index_pro(self, item: Any, start: int = 0, end: int = None, first: bool = False) -> int | tuple:
        """
        Year, the index pro.
        Return index of value.
        Raises ValueError if the value is not present.
        :param item: The object you want to find
        :param start: The start index
        :param end: The end index
        :param first: only find the first index element
        :return:
        """
        pass

    def copy(self) -> 'advanced_list':
        pass

    def only_copy_list(self) -> list:
        """Return a shallow copy of the list."""
        pass

    def end(self) -> Optional[int]:
        """Return the subscript of last element."""
        pass

    def exchange(self, subscript1: int, subscript2: int) -> None:
        """Exchange the values of the two subscripts"""
        pass


class limit_len_list(list):
    """This class can control the length of list"""
    _MAX_len = None
    extend_retain = False
    ignore_error: bool = False
    no_prompt: bool = False

    class OverMaxLengthError(Exception):
        """The OverMaxLengthError class"""
        pass

    def setMAXlength(self, length: int):
        """Set the max length of list"""
        pass

    def disableMAXlength(self):
        """Disable the max length limit"""
        pass

    def copy(self) -> 'limit_len_list':
        """Return a shallow copy of the list."""

    def only_copy_list(self):
        """only copy the list instead of limit_len_list"""
        pass


# SCRAPPED
class type_list(list):
    def __init__(self, *args, **kwargs):
        self._i = None
        self._i2 = None
        self._type_dic = {}
        self.type_lst = []
        self.ignore_error: bool = bool(kwargs.get("ignore_error"))
        self.no_prompt: bool = bool(kwargs.get("no_prompt"))
        self.retain: bool = False
        if kwargs.get("retain"):
            self.retain = True
        self._t = kwargs.get("type")
        self._None_t = False
        self._B_T_arg = False
        self._T_arg = None
        pass

    @staticmethod
    def __get_type_lst(lst: list) -> list: ...

    def _check(self) -> None: ...

    def type(self, _t: list | Any = None) -> None:
        """
        ENG(translator):Re-determine the list of allowed variable types based on the types within the given parameters\n
        ZH CN：根据此形参（内）的类型来重新决定允许的变量类型的列表
        :param _t:
        :return:
        """
        pass