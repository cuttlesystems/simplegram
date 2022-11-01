import os

def read_file(dir):
    with open(dir, 'r') as file:
        return file.read()

def read_file_by_line(dir):
    with open(dir, 'r') as file:
        return file.read().split('\n')