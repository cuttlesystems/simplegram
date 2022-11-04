# base method to create handler
from cuttle_builder.builder.additional.file_read_write.read_file import read_file

def create_handler(imports, type_, name, method_body, send_message):
    # read sample and put settings from upper methods
    code = read_file('builder/additional/samples/handler_sample.txt')
    code = code.format(imports, type_, name, method_body, send_message)
    return code