"""
script to build an executable file of 'simple_gram_chamomile' application
"""

from application_type_enum import ApplicationTypeEnum
from build_executable import build_executable_app


if __name__ == '__main__':
    build_executable_app(ApplicationTypeEnum.CLASSIC)
