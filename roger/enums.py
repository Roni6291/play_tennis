from enum import Enum


class Outlook(Enum):
    Overcast = 'overcast'
    Rain = 'rain'
    Sunny = 'sunny'


class Temperature(Enum):
    Cool = 'cool'
    Hot = 'hot'
    Mild = 'mild'


class Humidity(Enum):
    High = 'high'
    Normal = 'normal'


class Wind(Enum):
    Strong = 'strong'
    Weak = 'weak'
