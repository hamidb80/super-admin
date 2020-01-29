from connection import tunnel
from states import app_state
from utils import Password
from time import sleep
import socket
import os

### colors
class Colors:
    red      = '\33[31m'
    green    = '\33[32m'
    yellow   = '\33[33m'
    blue     = '\33[34m'
    
    bold     = '\33[1m'
    italic   = '\33[3m'
    end      = '\33[0m'
### variables


### functions dependant on events 

def connect():
    # change connection status to True
    app_state.is_connected = True

    # connection notification for admin mode
    if app_state.is_admin:
        print(Colors.green+'Connected'+Colors.end)

    # send server hostname and new user notification
    connection_initials()


def disconnect():
    # change connection status to False
    app_state.is_connected = False
    
    # connection notification for admin mode
    if app_state.is_admin:
        print(Colors.red+Colors.bold+'disconnected'+Colors.end)

def auth(data):
    # check if user has admin privilages
    if app_state.is_admin:
        print(Colors.yellow+'You already have admin privilages!'+Colors.end)
        
    else:
        # input server's password
        enteredpass = input("Enter server's password >\n")

        # make a new hash using the entered password and salt
        testhash = Password(enteredpass,data['salt'])

        # compare new hash and the server's hash
        if (testhash.key == data['key']):

            # give admin rights
            print(Colors.green+'Admin rights granted'+Colors.end)
            app_state.is_admin = True
            client_input()
            
        # if entered password was wrong
        else:
            print(Colors.red+Colors.bold+'Wrong password!'+Colors.end)
            # send wrong password notification to server
            tunnel.send('notification',{'type': 'wrongpass'})
            
            # change main input to False
            app_state.main_input_is_waiting = True
    
        
        
### functions independant from events

# client input
def main_input():
    
    while True:
        
        while app_state.is_admin==False and app_state.main_input_is_waiting:
            
            inp = input(Colors.green+'Mollasadra Client Manager App >\n'+Colors.end)
        
            # authenticate
            if 'auth' in inp:
                ask_auth()
                
                # change main input status
                app_state.main_input_is_waiting = False
            
            # print connection status
            elif 'status' in inp:
            
                if app_state.is_connected:
                    print(Colors.green+'You are connected'+Colors.end)
                
                else:
                    print(Colors.red+'You are not connected'+Colors.end)
            sleep(0.5)
        sleep(2)
            
            
def connection_initials():
    # get hostname
    hostname = socket.gethostname()
    
    # send hostname and new user notification to server
    tunnel.send('notification',{'type': 'connection_initials','hostname': hostname})

# ask for authentication from server
def ask_auth():
    
    # send asked for authentication notification to server
    tunnel.send('notification',{'type': 'askforauth'})
    
### admin functions

# run commands in client
def client_input():
    while True:
        while app_state.client_is_waiting and app_state.is_admin:
            # get user input
            inp = input('Client >\n')
            
            #check if user wants to run code in server
            if ' -s' in inp:
                
                inp = inp.replace(' -s','')
                print('Sending command',Colors.yellow+inp+Colors.end,'to server')
                # send command to server
                tunnel.send('execute', inp)

            elif 'exit' in inp:
                os.system('clear')
                app_state.is_admin = False
                app_state.main_input_is_waiting = True
                
            else:
                try:
                    exec(inp)
                except:
                    print('Err')
    
    
