
def get_state_name_by_mes_id(mes_id: int):
    return f'ramashechka_message_{mes_id}'

def to_state(state: str):
    return '\n\t{0} = State()'.format(get_state_name_by_mes_id(int(state)))