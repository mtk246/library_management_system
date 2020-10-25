from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedTk
from tkinter import messagebox
import sqlite3
import csv
import add_book
import add_member
import lend_book
import return_book
import member_info
import member_update

con = sqlite3.connect("library.db")
cur = con.cursor()

class Main(object):
    def __init__(self,master):
        self.master = master

        def ShowStatistics(evt):
            count_books = cur.execute("SELECT count(book_id) FROM books").fetchall()
            count_members = cur.execute("SELECT count(member_id) FROM members").fetchall()
            count_lend_books = cur.execute("SELECT count(book_id) FROM books WHERE book_status=1").fetchall()

            self.label_book_count.config(text="Books in library : " + str(count_books[0][0]) + " book(s).")
            self.label_member_count.config(text="Library Members : " + str(count_members[0][0]) + " member(s).")
            self.label_lend_book_count.config(text="Lend books from library : " + str(count_lend_books[0][0]) + " book(s).")

            ShowBook(self)

        def BookBorrowed(evt):
            books = cur.execute("SELECT * FROM lend_books").fetchall()
            try:
                self.label_book_info.config(state=NORMAL)
                self.label_book_info.delete(0,END)
                count = 1
                for book in books:
                    self.label_book_info.insert(count,"Book id- "+book[1].split("-")[0]+" by member id- "+book[2].split("-")[0])
                    count+=1
                self.label_book_info.config(state=DISABLED)
            except:
                pass

        def MemberInfo(evt):
            members = cur.execute("SELECT * FROM members").fetchall()
            try:
                self.member_info.delete(0,END)
                count = 1
                for member in members:
                    self.member_info.insert(count,"Member id- "+str(member[0])+" member name- "+member[1])
                    count+=1
            except:
                pass


        def ShowBook(self):
            books = cur.execute("SELECT * FROM books").fetchall()

            self.list_books.delete(0,END)
            count = 1
            for book in books:
                with open("text/all_books.txt", 'w', encoding='utf-8') as file:
                    file.write("All Books' Information" + "\n\n")
                    query = cur.execute("SELECT * FROM books").fetchall()
                    for i in query:
                        check_available = str(i[4])
                        if check_available == "0":
                            label_available = "Available"
                        elif check_available == "1":
                            label_available = "Not Available"

                        file.write("Book id= "+str(i[0]) + " , " + "Book name= " + str(i[1]) + " , " + "Author name= " + str(i[2])+ " , " + "Pages= "+ str(i[3]) + " , " + "Available= " + label_available +"\n")

                with open("excel/all_books.csv",'w',newline="") as file2:
                    query = cur.execute("SELECT * FROM books").fetchall()
                    for i in query:
                        excel_format = "{0}".format(" ".join(str(x) for x in i))
                        excel_double_format = excel_format.split(" ")
                        excel_file = csv.writer(file2, dialect="excel")
                        excel_file.writerow(excel_double_format)

                self.list_books.insert(count,str(book[0])+" - "+book[1])
                count += 1

            def BookInfo(evt):
                value = str(self.list_books.get(self.list_books.curselection()))
                id = value.split('-')[0]
                book = cur.execute("SELECT * FROM books WHERE book_id=?",(id,))
                book_info = book.fetchall()

                self.detail.config(state=NORMAL)
                self.detail.delete(0,END)
                self.detail.insert(0,"Book Name: "+book_info[0][1])
                self.detail.insert(1,"Author: "+book_info[0][2])
                self.detail.insert(2,"Pages: "+book_info[0][3])

                if book_info[0][4] == '0':
                    self.detail.insert(3,"Status: Available")
                else:
                    self.detail.insert(3, "Status: Not Available")
                self.detail.config(state=DISABLED)

            def DoubleClicked(evt):
                global lend_id
                value = str(self.list_books.get(self.list_books.curselection()))
                lend_id = value.split("-")[0]
                lend_book = LendBook()

            self.list_books.bind("<<ListboxSelect>>", BookInfo)
            self.tabs.bind("<<NotebookTabChanged>>", ShowStatistics)
            self.tabs.bind("<<NotebookTabChanged>>", BookBorrowed)
            self.list_books.bind("<Double-Button-1>",DoubleClicked)


