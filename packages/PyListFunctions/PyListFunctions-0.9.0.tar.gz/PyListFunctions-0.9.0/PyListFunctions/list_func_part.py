import gc
from typing import Any, Union


def get_type_lst(lst: Union[list, Any]):
    if not issubclass(type(lst), list):
        return [type(lst)]

    result_lst: list = []

    if len(lst) == 0 or object in lst:
        return [Any]

    for _i in range(len(lst)):
        if type(lst[_i]) is type:
            result_lst.append(lst[_i])
        else:
            result_lst.append(type(lst[_i]))
    return list(set(result_lst))


def tidy_up_list(lst: list, bool_mode: bool = False, eval_mode: bool = False, float_mode: bool = False,
                 int_mode: bool = False, none_mode: bool = False) -> list:

    # 判断是否是list类型，否则返回形参原本值
    if type(lst) is not list and not (len(lst) <= 0):
        return lst

    bool_mode = bool(bool_mode)
    eval_mode = bool(eval_mode)
    float_mode = bool(float_mode)
    int_mode = bool(int_mode)

    _lst_types: list = []
    _point_j: int = 0
    _point_l: list = []
    _str_app_l: list = []
    _type_content: dict = {'str': [], 'int': [], 'float': [], 'lst': [], 'dic': [], 'set': [], 'tuple': [],
                           'complex': [],
                           'None': []}

    # 保存原有特殊变量原本值
    for i in range(len(lst)):
        if isinstance(lst[i], str) and (lst[i] not in _type_content['str']):
            _type_content['str'].append(lst[i])

        if isinstance(lst[i], int) and (lst[i] not in _type_content['int']):
            _type_content['int'].append(lst[i])

        if isinstance(lst[i], float) and (lst[i] not in _type_content['float']):
            _type_content['float'].append(lst[i])

        if type(lst[i]) is None and (lst[i] not in _type_content['None']):
            _type_content['None'].append(lst[i])

        if type(lst[i]) is list and (lst[i] not in _type_content['lst']):
            _type_content['lst'].append(lst[i])

        if type(lst[i]) is dict and (lst[i] not in _type_content['dic']):
            _type_content['dic'].append(lst[i])

        if type(lst[i]) is set and (lst[i] not in _type_content['set']):
            _type_content['set'].append(lst[i])

        if type(lst[i]) is tuple and (lst[i] not in _type_content['tuple']):
            _type_content['tuple'].append(lst[i])
        if type(lst[i]) is complex and (lst[i] not in _type_content['complex']):
            _type_content['complex'].append(lst[i])

        lst[i] = str(lst[i])

    # 排序+去除重复值
    lst = list(set(lst))
    for i in range(len(lst)):
        lst[i] = str(lst[i])
    lst = sorted(lst, key=str.lower)

    # 判断列表值是何类型1
    for i in range(len(lst)):
        _point_l.append([])
        _str_app_l.append([])
        for j in lst[i]:
            if 48 <= ord(j) <= 57:
                continue
            elif j == '.':
                if not _point_l[i]:
                    _point_l[i].append(True)
                else:
                    continue
            else:
                if not _str_app_l[i]:
                    _str_app_l[i].append(True)
                else:
                    continue

    # 判断列表值是何类型2
    for i in range(len(_point_l)):
        if True in _str_app_l[i]:
            _lst_types.append('str')
        elif True in _point_l[i] and _str_app_l[i] == []:
            for j in range(len(lst[i])):
                if lst[i][j] == '.':
                    _point_j += 1
            if _point_j == 1:
                _lst_types.append('float')
                _point_j = 0
            else:
                _lst_types.append('str')
                _point_j = 0
        else:
            _lst_types.append('int')

    # 转换类型
    for i in range(len(_lst_types)):
        if _lst_types[i] == 'str':
            if eval_mode:
                try:
                    lst[i] = eval(lst[i])
                except:
                    pass
            pass
        try:
            if _lst_types[i] == 'float':
                lst[i] = float(lst[i])
            if _lst_types[i] == 'int':
                lst[i] = int(lst[i])
        except ValueError:
            pass

    # code burger(bushi     (将收集到的特殊数据插入回列表)
    for i in range(len(_type_content['complex'])):
        lst.remove(str(_type_content['complex'][i]))
        lst.append(_type_content['complex'][i])
    for i in range(len(_type_content['tuple'])):
        lst.remove(str(_type_content['tuple'][i]))
        lst.append(_type_content['tuple'][i])
    for i in range(len(_type_content['lst'])):
        lst.remove(str(_type_content['lst'][i]))
        lst.append(_type_content['lst'][i])
    for i in range(len(_type_content['set'])):
        lst.remove(str(_type_content['set'][i]))
        lst.append(_type_content['set'][i])
    for i in range(len(_type_content['dic'])):
        lst.remove(str(_type_content['dic'][i]))
        lst.append(_type_content['dic'][i])

    if bool_mode:
        for i in range(len(lst)):
            if lst[i] == 'True':
                lst[i] = bool(1)
            elif lst[i] == 'False':
                lst[i] = bool(0)

    del _lst_types, _point_j, _point_l, _str_app_l, _type_content
    gc.collect()

    return lst


