from pathlib import Path

from cuttle_builder.bot_generator_params import CUTTLE_BUILDER_PATH
from cuttle_builder.builder.additional.file_read_write.read_file import read_file
from cuttle_builder.builder.state_generator.to_state import to_state


def create_state(extended_imports: str,states: list) -> str:
    state_sample = (
            CUTTLE_BUILDER_PATH / 'builder' / 'additional' / 'samples' / 'state_sample.txt')
    code = read_file(state_sample)
    code = code.format(extended_imports)
    for state in states:
        code += to_state(state)
    return code
