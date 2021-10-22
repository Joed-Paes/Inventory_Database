from tkinter import *
from PIL import Image, ImageTk  # pip install pillow
from employee import employeeClass
from supplier import supplierClass
from category import categoryClass
from product import productClass
from sales import salesClass
from graphs import graphsClass
import time
import sqlite3
from tkinter import messagebox
import os

class IMS:
    def __init__(self, root):
        self.root = root;
        self.root.geometry("1350x700+0+0")
        self.root.title("Inventory Management System | Developed by Joed")
        self.root.config(bg="white")

        #======= Title ======
        self.icon_title = PhotoImage(file="images/logo1.png")
        title = Label(self.root, text="Inventory Management System",image=self.icon_title,
                compound=LEFT,font=("times new roman",20,"bold"),bg="#010c48",fg="white",
                anchor="w",padx=20).place(x=0,y=0,relwidth=1,height=70)

        #======= btn_logout ======
        btn_logout = Button(self.root, text="Logout",command=self.logout,font=("times new roman",15,"bold"),
                bg="yellow",cursor="hand2").place(x=1200,y=10,height=30,width=130)

        #======= clock ===========
        self.lbl_clock = Label(self.root, text="Welcome to Inventory Management System\t\t Date: MM-MM-YYYY\t\t Time: HH:MM:SS",
                font=("times new roman",10,"bold"),bg="#010c48",fg="white")
        self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)

        #====== Left Menu =======
        self.MenuLogo = Image.open("images/logo1.png")
        self.MenuLogo = self.MenuLogo.resize((200,200),Image.ANTIALIAS)
        self.MenuLogo = ImageTk.PhotoImage(self.MenuLogo)
        LeftMenu = Frame(self.root,bd=2,relief=RIDGE,bg="white")
        LeftMenu.place(x=0,y=102,width=200,height=570)

        lbl_menuLogo = Label(LeftMenu,image=self.MenuLogo)
        lbl_menuLogo.pack(side=TOP,fill=X)

        lbl_menu = Label(LeftMenu, text="Menu",font=("times new roman",20),
                bg="#009688").pack(side=TOP,fill=X)
        btn_employee = Button(LeftMenu, text="Employee",command=self.employee,font=("times new roman",20,"bold"),
                bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_supplier = Button(LeftMenu, text="Supplier",command=self.supplier,font=("times new roman",20,"bold"),
                bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_category = Button(LeftMenu, text="Category",command=self.category,font=("times new roman",20,"bold"),
                bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_products = Button(LeftMenu, text="Products",command=self.product,font=("times new roman",20,"bold"),
                bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_sales = Button(LeftMenu, text="Sales",command=self.sales,font=("times new roman",20,"bold"),
                bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_analysis = Button(LeftMenu, text="Graphs",command=self.graphs,font=("times new roman",20,"bold"),
                bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_exit = Button(LeftMenu, text="Exit",command=self.root.quit,font=("times new roman",20,"bold"),
                bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)

        #======= content =========
        self.lbl_employee = Label(self.root,text="Total employee\n[ 0 ]",bg="#33bbf9",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_employee.place(x=300,y=120,height=150,width=300)

        self.lbl_category = Label(self.root,text="Total category\n[ 0 ]",bg="#33bbf9",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_category.place(x=610,y=120,height=150,width=300)

        self.lbl_products = Label(self.root,text="Total products\n[ 0 ]",bg="#33bbf9",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_products.place(x=920,y=120,height=150,width=300)

        self.lbl_sales = Label(self.root,text="Total sales\n[ 0 ]",bg="#33bbf9",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_sales.place(x=300,y=280,height=150,width=300)

        #======= footer ===========
        lbl_footer = Label(self.root, text="IMS - Inventory Management System | Developed by JP\nFor any technical issue contact: +559999-9999",
                font=("times new roman",10,"bold"),bg="#010c48",fg="white").pack(side=BOTTOM,fill=X)

        self.update_content()

    #====================== ALL FUNCTIONS ===============================

    def employee(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = employeeClass(self.new_win)

    def supplier(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = supplierClass(self.new_win)

    def category(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = categoryClass(self.new_win)

    def product(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = productClass(self.new_win)

    def sales(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = salesClass(self.new_win)

    def graphs(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = graphsClass(self.new_win)

    def update_content(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("select * from product")
            products=cur.fetchall()
            self.lbl_products.config(text=f'Total products\n [{str(len(products))}]')

            cur.execute("select * from employee")
            employees=cur.fetchall()
            self.lbl_employee.config(text=f"Total employee\n[ {str(len(employees))} ]")

            cur.execute("select * from category")
            categories=cur.fetchall()
            self.lbl_category.config(text=f"Total category\n[ {str(len(categories))} ]")

            bills=len(os.listdir('bills'))
            self.lbl_sales.config(text=f"Total sales\n[ {str(bills)} ]")

            time_=time.strftime("%H:%M:%S")
            date_=time.strftime("%d-%m-%Y")
            self.lbl_clock.config(text=f"Welcome to Inventory Management System\t\t Date: {str(date_)}\t\t Time: {str(time_)}")
            self.lbl_clock.after(200,self.update_content)

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}", parent=self.root)

    def logout(self):
        self.root.destroy()
        os.system("python login.py")

if __name__ == "__main__":
    root = Tk()
    obj = IMS(root)
    root.mainloop()
