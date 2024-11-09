from .ListenerV2 import ListenerV2

__version__ = "5.1.1"

class Xray():
    ROBOT_LIBRARY_LISTENER = ListenerV2()
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = __version__