# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 11:40:32 2019

@author: zachm
"""
import tkinter as tk
import os
from tkinter import filedialog, simpledialog
def get_string(root=None, prompt="Input String"):
    destroy = False
    if root == None:
        root =tk.Tk()
        destroy = True
    root.withdraw()
    str_out = simpledialog.askstring(title = "User input",prompt = prompt,\
                                     parent=root)
    if destroy:
        root.destroy()
    return str_out

def get_api_key(root=None,save_api_key=True):
    api_location =  os.environ["AppData"] + "\\TodoistAPI\\api_key.txt"
    if not os.path.exists(os.environ["AppData"] + "\\TodoistAPI"):
        os.mkdir(os.environ["AppData"] + "\\TodoistAPI")
    try:      
        api_file = open(api_location,'rt')
        api_key = api_file.readline()
        api_file.close()
    except:
        api_key = get_string(prompt="Enter your todoist API Key" + \
                             "(https://todoist.com/prefs/integrations -> " + \
                             "API Token)")
    if save_api_key:
        f = open(api_location,'wt')
        f.write(api_key)
        
    return api_key