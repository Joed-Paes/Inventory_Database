from tkinter import *
from tkinter import messagebox
from PIL import ImageTk # pip install pillow
import sqlite3
import os
import email_pass
import smtplib # pip install smtplib
import time

class Login_System:

    def __init__(self,root):
        self.root=root
        self.root.title("Login System | Developed by Joed Paes | JP Software")
        self.root.geometry("1150x700+0+0")
        self.root.config(bg="white")

        #========= Variables =======
        self.employee_id = StringVar()
        self.password = StringVar()
        self.otp=''

        #========== Images =========
        self.phone_image=ImageTk.PhotoImage(file="images/login4.jpeg")
        self.lbl_Photo_Image=Label(self.root,image=self.phone_image,bd=0).place(x=200,y=50)

        #======= Login Frame ========
        login_frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        login_frame.place(x=650,y=90,width=350,height=460)

        title = Label(login_frame,text="Login System",font=("Elephant",30,"bold"),bg="white").place(x=0,y=30,relwidth=1)

        lbl_user = Label(login_frame,text="Employee ID",font=("Adalus",15),bg="white",fg="#767171").place(x=20,y=100)
        txt_user = Entry(login_frame,font=("times new roman",15),textvariable=self.employee_id,bg="#ECECEC").place(x=20,y=130,width=200)

        lbl_password = Label(login_frame,text="Password",font=("Adalus",15),bg="white",fg="#767171").place(x=20,y=180)
        txt_password = Entry(login_frame,font=("times new roman",15),textvariable=self.password,show="*",bg="#ECECEC").place(x=20,y=210,width=200)

        btn_login = Button(login_frame,text="Log in",command=self.login,font=("Arial Rounded MT Bold",15),bg="#00B0F0",fg="white",activeforeground="white",cursor="hand2").place(x=20,y=270,width=300)

        hr = Label(login_frame,bg="lightgray").place(x=20,y=340,width=300,height=2)
        or_ = Label(login_frame,text="OR",bg="white",fg="lightgray",font=("times new roman",15)).place(x=150,y=330)

        btn_forget=Button(login_frame,text="Forget Password?",command=self.forget_window,font=("times new roman",15),bg="white",fg="#00759E",bd=0,activebackground="#00759E",cursor="hand2").place(x=80,y=380)

        #======= Register Frame ========
        register_frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        register_frame.place(x=650,y=560,width=350,height=80)

        lbl_register = Label(register_frame,text="Don't have an account?",font=("times new roman",13),bg="white").place(x=40,y=20)
        btn_register=Button(register_frame,text="Sign up",font=("times new roman",13),bg="white",fg="#00759E",bd=0,activebackground="#00759E",cursor="hand2").place(x=210,y=18)

        #===== Animation of Images ======
        self.im1=ImageTk.PhotoImage(file="images/login1.jpeg")
        self.im2=ImageTk.PhotoImage(file="images/login2.jpeg")
        self.im3=ImageTk.PhotoImage(file="images/login3.jpeg")

        self.lbl_change_image=Label(self.root,bg="white")
        self.lbl_change_image.place(x=400,y=250,width=200,height=400)

        self.animate()

