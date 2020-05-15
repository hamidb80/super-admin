from config import APP_NAME


class events_names:
    connect = 'connect'
    reconnect = 'reconnect'
    disconnect = 'disconnect'

    hello = 'hello'

    auth = 'auth'

    auth_check = 'auth_check'

    execute = 'execute'
    execute_result = 'execute_result'

    online_users = 'online_users'
    online_users_res = 'online_users_result'

    send_event = 'send_event'



class Messages:

    connected = 'Connected'

    disconnected = 'disconnected'

    error = 'Err'

    hello_from_server = 'server said hello'

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

    command_not_defined = 'the commnad not defined'

    client_help = (
        "command list:\n"
        "- status    : check status (online or offline)\n"
        "- clear     : clear console\n"
        "- auth      : authenticate user\n"
    )

    admin_help = (
        "command list:\n"
        "- quit/Q                      : exit from admin mode\n"
        "- clear/C                     : clear console\n"
        "- exec/E {command}            : execute commands in server\n"
        "- get/G <stuff>               : get stuff\n"
        "--- stuff: [ online-users, ]\n"
        "- send/S <event>  -u          : send event to all users\n"
        "- send/S <event> - data  -u   : send event with data to all users\n"
        "- alias/A <alias> = <command> : define an alias\n"
        "- alias-list/AL               : show the list of aliases\n"
        "- call-alias/CA               : call an alias\n"
    )
