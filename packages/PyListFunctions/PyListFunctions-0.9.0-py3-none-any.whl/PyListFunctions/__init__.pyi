from typing import Any, List, Literal, overload


# list func

def get_type_lst(lst: list | Any) -> list: pass

def tidy_up_list(lst: list, bool_mode: bool = False, eval_mode: bool = False, float_mode: bool = False,
                 int_mode: bool = False, none_mode: bool = False) -> list: pass

def deeply_tidy_up_list(lst: list) -> list: ...

def bubble_sort(lst: List[int], if_round: bool = False, in_reverse_order: bool = False) -> list: pass

def list_calculation(*args: List[int] | List[List[int]], calculation: str = Literal["+", "-", "*", "/", "//", "%"], multi_calculation: str = "", nesting: bool = False) -> list: pass

def in_list_calculation(lst: list[int], calculation: str = "+", multi_calculation: str = "") -> int | float | list: pass

def var_in_list(lst: list, __class: type, return_lst: bool = False, only_return_lst: bool = False) -> int | tuple | list: pass

def csv_to_lst_or_dic(csv, dict_mode: bool = False): pass

def len_sorted_lst(lst: list, reverse: bool = False, filtration: bool = True) -> list: pass

def populate_lsts(*args: List, _type: int = 0, nesting: bool = False) -> None: pass

def list_internal_situation(lst: list) -> None: pass

def remove_nesting(lst: list) -> list: pass

def uniformly_slice_list(lst: list, num_parts: int) -> list: pass

def slice_two_dimensional_list(lst: list) -> list: pass

def location_moving(lst: list, offset: int) -> list: pass

# str func

def replace_str(string: str, __c: str, __nc: str = '', num: int = 0, __start: int = 0, __end: int = None) -> str: pass

def randstr(length: int, *, use_symbol: bool = False, without_character: bool = False) -> str: pass

def reverse_str(string: str) -> str: pass

def statistics_str(string: str) -> tuple: pass

def find_list(lst: list, __fc: str, start: bool = False, mid: bool = False, end: bool = False) -> list: pass


# bool func

def can_variable(string: str) -> bool: pass


# other


@overload
def nrange(stop: int) -> int:
    """
    An easy func to get the frequency of range
    :param stop:
    :return:
    """
    pass

@overload
def nrange(start: int, stop: int) -> int:
    """
    An easy func to get the frequency of range
    :param start:
    :param stop:
    :return:
    """
    pass

@overload
def nrange(start: int, stop: int, step: int) -> int:
    """
    An easy func to get the frequency of range
    :param start:
    :param stop:
    :param step:
    :return:
    """
    pass
