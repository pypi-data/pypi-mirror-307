def var_in_list(lst: list, __class: type, return_lst: bool = False, only_return_lst: bool = False) -> Union[int, tuple, list]:

    if return_lst and only_return_lst:
        raise ValueError("return_lst and only_return_lst cannot be True at the same time")

    def in_def_var_in_list(lst2: list) -> Union[int, tuple, list]:
        if return_lst:
            if globals().get("$all_result") is None:
                globals().update({"$all_result": 0})
            if globals().get("$all_result_lst") is None:
                globals().update({"$all_result_lst": list([])})
        elif only_return_lst:
            if globals().get("$all_result_lst") is None:
                globals().update({"$all_result_lst": list([])})
        else:
            if globals().get("$all_result") is None:
                globals().update({"$all_result": 0})
        for _i in range(len(lst2)):
            if isinstance(lst2[_i], __class):
                if return_lst:
                    globals().update({"$all_result": globals().get("$all_result") + 1}), globals().get(
                        "$all_result_lst").append(lst2[_i])
                elif only_return_lst:
                    globals().get("$all_result_lst").append(lst2[_i])
                else:
                    globals().update({"$all_result": globals().get("$all_result") + 1})
            elif isinstance(lst2[_i], list):
                in_def_var_in_list(lst2[_i])
        if return_lst:
            return globals().get("$all_result"), globals().get("$all_result_lst")
        elif only_return_lst:
            return globals().get("$all_result_lst")
        else:
            return globals().get("$all_result")

    return_lst = bool(return_lst)
    result = in_def_var_in_list(lst)
    if return_lst:
        globals().pop("$all_result"), globals().pop("$all_result_lst")
    elif only_return_lst:
        globals().pop("$all_result_lst")
    else:
        globals().pop("$all_result")
    return result