#Frames
        main_frame = ttk.Frame(self.master)
        main_frame.pack()

        top_frame = Frame(main_frame,width=1280,height=100,relief=GROOVE,bg='#f8f8f8')
        top_frame.pack(side=TOP,fill=X)

        center_frame = Frame(main_frame,width=1280,height=650,relief=GROOVE,bg="#ececec",bd=5,borderwidth=3)
        center_frame.pack(side=BOTTOM,fill=X)

        center_left_frame = Frame(center_frame,width=880,height=650,relief=RIDGE,bg="#ececec",bd=5,borderwidth=3)
        center_left_frame.pack(side=LEFT)

        center_right_frame = Frame(center_frame,width=400,height=650,relief=RIDGE,bg="#ececec",bd=5,borderwidth=3)
        center_right_frame.pack()

#Content in Center Left Frames
        self.tabs = ttk.Notebook(center_left_frame, width=880, height=650)
        self.tabs.pack()

        self.tab1_icon = PhotoImage(file="image/book_2.png")
        self.tab2_icon = PhotoImage(file="image/statistics.png")
        self.tab3_icon = PhotoImage(file="image/book_borrowed.png")
        self.tab4_icon = PhotoImage(file="image/book_borrowed.png")

        self.tab1 = ttk.Frame(self.tabs)
        self.tab2 = ttk.Frame(self.tabs)
        self.tab3 = ttk.Frame(self.tabs)
        self.tab4 = ttk.Frame(self.tabs)

        self.tabs.add(self.tab1, text="Library Management",image=self.tab1_icon,compound=LEFT)
        self.tabs.add(self.tab2, text="Statistics",image=self.tab2_icon,compound=LEFT)
        self.tabs.add(self.tab3, text="Book borrowed from library",image=self.tab3_icon,compound=LEFT)
        self.tabs.add(self.tab4, text="Member Info",image=self.tab4_icon,compound=LEFT)

#Library Management Tab
        #ListBar
        self.list_books = Listbox(self.tab1,width=50,height=30,bd=5,font=("Proxima Nova","10","bold"),relief=FLAT)
        self.scrollbar = Scrollbar(self.tab1,orient=VERTICAL)
        self.list_books.insert(0,"All Books :")
        self.list_books.grid(row=0,column=0,padx=(10,0),sticky=N)
        self.scrollbar.config(command=self.list_books.yview)
        self.list_books.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.grid(row=0,column=0,sticky=N+S+E)

        #ListDetails
        self.detail = Listbox(self.tab1,width=32,height=29,bd=5,font=("Proxima Nova","10","bold"),relief=FLAT)
        self.detail.config(state=NORMAL)
        self.detail.grid(row=0,column=1,padx=(10,0),ipadx=20,ipady=10)

#Statistics
        #ListBar
        self.label_book_count = Label(self.tab2,font=("Proxima Nova","15","bold"))
        self.label_member_count = Label(self.tab2,font=("Proxima Nova","15","bold"))
        self.label_lend_book_count = Label(self.tab2,font=("Proxima Nova","15","bold"))

        self.label_book_count.grid(row=0,padx=20,pady=(15,0),sticky=W)
        self.label_member_count.grid(row=1,padx=20,pady=(15,0),sticky=W)
        self.label_lend_book_count.grid(row=2,padx=20,pady=(15,0),sticky=W)

        ShowBook(self)
        ShowStatistics(self)

# BookBorrowed
        # ListBar
        self.label_book_info = Listbox(self.tab3, font=("Proxima Nova","10","bold"),width=100,height=28)
        self.list_books.insert(0, "All Books :")
        self.label_book_info_scrollbar = Scrollbar(self.tab3,orient=VERTICAL)
        self.label_book_info.grid(row=0, padx=20, pady=(15, 0), sticky=W)
        self.label_book_info_scrollbar.config(command=self.label_book_info.yview)
        self.label_book_info.config(yscrollcommand=self.label_book_info_scrollbar.set)
        self.label_book_info_scrollbar.grid(row=0,column=0,pady=(15,0),sticky=N+S+E)
        BookBorrowed(self)

