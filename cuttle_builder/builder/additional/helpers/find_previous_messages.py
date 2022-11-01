
def find_previous_messages(id, variants):
    return [item for item in variants if item['next_id']==id]
    