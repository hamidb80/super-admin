from utils import Messages
from monkey_patch import print

# default events ------------------------------

def connect(data):
    print(Messages.connected)


def reconnect(data=None):
    pass


def disconnect(data):
    print(Messages.disconnected)

# custom events --------------------------------
def hello(data=None):
    print(Messages.hello_from_server)