#MemberList
        # ListBar
        self.member_info = Listbox(self.tab4, font=("Proxima Nova","10","bold"), width=50, height=28)
        self.member_info_scrollbar = Scrollbar(self.tab4, orient=VERTICAL)
        self.member_info.grid(row=0, padx=20, pady=(15, 0), sticky=W)
        self.member_info_scrollbar.config(command=self.member_info.yview)
        self.member_info.config(yscrollcommand=self.member_info_scrollbar.set)
        self.member_info_scrollbar.grid(row=0, column=0, pady=(15, 0), sticky=N + S + E)
        self.member_get_info_btn = Button(self.tab4,text="Get Info",font=("Open Sans","12","bold"),fg="#107896",width=15,relief=GROOVE,command=self.MemberInfoBtn)
        self.member_get_info_btn.grid(row=0,column=1,padx=40,pady=(30,0),sticky=N)
        self.member_update_info_btn = Button(self.tab4,text="Update Info",font=("Open Sans","12","bold"),fg="#107896",width=15,relief=GROOVE,command=self.MemberUpdateBtn)
        self.member_update_info_btn.grid(row=0,column=1,padx=50,pady=(80,0),sticky=N)
        self.member_delete_info_btn = Button(self.tab4, text="Delete Member", font=("Open Sans","12","bold"),fg="#107896", width=15,relief=GROOVE,command=self.MemberDeleteBtn)
        self.member_delete_info_btn.grid(row=0, column=1, padx=50, pady=(130, 0), sticky=N)
        MemberInfo(self)


#Content in Center Right Frames
        #SearchBar
        self.search_bar_frame = Frame(center_right_frame,width=400,height=100,relief=GROOVE,bg="#ececec")
        self.search_bar_frame.pack(fill=BOTH)

        self.label_search_bar = Label(self.search_bar_frame,text="Search:",font=("Open Sans","12","bold"),bg="#ececec")
        self.label_search_bar.grid(row=0,column=0,padx=(10,5),pady=10)

        self.entry_search_bar = ttk.Entry(self.search_bar_frame,font=("Open Sans","12","italic"),width=18,justify=CENTER)
        self.entry_search_bar.grid(row=0,column=1,padx=3,pady=10,ipadx=10,ipady=10)

        self.btn_search_bar = Button(self.search_bar_frame,text="Search Book",font=("Open Sans","8","bold"),fg="#107896",relief=GROOVE,width=12,height=1,command=self.funcSearchBooks)
        self.btn_search_bar.grid(row=0,column=2,padx=3,pady=10)

        #ListBar
        self.list_box_frame = Frame(center_right_frame,width=400,height=100, relief=GROOVE,bg="#f8f8f8")
        self.list_box_frame.pack(fill=BOTH,padx=10,pady=20)

        self.listChoice = IntVar()
        self.radio_btn_1 = Radiobutton(self.list_box_frame,text="All Books",font=("Open Sans","9"),value=1,bg="#f8f8f8",var=self.listChoice)
        self.radio_btn_2 = Radiobutton(self.list_box_frame,text="Available in Library",font=("Open Sans","9"),value=2,bg="#f8f8f8",var=self.listChoice)
        self.radio_btn_3 = Radiobutton(self.list_box_frame,text="Lend Books",font=("Open Sans","9"),value=3,bg="#f8f8f8",var=self.listChoice)

        self.radio_btn_1.grid(row=0,column=0,padx=6,pady=10)
        self.radio_btn_2.grid(row=0,column=1,padx=6,pady=10)
        self.radio_btn_3.grid(row=0,column=2,padx=6,pady=10)

        self.btn_list_box = Button(self.list_box_frame,text="Sort Book",font=("Open Sans","10","bold"),fg="#107896",relief=GROOVE,width=12,height=1,command=self.funcSortBooks)
        self.btn_list_box.grid(row=1,column=1,pady=10)



