from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3

con = sqlite3.connect("library.db")
cur = con.cursor()

class MemberInfo(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.title("Member Information")
        self.geometry("720x480+550+250")
        self.resizable(False, False)
        self.iconbitmap("image/book_tk.ico")

        # Frames
        self.top_frame = Frame(self, height=100, bg="white")
        self.top_frame.pack(fill=X)

        self.bottom_frame = Frame(self, height=380, bg="#d3d3d3")
        self.bottom_frame.pack(fill=X)

        # Top_Frame
        self.label_add_member_icon = PhotoImage(file="image/member_information.png")
        self.label_add_member = Label(self.top_frame, text="Member Information", image=self.label_add_member_icon,
                                      font="Roboto 20 bold", bg="white", compound=LEFT, padx=20)
        self.label_add_member.place(x=200, y=16)

        with open("text/temp_member_info.txt",'r') as temp_file:
            member_id_read = temp_file.read()

        query = cur.execute("SELECT * FROM members WHERE member_id=?",(member_id_read)).fetchall()
        tuple = query[0]

        self.label_name = Label(self.bottom_frame,text="Name: " + tuple[1],font=("Open Sans","13","bold"),bg="#d3d3d3")
        self.label_email = Label(self.bottom_frame,text="Email: " + tuple[2],font=("Open Sans","13","bold"),bg="#d3d3d3")
        self.label_phone = Label(self.bottom_frame,text="Phone: " + tuple[3],font=("Open Sans","13","bold"),bg="#d3d3d3")
        self.exit_btn = Button(self.bottom_frame,text="Exit",font=("Open Sans", "11","bold"),fg="#107896",relief=GROOVE,width=10,height=2,command=self.ExitBtn)

        self.label_name.place(x=250,y=50)
        self.label_email.place(x=250,y=90)
        self.label_phone.place(x=250,y=130)
        self.exit_btn.place(x=300,y=170)

    def ExitBtn(self):
        self.destroy()


