
import tkinter as tk
from .api_handler import *
from .xl_handler import *
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


def parse_file(wb):
    #make sure we have a workbook
    if not isinstance(wb, BookType):
        raise ValueError('The parse_file function can only be called on an\
                         Excel Workbook (class xlrd.book.Book).')

    #Create output container
    projects={}
    
    #Get list of tabs (projects)
    lstProjects = wb.sheets()

    #Initial coordinates (zero-indexed)
    start_row, start_col = 4, 1
    
    #Loop through projects and get records
    for i in lstProjects:
        projContents=[]
        for r in range(start_row, i.nrows-1):
            content = get_cell(i,r,start_col+2)
            if (content != None) and (content != '') :
                projContents.append({
                    "ref_no":get_cell(i,r,start_col),
                    "category":get_cell(i,r,start_col+1),
                    "content":content,
                    "assigned":get_cell(i,r,start_col+3),
                    "due_date":get_cell(i,r,start_col+4),
                    "status":get_cell(i,r,start_col+5),
                    "notes":get_cell(i,r,start_col+6)
                    })
        #Print for debugging
        '''for p in projContents:            
            print("=== " + i.name + " ===")
            for k in p:
                print("\t  - "+k+": "+str(p[k]))
        '''
        projects[i.name]=projContents
    return projects





def run():
    api_key = get_string(\
                         prompt="Enter your todoist API Key \
                         (https://todoist.com/prefs/integrations -> \
                         API Token)")
    initials = get_string(prompt="Enter initials for filter (use * for all)")
    proj_list = parse_file(\
                           open_xl_workbook(\
                                title="Select 90-Day Plan to Import"))
    api = open_api(api_key)
    print("API Key [" + str(api_key) + "] used...")
    print("Connected to user [" + api.state['user']['full_name'] + "]...")
    
    sync_project_to_app(\
                        proj_name=proj_list, \
                        task_list=None, \
                        assigned_to=initials,\
                        overwrite_proj=False,\
                        api=api)
