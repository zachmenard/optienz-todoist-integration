# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 12:55:42 2019

@author: zachm
"""
import datetime, xlrd
from tkinter import *
from tkinter import filedialog, simpledialog
BookType = xlrd.book.Book
def minimalist_xldate_as_datetime(xldate, datemode=0):
    # datemode: 0 for 1900-based, 1 for 1904-based
    return (
        datetime.datetime(1899, 12, 30)
        + datetime.timedelta(days=xldate + 1462 * datemode)
        )
def xldate_to_todoist(xldate, datemod=0):
    dt = minimalist_xldate_as_datetime(xldate, datemod)
    # Mon 07 Aug 2006 12:34:56 +0000
    out_date = {"string": dt.strftime("%m/%d/%Y")}
    return out_date

def open_xl_workbook(root=None, path='',title="Select File"):
    destroy = False
    if root == None:        
        root = Tk()
        destroy = True
    root.mainloop()
    root.withdraw()
    if (path==''):
        fname =  \
        filedialog.askopenfilename(\
            initialdir = "/", \
            title = title,\
            filetypes = (("Excel","*.xls*"),("All","*")))
        if destroy:
            root.destroy()
    else:
        fname=path
    return xlrd.open_workbook(fname)

def get_cell(sht,row,col):
    val=None
    try:
        val=sht.cell_value(row,col)
    except Exception:
        pass
    return val