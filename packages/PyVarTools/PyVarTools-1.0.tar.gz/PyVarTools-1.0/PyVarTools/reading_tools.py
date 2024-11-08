from re import DOTALL, findall, search, sub
#
#
#
#
def read_integer(variable: str):
    return int(search(r"\A(-?\d+)\Z", variable).group(1))
#
#
#
#
def read_float(variable: str):
    return float(search(r"\A(-?\d+\.\d+)\Z", variable).group(1))
#
#
#
#
def read_string(variable: str):
    return search(r"\A\"(.*)\"\Z", variable).group(1)
#
#
#
#
def read_boolean(variable: str):
    return variable == "True"
#
#
#
#
def remove_leading_space(text: str):
    return sub(r"(\n|\A) {4}", r"\1", text)
#
#
#
#
def read_tuple(variable: str):
    variable = remove_leading_space(search(r"\A\((.*)\n\)\Z", variable, DOTALL).group(1))
    tuple_ = tuple(read_variable(item) for item in findall(r"(?:\n|\A)(\{.*?\n}|\[.*?\n]|\(.*?\n\)|\bNone\b|\bTrue\b|\bFalse\b|\".*?\"|-?\d+(?:\.\d+)?)(?:,|\Z)", variable, DOTALL))

    return tuple_
#
#
#
#
def read_list(variable: str):
    variable = remove_leading_space(search(r"\A\[(.*)\n]\Z", variable, DOTALL).group(1))
    list_ = []

    for item in findall(r"(?:\n|\A)(\{.*?\n}|\[.*?\n]|\(.*?\n\)|\bNone\b|\bTrue\b|\bFalse\b|\".*?\"|-?\d+(?:\.\d+)?)(?:,|\Z)", variable, DOTALL):
        list_.append(read_variable(item))

    return list_
#
#
#
#
def read_dictionary(variable: str):
    variable = remove_leading_space(search(r"\A\{(.*)\n}\Z", variable, DOTALL).group(1))
    dictionary = {}

    for item in findall(
            r"(?:\n|\A)(\".*?\"|-?\d+(?:.\d+)?): (\{.*?\n}|\[.*?\n]|\(.*?\n\)|\bNone\b|\bTrue\b|\bFalse\b|\".*?\"|-?\d+(?:\.\d+)?)(?:,|\Z)",
            variable,
            DOTALL
    ):
        dictionary[read_variable(item[0])] = read_variable(item[1])

    return dictionary
#
#
#
#
def get_variable_type(variable: str):
    if search(r"\A\{.*}\Z", variable, DOTALL):
        return "dict"
    elif search(r"\A\[.*]\Z", variable, DOTALL):
        return "list"
    elif search(r"\A\(.*\)\Z", variable, DOTALL):
        return "tuple"
    elif search(r"\A(?:\bTrue\b|\bFalse\b)\Z", variable, DOTALL):
        return "bool"
    elif search(r"\A\".*\"\Z", variable, DOTALL):
        return "str"
    elif search(r"\A-?\d+\.\d+\Z", variable, DOTALL):
        return "float"
    elif search(r"\A-?\d+\Z", variable, DOTALL):
        return "int"
    else:
        return None
#
#
#
#
def read_variable(text: str):
    variable_type = get_variable_type(text)

    if variable_type == "dict":
        return read_dictionary(text)
    elif variable_type == "list":
        return read_list(text)
    elif variable_type == "tuple":
        return read_tuple(text)
    elif variable_type == "bool":
        return read_boolean(text)
    elif variable_type == "str":
        return read_string(text)
    elif variable_type == "float":
        return read_float(text)
    elif variable_type == "int":
        return read_integer(text)
    else:
        return None
