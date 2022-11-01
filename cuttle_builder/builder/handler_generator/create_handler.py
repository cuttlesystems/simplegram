# base method to create handler

from builder import read_file 

def create_handler(imports, type_, name, additional_function, send_method):
    # read sample and put settings from upper methods
    code = read_file('builder/additional/samples/handler_sample.txt') 
    code = code.format(imports, type_, name, additional_function, send_method)
    return code