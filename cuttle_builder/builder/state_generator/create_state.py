from pathlib import Path

from cuttle_builder.builder.additional.file_read_write.read_file import read_file
from cuttle_builder.builder.state_generator.to_state import to_state


def create_state(states: list) -> str:
    state_sample = Path(__file__).parent.parent / 'additional/samples/state_sample.txt'
    code = read_file(state_sample)
    for state in states:
        code += to_state(state)
    return code