from uselib.conversion import convert_from_string

print(convert_from_string("true"))
print(convert_from_string("false"))
print(convert_from_string("fals"))
print(convert_from_string("1212213") + 1)
print(convert_from_string("1212213asdasd"))
print(convert_from_string("12122.020.1"))
print(convert_from_string("12122.020") + 1)
