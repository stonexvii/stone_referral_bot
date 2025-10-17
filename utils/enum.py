import os
from enum import Enum


class MessagePath(Enum):
    TEXT = os.path.join('messages', 'text')
    PICT = os.path.join('messages', 'pictures')
