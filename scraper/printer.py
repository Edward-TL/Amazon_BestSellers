def centered_string(string):
    rest = 21 - len(string)
    n_spaces = int(rest/2)

    string_spaces = ' ' * n_spaces
    
    centered_string = string_spaces + string + string_spaces

    if len(centered_string)<21:
        centered_string = ' ' + centered_string

    return centered_string

def print_header(country_count):
    if country_count == 0:
        print(f'      Log Date    | Country |        category       | header | status | Loaded |')
    else:
        print(' ---------------- | ------- | --------------------- | ------ | ------ | ------ |')

    