def deeply_tidy_up_list(lst: list) -> list:

    if type(lst) is not list:
        return lst

    _j: int = 0
    lst = tidy_up_list(lst)

    for _i in lst:
        if type(_i) is list:
            lst[_j] = deeply_tidy_up_list(_i)
        _j += 1

    return lst


def bubble_sort(lst: list, if_round: bool = False, in_reverse_order: bool = False) -> list:

    if not issubclass(type(lst), list):
        return lst

    _i: int = 0
    if_round = bool(if_round)
    lst_T = lst.copy()

    for _i in range(len(lst_T)):
        if (not (isinstance(lst_T[_i], int) or isinstance(lst_T[_i], float))) or len(lst_T) == 0:
            return lst_T

    if if_round:
        try:
            from math import ceil
            for _i in range(len(lst_T)):
                if isinstance(lst_T[_i], float):
                    lst_T[_i] = ceil(lst_T[_i])
        except ImportError:
            def ceil() -> None:
                ceil()

            for _i in range(len(lst_T)):
                if isinstance(lst_T[_i], float):
                    lst_T[_i] = round(lst_T[_i])

    lst_len = len(lst_T)
    for _i in range(lst_len):
        for _j in range(lst_len - 1 - _i):
            if in_reverse_order:
                if lst_T[_j + 1] >= lst_T[_j]:
                    lst_T[_j], lst_T[_j + 1] = lst_T[_j + 1], lst_T[_j]
            else:
                if lst_T[_j + 1] <= lst_T[_j]:
                    lst_T[_j], lst_T[_j + 1] = lst_T[_j + 1], lst_T[_j]

    try:
        del _i, _j
    except UnboundLocalError:
        pass
    gc.collect()

    return lst_T


def list_calculation(*args: list, calculation: str = "+", multi_calculation: str = "", nesting: bool = False) -> list:
    def two_lsts_cala(lst: list, lst2: list, cala: str = "+") -> list:
        result: list = lst.copy()
        try:
            for i2 in range(len(lst if len(lst) > len(lst2) else lst2)):
                if cala == '+':
                    result[i2] += lst2[i2]
                elif cala == '-':
                    result[i2] -= lst2[i2]
                elif cala == '*':
                    result[i2] -= lst2[i2]
                elif cala == '**':
                    result[i2] -= lst2[i2]
                elif cala == '/':
                    result[i2] -= lst2[i2]
                elif cala == '//':
                    result[i2] -= lst2[i2]
                elif cala == '%':
                    result[i2] -= lst2[i2]
        except IndexError:
            if len(lst) < len(lst2):
                for i3 in range(len(lst2)-len(lst)):
                    result.append(lst2[len(lst)+i3])
            return result.copy()
        return result.copy()

    if len(args) <= 0 or len(calculation) <= 0:
        raise ValueError("No any list given")

    if len(calculation) > 1:
        raise ValueError("the length of calculation symbol can only be 1")

    if nesting:
        args = eval(str(args)[1:len(str(args)) - 2:])

    args = list(args)

    i: int = 0

    while i < len(args):
        if not issubclass(type(args[i]), list) or args[i] == []:
            args.remove(args[i])
            i -= 1
        else:
            args[i] = [element for element in args[i] if isinstance(element, int)]
        i += 1

    for_multi_calculation_sub: int = 0
    Result = args[0]
    if_multi_calculation: bool = False
    if len(multi_calculation) != 0:
        if_multi_calculation = True
        multi_calculation = multi_calculation[:len(args) - 1:]
        multi_calculation = multi_calculation.split(",")

    for i in range(len(args)-1):
        if for_multi_calculation_sub > len(multi_calculation)-1:
            for_multi_calculation_sub = 0
        Result = two_lsts_cala(Result, args[i + 1], cala=multi_calculation[for_multi_calculation_sub])
        for_multi_calculation_sub += 1

    return Result