#ToolBars
        self.add_book_icon = PhotoImage(file="image/book.png")
        self.add_book = Button(top_frame,text="Add Book",font="Roboto 12 bold",image=self.add_book_icon,compound=LEFT,padx=20,pady=10,relief=FLAT,bg="#dddddd",bd=3,command=self.funcAddBook)
        self.add_book.pack(side=LEFT,padx=10,pady=10)

        self.add_member_icon = PhotoImage(file="image/add_member.png")
        self.add_member = Button(top_frame,text="Add Member",font="Roboto 12 bold",image=self.add_member_icon,compound=LEFT,padx=20,pady=10,relief=FLAT,bg="#dddddd",bd=3,command=self.funcAddMember)
        self.add_member.pack(side=LEFT,padx=10,pady=10)

        self.give_book_icon = PhotoImage(file="image/give_book.png")
        self.give_book = Button(top_frame,text="Lend Book",font="Roboto 12 bold",image=self.give_book_icon,compound=LEFT,padx=20,pady=10,relief=FLAT,bg="#dddddd",bd=3,command=self.funcLendBook)
        self.give_book.pack(side=LEFT,padx=10,pady=10)

        self.return_book_icon = PhotoImage(file="image/return_book.png")
        self.return_book = Button(top_frame, text="Return Book", font="Roboto 12 bold", image=self.return_book_icon,
                                compound=LEFT, padx=20, pady=10, relief=FLAT, bg="#dddddd", bd=3,
                                command=self.funcReturnBook)
        self.return_book.pack(side=LEFT, padx=10, pady=10)

#Functions
    def funcAddBook(self):
        open_add_book = add_book.AddBook()

    def funcAddMember(self):
        open_add_member = add_member.AddMember()

    def MemberInfoBtn(self):
        self.get_info_btn = self.member_info.get(self.member_info.curselection())
        split_get_info = self.get_info_btn.split()
        with open("text/temp_member_info.txt",'w') as temp_file:
            temp_file.write(split_get_info[2])
        open_member_info = member_info.MemberInfo()

    def MemberUpdateBtn(self):
        self.get_info_btn = self.member_info.get(self.member_info.curselection())
        split_get_info = self.get_info_btn.split()
        with open("text/temp_member_info.txt", 'w') as temp_file:
            temp_file.write(split_get_info[2])
        open_member_info = member_update.MemberUpdate()

    def MemberDeleteBtn(self):
        self.get_info_btn = self.member_info.get(self.member_info.curselection())
        split_get_info = self.get_info_btn.split()
        try:
            member_id = split_get_info[2]
            message_box = messagebox.askquestion("Delete","Are you confirm to delete "+split_get_info[5])
            if message_box == "yes":
                query = cur.execute("DELETE FROM members WHERE member_id=?",(member_id))
                con.commit()
                messagebox.showinfo("Success","Delete "+split_get_info[5]+" successfully!")
            else:
                messagebox.showinfo("Error","Error deleting member")
        except:
            messagebox.showinfo("Error","Error deleting member")

    def funcLendBook(self):
        open_lend_book = lend_book.LendBook()

    def funcReturnBook(self):
        open_return_book = return_book.ReturnBook()

    def funcSearchBooks(self):
        try:
            if self.entry_search_bar.get() != "":
                books = self.entry_search_bar.get()
                query = "SELECT * FROM books WHERE book_name LIKE ?"
                search = cur.execute(query,("%"+books+"%",)).fetchall()

                self.list_books.delete(0,END)
                self.list_books.insert(0,"You searched :")
                count = 1
                for book in search:
                    self.list_books.insert(count,str(book[0])+" - "+book[1])
                    count+=1
            elif self.entry_search_bar.get() == "":
                all_books = con.execute("SELECT * FROM books").fetchall()
                self.list_books.delete(0, END)

                self.list_books.insert(0, "All Books :")
                count = 1
                for book in all_books:
                    self.list_books.insert(count, str(book[0]) + " - " + book[1])
                    count += 1
        except:
            pass

    def funcSortBooks(self):
        value = self.listChoice.get()
        if value == 1:
            all_books = con.execute("SELECT * FROM books").fetchall()
            self.list_books.delete(0,END)

            self.list_books.insert(0,"All Books :")
            count=1
            for book in all_books:
                self.list_books.insert(count,str(book[0])+" - "+book[1])
                count+=1
        elif value == 2:
            in_library = con.execute("SELECT * FROM books WHERE book_status=?",(0,)).fetchall()
            self.list_books.delete(0,END)

            self.list_books.insert(0,"Available in Library :")
            count = 1
            for book in in_library:
                self.list_books.insert(count,str(book[0])+" - "+book[1])
                count+=1
        elif value == 3:
            lend_books = con.execute("SELECT * FROM books WHERE book_status=?",(1,)).fetchall()
            self.list_books.delete(0,END)

            self.list_books.insert(0,"Lend Books :")
            count = 1
            for book in lend_books:
                self.list_books.insert(count,str(book[0])+" - "+book[1])
                count+=1


