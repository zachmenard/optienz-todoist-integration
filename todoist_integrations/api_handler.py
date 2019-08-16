# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 12:51:36 2019

@author: zachm
"""

from todoist.api import TodoistAPI
from todoist.models import *
from .xl_handler import xldate_to_todoist
import re
import tkinter as tk
from tkinter import ttk
from collections.abc import Iterable

sticky_all = tk.N+tk.S+tk.E+tk.W
todoist_types = (Collaborator, CollaboratorState, Filter,
 GenericNote, Item, Label, LiveNotification, Model, Note, Project,
 ProjectNote, Reminder)

class main_window(object):
    def __init__(self,api=None):
        self.root = tk.Tk()
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.build_widgets()
        if api != None:
            self.load_api(api)
        self.root.mainloop()
    def build_widgets(self):
        self.pane = tk.Frame(self.root)
        self.pane.columnconfigure(0, weight=1)
        self.pane.rowconfigure(0, weight=1)
        self.pane.grid(row=0,column=0,sticky=sticky_all)
        self.tree = ttk.Treeview(self.pane)
        self.tree.grid(row=0,column=0,sticky=sticky_all)
        self.btn_load=tk.Button(self.pane)
        
    def load_api(self,api):
        self.tree.delete(*self.tree.get_children())
        p_node = self.tree.insert('','end',text='API')
        self.add_nodes(p_node, api.state)
    def add_nodes(self,p_node, dict_obj):
        if isinstance(dict_obj,dict):
            for key in dict_obj:
                item = dict_obj[key]
                c_node = self.tree.insert(p_node,'end',text=key)
                if isinstance(item,Iterable):                    
                    self.add_nodes(c_node,item)
                else:
                    self.tree.item(c_node,text=key + ":\t" + str(item))
        elif isinstance(dict_obj, todoist_types):
            old_text = self.tree.item(p_node)['text']
            try:
                self.tree.item(p_node,text=old_text + ' ' + \
                               dict_obj.data['name'])
                
            except:
                try:
                    self.tree.item(p_node,text=old_text + ' ' + \
                               dict_obj.data['content'])
                except:
                    self.tree.item(p_node,text=old_text)
            self.add_nodes(p_node, dict_obj.data)
        elif isinstance(dict_obj,list):
            l_node = self.tree.insert(p_node,'end',text='List')
            for i,item in enumerate(dict_obj):
                c_node = self.tree.insert(l_node,'end',text='['+str(i)+']')
                self.add_nodes(c_node,item)
        else:
            c_node = self.tree.insert(p_node,'end',text=str(dict_obj))
            

    
                        
            
class client_api(TodoistAPI):
    def __init__(self,key):
        super().__init__(token=key)
    def visualize(self):
        main_window(self)
    def delete_empty_items(self):
        n = 0
        for item in self.state['items']:
            if item['content']=='':
                print("Deleting: " + str(item['id']))
                item.delete()
                n+=1
            if n==100:
                self.commit()
        self.commit()
        

def open_api(key=None):
    #creates an api link
    if key == None:
        key = 'ef4f8584f54b60f15b12597c1419f8e761b33427'
    api = client_api(key)
    api.sync()
    return api

def add_project(api, p_name, overwrite=False,**kwargs):
    '''
    Either adds a new project or gets the project from
    the API with the same name. If overwrite == True a
    new project is created and any existing project
    with that name is deleted

    kwargs
    name,String	           The name of the project (a string value).
    color,Integer          The color of the project (a number between 0 and 11, or between 0 and 21 for premium users).
    indent,Integer         The indent of the item (a number between 1 and 4, where 1 is top-level).
    item_order,Integer     Project’s order in the project list (a number, where the smallest value should place the project at the top).
    collapsed,Integer      Whether the project’s sub-projects are collapsed (where 1 is true and 0 is false).
    is_favorite,Integer    Whether the project is favorite (where 1 is true and 0 is false).
    '''
    p = None
    lstProj = api.state['projects']
    for proj in lstProj:
        if proj['name'] == p_name:
            p = proj
            break
    if p == None:
        p = api.projects.add(p_name)
    if overwrite:
        p.delete()
        p = api.projects.add(p_name)
    p.update(**kwargs)
    api.commit()
    return p

def get_tasks(api, proj):
    try:
        return api.projects.get_data(proj['id'])['items']
    except Exception:
        return []

def find_task_in_proj(api, proj, content):
    tsk = get_tasks(api, proj)
    for t in tsk:
        if t['content'] == content:
            return t
    return None



def add_task(api, proj, content='', overwrite=False, do_commit=True, **kwargs):
    '''
    Either adds a new task or gets the task from
    the project. If overwrite == True a
    new task is created and any existing task
    with that name is deleted. Otherwise the selected task
    is updated using the keyword arguments

    kwargs -- immutable
    id,Integer
	The id of the task.
    user_id,Integer
	The owner of the task.
    project_id,Integer -- set by the proj argument
	Project that the task resides in
    content,String
	The text of the task
    date_string,String
	The date of the task, added in free form text, for example it can be every day @ 10 (or null or an empty string if not set). Look at our reference to see which formats are supported.
    date_lang,String
	The language of the date_string (valid languages are: en, da, pl, zh, ko, de, pt, ja, it, fr, sv, ru, es, nl).
    due_date_utc,String
	The date of the task in the format Mon 07 Aug 2006 12:34:56 +0000 (or null if not set). For all day task (i.e. task due “Today”), the time part will be set as xx:xx:59.
    priority,Integer
	The priority of the task (a number between 1 and 4, 4 for very urgent and 1 for natural).
        Note: Keep in mind that very urgent is the priority 1 on clients.
        So, p1 will return 4 in the API.
    indent,Integer
	The indent of the task (a number between 1 and 5, where 1 is top-level).
    item_order,Integer
	The order of the task inside a project (the smallest value would place the task at the top).
    day_order,Integer
	The order of the task inside the Today or Next 7 days view (a number, where the smallest value would place the task at the top).
    collapsed,Integer
	Whether the task’s sub-tasks are collapsed (where 1 is true and 0 is false).
    labels,Array of Integer
	The tasks labels (a list of label ids such as [2324,2525]).
    assigned_by_uid,Integer
	The id of the user who assigns the current task. This makes sense for shared projects only. Accepts 0 or any user id from the list of project collaborators. If this value is unset or invalid, it will automatically be set up to your uid.
    responsible_uid,Integer
	The id of user who is responsible for accomplishing the current task. This makes sense for shared projects only. Accepts any user id from the list of project collaborators or null or an empty string to unset.
    checked,Integer
	Whether the task is marked as completed (where 1 is true and 0 is false).
    in_history,Integer
	Whether the task has been marked as completed and is marked to be moved to history, because all the child tasks of its parent are also marked as completed (where 1 is true and 0 is false)
    is_deleted,Integer
	Whether the task is marked as deleted (where 1 is true and 0 is false).
    is_archived,Integer
	Whether the task is marked as archived (where 1 is true and 0 is false).
    sync_id,Integer
	A special id for shared tasks (a number or null if not set). Used internally and can be ignored.
    date_added,String
	The date when the task was created.'''
    tsk = find_task_in_proj(api, proj, content)
    if tsk!=None:
        if overwrite:            
            tsk.delete()
            item = api.add_item(content=content,project_id=proj['id'])
        else:
            item = tsk
    else:
        item = api.add_item(content=content,project_id=proj['id'])
    item.update(**kwargs)
    if do_commit:
        api.commit()
    return item
    
def filter_by_assignment(task_list, assigned_to=None):
    '''Returns a subset of the task_list parameter containing only those
    tasks which are assigned to the person listed in the assigned_to argument.
    If '*' is passed in the assigned_to argument or it is left blank all tasks
    are returned.'''
    if assigned_to==None:
        assigned_to = '*'
    assigned_to = str(assigned_to).strip()
    if (assigned_to=='*'):
        return task_list
    else:
        filtered_tasks = []
        #delimiter-independent search via regular expression
        re_search='\W*\s*'+str(assigned_to)+'\s*\W*'
        for tsk in task_list:
            m = re.search(re_search,tsk['assigned'])
            if m != None:
               filtered_tasks.append(tsk)
        return filtered_tasks

def sync_project_to_app(proj_name, task_list, assigned_to="*", proj_params={},\
                        overwrite_proj=False, overwrite_tasks=False, api=None):
    '''Syncs a project and all associated tasks to ToDoist app.'''
    if (api==None):
        api = open_api()
    if isinstance(proj_name,dict):
        print("Dictionary passed")
        for k in proj_name:
            sync_project_to_app(k, proj_name[k], assigned_to, proj_params, \
                                overwrite_proj, overwrite_tasks, api)
    else:
        print("Updating project <"+str(proj_name)+">...")
        p = add_project(api,proj_name,overwrite_proj,**proj_params)
        print("\t -- Project found/generated: First pass to add tasks")
        filtered_tasks = filter_by_assignment(task_list,assigned_to)
        t_ids = []
        for tsk in filtered_tasks:
            print("\t Updating task <"+tsk['content']+">...")
            task_args= {
                "due":{"string":tsk["due_date"]} if not \
                (str(tsk["due_date"]).isnumeric() or \
                 isinstance(tsk['due_date'],(int,float))) else \
                xldate_to_todoist(float(tsk["due_date"])),
                "notes":tsk["notes"]
                }
            task_obj = add_task(api,p,tsk['content'],overwrite_tasks,False)
            t_ids.append([task_obj['id'],task_args])
            
            task_obj.update(**task_args)
            #for t_item in task_obj:
            #    print("\t  **"+t_item+": "+str(task_obj[t_item]))
        api.commit()
        print("\t -- Second pass to add due dates")
        for tsk in t_ids:
            print("\t Setting task date id="+str(tsk[0])+"...")
            api.items.get_by_id(tsk[0]).update(**tsk[1])
            #for t_item in task_obj:
            #    print("\t  **"+t_item+": "+str(task_obj[t_item]))
        api.commit()
        
        #print("Committing project "+str(proj_name)+"...")
        
    return api