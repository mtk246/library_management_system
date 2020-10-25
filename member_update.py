from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3

con = sqlite3.connect("library.db")
cur = con.cursor()

class MemberUpdate(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.title("Member Information Update")
        self.geometry("720x480+550+250")
        self.resizable(False, False)
        self.iconbitmap("image/book_tk.ico")

        # Frames
        self.top_frame = Frame(self, height=100, bg="white")
        self.top_frame.pack(fill=X)

        self.bottom_frame = Frame(self, height=380, bg="#d3d3d3")
        self.bottom_frame.pack(fill=X)

        # Top_Frame
        self.label_update_member_icon = PhotoImage(file="image/member_update.png")
        self.label_update_member = Label(self.top_frame, text="Member Information Update", image=self.label_update_member_icon,
                                      font="Roboto 20 bold", bg="white", compound=LEFT, padx=20)
        self.label_update_member.place(x=180, y=16)

        with open("text/temp_member_info.txt",'r') as temp_file:
            self.member_id_read = temp_file.read()

        query = cur.execute("SELECT * FROM members WHERE member_id=?",(self.member_id_read)).fetchall()
        tuple = query[0]

        self.label_name = Label(self.bottom_frame,text="Name: ",font=("Open Sans","13","bold"),bg="#d3d3d3")
        self.entry_label_name = Entry(self.bottom_frame,width=20,font=("Open Sans","13","bold"))
        self.label_email = Label(self.bottom_frame,text="Email: ",font=("Open Sans","13","bold"),bg="#d3d3d3")
        self.entry_email = Entry(self.bottom_frame, width=20, font=("Open Sans","13","bold"))
        self.label_phone = Label(self.bottom_frame,text="Phone: ",font=("Open Sans","13","bold"),bg="#d3d3d3")
        self.entry_phone = Entry(self.bottom_frame, width=20, font=("Open Sans","13","bold"))
        self.update_btn = Button(self.bottom_frame,text="Update",font=("Open Sans", "11","bold"),fg="#107896",relief=GROOVE,width=10,height=2,command=self.UpdateBtn)
        self.exit_btn = Button(self.bottom_frame,text="Exit",font=("Open Sans", "11","bold"),fg="#107896",relief=GROOVE,width=10,height=2,command=self.ExitBtn)

        self.label_name.place(x=250,y=50)
        self.entry_label_name.place(x=350,y=50)
        self.label_email.place(x=250,y=90)
        self.entry_email.place(x=350,y=90)
        self.label_phone.place(x=250,y=130)
        self.entry_phone.place(x=350,y=130)
        self.update_btn.place(x=290,y=180)
        self.exit_btn.place(x=430,y=180)

    def UpdateBtn(self):
        get_name = self.entry_label_name.get()
        get_email = self.entry_email.get()
        get_phone = self.entry_phone.get()

        try:
            if get_name and get_email and get_phone != "":
                cur.execute("UPDATE members SET member_name=?,member_email=?,member_phone=? WHERE member_id=?",(get_name,get_email,get_phone,self.member_id_read))
                con.commit()
                messagebox.showinfo("Success","Update member info successfully!")
            else:
                messagebox.showerror("Error","Member info not updated")
        except:
            messagebox.showerror("Error","Member info not updated")
        finally:
            self.destroy()

    def ExitBtn(self):
        self.destroy()


