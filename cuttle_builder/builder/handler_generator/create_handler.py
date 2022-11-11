# base method to create handler
from pathlib import Path

from cuttle_builder.bot_generator_params import CUTTLE_BUILDER_PATH
from cuttle_builder.builder.additional.file_read_write.read_file import read_file


def create_handler(imports, type_, name, method_body, send_message):
    handler_sample = (
        CUTTLE_BUILDER_PATH / 'builder' / 'additional' / 'samples' / 'handler_sample.txt')
    # read sample and put settings from upper methods
    code = read_file(handler_sample)
    code = code.format(imports, type_, name, method_body, send_message)
    return code
