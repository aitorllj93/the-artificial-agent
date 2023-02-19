
def get_value_from_dict(dic_obj, path: str, default):
    """
    get value from dict with key path.
    :param dic_obj: dict
    :param path: dict path
    :param default: default value
    :return:
    """
    if not dic_obj or not path:
        return default

    keys = path.split('.')

    pre_obj = dic_obj
    for key in keys:
        t = type(pre_obj)
        if t is dict:
            pre_obj = pre_obj.get(key)
        elif (t is list or t is tuple) and str(key).isdigit() and len(pre_obj) > int(key):
            pre_obj = pre_obj[int(key)]
        else:
            return default
    return pre_obj


def set_value_into_dict(dic_obj, path: str, value):
    """
    set value into dict with key path.
    :param dic_obj: dict
    :param path: dict path
    :param value: value
    :return:
    """
    if not dic_obj or not path:
        return

    keys = path.split('.')

    pre_obj = dic_obj
    for key in keys:
        t = type(pre_obj)
        isLast = key == keys[-1]
        if t is dict:
            if key in pre_obj:
                pre_obj = pre_obj[key]
            else:
                if isLast:
                    pre_obj[key] = value
                    return
                else:
                    pre_obj[key] = {}
                    pre_obj = pre_obj[key]
        elif (t is list or t is tuple) and str(key).isdigit() and len(pre_obj) > int(key):
            pre_obj = pre_obj[int(key)]
        else:
            return
