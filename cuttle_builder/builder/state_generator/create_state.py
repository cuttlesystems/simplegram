from cuttle_builder.builder.additional.file_read_write.read_file import read_file
from cuttle_builder.builder.state_generator.to_state import to_state


def create_state(states: list) -> str:
    code = read_file('builder/additional/samples/state_sample.txt')
    for state in states:
        code += to_state(state)
    return code