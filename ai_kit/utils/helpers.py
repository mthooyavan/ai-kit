def get_nested_key_value(dictionary: dict, nested_key: str, default=None):
    """
    Get value from a dictionary using a nested key path.

    Args:
        dictionary (dict): Dictionary to search in
        nested_key (str): Nested key path using __ as separator (e.g. 'settings__api_key')
        default: Value to return if key not found (default: None)

    Returns:
        Value from dictionary at nested key path, or default if not found
    """
    keys = nested_key.split("__")
    value = dictionary

    try:
        for key in keys:
            value = value[key]
        return value
    except (KeyError, TypeError):
        return default
