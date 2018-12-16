
def get_normalized_full_name(raw):
    fullname = raw.strip()
    if fullname[0] == '(' and fullname[-1] == ')':
        return fullname[1:-1]
    return fullname
