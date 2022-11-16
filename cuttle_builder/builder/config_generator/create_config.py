from pathlib import Path

from cuttle_builder.bot_generator_params import CUTTLE_BUILDER_PATH
from cuttle_builder.builder.additional.file_read_write.read_file import read_file


# def create_handler(imports, content_type, name, method_body, send_method):
#     handler_sample = (
#         CUTTLE_BUILDER_PATH / 'builder' / 'additional' / 'samples' / 'handler_sample.txt')
#     # read sample and put settings from upper methods
#     code = read_file(handler_sample)
#     code = code.format(imports, content_type, name, method_body, send_method)
#     return code

def create_config(imports, data):

    config_sample = (
        CUTTLE_BUILDER_PATH / 'builder' / 'additional' / 'samples' / 'config_sample.txt')
    code = read_file(config_sample)
    code = code.format(imports,
                       data['TOKEN']
                       )
    return code

