def find_nearest_key(value, dict_with_numeric_keys):
    keys = sorted(dict_with_numeric_keys.keys())
    for key in keys:
        if value < key:
            return dict_with_numeric_keys.get(key)
    return dict_with_numeric_keys.get(keys[-1])


def seconds_to_minutes(seconds):
    minutes = seconds // 60
    return minutes
