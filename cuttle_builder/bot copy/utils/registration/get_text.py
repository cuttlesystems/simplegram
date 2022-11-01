
def read_file(filename):
    with open(filename, encoding='utf-8') as file:
        contents = file.read()
        return contents
