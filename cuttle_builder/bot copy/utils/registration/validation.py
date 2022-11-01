
def validation(name: str):
    if not name:
        return False
    if not name.isalpha():
        print(name)
        return False
    if len(name) < 2:
        return False
    return True


def valid_height(height):
    if not height.isnumeric():
        return False
    if int(height) > 300:
        return False
    if int(height) < 100:
        return False
    return True


def valid_weight(weight):
    if not weight.isnumeric():
        return False
    if int(weight) > 150:
        return False
    if int(weight) < 35:
        return False
    return True