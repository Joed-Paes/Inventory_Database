from tkinter import *
from PIL import Image, ImageTk  # pip install pillow
from tkinter import ttk, messagebox
import sqlite3
import os

class salesClass:
    def __init__(self, root):
        self.root = root;
        self.root.geometry("1100x500+220+130")
        self.root.title("Inventory Management System | Developed by Joed")
        self.root.config(bg="white")
        self.root.focus_force()
        #################################

        ### variables
        self.bills_list = []
        self.var_invoice = StringVar()

        # title
        title = Label(self.root,text="View Customer Bills",font=("goudy old style",20,"bold"),bg="blue",fg="white").pack(side=TOP,fill=X,padx=10,pady=5)

        lbl_invoice = Label(self.root,text="Invoice number:",font=("times new roman",15),bg="white").place(x=20,y=100)
        txt_invoice = Entry(self.root,textvariable=self.var_invoice,font=("times new roman",15),bg="white").place(x=160,y=100,width=150,height=28)
        # button
        btn_search = Button(self.root,text="Search",command=self.search,font=("times new roman",15,"bold"),bg="green",cursor="hand2").place(x=320,y=100,width=80,height=28)
        btn_clear = Button(self.root,text="Clear",command=self.clear,font=("times new roman",15,"bold"),bg="gray",cursor="hand2").place(x=410,y=100,width=80,height=28)

        # frame - Bill List
        salesFrame = Frame(self.root,bd=3,relief=RIDGE,bg="white")
        salesFrame.place(x=20,y=140,width=200,height=330)

        scrolly = Scrollbar(salesFrame,orient=VERTICAL)
        self.sales_list = Listbox(salesFrame,font=("times new roman",15),bg="white",yscrollcommand=scrolly.set)
        scrolly.pack(side=RIGHT,fill=Y)
        scrolly.config(command=self.sales_list.yview)
        self.sales_list.pack(fill=BOTH, expand=1)
        self.sales_list.bind("<ButtonRelease-1>",self.get_data)

        # frame - Bill Area
        billsFrame = Frame(self.root,bd=3,relief=RIDGE,bg="white")
        billsFrame.place(x=280,y=140,width=410,height=330)

        title = Label(billsFrame,text="Customer Bill Area",font=("goudy old style",15,"bold"),bg="orange").pack(side=TOP,fill=X)

        scrolly2 = Scrollbar(billsFrame,orient=VERTICAL)
        self.bills_area = Text(billsFrame,font=("goudy old style",15),bg="lightyellow",yscrollcommand=scrolly2.set)
        scrolly2.pack(side=RIGHT,fill=Y)
        scrolly2.config(command=self.bills_area.yview)
        self.bills_area.pack(fill=BOTH, expand=1)

        # image
        #====== Left Menu =======
        self.bill_photo = Image.open("images/logo1.png")
        self.bill_photo = self.bill_photo.resize((300,300),Image.ANTIALIAS)
        self.bill_photo = ImageTk.PhotoImage(self.bill_photo)

        lbl_image = Label(self.root,image=self.bill_photo).place(x=750,y=150)

        self.show()

    def show(self):
        del self.bills_list[:]
        self.sales_list.delete(1,END)
        #print(os.listdir("bills"))
        for i in os.listdir('bills'):
            if i.split('.')[-1]=='txt':
                self.sales_list.insert(END,i)
                self.bills_list.append(i.split('.')[0])

    def get_data(self,ev):
        index_ = self.sales_list.curselection()
        filename = self.sales_list.get(index_)
        #print(filename)
        self.bills_area.delete('1.0',END)
        fp = open(f'bills/{filename}','r')
        for i in fp:
            self.bills_area.insert(END,i)
        fp.close()

    def search(self):
        if self.var_invoice.get()=="":
            messagebox.showerror("Error","Invoice number must be required",parent=self.root)
        else:
            if self.var_invoice.get() in self.bills_list:
                self.bills_area.delete('1.0',END)
                fp = open(f'bills/{self.var_invoice.get()}.txt','r')
                for i in fp:
                    self.bills_area.insert(END,i)
                fp.close()
            else:
                messagebox.showerror("Error","Invalid invoice number",parent=self.root)

    def clear(self):
        self.show()
        self.var_invoice.set("")
        self.bills_area.delete('1.0',END)




if __name__=="__main__":
    root = Tk();
    obj = salesClass(root)
    root.mainloop()
