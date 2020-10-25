from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3

con = sqlite3.connect("library.db")
cur = con.cursor()

class ReturnBook(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.title("Return Book")
        self.geometry("720x480+550+250")
        self.resizable(False, False)
        self.iconbitmap("image/book_tk.ico")

        query = "SELECT * FROM lend_books"
        books = cur.execute(query).fetchall()
        book_list = []
        for book in books:
            book_list.append(book[1])

        query2 = "SELECT * FROM lend_books"
        members = cur.execute(query2).fetchall()
        member_list = []
        for member in members:
            member_list.append(member[2])


        # Frames
        self.top_frame = Frame(self, height=100, bg="white")
        self.top_frame.pack(fill=X)

        self.bottom_frame = Frame(self, height=380, bg="#d3d3d3")
        self.bottom_frame.pack(fill=X)

        # Top_Frame
        self.label_add_member_icon = PhotoImage(file="image/return_book.png")
        self.label_add_member = Label(self.top_frame, text="Return Book", image=self.label_add_member_icon,
                                      font="Roboto 20 bold", bg="white", compound=LEFT, padx=20)
        self.label_add_member.place(x=240, y=12)

        # Bottom_Frame
        self.bookname = StringVar()
        self.label_name = Label(self.bottom_frame, text="Book ID:", font=("Open Sans","13","bold"), bg="#d3d3d3")
        self.combo_label_name = ttk.Combobox(self.bottom_frame,textvariable=self.bookname)
        self.combo_label_name['values'] = book_list
        self.label_name.place(x=180, y=60)
        self.combo_label_name.place(x=320, y=60)


        self.membername = StringVar()
        self.member_name = Label(self.bottom_frame, text="Member ID:", font=("Open Sans","13","bold"), bg="#d3d3d3")
        self.combo_member_name = ttk.Combobox(self.bottom_frame,textvariable=self.membername,)
        self.combo_member_name['values'] = member_list
        self.member_name.place(x=150, y=120)
        self.combo_member_name.place(x=320, y=120)


        self.add_btn = Button(self.bottom_frame, text="Return Book",font=("Open Sans", "11","bold"),fg="#107896",relief=GROOVE,width=15,height=2,command=self.ReturnBook)
        self.add_btn.place(x=320, y=180)

    def ReturnBook(self):
        self.book_name = self.combo_label_name.get()
        self.member_name = self.combo_member_name.get()

        try:
            if self.book_name and self.member_name != "":
                self.bookid = self.book_name.split("-")[0]
                query_all = cur.execute("SELECT * FROM lend_books WHERE lend_book_id=? and lend_member_id=?",(self.book_name,self.member_name)).fetchall()
                con.commit()
                self.check_bookid = query_all[0][1]
                self.check_member_name = query_all[0][2]

                if self.book_name == self.check_bookid and self.member_name == self.check_member_name:
                    cur.execute("UPDATE books SET book_status=? WHERE book_id=?",(0,self.bookid))
                    con.commit()
                    cur.execute("DELETE FROM lend_books WHERE lend_book_id=?",(self.book_name,))
                    con.commit()
                    messagebox.showinfo("Success", "Return book to the library successfully")
            else:
                message_box = messagebox.showerror("Error","Please Check the form again!")
        except:
            message_box = messagebox.showerror("Error","Please Check the form again!")
        finally:
            self.destroy()

        with open("text/lend_book.txt", 'w', encoding='utf-8') as file:
            file.write("Lent Book Information" + "\n\n")
            query = cur.execute("SELECT * FROM lend_books").fetchall()
            for i in query:
                list_split_1 = i[1].split("-")
                list_double_split_1 = list_split_1[0]

                list_split_2 = i[2].split("-")
                list_double_split_2 = list_split_2[0]

                file.write(str(i[0]) + "  " + "Book id= " + str(list_double_split_1) + "  " + "Member id= " + str(list_double_split_2) + "\n")