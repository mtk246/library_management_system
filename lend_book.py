from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3

con = sqlite3.connect("library.db")
cur = con.cursor()

class LendBook(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.title("Lend Book")
        self.geometry("720x480+550+250")
        self.resizable(False, False)
        self.iconbitmap("image/book_tk.ico")

        query = "SELECT * FROM books WHERE book_status='0'"
        books = cur.execute(query).fetchall()
        book_list = []
        for book in books:
            book_list.append(str(book[0])+" - "+book[1])

        query2 = "SELECT * FROM members"
        members = cur.execute(query2).fetchall()
        member_list = []
        for member in members:
            member_list.append(str(member[0])+" - "+member[1])


        # Frames
        self.top_frame = Frame(self, height=100, bg="white")
        self.top_frame.pack(fill=X)

        self.bottom_frame = Frame(self, height=380, bg="#d3d3d3")
        self.bottom_frame.pack(fill=X)

        # Top_Frame
        self.label_add_member_icon = PhotoImage(file="image/give_book.png")
        self.label_add_member = Label(self.top_frame, text="Lend Book", image=self.label_add_member_icon,
                                      font="Roboto 20 bold", bg="white", compound=LEFT, padx=20)
        self.label_add_member.place(x=240, y=12)

        # Bottom_Frame
        self.bookname = StringVar()
        self.label_name = Label(self.bottom_frame, text="Book Name:", font=("Open Sans","13","bold"), bg="#d3d3d3")
        self.combo_label_name = ttk.Combobox(self.bottom_frame,textvariable=self.bookname)
        self.combo_label_name['values'] = book_list
        self.label_name.place(x=180, y=60)
        self.combo_label_name.place(x=320, y=60)


        self.membername = StringVar()
        self.member_name = Label(self.bottom_frame, text="Member Name:", font=("Open Sans","13","bold"), bg="#d3d3d3")
        self.combo_member_name = ttk.Combobox(self.bottom_frame,textvariable=self.membername,)
        self.combo_member_name['values'] = member_list
        self.member_name.place(x=150, y=120)
        self.combo_member_name.place(x=320, y=120)


        self.add_btn = Button(self.bottom_frame, text="Give Book",font=("Open Sans", "11","bold"),fg="#107896",relief=GROOVE,width=15,height=2,command=self.LendBook)
        self.add_btn.place(x=320, y=180)

    def LendBook(self):
        book_name = self.combo_label_name.get()
        self.bookid = book_name.split("-")[0]
        member_name = self.combo_member_name.get()
        print(member_name)
        try:
            if book_name and member_name != "":
                query = cur.execute("SELECT count(lend_member_id) FROM lend_books WHERE lend_member_id=?",(member_name,)).fetchall()
                times_lend_member = query[0][0]
                print(times_lend_member)
                if times_lend_member >= 3:
                    messagebox.showerror("Exceed the amount of lend time",member_name.split("-")[1] + " lend the books for 3 times already!")
                else:
                    cur.execute("INSERT INTO 'lend_books' (lend_book_id,lend_member_id) VALUES(?,?)",(book_name,member_name))
                    con.commit()
                    messagebox.showinfo("Success","Give book to the member successfully")
                    cur.execute("UPDATE books SET book_status=? WHERE book_id=?",(1,self.bookid))
                    con.commit()
            else:
                messagebox.showerror("Error","Please Check again!")
        except:
            messagebox.showerror("Error","Please Check again!")
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