from time import sleep
from states import app_state

def kill():
    pass

def connection_checker(max_timeout = 5):
    fail_seconds = 0

    while True:
        if app_state.is_connected is True:
            fail_seconds = 0

        else:
            fail_seconds += 1

            if fail_seconds > max_timeout:
                fail_seconds = 0

                kill()

        sleep(1)
