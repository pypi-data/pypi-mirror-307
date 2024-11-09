import gc


def replace_str(string, __c, __nc='', num=0, __start=0, __end=None):

    if (len(str(__c)) == 0) or (len(str(string)) == 0):
        raise ValueError("Original character cannot be empty!")

    if len(__c) == 1 and __c not in list(str(string)):
        return string

    string = str(string)
    __c = str(__c)
    __nc = str(__nc)
    lst_string = list(string)
    if __end is None:
        __end = len(lst_string)

    if len(__c) == 1 and num == 0:
        tmp_lst_str: list = []
        for _i in range(__start, __end, 1):
            tmp_lst_str.append(lst_string[_i])
        tmp_str = str("".join(tmp_lst_str)).replace(__c, __nc)
        return string[:__start:] + tmp_str

    elif len(__c) == 1 and num != 0:
        times: int = 0
        _i: int = 0
        for _i in range(__start, __end, 1):
            if lst_string[_i] == __c:
                times += 1
                if times == num:
                    break
        if times != num:
            return string
        lst_string[_i] = __nc
        new_string = str("".join(lst_string))

        del _i, times, lst_string
        gc.collect()

        return new_string

    elif len(__c) > 1 and num == 0:
        tmp_lst_str: list = []
        for _i in range(__start, __end, 1):
            tmp_lst_str.append(lst_string[_i])
        tmp_str = str("".join(tmp_lst_str)).replace(__c, __nc)
        return string[:__start:] + tmp_str

    elif len(__c) > 1 and num != 0:
        temp_bool: bool = False
        times: int = 0
        _i: int = __start
        while not (_i == __end - len(__c) or times >= num):
            temp = lst_string[_i:len(__c) + _i:]
            temp = str("".join(temp))
            if temp == __c:
                _i += len(__c)
                times += 1
                continue
            _i += 1
        if times != num:
            return string
        temp2 = list(__nc)
        _i -= 1
        for _j in range(len(__nc)):
            if len(__nc) > len(__c):
                if _j >= len(__c):
                    lst_string.insert(int(_i + _j), temp2[_j])
                else:
                    lst_string[_i + _j] = temp2[_j]
            else:
                temp_bool = True
                break
        if temp_bool and len(__nc) != 0:
            for _j in range(len(__c) - len(__nc)):
                lst_string.pop(_i)
            for _j in range(len(__nc)):
                lst_string[_i + _j] = temp2[_j]
        elif len(__nc) == 0:
            for _j in range(len(__c)):
                lst_string.pop(_i)
        new_string = str("".join(lst_string))

        try:
            del _i, _j, temp, temp2, temp_bool, times
        except UnboundLocalError:
            pass
        gc.collect()

        return new_string


def randstr(length, *, use_symbol=False, without_character=False):
    """
    Generate a string of random ASCII characters
    :param length:
    :param use_symbol:
    :param without_character:
    """
    import random
    tmp: object
    lst_string: list = []
    symbol_lst = ['`', '~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '=', '+', '[', ']', '{', '}',
                  '\\', '|', ';', ':', "'", '"', ',', '<', '>', '/', '?']

    if not without_character:
        for i in range(length):
            if use_symbol:
                tmp = random.randint(0, 2)
                if tmp == 0:
                    lst_string.append(chr(random.randint(ord('A'), ord('Z'))))
                elif tmp == 1:
                    lst_string.append(chr(random.randint(ord('a'), ord('z'))))
                else:
                    lst_string.append(random.choice(symbol_lst))
            else:
                tmp = random.randint(0, 1)
                if tmp:
                    lst_string.append(chr(random.randint(ord('A'), ord('Z'))))
                else:
                    lst_string.append(chr(random.randint(ord('a'), ord('z'))))
    elif use_symbol:
        for i in range(length):
            lst_string.append(random.choice(symbol_lst))
    else:
        return ''
    return "".join(lst_string)


def reverse_str(string):

    if len(str(string)) <= 0:
        return string
    return str("".join(list(reversed(list(str(string))))))


def statistics_str(string):

    from collections import Counter
    from list_func_part import bubble_sort

    string = str(string)
    lst_string = list(string).copy()
    all_l: list = []
    all_d: dict = {}

    # Ascii部分
    for _i in lst_string:
        all_l.append(ord(_i))

    all_l = bubble_sort(all_l)

    for _i in range(len(all_l)):
        all_d.update({f"{chr(all_l[_i])}": all_l[_i]})

    # 次数部分
    num = str(Counter(lst_string))[8::]
    num = eval(num[:len(num) - 1:])

    return all_d, num


def find_list(lst, __fc, start=False, mid=False, end=False):

    if not (isinstance(lst, list)):
        return lst

    find: list = []
    _i: int = 0
    __fc, start, mid, end = str(__fc), bool(start), bool(mid), bool(end)

    for _i in range(len(lst)):
        if __fc in lst[_i] and start and not (mid and end) and _i == 0:
            find.append(lst[_i])
        elif __fc in lst[_i] and mid and not (start and end) and _i == len(lst) // 2:
            find.append(lst[_i])
        elif __fc in lst[_i] and end and not (start and mid) and _i == len(lst) - 1:
            find.append(lst[_i])
        else:
            if start and mid:
                if (__fc in lst[_i] and _i == 0) or (__fc in lst[_i] and _i == len(lst) // 2):
                    find.append(lst[_i])
            elif start and end:
                if (__fc in lst[_i] and _i == 0) or (__fc in lst[_i] and _i == len(lst) - 1):
                    find.append(lst[_i])
            elif mid and end:
                if (__fc in lst[_i] and len(lst) // 2) or (__fc in lst[_i] and _i == len(lst) - 1):
                    find.append(lst[_i])
            else:
                if __fc in lst[_i]:
                    find.append(lst[_i])

    try:
        del _i
    except UnboundLocalError:
        pass
    gc.collect()

    return find
