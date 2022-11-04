def write_file(dir, code):
    f = open(dir, "a")
    f.seek(0,0)
    f.write(code)
    f.close()

def write_into_init(dir, code):
    with open(dir, 'r+') as file:
        file_data = file.read()
        file.seek(0, 0)
        file.write(code + file_data)
        # file.close()