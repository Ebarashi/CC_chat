import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog

HOST = '127.0.0.1'
PORT = 6666


class Client:

    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

        msg = tkinter.Tk()
        msg.withdraw()

        self.name = simpledialog.askstring("Name", "Enter your name", parent=msg)

        self.gui_done = False
        self.running = True

        gui_thread = threading.Thread(target=self.gui_loop)
        recieve_thread = threading.Thread(target=self.receive)

        gui_thread.start()
        recieve_thread.start()

    def gui_loop(self):

        self.window = tkinter.Tk()
        self.window.configure(bg="lightgray")

        self.chat_label = tkinter.Label(self.window, text="Chat:", bg="lightgray")
        self.chat_label.config(font=("casual", 12))
        self.chat_label.pack(padx=20, pady=5)

        self.text_area = tkinter.scrolledtext.ScrolledText(self.window)
        self.text_area.pack(padx=20, pady=5)
        self.text_area.config(state='disabled')

        self.msg_label = tkinter.Label(self.window, text="Message:", bg="lightgray")
        self.msg_label.config(font=("casual", 12))
        self.msg_label.pack(padx=2, pady=3)

        self.input = tkinter.Text(self.window, height=3)
        self.input.pack(padx=20, pady=5)

        self.send_button = tkinter.Button(self.window, text="send", command=self.write)
        self.send_button.pack(padx=20, pady=5)

        self.exit_button = tkinter.Button(self.window, text="exit")
        self.exit_button.pack(padx=20, pady=5)

        self.gui_done = True
        self.window.protocol("WM_DELETE_WINDOW", self.stop)
        self.window.mainloop()



    def stop(self):
        self.running = False
        self.window.destroy()
        self.sock.close()
        exit(0)

    def write(self):
        messege = f"{self.name}: {self.input.get('1.0', 'end')}"
        self.sock.send(messege.encode('utf-8'))
        self.input.delete('1.0', 'end')

    def receive(self):
        while self.running:
            try:
                messege = self.sock.recv(1024).decode('utf-8')
                if messege == 'NAME':
                    self.sock.send(self.name.encode('utf-8'))
                else:
                    if self.gui_done:
                        self.text_area.config(state='normal')
                        self.text_area.insert('end', messege)
                        self.text_area.yview('end')
                        self.text_area.config(state='disabled')
            except:
                break


client = Client(HOST, PORT)
