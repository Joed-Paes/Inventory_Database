from tkinter import *
from PIL import Image, ImageTk  # pip install pillow
from tkinter import ttk, messagebox
import sqlite3

class supplierClass:
    def __init__(self, root):
        self.root = root;
        self.root.geometry("900x500+220+130")
        self.root.title("Inventory Management System | Developed by Joed")
        self.root.config(bg="white")
        self.root.focus_force()
        #################################
        # All variables
        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()

        self.var_sup_invoice = StringVar()
        self.var_name = StringVar()
        self.var_contact = StringVar()

        # Title
        title = Label(self.root,text="Supplier Details",font=("goudy old style",15,"bold"),bg="blue",fg="white")
        title.place(x=0,y=5,relwidth=1,height=40)

        # options
        lbl_search = Label(self.root,text="Invoice no:",bg="white",font=("goudy old style",12))
        lbl_search.place(x=470,y=70)

        txt_search = Entry(self.root,textvariable=self.var_searchtxt,font=("goudy old style",12),bg="lightyellow")
        txt_search.place(x=570,y=70,width=150)
        btn_search = Button(self.root,text="Search",command=self.search,font=("goudy old style",12),bg="green",fg="white",cursor="hand2")
        btn_search.place(x=730,y=70,width=100, height=25)

        # content
        # row 1
        Yrow1 = 80
        lbl_supplier_invoice = Label(self.root,text="Invoice No:",font=("goudy old style",10),bg="white").place(x=10,y=Yrow1)
        txt_supplier_invoice = Entry(self.root,textvariable=self.var_sup_invoice,font=("goudy old style",10),bg="white").place(x=100,y=Yrow1,width=180)

        # row 2
        Yrow2 = 110
        lbl_name = Label(self.root,text="Name:",font=("goudy old style",10),bg="white").place(x=10,y=Yrow2)
        txt_name = Entry(self.root,textvariable=self.var_name,font=("goudy old style",10),bg="white").place(x=100,y=Yrow2,width=180)

        # row 3
        Yrow3 = 140
        lbl_contact = Label(self.root,text="Contact:",font=("goudy old style",10),bg="white").place(x=10,y=Yrow3)
        txt_contact = Entry(self.root,textvariable=self.var_contact,font=("goudy old style",10),bg="white").place(x=100,y=Yrow3,width=180)

        # row 4
        Yrow4 = 170
        lbl_description = Label(self.root,text="Description:",font=("goudy old style",10),bg="white").place(x=10,y=Yrow4)
        self.txt_description = Text(self.root,font=("goudy old style",10),bg="white")
        self.txt_description.place(x=100,y=Yrow4,width=300,height=90)

        # buttons
        btn_add = Button(self.root,text="Save",command=self.add,font=("goudy old style",10),bg="blue",fg="white",cursor="hand2").place(x=50,y=280,width=90, height=30)
        btn_update = Button(self.root,text="Update",command=self.update,font=("goudy old style",10),bg="blue",fg="white",cursor="hand2").place(x=150,y=280,width=90, height=30)
        btn_delete = Button(self.root,text="Delete",command=self.delete,font=("goudy old style",10),bg="blue",fg="white",cursor="hand2").place(x=250,y=280,width=90, height=30)
        btn_clear = Button(self.root,text="Clear",command=self.clear,font=("goudy old style",10),bg="blue",fg="white",cursor="hand2").place(x=350,y=280,width=90, height=30)

        # supplier details
        sup_frame = Frame(self.root, bd=3, relief=RIDGE)
        sup_frame.place(x=450,y=100,width=430,height=200)

        scrolly = Scrollbar(sup_frame,orient=VERTICAL)
        scrollx = Scrollbar(sup_frame,orient=HORIZONTAL)

        self.SupplierTable = ttk.Treeview(sup_frame,columns=("invoice","name","contact","desc"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.SupplierTable.xview)
        scrolly.config(command=self.SupplierTable.yview)

        self.SupplierTable.heading("invoice",text="Invoice No.")
        self.SupplierTable.heading("name",text="Name")
        self.SupplierTable.heading("contact",text="Contact")
        self.SupplierTable.heading("desc",text="Description")

        self.SupplierTable["show"]="headings"

        self.SupplierTable.column("invoice",width=90)
        self.SupplierTable.column("name",width=100)
        self.SupplierTable.column("contact",width=100)
        self.SupplierTable.column("desc",width=100)
        self.SupplierTable.pack(fill=BOTH,expand=1)
        self.SupplierTable.bind("<ButtonRelease-1>",self.get_data)

        self.show()
#===============================================================================

    def add(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()

        try:
            if self.var_sup_invoice.get()=="":
                messagebox.showerror("Error","Invoice must be required",parent=self.root)
            else:
                cur.execute("Select * from supplier where invoice=?",(self.var_sup_invoice.get(),))
                row = cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","Invoice number already assigned, try different!")
                else:
                    cur.execute("Insert into supplier(invoice,name,contact,desc) values(?,?,?,?)",(
                                    self.var_sup_invoice.get(),
                                    self.var_name.get(),
                                    self.var_contact.get(),
                                    self.txt_description.get('1.0',END),
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Supplier added successfully!",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}")


    def show(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("Select * from supplier")
            rows = cur.fetchall()
            self.SupplierTable.delete(*self.SupplierTable.get_children())
            for row in rows:
                self.SupplierTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}")

    def get_data(self,ev):
        f = self.SupplierTable.focus()
        content = (self.SupplierTable.item(f))
        row = content['values']
        # print(row)
        self.var_sup_invoice.set(row[0])
        self.var_name.set(row[1])
        self.var_contact.set(row[2])
        self.txt_description.delete('1.0',END)
        self.txt_description.insert(END,row[3])

    def update(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_sup_invoice.get()=="":
                messagebox.showerror("Error","Invoice number must be required",parent=self.root)
            else:
                cur.execute("Select * from supplier where invoice=?",(self.var_sup_invoice.get(),))
                row = cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid invoice number")
                else:
                    cur.execute("Update supplier set name=?,contact=?,desc=? where invoice=?",(
                                    self.var_name.get(),
                                    self.var_contact.get(),
                                    self.txt_description.get('1.0',END),
                                    self.var_sup_invoice.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Supplier updated successfully!",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}")

    def delete(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_sup_invoice.get()=="":
                messagebox.showerror("Error","Invoice number must be required",parent=self.root)
            else:
                cur.execute("Select * from supplier where invoice=?",(self.var_sup_invoice.get(),))
                row = cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid invoice number")
                else:
                    op = messagebox.askyesno("Confirm","Do you really want to delete?",parent=self.root)
                    if op==True:
                        cur.execute("Delete from supplier where invoice=?",(self.var_sup_invoice.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Supplier deleted successfully",parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}")

    def clear(self):
        self.var_sup_invoice.set("")
        self.var_name.set("")
        self.var_contact.set("")
        self.txt_description.delete('1.0',END)
        self.var_searchtxt.set("")
        # show the update
        self.show()

    def search(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_searchtxt.get() == "":
                messagebox.showerror("Error","Invoice number must be required",parent=self.root)
            else:
                cur.execute("Select * from supplier where invoice=?",(self.var_searchtxt.get(),))
                row = cur.fetchone()
                if row!=None:
                    self.SupplierTable.delete(*self.SupplierTable.get_children())
                    self.SupplierTable.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","No record found!",parent=self.root)

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}")

if __name__=="__main__":
    root = Tk();
    obj = supplierClass(root)
    root.mainloop()
