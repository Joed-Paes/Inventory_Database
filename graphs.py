from tkinter import *
from PIL import Image, ImageTk  # pip install pillow
from tkinter import ttk, messagebox
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class graphsClass:
    def __init__(self, root):
        self.root = root;
        self.root.geometry("900x500+220+130")
        self.root.title("Inventory Management System | Developed by Joed")
        self.root.config(bg="white")
        self.root.focus_force()

        # =============== Create/Get Data =====================
        data1 = {'Country': ['US','CA','GER','UK','FR'],
                'GDP_Per_Capita': [45000,42000,52000,49000,47000]}
        df1 = pd.DataFrame(data1,columns=['Country','GDP_Per_Capita'])

        data2 = {'Year': [1920,1930,1940,1950,1960,1970,1980,1990,2000,2010],
                'Unemployment_Rate': [9.8,12,8,7.2,6.9,7,6.5,6.2,5.5,6.3]}
        df2 = pd.DataFrame(data2,columns=['Year','Unemployment_Rate'])

        data3 = {'Interest_Rate': [5,5.5,6,5.5,5.25,6.5,7,8,7.5,8.5],
                'Stock_Index_Price': [1500,1520,1525,1523,1515,1540,1545,1560,1555,1565]}
        df3 = pd.DataFrame(data3,columns=['Interest_Rate','Stock_Index_Price'])

        # create tab control
        tabcontrol = ttk.Notebook(self.root,cursor="hand2",padding=2,style="TNotebook",takefocus=False,width=500,height=400)

        # create a number of tabs you want to add
        tab1 = Frame(tabcontrol,bg="white",relief=RIDGE,width=500,height=500)
        tab2 = Frame(tabcontrol,bg="white",relief=RIDGE,width=500,height=500)
        tab3 = Frame(tabcontrol,bg="white",relief=RIDGE,width=500,height=500)

        # add the tabs to the tabcontrol
        tabcontrol.add(tab1,text="Graph 1")
        tabcontrol.add(tab2,text="Graph 2")
        tabcontrol.add(tab3,text="Graph 3")

        # grid the tabcontrol
        tabcontrol.grid(row=0,column=0,padx=50,pady=50)

        figure1 = plt.Figure(figsize=(6,5), dpi=100)
        ax1 = figure1.add_subplot(111)
        bar1 = FigureCanvasTkAgg(figure1, tab1)
        bar1.get_tk_widget().pack(side=LEFT, fill=BOTH)
        df1 = df1[['Country','GDP_Per_Capita']].groupby('Country').sum()
        df1.plot(kind='bar', legend=True, ax=ax1)
        ax1.set_title('Country Vs. GDP Per Capita')

        figure2 = plt.Figure(figsize=(5,4), dpi=100)
        ax2 = figure2.add_subplot(111)
        line2 = FigureCanvasTkAgg(figure2, tab2)
        line2.get_tk_widget().pack(side=LEFT, fill=BOTH)
        df2 = df2[['Year','Unemployment_Rate']].groupby('Year').sum()
        df2.plot(kind='line', legend=True, ax=ax2, color='r',marker='o', fontsize=10)
        ax2.set_title('Year Vs. Unemployment Rate')

        figure3 = plt.Figure(figsize=(5,4), dpi=100)
        ax3 = figure3.add_subplot(111)
        ax3.scatter(df3['Interest_Rate'],df3['Stock_Index_Price'], color = 'g')
        scatter3 = FigureCanvasTkAgg(figure3, tab3)
        scatter3.get_tk_widget().pack(side=LEFT, fill=BOTH)
        ax3.legend(['Stock_Index_Price'])
        ax3.set_xlabel('Interest Rate')
        ax3.set_title('Interest Rate Vs. Stock Index Price')

if __name__=="__main__":
    root = Tk();
    obj = graphsClass(root)
    root.mainloop()
