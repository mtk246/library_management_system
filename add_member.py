from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3

con = sqlite3.connect("library.db")
cur = con.cursor()

class AddMember(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.title("Add Member")
        self.geometry("720x480+550+250")
        self.resizable(False, False)
        self.iconbitmap("image/book_tk.ico")

#Frames
        self.top_frame = Frame(self,height=100,bg="white")
        self.top_frame.pack(fill=X)

        self.bottom_frame = Frame(self,height=380,bg="#d3d3d3")
        self.bottom_frame.pack(fill=X)

        #Top_Frame
        self.label_add_member_icon = PhotoImage(file="image/add_member.png")
        self.label_add_member = Label(self.top_frame,text="Add Member",image=self.label_add_member_icon,font="Roboto 20 bold",bg="white",compound=LEFT,padx=20)
        self.label_add_member.place(x=240,y=12)

        #Bottom_Frame
        self.name = Label(self.bottom_frame,text="Name:",font=("Open Sans","13","bold"),bg="#d3d3d3")
        self.entry_name = ttk.Entry(self.bottom_frame,font=("Proxima Nova","13"),width=20)
        self.name.place(x=220, y=30)
        self.entry_name.place(x=320, y=30)

        self.email = Label(self.bottom_frame, text="Email:", font=("Open Sans","13","bold"), bg="#d3d3d3")
        self.entry_email = ttk.Entry(self.bottom_frame, font=("Proxima Nova","13"), width=20)
        self.email.place(x=220, y=90)
        self.entry_email.place(x=320, y=90)

        self.phone = Label(self.bottom_frame,text="Phone:",font=("Open Sans","13","bold"),bg="#d3d3d3")
        self.entry_phone = ttk.Entry(self.bottom_frame, font=("Proxima Nova","13"), width=20)
        self.phone.place(x=220, y=150)
        self.entry_phone.place(x=320, y=150)

        self.add_btn = Button(self.bottom_frame,text="Add Member",font=("Open Sans", "11","bold"),fg="#107896",relief=GROOVE,width=15,height=2,command=self.AddMember)
        self.add_btn.place(x=320,y=210)

    def AddMember(self):
        name = self.entry_name.get()
        email = self.entry_email.get()
        phone = self.entry_phone.get()

        if (name and email and phone != ""):
            try:
                query = "INSERT INTO 'members' (member_name,member_email,member_phone) VALUES(?,?,?)"
                cur.execute(query,(name,email,phone))
                con.commit()
                message_box = messagebox.showinfo("Success","Member added successfully!")
            except:
                message_box = messagebox.showerror("Error","Error adding member!",icon="warning")
        else:
            message_box = messagebox.showerror("Error","Error adding member!",icon="warning")

        self.destroy()