def var_in_list(lst: list, __class: type, return_lst: bool = False, only_return_lst: bool = False) -> Union[int, tuple, list]:
    if return_lst and only_return_lst:
        raise ValueError("return_lst and only_return_lst cannot be True at the same time")

    def in_def_var_in_list(lst2: list, all_result=0, all_result_lst=None) -> Union[int, tuple, list]:
        if return_lst:
            if all_result_lst is None:
                all_result_lst = []
        elif only_return_lst:
            if all_result_lst is None:
                all_result_lst = []
        for _i in range(len(lst2)):
            if isinstance(lst2[_i], __class):
                if return_lst:
                    all_result += 1
                    all_result_lst.append(lst2[_i])
                elif only_return_lst:
                    all_result_lst.append(lst2[_i])
                else:
                    all_result += 1
            elif isinstance(lst2[_i], list):
                all_result, all_result_lst = in_def_var_in_list(lst2[_i], all_result, all_result_lst)
        if return_lst:
            return all_result, all_result_lst
        elif only_return_lst:
            return all_result_lst
        else:
            return all_result

    return_lst = bool(return_lst)
    result = in_def_var_in_list(lst)
    return result


def in_list_calculation(lst: list, calculation: str = "+", multi_calculation: str = "") -> Union[int, float, list]:

    import gc

    if not isinstance(lst, list):
        return lst.copy()

    nums_lst = var_in_list(lst, int, only_return_lst=True) + var_in_list(lst, float, only_return_lst=True)

    if not nums_lst:
        return lst.copy()
    else:
        result: int = nums_lst[0]
        if multi_calculation == "":
            result: int = nums_lst[0]
            nums_lst.pop(0)
            for _i in range(len(nums_lst)):
                if calculation == "+":
                    result += nums_lst[_i]
                elif calculation == "-":
                    result -= nums_lst[_i]
                elif calculation == "*":
                    result *= nums_lst[_i]
                elif calculation == "**":
                    result **= nums_lst[_i]
                elif calculation == "/":
                    result /= nums_lst[_i]
                elif calculation == "//":
                    result //= nums_lst[_i]
                elif calculation == "%":
                    result %= nums_lst[_i]
        else:
            lst_cal = multi_calculation.split(",")
            if len(lst_cal) > len(nums_lst) - 1:
                lst_cal = list(multi_calculation)[:len(nums_lst):]
            elif len(lst_cal) < len(nums_lst) - 1:
                lst_cal_copy = lst_cal.copy()
                lst_cal_copy_subscript: int = 0
                tmp_lst = [_ for _ in range(0, len(nums_lst), len(lst_cal))]
                for _i in range(len(nums_lst) - 1 - len(lst_cal)):
                    if _i in tmp_lst:
                        lst_cal_copy_subscript = 0
                    lst_cal.append(lst_cal_copy[lst_cal_copy_subscript])
                    lst_cal_copy_subscript += 1
            for _i in range(len(nums_lst)):
                if _i == 0:
                    continue
                if _i == len(lst_cal) + 1:
                    break
                if lst_cal[_i - 1] == "+":
                    result += nums_lst[_i]
                elif lst_cal[_i - 1] == "-":
                    result -= nums_lst[_i]
                elif lst_cal[_i - 1] == "*":
                    result *= nums_lst[_i]
                elif lst_cal[_i - 1] == "**":
                    result **= nums_lst[_i]
                elif lst_cal[_i - 1] == "/":
                    result /= nums_lst[_i]
                elif lst_cal[_i - 1] == "//":
                    result //= nums_lst[_i]
                elif lst_cal[_i - 1] == "%":
                    result %= nums_lst[_i]

    try:
        del nums_lst
        del lst_cal
        del lst_cal_copy, lst_cal_copy_subscript, tmp_lst
    except UnboundLocalError:
        pass
    gc.collect()

    return result


def csv_to_lst_or_dic(csv, dict_mode: bool = False) -> Union[list, dict, None]:

    try:
        import pandas as pd
    except ModuleNotFoundError:
        return

    if not isinstance(csv, pd.DataFrame):
        return

    dict_mode = bool(dict_mode)

    if not dict_mode:
        two_dimensional_arrays: list = []
        columns = csv.columns.tolist()
        rows = csv[columns]

        for _i in range(len(columns)):
            two_dimensional_arrays.append([])
            for _j in range(csv.shape[0]):
                two_dimensional_arrays[_i].append(str(rows.loc[_j, columns[_i]]))

        return two_dimensional_arrays

    else:
        _dict: dict = {}
        columns = csv.columns.tolist()
        rows = csv[columns]

        for _i in range(len(columns)):
            _dict.update({f"{columns[_i]}": []})
            for _j in range(csv.shape[0]):
                _dict[columns[_i]].append(str(rows.loc[_j, columns[_i]]))

        return _dict


