from enum import Enum


class ServiceName(str, Enum):
    dict = 'dict'
    patient = 'patient'
    practice = 'practice'
    ml = 'ml'
