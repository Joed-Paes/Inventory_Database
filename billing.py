from tkinter import *
from PIL import Image, ImageTk  # pip install pillow
from tkinter import ttk, messagebox
import sqlite3
import time
import os, sys, subprocess
import tempfile

class billClass:
    def __init__(self, root):
        self.root = root;
        self.root.geometry("1350x700+0+0")
        self.root.title("Inventory Management System | Developed by Joed")
        self.root.config(bg="white")
        self.cart_list = []
        self.chk_print = 0

        #====== Variables =======
        self.var_search = StringVar()

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

        #==== Product Frame ===============
        productFrame1 = Frame(self.root,bd=3,relief=RIDGE,bg="white")
        productFrame1.place(x=10,y=110,width=410,height=550)

        productTitle = Label(productFrame1,text="All products",font=("goudy old style",15),bg="black",fg="white")
        productTitle.pack(side=TOP,fill=X)

        productFrame2 = Frame(productFrame1,bd=2,relief=RIDGE,bg="white")
        productFrame2.place(x=2,y=42,width=398,height=90)

        lbl_search = Label(productFrame2,text="Seach Product | By Name",font=("times new roman",15,"bold"),bg="white",fg="green").place(x=2,y=5)

        lbl_name = Label(productFrame2,text="Product Name",font=("times new roman",15,"bold"),bg="white").place(x=2,y=45)
        txt_search = Entry(productFrame2,textvariable=self.var_search,font=("times new roman",15),bg="white").place(x=150,y=45,width=150)
        btn_search = Button(productFrame2,text="Search",command=self.search,font=("goudy old style",10),bg="white",cursor="hand2").place(x=310,y=45,width=80,height=28)
        btn_show_all = Button(productFrame2,text="Show All",command=self.show,font=("goudy old style",10),bg="white",cursor="hand2").place(x=310,y=15,width=80,height=28)

        #============= Product Details
        productFrame3 = Frame(productFrame1, bd=3, relief=RIDGE)
        productFrame3.place(x=2,y=140,width=398,height=380)

        scrolly = Scrollbar(productFrame3,orient=VERTICAL)
        scrollx = Scrollbar(productFrame3,orient=HORIZONTAL)

        self.productTable = ttk.Treeview(productFrame3,columns=("pid","name","price","qty","status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.productTable.xview)
        scrolly.config(command=self.productTable.yview)

        self.productTable.heading("pid",text="P ID.")
        self.productTable.heading("name",text="Name")
        self.productTable.heading("price",text="Price")
        self.productTable.heading("qty",text="Qty")
        self.productTable.heading("status",text="Status")

        self.productTable["show"]="headings"

        self.productTable.column("pid",width=50)
        self.productTable.column("name",width=80)
        self.productTable.column("price",width=80)
        self.productTable.column("qty",width=80)
        self.productTable.column("status",width=80)
        self.productTable.pack(fill=BOTH,expand=1)
        self.productTable.bind("<ButtonRelease-1>",self.get_data)

        lbl_note = Label(productFrame1,text="Note: 'Enter 0 quantity to remove product from the cart'",font=("goudy old style",10),anchor="w",bg="white",fg="red").pack(side=BOTTOM,fill=X)

        # ======== Customer Frame ===========
        self.var_customer_name = StringVar()
        self.var_customer_contact = StringVar()

        customerFrame = Frame(self.root,bd=3,relief=RIDGE,bg="white")
        customerFrame.place(x=425,y=110,width=530,height=70)

        customerTitle = Label(customerFrame,text="Customer details",font=("goudy old style",15),bg="lightgray")
        customerTitle.pack(side=TOP,fill=X)

        lbl_customer_name = Label(customerFrame,text="Name:",font=("times new roman",15,"bold"),bg="white").place(x=5,y=35)
        txt_customer_name = Entry(customerFrame,textvariable=self.var_customer_name,font=("times new roman",15),bg="lightyellow").place(x=70,y=35,width=150)

        lbl_customer_contact = Label(customerFrame,text="Contact No:",font=("times new roman",15,"bold"),bg="white").place(x=250,y=35)
        txt_customer_contact = Entry(customerFrame,textvariable=self.var_customer_contact,font=("times new roman",15),bg="lightyellow").place(x=360,y=35,width=150)

        #====== Calc + Cart Frame =============
        calc_cartFrame = Frame(self.root,bd=2,relief=RIDGE,bg="white")
        calc_cartFrame.place(x=425,y=190,width=530,height=360)

        #====== Calculator Frame =============
        self.var_cal_input = StringVar()

        calcFrame = Frame(calc_cartFrame,bd=8,relief=RIDGE,bg="white")
        calcFrame.place(x=5,y=5,width=268,height=340)

        self.txt_cal_input = Entry(calcFrame,textvariable=self.var_cal_input,font=("arial",15,"bold"),width=21,bd=10,relief=GROOVE,state="readonly",justify=RIGHT)
        self.txt_cal_input.grid(row=0,columnspan=4)

        btn_7 = Button(calcFrame,text="7",font=("arial",15,"bold"),command=lambda:self.get_input(7),bd=5,width=2,pady=14,cursor="hand2").grid(row=1,column=0)
        btn_8 = Button(calcFrame,text="8",font=("arial",15,"bold"),command=lambda:self.get_input(8),bd=5,width=2,pady=14,cursor="hand2").grid(row=1,column=1)
        btn_9 = Button(calcFrame,text="9",font=("arial",15,"bold"),command=lambda:self.get_input(9),bd=5,width=2,pady=14,cursor="hand2").grid(row=1,column=2)
        btn_add = Button(calcFrame,text="+",font=("arial",15,"bold"),command=lambda:self.get_input("+"),bd=5,width=2,pady=12,cursor="hand2").grid(row=1,column=3)

        btn_4 = Button(calcFrame,text="4",font=("arial",15,"bold"),command=lambda:self.get_input(4),bd=5,width=2,pady=14,cursor="hand2").grid(row=2,column=0)
        btn_5 = Button(calcFrame,text="5",font=("arial",15,"bold"),command=lambda:self.get_input(5),bd=5,width=2,pady=14,cursor="hand2").grid(row=2,column=1)
        btn_6 = Button(calcFrame,text="6",font=("arial",15,"bold"),command=lambda:self.get_input(6),bd=5,width=2,pady=14,cursor="hand2").grid(row=2,column=2)
        btn_sub = Button(calcFrame,text="-",font=("arial",15,"bold"),command=lambda:self.get_input("-"),bd=5,width=2,pady=12,cursor="hand2").grid(row=2,column=3)

        btn_1 = Button(calcFrame,text="1",font=("arial",15,"bold"),command=lambda:self.get_input(1),bd=5,width=2,pady=14,cursor="hand2").grid(row=3,column=0)
        btn_2 = Button(calcFrame,text="2",font=("arial",15,"bold"),command=lambda:self.get_input(2),bd=5,width=2,pady=14,cursor="hand2").grid(row=3,column=1)
        btn_3 = Button(calcFrame,text="3",font=("arial",15,"bold"),command=lambda:self.get_input(3),bd=5,width=2,pady=14,cursor="hand2").grid(row=3,column=2)
        btn_mul = Button(calcFrame,text="x",font=("arial",15,"bold"),command=lambda:self.get_input("*"),bd=5,width=2,pady=14,cursor="hand2").grid(row=3,column=3)

        btn_0 = Button(calcFrame,text="0",font=("arial",15,"bold"),command=lambda:self.get_input(0),bd=5,width=2,pady=14,cursor="hand2").grid(row=4,column=0)
        btn_c = Button(calcFrame,text="c",font=("arial",15,"bold"),command=self.clear_cal,bd=5,width=2,pady=14,cursor="hand2").grid(row=4,column=1)
        btn_eq = Button(calcFrame,text="=",font=("arial",15,"bold"),command=self.perform_cal,bd=5,width=2,pady=14,cursor="hand2").grid(row=4,column=2)
        btn_div = Button(calcFrame,text="/",font=("arial",15,"bold"),command=lambda:self.get_input("/"),bd=5,width=2,pady=14,cursor="hand2").grid(row=4,column=3)

        #====== Cart Frame =============
        cartFrame = Frame(calc_cartFrame, bd=3, relief=RIDGE)
        cartFrame.place(x=280,y=5,width=245,height=340)

        self.cartTitle = Label(cartFrame,text="Cart Total Products: [0]",font=("goudy old style",10,"bold"),bg="lightgray")
        self.cartTitle.pack(side=TOP,fill=X)

        scrolly = Scrollbar(cartFrame,orient=VERTICAL)
        scrollx = Scrollbar(cartFrame,orient=HORIZONTAL)

        self.cartTable = ttk.Treeview(cartFrame,columns=("pid","name","qty","price"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.cartTable.xview)
        scrolly.config(command=self.cartTable.yview)

        self.cartTable.heading("pid",text="P ID.")
        self.cartTable.heading("name",text="Name")
        self.cartTable.heading("qty",text="Qty")
        self.cartTable.heading("price",text="Price")

        self.cartTable["show"]="headings"

        self.cartTable.column("pid",width=50)
        self.cartTable.column("name",width=80)
        self.cartTable.column("qty",width=80)
        self.cartTable.column("price",width=80)
        self.cartTable.pack(fill=BOTH,expand=1)
        self.cartTable.bind("<ButtonRelease-1>",self.get_data_cart)

        #============= Add Widgets Cart Frame ================
        self.var_pid = StringVar()
        self.var_name = StringVar()
        self.var_price = StringVar()
        self.var_qty = StringVar()
        self.var_stock = StringVar()

        addWidgetCartFrame = Frame(self.root, bd=2, relief=RIDGE,bg="white")
        addWidgetCartFrame.place(x=425,y=550,width=530,height=110)

        lbl_pName = Label(addWidgetCartFrame,text="Product Name",font=("goudy old style",10,"bold"),bg="white").place(x=5,y=5)
        txt_pName = Entry(addWidgetCartFrame,textvariable=self.var_name,font=("goudy old style",10),bg="lightyellow",state='readonly').place(x=5,y=25,width=250,height=22)

        lbl_price = Label(addWidgetCartFrame,text="Price per Qtd",font=("goudy old style",10,"bold"),bg="white").place(x=280,y=5)
        txt_price = Entry(addWidgetCartFrame,textvariable=self.var_price,font=("goudy old style",10),bg="lightyellow",state='readonly').place(x=280,y=25,width=100,height=22)

        lbl_qty = Label(addWidgetCartFrame,text="Quantity",font=("goudy old style",10,"bold"),bg="white").place(x=400,y=5)
        txt_qty = Entry(addWidgetCartFrame,textvariable=self.var_qty,font=("goudy old style",10),bg="lightyellow").place(x=400,y=25,width=100,height=22)

        self.lbl_inStock = Label(addWidgetCartFrame,text="In stock: --",font=("goudy old style",10,"bold"),bg="white")
        self.lbl_inStock.place(x=5,y=70)

        btn_clear_cart = Button(addWidgetCartFrame,text="Clear",command=self.clear_cart,font=("goudy old style",10),bg="lightgray",cursor="hand2").place(x=130,y=65,width=150,height=30)
        btn_add_cart = Button(addWidgetCartFrame,text="Add | Update Cart",command=self.add_update_cart,font=("goudy old style",10),bg="orange",cursor="hand2").place(x=300,y=65,width=200,height=30)

        #=================== Billing Area ====================
        billFrame = Frame(self.root,bd=2,relief=RIDGE,bg="white")
        billFrame.place(x=960,y=110,width=400,height=410)

        billTitle = Label(billFrame,text="Customer Bill Area",font=("goudy old style",15,"bold"),bg="yellow")
        billTitle.pack(side=TOP,fill=X)

        scrolly = Scrollbar(billFrame,orient=VERTICAL)
        self.txt_bill_area = Text(billFrame,yscrollcommand=scrolly.set)
        self.txt_bill_area.pack(fill=BOTH,expand=1)
        scrolly.config(command=self.txt_bill_area.yview)

        #=================== Billing Buttons ==================
        billMenuFrame = Frame(self.root,bd=2,relief=RIDGE,bg="white")
        billMenuFrame.place(x=960,y=520,width=400,height=140)

        self.lbl_amount = Label(billMenuFrame,text="Bill Amount\n[0]",font=("goudy old style",12,"bold"),bg="gray",fg="white")
        self.lbl_amount.place(x=5,y=5,width=120,height=70)

        self.lbl_discount = Label(billMenuFrame,text="Discount\n[5%]",font=("goudy old style",12,"bold"),bg="gray",fg="white")
        self.lbl_discount.place(x=140,y=5,width=120,height=70)

        self.lbl_net_pay = Label(billMenuFrame,text="Net Pay\n[0]",font=("goudy old style",12,"bold"),bg="gray",fg="white")
        self.lbl_net_pay.place(x=270,y=5,width=120,height=70)

        btn_print = Button(billMenuFrame,text="Print",command=self.print_bill,font=("goudy old style",10,"bold"),bg="blue",fg="white",cursor="hand2")
        btn_print.place(x=5,y=80,width=120,height=50)

        btn_clear_all = Button(billMenuFrame,text="Clear all",command=self.clear_all,font=("goudy old style",10,"bold"),bg="blue",fg="white",cursor="hand2")
        btn_clear_all.place(x=140,y=80,width=120,height=50)

        btn_generate = Button(billMenuFrame,text="Generate Bill",command=self.generate_bill,font=("goudy old style",10,"bold"),bg="blue",fg="white",cursor="hand2")
        btn_generate.place(x=270,y=80,width=120,height=50)

        #======= footer ===========
        lbl_footer = Label(self.root, text="IMS - Inventory Management System | Developed by JP\nFor any technical issue contact: +559999-9999",
                font=("times new roman",10,"bold"),bg="#010c48",fg="white").pack(side=BOTTOM,fill=X)

        self.show()
        self.update_date_time()

#================== ALL FUNCTIONS =============================

    def get_input(self,num):
        xnum = self.var_cal_input.get()+str(num)
        self.var_cal_input.set(xnum)

    def clear_cal(self):
        self.var_cal_input.set("")

    def perform_cal(self):
        result = self.var_cal_input.get()
        self.var_cal_input.set(eval(result))

    def show(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("Select pid, name, price, quantity, status from product where status='Active'")
            rows = cur.fetchall()
            self.productTable.delete(*self.productTable.get_children())
            for row in rows:
                self.productTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}")

    def get_data(self,ev):
        f = self.productTable.focus()
        content = (self.productTable.item(f))
        row = content['values']
        #print(row)
        self.var_pid.set(row[0])
        self.var_name.set(row[1])
        self.var_price.set(row[2])
        self.lbl_inStock.config(text=f"In stock: [{str(row[3])}]")
        self.var_stock.set(row[3])
        self.var_qty.set(1)

    def get_data_cart(self,ev):
        f = self.cartTable.focus()
        content = (self.cartTable.item(f))
        row = content['values']
        #print(row)
        self.var_pid.set(row[0])
        self.var_name.set(row[1])
        self.var_qty.set(row[2])
        self.var_price.set(row[3])
        self.lbl_inStock.config(text=f"In stock: [{str(row[4])}]")
        self.var_stock.set(row[4])

    def clear_cart(self):
        self.var_pid.set("")
        self.var_name.set("")
        self.var_price.set("")
        self.var_qty.set("")
        self.lbl_inStock.config(text=f"In stock: --")
        # show the update
        #self.show()

    def clear_all(self):
        del self.cart_list[:]
        self.clear_cart()
        self.cartTitle.config(text=f"Cart Total Products: [0]")
        self.txt_bill_area.delete('1.0',END)
        self.var_customer_name.set("")
        self.var_customer_contact.set("")
        self.var_search.set("")
        # show the update
        self.show()
        self.show_cart()
        self.chk_print = 0


    def search(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_search.get() == "":
                messagebox.showerror("Error","Search input must be required",parent=self.root)
            else:
                cur.execute("Select pid, name, price, quantity, status from product where name like '%"+self.var_search.get()+"%' and status='Active'")
                rows = cur.fetchall()
                if len(rows)!=0:
                    self.productTable.delete(*self.productTable.get_children())
                    for row in rows:
                        self.productTable.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","No product found!",parent=self.root)

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}")

    def add_update_cart(self):
        if self.var_pid.get()=="":
            messagebox.showerror("Error","Please, select a product from  the list",parent=self.root)
        elif self.var_qty.get()=="":
            messagebox.showerror("Error","Quantity is required",parent=self.root)
        elif int(self.var_qty.get())>int(self.var_stock.get()):
            messagebox.showerror("Error","Invalid quantity",parent=self.root)
        else:
            #price_cal = int(self.var_qty.get())*float(self.var_price.get())
            #price_cal = float(price_cal)
            price_cal = self.var_price.get()
            #print(price_cal)
            # pid, name, qty, price, stock
            cart_data = [self.var_pid.get(),self.var_name.get(),self.var_qty.get(),price_cal,self.var_stock.get()]
            #print(self.cart_list)
            #======= update cart ============
            present='no'
            index_=0
            for row in self.cart_list:
                if self.var_pid.get()==row[0]:
                    present='yes'
                    break
                index_+=1

            if present=='yes':
                op=messagebox.askyesno('Confirm',"Product already present\n Do you want to update or remove? ",parent=self.root)
                if op==True:
                    if self.var_qty.get()=='0':
                        self.cart_list.pop(index_)
                    else:
                        # pid, name, qty, price, stock
                        self.cart_list[index_][2]=self.var_qty.get()# qty
                        self.cart_list[index_][3]=price_cal
            else:
                self.cart_list.append(cart_data)

            self.show_cart()
            self.bill_updates()

    def bill_updates(self):
        self.bill_amount = 0
        self.net_pay = 0
        self.discount = 0
        for row in self.cart_list:
            self.bill_amount = self.bill_amount + (float(row[3])*int(row[2]))

        self.discount = (self.bill_amount*5)/100
        self.net_pay = self.bill_amount-self.discount

        self.lbl_amount.config(text=f"Bill Amount\nR${str(self.bill_amount)}")
        self.lbl_net_pay.config(text=f"Net pay\nR${str(self.net_pay)}")
        self.cartTitle.config(text=f"Cart Total Products: [{str(len(self.cart_list))}]")

    def show_cart(self):
        try:
            self.cartTable.delete(*self.cartTable.get_children())
            for row in self.cart_list:
                self.cartTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}", parent=self.root)

    def generate_bill(self):
        if self.var_customer_name.get()=="" or self.var_customer_contact.get()=="":
            messagebox.showerror("Error","Customer details are required!", parent=self.root)
        elif len(self.cart_list)==0:
            messagebox.showerror("Error","Please, add product to the cart!", parent=self.root)
        else:
            # ====== Bill Top =======
            self.bill_top()
            # ====== Bill Middle =======
            self.bill_middle()
            # ====== Bill Bottom =======
            self.bill_bottom()

            fp = open(f'bills/{str(self.invoice)}.txt','w')
            fp.write(self.txt_bill_area.get('1.0',END))
            fp.close()
            messagebox.showinfo('Saved','Bill has been saved in backend!',parent=self.root)
            self.chk_print = 1

    def bill_top(self):
        self.invoice = int(time.strftime("%H%M%S"))+int(time.strftime("%d%m%Y"))
        bill_top_temp=f'''
\t\t XYZ-Inventory
\t Phone No. 98725*******, Jales-SP
{str("="*47)}
Customer Name: {self.var_customer_name.get()}
Ph No.: {self.var_customer_contact.get()}
Bill No.: {str(self.invoice)}\t\t\t Date: {str(time.strftime("%d/%m/%Y"))}
{str("="*47)}
Product Name \t\t\t Qty \t Price
{str("="*47)}
        '''
        self.txt_bill_area.delete('1.0',END)
        self.txt_bill_area.insert('1.0',bill_top_temp)

    def bill_middle(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            for row in self.cart_list:
                # pid, name, qty, price, stock
                pid=row[0]
                name=row[1]
                qty=row[2]
                qty_upd = int(row[4])-int(row[2])    # update the stock
                if int(qty)==row[4]:
                    status = 'Inactive'
                if int(qty)!=row[4]:
                    status = 'Active'
                price=float(row[3])*int(row[2])
                price=str(price)
                self.txt_bill_area.insert(END,"\n "+name+"\t\t\t"+qty+"\tR$"+price)

                # ==== update qty in product table
                cur.execute('Update product set quantity=?, status=? where pid=?',(
                    qty_upd,
                    status,
                    pid
                ))
                con.commit()
            con.close()
            self.show()

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}", parent=self.root)

    def bill_bottom(self):
        bill_bottom_temp=f'''
{str("="*47)}
Bill Amount\t\t\t\tR${self.bill_amount}
Discount\t\t\t\tR${self.discount}
Net Pay\t\t\t\tR${self.net_pay}
{str("="*47)}\n
        '''
        self.txt_bill_area.insert(END,bill_bottom_temp)


    def update_date_time(self):
        time_=time.strftime("%H:%M:%S")
        date_=time.strftime("%d-%m-%Y")
        self.lbl_clock.config(text=f"Welcome to Inventory Management System\t\t Date: {str(date_)}\t\t Time: {str(time_)}")
        self.lbl_clock.after(200,self.update_date_time)

    def print_bill(self):
        if self.chk_print==1:
            messagebox.showinfo('Print',"Please, wait while printing...",parent=self.root)
            self.new_file = tempfile.mktemp('.txt')
            open(self.new_file,'w').write(self.txt_bill_area.get('1.0',END))
            self.open_file()
        else:
            messagebox.showerror('Error',"Please, generate a bill to print the receipt")

    def open_file(self):
        if sys.platform == "win32":
            os.startfile(self.new_file,'print')
        else:
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, self.new_file])

    def logout(self):
        self.root.destroy()
        os.system("python login.py")


if __name__ == "__main__":
    root = Tk()
    obj = billClass(root)
    root.mainloop()
