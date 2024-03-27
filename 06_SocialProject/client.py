import cmd
import threading
import readline
import shlex
import socket

connection = None
client_active = True
completion_message = None
HOST = '0.0.0.0'
PORT = 1337

def send_message(msg):
    connection.send(f"{msg}\n".encode())

def receive_messages(command_line_interface):
    global completion_message

    while client_active:
        data = connection.recv(1024).decode().strip().split("@")
        if data and len(data) == 1:
            print(f'\n{data[0]}\n{command_line_interface.prompt}{readline.get_line_buffer()}', end="", flush=True)
        elif data and data[0].strip() == "compl":
            completion_message = data[1]

class CowsayCommand(cmd.Cmd):
    prompt = "cmd>> "

    def do_who(self, arg):
        send_message("who")

    def do_cows(self, arg):
        send_message("cows")

    def do_login(self, arg):
        send_message(f"login {arg}")

    def complete_login(self, text, line, begidx, endidx):
        global completion_message

        send_message("compl@cows")
        while completion_message is None:
            pass

        suggestions = completion_message[1:-1].replace("'", "").split(",")
        completion_message = None
        suggestions = list(map(str.strip, suggestions))

        if line.split()[-1] == "login":
            return suggestions
        return [s for s in suggestions if s.startswith(line.split()[-1])]

    def do_say(self, arg):
        cow, msg = shlex.split(arg)
        send_message(f"say {cow} {msg}")

    def complete_say(self, text, line, begidx, endidx):
        global completion_message

        send_message("compl@who")
        while completion_message is None:
            pass

        suggestions = completion_message[1:-1].replace("'", "").split(",")
        completion_message = None
        suggestions = list(map(str.strip, suggestions))

        if line.split()[-1] == "say":
            return suggestions
        return [s for s in suggestions if s.startswith(line.split()[-1])]

    def do_yield(self, arg):
        send_message(f"yield {arg}")

    def do_quit(self, args):
        send_message("quit")

if __name__ == "__main__":
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect((HOST, PORT))

    cmd_interface = CowsayCommand()
    recv_thread = threading.Thread(target=receive_messages, args=(cmd_interface,))
    recv_thread.start()
    cmd_interface.cmdloop()

    connection.close()
    client_active = False
