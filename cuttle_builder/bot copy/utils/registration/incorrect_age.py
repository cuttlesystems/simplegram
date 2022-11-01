def incorrect_age(age: str):
    if int(age) > 70:
        return 'old'
    elif int(age) < 18:
        return 'young'
    return False