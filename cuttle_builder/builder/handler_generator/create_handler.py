# base method to create handler

from cuttle_builder.bot_generator_params import CUTTLE_BUILDER_PATH
from cuttle_builder.builder.additional.file_read_write.read_file import read_file


def create_handler(imports, content_type, name, method_body, send_method, handler_sample_name):
    handler_sample = (
        CUTTLE_BUILDER_PATH / 'builder' / 'additional' / 'samples' / handler_sample_name)
    # read sample and put settings from upper methods
    code = read_file(handler_sample)
    code = code.format(imports=imports,
                       handler_params=content_type,
                       handler_name=name,
                       state_to_set=method_body,
                       answer_content=send_method)
    return code
