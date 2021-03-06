import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog

# HOST = '10.0.0.5'
PORT = 6666


class Client:

    def __init__(self, port):
        msg = tkinter.Tk()
        msg.geometry("50x50+400+100")
        msg.withdraw()
        self.name = simpledialog.askstring("Name", "Enter your name", parent=msg)
        self.serverIp = simpledialog.askstring("ServerIP", "Enter server ip(exp 10.0.0.4):", parent=msg)
        self.sock = None
        while self.sock is None and self.serverIp != 'exit':
            try:
                host = self.serverIp
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.connect((host, port))
            except:
                self.serverIp = simpledialog.askstring("ServerIP",
                                                       "IP WAS NOT CORRECT PLZ TRY AGAIN\n write exit for stopping",
                                                       parent=msg)
                self.sock = None
        if self.serverIp == 'exit':
            exit(0)
        msg.destroy()
        self.gui_done = False
        self.running = True

        gui_thread = threading.Thread(target=self.gui_loop)
        recieve_thread = threading.Thread(target=self.receive)
        # recieve_thread = threading.Thread(target=self.receive, daemon=True)

        gui_thread.start()
        recieve_thread.start()

    def gui_loop(self):
        self.window = tkinter.Tk()
        self.window.geometry("690x480+400+100")
        self.window.title(self.name)
        self.window.configure(bg="lightgreen")

        self.logout_button = tkinter.Button(self.window, text="Logout", command=self.logout, padx=10, pady=5)
        self.logout_button.grid(row=0, column=0)

        self.list_button = tkinter.Button(self.window, text="online list", command=self.list_online, padx=10, pady=5)
        self.list_button.grid(row=0, column=1)

        self.files_button = tkinter.Button(self.window, text="server files", padx=20, pady=5, command=self.show_files)
        self.files_button.grid(row=0, column=2)

        self.clear_button = tkinter.Button(self.window, text="clear", command=self.clear, padx=2, pady=5)
        self.clear_button.grid(row=0, column=3)

        self.text_area = tkinter.scrolledtext.ScrolledText(self.window, height=20, width=50)
        self.text_area.grid(row=2, column=1)
        self.text_area.config(state='disabled')

        self.to_label = tkinter.Label(self.window, text="To(blank to all)", bg="lightgray", padx=0.5, pady=1)
        self.to_label.config(font=("Ariel", 9))
        self.to_label.grid(row=6, column=0)

        self.to_input = tkinter.Text(self.window, height=1, width=15)
        self.to_input.grid(row=7, column=0)

        self.msg_label = tkinter.Label(self.window, text="Message", bg="lightgray", padx=0.5, pady=1)
        self.msg_label.config(font=("casual", 9))
        self.msg_label.grid(row=6, column=1)

        self.input = tkinter.Text(self.window, height=2, width=50)
        self.input.grid(row=7, column=1)

        self.send_button = tkinter.Button(self.window, text="send", command=self.write, padx=20, pady=5)
        self.send_button.grid(row=7, column=2)

        self.file_label = tkinter.Label(self.window, text="server file name", bg="lightgray", padx=0.5, pady=1)
        self.file_label.config(font=("casual", 9))
        self.file_label.grid(row=9, column=0)

        self.file_input = tkinter.Text(self.window, height=1, width=15)
        self.file_input.grid(row=10, column=0)

        self.save_label = tkinter.Label(self.window, text="save as", bg="lightgray", padx=0.5, pady=1)
        self.save_label.config(font=("casual", 9))
        self.save_label.grid(row=9, column=1)

        self.save_input = tkinter.Text(self.window, height=1, width=50)
        self.save_input.grid(row=10, column=1)

        self.proceed_button = tkinter.Button(self.window, text="proceed", command=self.proceed, padx=20, pady=5)
        self.proceed_button.grid(row=10, column=2)

        self.gui_done = True
        self.window.protocol("WM_DELETE_WINDOW", self.stop)
        self.window.mainloop()

    def proceed(self):
        pass

    def stop(self):
        self.running = False
        self.window.destroy()
        self.sock.close()
        exit(0)

    def logout(self):
        self.running = False
        self.window.destroy()
        self.sock.close()
        exit(0)

    def show_files(self):
        message = "serverFiles"
        self.sock.send(message.encode('utf-8'))

    def list_online(self):
        message = "online"
        self.sock.send(message.encode('utf-8'))

    def clear(self):
        self.text_area.config(state='normal')
        self.text_area.delete('1.0', 'end')
        self.text_area.config(state='disabled')

    def write(self):
        if self.to_input.compare('end-1c', '==', '1.0'):
            message = f"{self.name}:{self.input.get('1.0', 'end')}"
            self.sock.send(message.encode('utf-8'))
            # self.input.delete('1.0', 'end')
        else:
            private_m = f"private+{self.to_input.get('1.0', 'end')}+private from {self.name}:{self.input.get('1.0', 'end')}"
            self.sock.send(private_m.encode('utf-8'))
        self.input.delete('1.0', 'end')
        # self.to_input.delete('1.0', 'end')

    def receive(self):
        while self.running:
            try:
                message = self.sock.recv(1024).decode('utf-8')
                header = message.split('+')[0]
                if message == 'name':
                    self.sock.send(self.name.encode('utf-8'))
                elif 'users' == header:
                    online_window = tkinter.Toplevel(self.window)
                    online_window.geometry("172x120+400+100")
                    online_window.title("online")
                    online_window.configure(bg="lightblue")
                    tkinter.Label(online_window, bg="lightblue", text="users: " + message.split('+')[1],
                                  wraplength=130).pack()
                elif 'server files:' == header:
                    online_window2 = tkinter.Toplevel(self.window)
                    online_window2.geometry("172x120+400+100")
                    online_window2.title("server files")
                    online_window2.configure(bg="lightblue")
                    tkinter.Label(online_window2, bg="lightblue", text="server files: " + message.split('+')[1],
                                  wraplength=130).pack()
                else:
                    if self.gui_done:
                        self.text_area.config(state='normal')
                        self.text_area.insert('end', message)
                        self.text_area.yview('end')
                        self.text_area.config(state='disabled')
            except:
                break
            # try:
            #     self.sock.close()
            # except socket.error:
            #     return


client = Client(PORT)
