import sys


def is_run_with_gunicorn() -> bool:
    is_gunicorn = False
    args = sys.argv
    if len(args) > 2:
        param = args[1]
        is_gunicorn = 'wsgi' in param
    return is_gunicorn
