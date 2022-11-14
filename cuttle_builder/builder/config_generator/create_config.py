from cuttle_builder.bot_generator_params import CUTTLE_BUILDER_PATH
from cuttle_builder.builder.additional.file_read_write.read_file import read_file


def create_config(data):
    config_sample = (
            CUTTLE_BUILDER_PATH / 'builder' / 'additional' / 'samples' / 'config_sample.txt')
    # read sample and put settings from upper methods
    code = read_file(config_sample)
    code = code.format(data['TOKEN'])
    return code
