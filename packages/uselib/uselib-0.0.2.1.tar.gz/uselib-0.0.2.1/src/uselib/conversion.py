def convert_from_string(string: str) -> bool | int | float | str:
    if string in ("true", "True"):
        return True
    if string in ("false", "False"):
        return False
    if string.isdecimal():
        return int(string)
    if string.replace(".", "", 1).isdecimal():
        return float(string)
    return string
