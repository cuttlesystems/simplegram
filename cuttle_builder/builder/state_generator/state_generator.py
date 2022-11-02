from builder.additional.file_read_write.read_file import read_file
from builder.state_generator.to_state import to_state

def state_generator(states: list) -> str:
    code = read_file('builder/additional/samples/state_sample.txt') 
    for state in states:
        code += to_state(state)
    return code