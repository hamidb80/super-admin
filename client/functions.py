from time import sleep

from config import ADDR
from states import app_state
from actions import lock, check

def connection_checker():
    while True:

        if app_state.is_connected:
            # reset fails to zero
            app_state.fails = 0

            # check while connected
            while app_state.is_connected:
                check()
                sleep(1)

                if app_state.fails > 3:
                    app_state.is_connected = False

        elif app_state.is_connected is False:
            lock()
            sleep(5)
            