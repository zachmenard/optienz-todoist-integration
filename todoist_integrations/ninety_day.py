from .api_handler import *
from .xl_handler import *

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
    
    initials = get_string(prompt="Enter initials for filter (use * for all)")
    try:
        proj_list = parse_file(\
                           open_xl_workbook(\
                                title="Select 90-Day Plan to Import"))
    except:
        print("Aborting operation, no file selected")
        return
    api = open_api()
    print("API Key [" + str(api_key) + "] used...")
    print("Connected to user [" + api.state['user']['full_name'] + "]...")
    
    api.sync_project_to_app(\
                        proj_name=proj_list, \
                        task_list=None, \
                        assigned_to=initials,\
                        overwrite_proj=False)
