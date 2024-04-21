from enum import Enum


class Outlook(str, Enum):
    Overcast = 'overcast'
    Rain = 'rain'
    Sunny = 'sunny'


class Temperature(str, Enum):
    Cool = 'cool'
    Hot = 'hot'
    Mild = 'mild'


class Humidity(str, Enum):
    High = 'high'
    Normal = 'normal'


class Wind(str, Enum):
    Strong = 'strong'
    Weak = 'weak'
