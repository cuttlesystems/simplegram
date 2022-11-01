from datetime import datetime, timedelta

def date_to_age(birth_date: datetime):
    return (datetime.now() - birth_date) // timedelta(days=365.2425)