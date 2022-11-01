def valid_height(height):
    if not height.isnumeric():
        return False
    if int(height) > 300:
        return False
    if int(height) < 100:
        return False
    return True