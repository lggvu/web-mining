def create_object_from_two_arr(keys, values):
    obj = {}

    for key, value in zip(keys, values):
        if value:
            obj[key] = value

    return obj
