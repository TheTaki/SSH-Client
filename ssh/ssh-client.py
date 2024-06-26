import tkinter as tk
import paramiko
import threading
import time
import pwmanager
import os


class SSHClient:
#aufbau des GUI Interaface mit TKInter
    def __init__(self, root):
        self.root = root
        self.root.title("SSH Client")
        self.root.geometry("800x600")

        self.host_label = tk.Label(root, text="Host:")
        self.host_label.pack()
        self.host_entry = tk.Entry(root, width=50)
        self.host_entry.pack()

        self.username_label = tk.Label(root, text="Username:")
        self.username_label.pack()
        self.username_entry = tk.Entry(root, width=50)
        self.username_entry.pack()

        self.password_label = tk.Label(root, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(root, width=50, show="*")
        self.password_entry.pack()

        self.connect_button = tk.Button(root, text="Connect", command=self.connect)
        self.connect_button.pack()

        self.output_area = tk.Text(root, width=100, height=20)
        self.output_area.pack()

        self.command_entry = tk.Entry(root, width=100)
        self.command_entry.pack()
        self.command_entry.bind("<Return>", self.send_command)

        self.ssh = None
        self.channel = None

#funktion zum Verbindungsaufbau zum Ziel
    def connect(self):
        try:
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            host = self.host_entry.get()
            username = self.username_entry.get()
            password = self.password_entry.get()
            self.ssh.connect(host, username=username, password=password)

            self.channel = self.ssh.invoke_shell()
#Einen snede kanal erstllen, SSH braucht sowas
            self.channel.send("\n")

            self.receive_thread = threading.Thread(target=self.receive_output)
            self.receive_thread.daemon = True
            self.receive_thread.start()

            self.output_area.insert(tk.END, "Connected to the server.\n")
#exeption falls, es nicht geht
        except Exception as e:
            self.output_area.insert(tk.END, f"An error occurred: {e}\n")
#Funktion zum Forwarden der eingegebenen commands int der command line
    def send_command(self, event):
        command = self.command_entry.get() + "\n"
        if self.channel is not None:
            self.channel.send(command)
            self.command_entry.delete(0, tk.END)
#den Output in das Textfeld forwarden
    def receive_output(self):
        while True:
            if self.channel.recv_ready():
                output = self.channel.recv(1024).decode('utf-8')
                self.output_area.insert(tk.END, output)
                self.output_area.see(tk.END)
            time.sleep(0.1)

if __name__ == "__main__":
    root = tk.Tk()
    app = SSHClient(root)
    root.mainloop()
    open(pwmanager)
