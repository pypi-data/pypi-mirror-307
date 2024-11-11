def string_as_bool(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, int):
        return bool(value)

    lvalue = value.lower().strip()
    if lvalue in ["true", "tru", "tr", "t", "yes", "y"]:
        return True
    if lvalue in ["false", "fals", "fal", "fa", "f", "no", "n"]:
        return False
    raise ValueError(f"Expected boolean value, got '{value}' instead.")
