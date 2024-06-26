import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
import os

class PWManager:
    def __init__(self):
        self.filename = ""
        self.DB = {}

    def create_new_db(self):
        self.filename = simpledialog.askstring("Input", "Wie willst du die neue Datenbank nennen?")
        if self.filename:
            self.DB = {}
            with open(self.filename + '.txt', 'w') as f:
                f.write(str(self.DB))
            messagebox.showinfo("Info", "Datenbank erstellt")

    def load_existing_db(self):
        self.filename = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if self.filename and os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                self.DB = eval(f.read())
            messagebox.showinfo("Info", "Datenbank geladen")
        else:
            messagebox.showerror("Error", "Datei existiert nicht!")

    def show_all_pws(self):
        pws = '\n'.join([f"{k}: {v}" for k, v in self.DB.items()])
        messagebox.showinfo("Alle Passwörter", pws if pws else "Keine Passwörter gefunden")

    def add_new_pw(self):
        key = simpledialog.askstring("Input", "Bitte geben sie den Nutzernamen ein:")
        if key:
            if key in self.DB:
                messagebox.showerror("Error", "Schlüssel existiert bereits!")
            else:
                value = simpledialog.askstring("Input", "Bitte geben sie das Passwort ein:")
                if value:
                    self.DB[key] = value
                    with open(self.filename, 'w') as f:
                        f.write(str(self.DB))
                    messagebox.showinfo("Info", "Passwort hinzugefügt")

    def delete_pw(self):
        key = simpledialog.askstring("Input", "Bitte geben sie den Nutzernamen ein:")
        if key and key in self.DB:
            del self.DB[key]
            with open(self.filename, 'w') as f:
                f.write(str(self.DB))
            messagebox.showinfo("Info", "Passwort gelöscht")
        else:
            messagebox.showerror("Error", "Passwort existiert nicht!")

    def update_pw(self):
        key = simpledialog.askstring("Input", "Bitte geben sie den Nutzernamen ein:")
        if key and key in self.DB:
            value = simpledialog.askstring("Input", "Bitte geben sie das neues Passwort ein:")
            if value:
                self.DB[key] = value
                with open(self.filename, 'w') as f:
                    f.write(str(self.DB))
                messagebox.showinfo("Info", "Passwort aktualisiert")
        else:
            messagebox.showerror("Error", "Schlüssel existiert nicht!")

def main():
    manager = PWManager()

    def create_db():
        manager.create_new_db()

    def load_db():
        manager.load_existing_db()

    def show_pws():
        manager.show_all_pws()

    def add_pw():
        manager.add_new_pw()

    def del_pw():
        manager.delete_pw()

    def upd_pw():
        manager.update_pw()

    root = tk.Tk()
    root.title("Password Manager")

    tk.Button(root, text="Create New Database", command=create_db).pack(fill=tk.X)
    tk.Button(root, text="Load Existing Database", command=load_db).pack(fill=tk.X)
    tk.Button(root, text="Show All Passwords", command=show_pws).pack(fill=tk.X)
    tk.Button(root, text="Add New Password", command=add_pw).pack(fill=tk.X)
    tk.Button(root, text="Delete Password", command=del_pw).pack(fill=tk.X)
    tk.Button(root, text="Update Password", command=upd_pw).pack(fill=tk.X)
    tk.Button(root, text="Exit", command=root.quit).pack(fill=tk.X)

    root.mainloop()

if __name__ == "__main__":
    main()
