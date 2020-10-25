from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3

con = sqlite3.connect("library.db")
cur = con.cursor()

class AddBook(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.title("Add Book")
        self.geometry("720x480+550+250")
        self.resizable(False, False)
        self.iconbitmap("image/book_tk.ico")

#Frames
        self.top_frame = Frame(self,height=100,bg="white")
        self.top_frame.pack(fill=X)

        self.bottom_frame = Frame(self,height=380,bg="#d3d3d3")
        self.bottom_frame.pack(fill=X)

        #Top_Frame
        self.label_add_book_icon = PhotoImage(file="image/book.png")
        self.label_add_book = Label(self.top_frame,text="Add Book",image=self.label_add_book_icon,font="Roboto 20 bold",bg="white",compound=LEFT,padx=20)
        self.label_add_book.place(x=240,y=12)

        #Bottom_Frame
        self.name = Label(self.bottom_frame,text="Name:",font=("Open Sans","13","bold"),bg="#d3d3d3")
        self.entry_name = ttk.Entry(self.bottom_frame,font=("Proxima Nova","13"),width=20)
        self.name.place(x=220, y=30)
        self.entry_name.place(x=320, y=30)

        self.author = Label(self.bottom_frame,text="Author:",font=("Open Sans","13","bold"),bg="#d3d3d3")
        self.entry_author = ttk.Entry(self.bottom_frame, font=("Proxima Nova","13"), width=20)
        self.author.place(x=220, y=90)
        self.entry_author.place(x=320, y=90)

        self.page = Label(self.bottom_frame,text="Page:",font=("Open Sans","13","bold"),bg="#d3d3d3")
        self.entry_page = ttk.Entry(self.bottom_frame, font=("Proxima Nova","13"), width=20)
        self.page.place(x=220, y=150)
        self.entry_page.place(x=320, y=150)

        self.add_btn = Button(self.bottom_frame,text="Add Book",font=("Open Sans", "11","bold"),fg="#107896",relief=GROOVE,width=15,height=2,command=self.AddBook)
        self.add_btn.place(x=320,y=210)

    def AddBook(self):
        name = self.entry_name.get()
        author_name = self.entry_author.get()
        page = self.entry_page.get()

        if (name and author_name and page != ""):
            try:
                query = "INSERT INTO 'books' (book_name,book_author,book_page) VALUES(?,?,?)"
                cur.execute(query,(name,author_name,page))
                con.commit()
                message_box = messagebox.showinfo("Success","Book added successfully!")
            except:
                message_box = messagebox.showerror("Error","Error adding book!",icon='warning')
        else:
            message_box = messagebox.showerror("Error","Error adding book!",icon='warning')

        self.destroy()
