"""
Inventory Management System with Database

Created on October 2021
@author: Joed Henrique Paes
"""

from login import Login_System # Our GUI Class

if __name__ == '__main__': # Direct script call

    root=Tk()
    obj=Login_System(root)
    root.mainloop()
