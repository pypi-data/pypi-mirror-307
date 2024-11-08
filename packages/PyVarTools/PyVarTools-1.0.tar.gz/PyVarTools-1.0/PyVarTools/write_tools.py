from re import sub
#
#
#
#
def write_integer(int_: int):
    return "%d" % int_
#
#
#
#
def write_float(float_: float):
    return "%f" % float_
#
#
#
#
def write_string(string: str):
    return "\"%s\"" % string
#
#
#
#
def write_boolean(bool_: bool):
    return "True" if bool_ else "False"
#
#
#
#
def add_leading_space(text: str):
    return sub(r"(\n|\A)", r"\1    ", text)
#
#
#
#
def write_tuple(tuple_: tuple):
    tuple_items = []

    for item in tuple_:
        tuple_items.append(add_leading_space(write_variable(item)))

    return "(\n%s\n)" % ",\n".join(tuple_items)
#
#
#
#
def write_list(list_: list):
    list_items = []

    for item in list_:
        list_items.append(add_leading_space(write_variable(item)))

    return "[\n%s\n]" % ",\n".join(list_items)
#
#
#
#
def write_dictionary(dictionary: dict):
    dictionary_items = []

    for key, value in dictionary.items():
        dictionary_items.append(add_leading_space("%s: %s" % (write_variable(key), write_variable(value))))

    return "{\n%s\n}" % ",\n".join(dictionary_items)
#
#
#
#
def write_variable(variable):
    if type(variable) == dict:
        return write_dictionary(variable)
    elif type(variable) == list:
        return write_list(variable)
    elif type(variable) == tuple:
        return write_tuple(variable)
    elif type(variable) == bool:
        return write_boolean(variable)
    elif type(variable) == str:
        return write_string(variable)
    elif type(variable) == float:
        return write_float(variable)
    elif type(variable) == int:
        return write_integer(variable)
    else:
        return "None"
