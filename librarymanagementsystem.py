import tkinter as tk
from tkinter import messagebox
import sqlite3

# Database setup
def connect():
    conn = sqlite3.connect("books.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, title TEXT, author TEXT, year INTEGER, isbn TEXT)")
    conn.commit()
    conn.close()

def insert(title, author, year, isbn):
    conn = sqlite3.connect("books.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO books VALUES (NULL, ?, ?, ?, ?)", (title, author, year, isbn))
    conn.commit()
    conn.close()

def view():
    conn = sqlite3.connect("books.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM books")
    rows = cur.fetchall()
    conn.close()
    return rows

def search(title="", author="", year="", isbn=""):
    conn = sqlite3.connect("books.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM books WHERE title=? OR author=? OR year=? OR isbn=?", (title, author, year, isbn))
    rows = cur.fetchall()
    conn.close()
    return rows

def delete(id):
    conn = sqlite3.connect("books.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM books WHERE id=?", (id,))
    conn.commit()
    conn.close()

def update(id, title, author, year, isbn):
    conn = sqlite3.connect("books.db")
    cur = conn.cursor()
    cur.execute("UPDATE books SET title=?, author=?, year=?, isbn=? WHERE id=?", (title, author, year, isbn, id))
    conn.commit()
    conn.close()

connect()

# GUI setup
class LibraryApp:
    def __init__(self, window):
        self.window = window
        self.window.wm_title("Library Management System")

        # Labels
        self.l1 = tk.Label(window, text="Title")
        self.l1.grid(row=0, column=0)

        self.l2 = tk.Label(window, text="Author")
        self.l2.grid(row=0, column=2)

        self.l3 = tk.Label(window, text="Year")
        self.l3.grid(row=1, column=0)

        self.l4 = tk.Label(window, text="ISBN")
        self.l4.grid(row=1, column=2)

        # Entries
        self.title_text = tk.StringVar()
        self.e1 = tk.Entry(window, textvariable=self.title_text)
        self.e1.grid(row=0, column=1)

        self.author_text = tk.StringVar()
        self.e2 = tk.Entry(window, textvariable=self.author_text)
        self.e2.grid(row=0, column=3)

        self.year_text = tk.StringVar()
        self.e3 = tk.Entry(window, textvariable=self.year_text)
        self.e3.grid(row=1, column=1)

        self.isbn_text = tk.StringVar()
        self.e4 = tk.Entry(window, textvariable=self.isbn_text)
        self.e4.grid(row=1, column=3)

        # Listbox and Scrollbar
        self.list1 = tk.Listbox(window, height=6, width=35)
        self.list1.grid(row=2, column=0, rowspan=6, columnspan=2)

        self.sb1 = tk.Scrollbar(window)
        self.sb1.grid(row=2, column=2, rowspan=6)

        self.list1.configure(yscrollcommand=self.sb1.set)
        self.sb1.configure(command=self.list1.yview)

        self.list1.bind('<<ListboxSelect>>', self.get_selected_row)

        # Buttons
        self.b1 = tk.Button(window, text="View all", width=12, command=self.view_command)
        self.b1.grid(row=2, column=3)

        self.b2 = tk.Button(window, text="Search entry", width=12, command=self.search_command)
        self.b2.grid(row=3, column=3)

        self.b3 = tk.Button(window, text="Add entry", width=12, command=self.add_command)
        self.b3.grid(row=4, column=3)

        self.b4 = tk.Button(window, text="Update selected", width=12, command=self.update_command)
        self.b4.grid(row=5, column=3)

        self.b5 = tk.Button(window, text="Delete selected", width=12, command=self.delete_command)
        self.b5.grid(row=6, column=3)

        self.b6 = tk.Button(window, text="Close", width=12, command=window.destroy)
        self.b6.grid(row=7, column=3)

    def get_selected_row(self, event):
        try:
            index = self.list1.curselection()[0]
            self.selected_tuple = self.list1.get(index)
            self.e1.delete(0, tk.END)
            self.e1.insert(tk.END, self.selected_tuple[1])
            self.e2.delete(0, tk.END)
            self.e2.insert(tk.END, self.selected_tuple[2])
            self.e3.delete(0, tk.END)
            self.e3.insert(tk.END, self.selected_tuple[3])
            self.e4.delete(0, tk.END)
            self.e4.insert(tk.END, self.selected_tuple[4])
        except IndexError:
            pass

    def view_command(self):
        self.list1.delete(0, tk.END)
        for row in view():
            self.list1.insert(tk.END, row)

    def search_command(self):
        self.list1.delete(0, tk.END)
        for row in search(self.title_text.get(), self.author_text.get(), self.year_text.get(), self.isbn_text.get()):
            self.list1.insert(tk.END, row)

    def add_command(self):
        insert(self.title_text.get(), self.author_text.get(), self.year_text.get(), self.isbn_text.get())
        self.list1.delete(0, tk.END)
        self.list1.insert(tk.END, (self.title_text.get(), self.author_text.get(), self.year_text.get(), self.isbn_text.get()))

    def delete_command(self):
        delete(self.selected_tuple[0])
        self.view_command()

    def update_command(self):
        update(self.selected_tuple[0], self.title_text.get(), self.author_text.get(), self.year_text.get(), self.isbn_text.get())
        self.view_command()

window = tk.Tk()
LibraryApp(window)
window.mainloop()