# ================== ALL FUNCTIONS =========================
    def animate(self):
        self.im=self.im1
        self.im1=self.im2
        self.im2=self.im3
        self.im3=self.im
        self.lbl_change_image.config(image=self.im)
        self.lbl_change_image.after(2000,self.animate)

    def login(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.employee_id.get()=="" or self.password.get()=="":
                messagebox.showerror("Error","All fields are required",parent=self.root)
            else:
                cur.execute("Select utype from employee where eid=? AND pass=?",(self.employee_id.get(),self.password.get(),))
                user = cur.fetchone()
                if user==None:
                    messagebox.showerror("Error","Invalid USERNAME/PASSWORD",parent=self.root)
                else:
                    if user[0]=="Admin":
                        self.root.destroy()
                        os.system("python dashboard.py")
                    else:
                        self.root.destroy()
                        os.system("python billing.py")

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}")

    def forget_window(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.employee_id.get()=="":
                messagebox.showerror("Error","Employee ID is required",parent=self.root)
            else:
                cur.execute("Select email from employee where eid=?",(self.employee_id.get(),))
                email = cur.fetchone()
                if email==None:
                    messagebox.showerror("Error","Invalid Employee ID, try again",parent=self.root)
                else:
                    self.var_otp = StringVar()
                    self.var_new_pass = StringVar()
                    self.var_conf_new_pass = StringVar()
                    # call send_email_function()
                    chk=self.send_email(email[0])
                    if chk=='f':
                        messagebox.showerror("Error","Connection error, try again",parent=self.root)
                    else:
                        self.forget_win=Toplevel(self.root)
                        self.forget_win.title("RESET PASWORD")
                        self.forget_win.geometry("400x350+500+100")
                        self.forget_win.focus_force()

                        title=Label(self.forget_win,text="Reset Password",font=("goudy old style",15,"bold"),bg="#3f51b5",fg="white").pack(side=TOP,fill=X)
                        lbl_reset=Label(self.forget_win,text="Enter OTP sent on registered email",font=("time new roman",15)).place(x=20,y=60)
                        txt_reset=Entry(self.forget_win,textvariable=self.var_otp,font=("time new roman",15),bg='lightyellow').place(x=20,y=90,width=250,height=30)

                        self.btn_reset=Button(self.forget_win,text="SUBMIT",command=self.validate_otp,font=("time new roman",15),bg='lightblue',cursor="hand2")
                        self.btn_reset.place(x=280,y=90,width=100,height=30)

                        new_pass=Label(self.forget_win,text="Enter new password",font=("time new roman",15)).place(x=20,y=160)
                        txt_new_pass=Entry(self.forget_win,textvariable=self.var_new_pass,font=("time new roman",15),bg='lightyellow').place(x=20,y=190,width=250,height=30)

                        conf_pass=Label(self.forget_win,text="Confirm the new password",font=("time new roman",15)).place(x=20,y=230)
                        txt_conf_pass=Entry(self.forget_win,textvariable=self.var_conf_new_pass,font=("time new roman",15),bg='lightyellow').place(x=20,y=260,width=250,height=30)

                        self.btn_update=Button(self.forget_win,text="Update",command=self.update_password,state="disable",font=("time new roman",15),bg='lightblue',cursor="hand2")
                        self.btn_update.place(x=150,y=300,width=100,height=30)

                        messagebox.showinfo("Information","The OTP number was sent for your registered email!",parent=self.forget_win)

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}")

    def update_password(self):
        if self.var_new_pass.get()=="" or self.var_conf_new_pass.get()=="":
            messagebox.showerror("Error","Password is required",parent=self.forget_win)
        elif self.var_new_pass.get() != self.var_conf_new_pass.get():
            messagebox.showerror("Error","Confirm password not correct, try again",parent=self.forget_win)
        else:
            con = sqlite3.connect(database=r'ims.db')
            cur = con.cursor()
            try:
                cur.execute("Update employee SET pass=? where eid=?",(self.var_new_pass.get(),self.employee_id.get(),))
                con.commit()
                messagebox.showinfo("Success","Password updated successfuly!",parent=self.forget_win)
                self.forget_win.destroy()
            except Exception as ex:
                messagebox.showerror("Error",f"Error due to: {str(ex)}")

    def validate_otp(self):
        if int(self.otp)==int(self.var_otp.get()):
            self.btn_update.config(state="normal")
            self.btn_reset.config(state="disable")
        else:
            messagebox.showerror("Error","Invalid OTP, try again",parent=self.forget_win)

    def send_email(self,to_):
        s=smtplib.SMTP('smtp.gmail.com',587)
        s.starttls()
        email_=email_pass.email_
        pass_=email_pass.pass_

        s.login(email_,pass_)

        self.otp=int(time.strftime("%H%S%M"))+int(time.strftime("%S"))

        subj='IMS-Reset Password OTP'
        msg=f'Dear Sir/Madam,\n\nYour reset OTP is {str(self.otp)}.\n\nBest regards,\nIMS Team'
        msg="Subject:{}\n\n{}".format(subj,msg)
        s.sendmail(email_,to_,msg)
        chk=s.ehlo()
        if chk[0]==250:
            return 's'
        else:
            return 'f'

root=Tk()
obj=Login_System(root)
root.mainloop()
