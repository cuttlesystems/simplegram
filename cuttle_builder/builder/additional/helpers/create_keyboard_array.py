
def create_keyboard_array(id, variants):
    return [item['text'] for item in variants if item['current_id']==id]
