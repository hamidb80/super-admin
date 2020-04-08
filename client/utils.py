from config import APP_NAME


class events_names:
    connect = 'connect'
    reconnect = 'reconnect'
    disconnect = 'disconnect'

    hello = 'hello'
    auth = 'auth'

    auth_check = 'auth_check'

class Messages:

    connected = 'Connected'

    disconnected = 'disconnected'

    error = 'Err'

    you_are_admin = 'You already have admin privillages!'

    admin_granted = 'Admin rights granted'

    wrong_pass = 'Wrong password!'

    yconnected = 'You are connected'

    ynotconnected = 'You are not connected'

    app_name = f'{APP_NAME} >\n'

    running_in_server = 'You are running commands in server now.'

    running_in_client = 'You are running commands in client now.'

    exiting_admin = 'Exiting admin mode.'

    enter_pass = "Enter server's password >\n"