class LendBook(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.title("Lend Book")
        self.geometry("720x480+550+250")
        self.resizable(False, False)
        self.iconbitmap("image/book_tk.ico")

        global lend_id
        self.bookid = int(lend_id)

        query = "SELECT * FROM books WHERE book_status='0'"
        books = cur.execute(query).fetchall()
        book_list = []
        for book in books:
            book_list.append(str(book[0]) + " - " + book[1])

        query2 = "SELECT * FROM members"
        members = cur.execute(query2).fetchall()
        member_list = []
        for member in members:
            member_list.append(str(member[0]) + " - " + member[1])


        # Frames
        self.top_frame = Frame(self, height=100, bg="white")
        self.top_frame.pack(fill=X)

        self.bottom_frame = Frame(self, height=380, bg="#d3d3d3")
        self.bottom_frame.pack(fill=X)

        # Top_Frame
        self.label_add_member_icon = PhotoImage(file="image/give_book.png")
        self.label_add_member = Label(self.top_frame, text="Lend Book", image=self.label_add_member_icon,
                                      font="Arial 23 bold", bg="white", compound=LEFT, padx=20)
        self.label_add_member.place(x=240, y=12)

        # Bottom_Frame
        self.bookname = StringVar()
        self.label_name = Label(self.bottom_frame, text="Book Name:", font="verdana 13 bold", bg="#d3d3d3")
        self.combo_label_name = ttk.Combobox(self.bottom_frame,textvariable=self.bookname)
        self.combo_label_name['values'] = book_list
        # self.combo_label_name.current(self.bookid-1)
        self.label_name.place(x=180, y=60)
        self.combo_label_name.place(x=320, y=60)


        self.membername = StringVar()
        self.member_name = Label(self.bottom_frame, text="Member Name:", font="verdana 13 bold", bg="#d3d3d3")
        self.combo_member_name = ttk.Combobox(self.bottom_frame,textvariable=self.membername,)
        self.combo_member_name['values'] = member_list
        self.member_name.place(x=150, y=120)
        self.combo_member_name.place(x=320, y=120)


        self.add_btn = Button(self.bottom_frame, text="Give Book", font="verdana 10", borderwidth=0, bg="white",
                              padx=20, pady=10,command=self.LendBook)
        self.add_btn.place(x=320, y=180)

    def LendBook(self):
        book_name = self.combo_label_name.get()
        self.bookid = book_name.split("-")[0]
        member_name = self.combo_member_name.get()
        text_book_name = book_name[0]
        text_member_name = member_name[0]
        print("Book id=",text_book_name, "Member id=",text_member_name)

        try:
            if book_name and member_name != "":
                query = cur.execute("SELECT count(lend_member_id) FROM lend_books WHERE lend_member_id=?",
                                    (member_name,)).fetchall()
                print(query)
                times_lend_member = query[0][0]
                print(times_lend_member)
                if times_lend_member >= 3:
                    messagebox.showerror("Exceed the amount of lend time",
                                         member_name.split("-")[1] + " lend the books for 3 times already!")
                else:
                    cur.execute("INSERT INTO 'lend_books' (lend_book_id,lend_member_id) VALUES(?,?)",
                                (book_name, member_name))
                    con.commit()
                    messagebox.showinfo("Success", "Give book to the member successfully")
                    cur.execute("UPDATE books SET book_status=? WHERE book_id=?", (1, self.bookid))
                    con.commit()
            else:
                messagebox.showerror("Error", "Please Check again!")
        except:
            messagebox.showerror("Error", "Please Check again!")
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

def Login():
    root_login = ThemedTk()
    root_login.get_themes()
    root_login.set_theme("arc")

    def BtnLogin():
        user_name = entry_username.get()
        password = entry_password.get()
        try:
            query = cur.execute("SELECT * FROM register_user").fetchall()
            if user_name==str(query[0][1]) and password==str(query[0][2]):
                messagebox.showinfo("Login Successful","Welcome to Library Management System")
                root_login.destroy()
                main()
            else:
                messagebox.showerror("Login Fail","Check username or password again")
                exit()
        except:
            messagebox.showerror("Login Fail","Check username or password again")
            exit()
    #
    # # MenuBar
    # menu_bar = Menu(root_login)
    # root_login.config(menu=menu_bar)
    # file = Menu(menu_bar, tearoff=0)
    # menu_bar.add_cascade(label="File", menu=file)
    # file.add_command(label="Add a Book", )
    # file.add_command(label="Add a Member", )
    # file.add_command(label="Show Member")
    # file.add_command(label="Exit", )

    main_frame = ttk.Frame(root_login, width=400, height=200)
    main_frame.pack(fill=X)

    label_username = Label(main_frame, text="Username:", font="Arial 15 bold")
    label_username.grid(row=0, column=0, padx=(30, 0), pady=(30, 0), sticky=W)

    entry_username = ttk.Entry(main_frame, width=23, font="Arial 13 bold")
    entry_username.grid(row=0, column=1, padx=(20, 0), pady=(30, 0))

    label_password = Label(main_frame, text="Password:", font="Arial 15 bold")
    label_password.grid(row=1, column=0, padx=(30, 0), pady=(15, 0), sticky=W)

    entry_password = ttk.Entry(main_frame, width=23, font="Arial 13 bold")
    entry_password.config(show="*")
    entry_password.grid(row=1, column=1, padx=(20, 0), pady=(15, 0))
    btn_login = Button(root_login, text="Login",font="Arial 13 bold",width=15,bg="#4285f4",fg="#ececec",command=BtnLogin)
    btn_login.place(x=120,y=120)


    root_login.title("Library Management System")
    root_login.geometry("400x200+700+400")
    root_login.resizable(False, False)
    root_login.iconbitmap("image/book_tk.ico")
    root_login.mainloop()

def main():
    def funcExit():
        message_box = messagebox.askquestion("Exit", "Do you want to exit?",icon='warning')
        if message_box == "yes":
            root.destroy()

    def funcAddBook():
        open_add_book = add_book.AddBook()

    def funcAddMember():
        open_add_member = add_member.AddMember()

    root = ThemedTk()
    root.get_themes()
    root.set_theme("arc")
    app = Main(root)

    #MenuBar
    menu_bar = Menu(root)
    root.config(menu=menu_bar)
    file = Menu(menu_bar,tearoff=0)
    menu_bar.add_cascade(label="File",menu=file)
    file.add_command(label="Add a Book",command=funcAddBook)
    file.add_command(label="Add a Member",command=funcAddMember)
    file.add_command(label="Show Member")
    file.add_command(label="Exit",command=funcExit)

    root.title("Library Management System")
    root.geometry("1280x720+450+150")
    root.resizable(False,False)
    root.iconbitmap("image/book_tk.ico")
    root.mainloop()

if __name__ == "__main__":
    main()