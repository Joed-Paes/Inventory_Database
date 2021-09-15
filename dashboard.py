from tkinter import *
from PIL import Image, ImageTk  # pip install pillow
from employee import employeeClass
from supplier import supplierClass
from category import categoryClass
from product import productClass
from sales import salesClass

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
        btn_logout = Button(self.root, text="Logout",font=("times new roman",15,"bold"),
                bg="yellow",cursor="hand2").place(x=1100,y=10,height=30,width=130)

        #======= clock ===========
        self.lbl_clock = Label(self.root, text="Welcome to Inventory Management System\t\t Date: MM-MM-YYYY\t\t Time: HH:MM:SS",
                font=("times new roman",10,"bold"),bg="#010c48",fg="white")
        self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)

        #====== Left Menu =======
        self.MenuLogo = Image.open("images/logo1.png")
        self.MenuLogo = self.MenuLogo.resize((200,200),Image.ANTIALIAS)
        self.MenuLogo = ImageTk.PhotoImage(self.MenuLogo)
        LeftMenu = Frame(self.root,bd=2,relief=RIDGE,bg="white")
        LeftMenu.place(x=0,y=102,width=200,height=565)

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
        btn_exit = Button(LeftMenu, text="Exit",command=self.root.quit,font=("times new roman",20,"bold"),
                bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)

        #======= content =========
        self.lbl_employee = Label(self.root,text="Total employee\n[ 0 ]",bg="#33bbf9",fg="white",
                font=("goudy old style",20,"bold")).place(x=300,y=120,height=150,width=300)
        self.lbl_category = Label(self.root,text="Total category\n[ 0 ]",bg="#33bbf9",fg="white",
                font=("goudy old style",20,"bold")).place(x=610,y=120,height=150,width=300)
        self.lbl_products = Label(self.root,text="Total products\n[ 0 ]",bg="#33bbf9",fg="white",
                font=("goudy old style",20,"bold")).place(x=920,y=120,height=150,width=300)
        self.lbl_sales = Label(self.root,text="Total sales\n[ 0 ]",bg="#33bbf9",fg="white",
                font=("goudy old style",20,"bold")).place(x=300,y=280,height=150,width=300)

        #======= footer ===========
        lbl_footer = Label(self.root, text="IMS - Inventory Management System | Developed by JP\nFor any technical issue contact: +559999-9999",
                font=("times new roman",10,"bold"),bg="#010c48",fg="white").pack(side=BOTTOM,fill=X)

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

if __name__ == "__main__":
    root = Tk()
    obj = IMS(root)
    root.mainloop()