def len_sorted_lst(lst: list, reverse: bool = False, filtration: bool = True) -> list:

    if not isinstance(lst, list):
        return lst.copy()
    else:
        lst_t = lst.copy()
        other_lst: list = []
        for _i in range(len(lst)):
            if not issubclass(type(lst[_i]), list) and filtration:
                other_lst.append(_i)
            elif not issubclass(type(lst[_i]), list) and not filtration:
                other_lst.append(lst[_i])
        if other_lst and filtration:
            other_lst = list(reversed(other_lst))
            for _i in range(len(other_lst)):
                lst_t.pop(other_lst[_i])
        elif other_lst and not filtration:
            for _i in range(len(other_lst)):
                lst_t.remove(other_lst[_i])

    len_dic: dict = {}
    len_lsts: list
    new_lst: list = []

    for _i in range(len(lst_t)):
        len_dic.update({_i: len(lst_t[_i])})

    if reverse:
        len_lsts = list(reversed(sorted(len_dic.items(), key=lambda x: x[1])))
    else:
        len_lsts = sorted(len_dic.items(), key=lambda x: x[1])

    for _i in range(len(len_lsts)):
        new_lst.append(lst_t[len_lsts[_i][0]])

    if not filtration:
        for _i in range(len(other_lst)):
            new_lst.append(other_lst[_i])

    return new_lst


def populate_lsts(*args, _type=0, nesting: bool = False) -> None:

    if bool(nesting):
        args = args[0]

    for _i in range(len(args)):
        if not issubclass(type(args[_i]), list):
            return

    len_dic: dict = {}
    len_lsts: list
    for _i in range(len(args)):
        len_dic.update({_i: len(args[_i])})

    len_lsts = list(reversed(sorted(len_dic.items(), key=lambda x: x[1])))
    for _i in range(len(len_lsts)):
        len_lsts[_i] = list(len_lsts[_i])

    for _i in range(len(len_lsts)):
        try:
            for _j in range(len_lsts[0][1] - len_lsts[_i + 1][1]):
                args[len_lsts[_i + 1][0]].append(_type)
        except IndexError:
            pass


def list_internal_situation(lst: list) -> None:

    in_index = []

    def in_list_internal_situation(lst2: list) -> None:
        nonlocal in_index

        def cur() -> None:
            print('->', end=" ")

        if not issubclass(type(lst2), list):
            return

        iter_lst = iter(lst2.copy())

        try:
            _i: int = 0
            while True:
                next(iter_lst)
                if in_index:
                    for _j in range(len(in_index)):
                        print("in index({})".format(in_index[_j]), end=" "), cur()
                print(f"{_i}", end=" "), cur(), print(f"value: {lst2[_i]}", end=" "), print(f"{type(lst2[_i])}")
                if isinstance(lst2[_i], list):
                    in_index.append(_i)
                    in_list_internal_situation(lst2[_i])
                _i += 1
        except StopIteration:
            if len(in_index) == 0:
                in_index.clear()
            else:
                in_index.pop(len(in_index) - 1)

    in_list_internal_situation(lst)


def remove_nesting(lst: list) -> list:
    result = []

    def in_remove_nesting(in_lst: list):

        nonlocal result
        i = 0

        while i < len(in_lst):
            if issubclass(type(in_lst[i]), list):
                in_remove_nesting(in_lst[i])
            else:
                result.append(in_lst[i])
            i += 1

    in_remove_nesting(lst.copy())

    return result


def uniformly_slice_list(lst: list, num_parts: int) -> list:
    n = len(lst)
    part_size = n // num_parts
    remainder = n % num_parts
    result = []
    start = 0

    for _ in range(num_parts):
        end = start + part_size
        if remainder > 0:
            end += 1
            remainder -= 1
        result.append(lst[start:end])
        start = end
    return result


def slice_two_dimensional_list(lst: list) -> list:
    num_rows = len(lst)
    if num_rows == 0:
        return []
    num_cols = len(lst[0])
    new_arr = [[] for _ in range(num_cols)]
    for row in lst:
        for col_index, value in enumerate(row):
            new_arr[col_index].append(value)
    return new_arr


def location_moving(lst: list, offset: int) -> list:
    if offset < 0:
        bc = (lst[:-offset]).copy()
        return (lst[-offset:]+bc).copy()
    elif offset == 0:
        return lst.copy()
    else:
        bc = (lst[len(lst)-offset:]).copy()
        return (bc+lst[:len(lst)-offset]).copy()
