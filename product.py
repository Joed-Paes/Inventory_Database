from tkinter import *
from PIL import Image, ImageTk  # pip install pillow
from tkinter import ttk, messagebox
import sqlite3

class productClass:
    def __init__(self, root):
        self.root = root;
        self.root.geometry("1200x500+100+130")
        self.root.title("Inventory Management System | Developed by Joed")
        self.root.config(bg="white")
        self.root.focus_force()
        #################################

        ### variables
        self.var_pid = StringVar()
        self.var_category = StringVar()
        self.var_supplier = StringVar()
        self.var_cat_list = []
        self.var_sup_list = []
        self.fetch_cat_sup()
        self.var_name = StringVar()
        self.var_price = StringVar()
        self.var_quantity = StringVar()
        self.var_status = StringVar()
        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()

        ### Frame
        productFrame = Frame(self.root,bd=3,relief=RIDGE,bg="white")
        productFrame.place(x=10,y=10,width=450,height=480)

        ### Title
        title = Label(productFrame,text="Manage Product Details",font=("goudy old style",10),bg="blue",fg="white").pack(side=TOP,fill=X)

        # Product Content
        lbl_category = Label(productFrame,text="Category:",font=("goudy old style",10),bg="white").place(x=30,y=30)
        lbl_supplier = Label(productFrame,text="Supplier:",font=("goudy old style",10),bg="white").place(x=30,y=80)
        lbl_name = Label(productFrame,text="Name:",font=("goudy old style",10),bg="white").place(x=30,y=130)
        lbl_price = Label(productFrame,text="Price:",font=("goudy old style",10),bg="white").place(x=30,y=180)
        lbl_quantity = Label(productFrame,text="Quantity:",font=("goudy old style",10),bg="white").place(x=30,y=230)
        lbl_status = Label(productFrame,text="Status:",font=("goudy old style",10),bg="white").place(x=30,y=280)

        cmd_category = ttk.Combobox(productFrame,textvariable=self.var_category,values=self.var_cat_list,state='readonly',justify=CENTER,font=("goudy old style",12))
        cmd_category.place(x=130,y=30,width=180)
        cmd_category.current(0)

        cmd_supplier = ttk.Combobox(productFrame,textvariable=self.var_supplier,values=self.var_sup_list,state='readonly',justify=CENTER,font=("goudy old style",12))
        cmd_supplier.place(x=130,y=80,width=180)
        cmd_supplier.current(0)

        txt_name = Entry(productFrame,textvariable=self.var_name,font=("goudy old style",10),bg="white").place(x=130,y=130,width=250)
        txt_price = Entry(productFrame,textvariable=self.var_price,font=("goudy old style",10),bg="white").place(x=130,y=180,width=250)
        txt_quantity = Entry(productFrame,textvariable=self.var_quantity,font=("goudy old style",10),bg="white").place(x=130,y=230,width=250)

        cmd_status = ttk.Combobox(productFrame,textvariable=self.var_status,values=("Active","Inactive"),state='readonly',justify=CENTER,font=("goudy old style",12))
        cmd_status.place(x=130,y=280,width=180)
        cmd_status.current(0)

        # Buttons
        btn_add = Button(productFrame,text="Save",command=self.add,font=("goudy old style",10),bg="blue",fg="white",cursor="hand2").place(x=30,y=350,width=90, height=30)
        btn_update = Button(productFrame,text="Update",command=self.update,font=("goudy old style",10),bg="blue",fg="white",cursor="hand2").place(x=130,y=350,width=90, height=30)
        btn_delete = Button(productFrame,text="Delete",command=self.delete,font=("goudy old style",10),bg="blue",fg="white",cursor="hand2").place(x=230,y=350,width=90, height=30)
        btn_clear = Button(productFrame,text="Clear",command=self.clear,font=("goudy old style",10),bg="blue",fg="white",cursor="hand2").place(x=330,y=350,width=90, height=30)

        # search frame
        SearchFrame = LabelFrame(self.root,text="Search Product",bg="white")
        SearchFrame.place(x=480,y=10,width=400,height=60)

        # options
        cmd_search = ttk.Combobox(SearchFrame,textvariable=self.var_searchby,values=("Select","Category","Supplier","Name"),state='readonly',justify=CENTER,font=("goudy old style",12))
        cmd_search.place(x=10,y=10,width=120)
        cmd_search.current(0)

        txt_search = Entry(SearchFrame,textvariable=self.var_searchtxt,font=("goudy old style",12),bg="lightyellow")
        txt_search.place(x=140,y=10,width=150)
        btn_search = Button(SearchFrame,text="Search",command=self.search,font=("goudy old style",10),bg="green",fg="white",cursor="hand2")
        btn_search.place(x=300,y=10,width=80, height=25)


        # Product Details
        prod_detailsFrame = Frame(self.root, bd=3, relief=RIDGE)
        prod_detailsFrame.place(x=480,y=70,width=700,height=420)

        scrolly = Scrollbar(prod_detailsFrame,orient=VERTICAL)
        scrollx = Scrollbar(prod_detailsFrame,orient=HORIZONTAL)

        self.ProductTable = ttk.Treeview(prod_detailsFrame,columns=("pid","category","supplier","name","price","quantity","status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.ProductTable.xview)
        scrolly.config(command=self.ProductTable.yview)

        self.ProductTable.heading("pid",text="PROD ID")
        self.ProductTable.heading("category",text="Category")
        self.ProductTable.heading("supplier",text="Supplier")
        self.ProductTable.heading("name",text="Name")
        self.ProductTable.heading("price",text="Price")
        self.ProductTable.heading("quantity",text="Quantity")
        self.ProductTable.heading("status",text="Status")

        self.ProductTable["show"]="headings"

        self.ProductTable.column("pid",width=90)
        self.ProductTable.column("category",width=100)
        self.ProductTable.column("supplier",width=100)
        self.ProductTable.column("name",width=100)
        self.ProductTable.column("price",width=100)
        self.ProductTable.column("quantity",width=100)
        self.ProductTable.pack(fill=BOTH,expand=1)
        self.ProductTable.bind("<ButtonRelease-1>",self.get_data)

        self.show()
        self.fetch_cat_sup()

####################### FUNCTIONS ################################

    def fetch_cat_sup(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("Select name from category")
            cat = cur.fetchall()
            self.var_cat_list.append("Empty")
            if len(cat)>0:
                cat = tuple(set(cat))
                del self.var_cat_list[:]
                self.var_cat_list.append("Select")
                for i in cat:
                    self.var_cat_list.append(i[0])

            cur.execute("Select name from supplier")
            sup = cur.fetchall()
            self.var_sup_list.append("Empty")
            if len(sup)>0:
                sup = tuple(set(sup))
                del self.var_sup_list[:]
                self.var_sup_list.append("Select")
                for i in sup:
                    self.var_sup_list.append(i[0])

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}")

    def add(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_category.get()=="Select" or self.var_category.get()=="Empty" or self.var_supplier.get()=="Select" or self.var_supplier.get()=="Empty" or self.var_name.get()=="":
                messagebox.showerror("Error","All fields are required",parent=self.root)
            else:
                cur.execute("Select * from product where pid=? and category=? and supplier=?",(self.var_pid.get(),self.var_category.get(),self.var_supplier.get(),))
                row = cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","Product already assigned!")
                else:
                    cur.execute("Insert into product(category,supplier,name,price,quantity,status) values(?,?,?,?,?,?)",(
                                    self.var_category.get(),
                                    self.var_supplier.get(),
                                    self.var_name.get(),
                                    self.var_price.get(),
                                    self.var_quantity.get(),
                                    self.var_status.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Product added successfully!",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}")


    def show(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("Select * from product")
            rows = cur.fetchall()
            self.ProductTable.delete(*self.ProductTable.get_children())
            for row in rows:
                self.ProductTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}")

    def get_data(self,ev):
        f = self.ProductTable.focus()
        content = (self.ProductTable.item(f))
        row = content['values']
        # print(row)
        self.var_pid.set(row[0])
        self.var_category.set(row[1])
        self.var_supplier.set(row[2])
        self.var_name.set(row[3])
        self.var_price.set(row[4])
        self.var_quantity.set(row[5])
        self.var_status.set(row[6])

    def update(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_pid.get()=="":
                messagebox.showerror("Error","Product name must be required",parent=self.root)
            else:
                cur.execute("Select * from product where pid=?",(self.var_pid.get(),))
                row = cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid product")
                else:
                    cur.execute("Update product set category=?,supplier=?,name=?,price=?,quantity=?,status=? where pid=?",(
                                    self.var_category.get(),
                                    self.var_supplier.get(),
                                    self.var_name.get(),
                                    self.var_price.get(),
                                    self.var_quantity.get(),
                                    self.var_status.get(),
                                    self.var_pid.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Product updated successfully!",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}")

    def delete(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_pid.get()=="":
                messagebox.showerror("Error","Product must be required",parent=self.root)
            else:
                cur.execute("Select * from product where pid=?",(self.var_pid.get(),))
                row = cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid product")
                else:
                    op = messagebox.askyesno("Confirm","Do you really want to delete?",parent=self.root)
                    if op==True:
                        cur.execute("Delete from product where pid=?",(self.var_pid.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Product deleted successfully",parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}")

    def clear(self):
        self.var_category.set("Select")
        self.var_supplier.set("Select")
        self.var_name.set("")
        self.var_price.set("")
        self.var_quantity.set("")
        self.var_status.set("Active")
        self.var_searchby.set("Select")
        self.var_searchtxt.set("")
        # show the update
        self.show()

    def search(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_searchby.get() == "Select":
                messagebox.showerror("Error","Select search by option",parent=self.root)
            elif self.var_searchtxt.get() == "":
                messagebox.showerror("Error","Search input must be required",parent=self.root)
            else:
                cur.execute("Select * from product where "+str(self.var_searchby.get())+" like '%"+self.var_searchtxt.get()+"%'")
                rows = cur.fetchall()
                if len(rows)!=0:
                    self.ProductTable.delete(*self.ProductTable.get_children())
                    for row in rows:
                        self.ProductTable.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","No record found!",parent=self.root)

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}")


if __name__=="__main__":
    root = Tk();
    obj = productClass(root)
    root.mainloop()
