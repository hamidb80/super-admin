from connection import tunnel
from states import app_state
from utils import Password
from time import sleep
import socket


### variables


### functions dependant on events 

def connect():
    # change connection status to True
    app_state.is_connected = True
    app_state.is_waiting = True

    # connection notification
    print('Connected')

    # send server hostname and new user notification
    connection_initials()


def disconnect():
    # change connection status to False
    app_state.is_connected = False
    
    # change command input status to False
    app_state.is_waiting = False

    # connection notification
    print('disconnected')

def auth(data):
    # split server hashed pass and salt
    data_chunks = data.split('nextis')
    
    # encode salt and server's hashed password
    salt = data_chunks[1].encode('ISO-8859-1')
    hashedpass = data_chunks[0].encode('ISO-8859-1')
    
    # input server's password
    enteredpass = input("Please enter server's password >\n")

    # make a new hash using the entered password and salt
    testhash = Password(enteredpass,salt)

    # compare new hash and the server's hash
    if (testhash.key == hashedpass):
        
        # send access notification to server
        tunnel.send('notification', "hasaccess")
        
        # give admin rights
        app_state.is_admin = True
        print('Admin rights granted')
        
        # ask wether to run execinserv()
        decide = input('Run commands in server now?\n')
        if "y" in decide:
            execinserv()
        
        else:
            app_state.is_waiting = True

    # if hashes didn't match
    else:
        print("Wrong Password")
        app_state.is_waiting = True
        tunnel.send('notification', "wrongpass")


### functions independant from events

def connection_initials():
    # get hostname
    hostname = socket.gethostname()
    
    data = "newuser"+" "+hostname
    # send hostname and new user notification to server
    tunnel.send('notification', data)

# ask for authentication from server
def ask_auth():
    # change command input status to Flase
    app_state.is_waiting = False
    
    # send asked for authentication notification to server
    tunnel.send('notification', "askforauth")

# get input from user
def command_input():
    # always run the function
    while True:
        # while waiting for command ask for input and execute it
        while app_state.is_waiting==True:
            inp = input('Client >\n')
            try:
                exec(inp)
            except:
                print("Err")
            
            sleep(0.5)
    sleep(2)
    
### admin functions

# execute commands in server
def execinserv():
    
    # check if user have admin rights
    if app_state.is_admin==False:
        # send illegal command notification
        print("You don't have admin rights!! go study something you lazy student!")
        tunnel.send('notification', "illegalcommand")

    # run only when user has admin privilages
    while app_state.is_admin:
        # get command input
        inp = input('Server > \n')
        
        # if exit was entered close the loop and accept client commands
        if "exit" in inp:
            app_state.is_waiting = True
            break
        
        try:
            print(f"I got it: {inp}")
            print(f"I'll send it to the server")
            
            # send the user input to server
            tunnel.send('execute', inp)

        except:
            print('Err')
            
        sleep(0.5)
