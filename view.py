import os, controller, webbrowser, tkMessageBox
import Tkinter as tk

class View(tk.Frame):

    controller          = None

    current_dir         = "~"
    items_selected      = []
    action              = None

    main_list           = None
    topMenu             = None
    contextMenu         = None

    fn_dialog           = None
    shf                 = None

    def __init__(self, master = None):
        self.controller     = controller.Controller()
        self.current_dir    = os.path.expanduser(self.current_dir)

        if master is None:
            master = tk.Tk()
            master.geometry("400x400")

        tk.Frame.__init__(self, master)
        self.pack(fill=tk.BOTH, expand=True) 
        self.master.bind("<Button-1>", self.closeContextMenu)
        self.createWidgets()
        
        self.master.title(self.current_dir + " - Pylemanager")
        self.master.mainloop()   
 
    def createWidgets(self):
        self.createTopMenu()
        self.createMainList()        
        self.createContextMenu()

    def createTopMenu(self):
        self.topMenu = tk.Menu(self)
        
        file_submenu = tk.Menu(self.topMenu, tearoff=0)
        file_submenu.add_command(label="New folder", command=self.newFolderDialog)
        file_submenu.add_separator()
        file_submenu.add_command(label="Quit", command=self.quit)

        edit_submenu = tk.Menu(self.topMenu, tearoff=0)
        edit_submenu.add_command(label="Copy", command=lambda: self.registerAction("copy"))
        edit_submenu.add_command(label="Cut", command=lambda: self.registerAction("cut")) 
        edit_submenu.add_command(label="Paste", command=self.execAction)
        edit_submenu.add_separator()
        edit_submenu.add_command(label="Delete", command=self.deleteAction)
 
        self.shf = tk.IntVar()
        self.shf.set(0)
        config_submenu = tk.Menu(self.topMenu, tearoff=0)
        config_submenu.add_checkbutton(label="Show hidden files", variable=self.shf, command=self.reloadMainList)
        config_submenu.add_separator()
        config_submenu.add_command(label="About", command=lambda: webbrowser.open("https://github.com/lucasmenendez/pylemanager"))

        self.topMenu.add_cascade(label="File", menu=file_submenu)
        self.topMenu.add_cascade(label="Edit", menu=edit_submenu)
        self.topMenu.add_cascade(label="Settings", menu=config_submenu)
        self.master.config(menu=self.topMenu)

    def createMainList(self):
        if self.main_list is None:
            self.main_list = tk.Listbox(self, selectmode=tk.MULTIPLE)
    
        self.main_list.pack(fill=tk.BOTH, expand=True)
        
        self.reloadMainList()       
        self.main_list.bind("<Double-Button-1>", self.reloadMainList) 

    def reloadMainList(self, event = None):
        if not event is None and self.main_list.curselection(): 
            item_index = self.main_list.curselection()[0]
            item = self.main_list.get(int(item_index))
         
            if item == "../":
                item = self.current_dir.split("/")
                del item[len(item) - 1]
                if len(item) > 1:
                    current_item = "/".join(item)
                else:
                    current_item = "/"
            else:
                current_item = self.current_dir + "/" + item
        
            if path.isdir(current_item):
                self.current_dir = current_item
            else:
                print current_item
                os.system("open " + current_item)    
         
        index = 0
        if self.shf is None:
            self.shf = tk.IntVar()
            self.shf.set(0)
       
        self.master.title(self.current_dir + " - Pylemanager")
        items = self.controller.loadFolder(self.current_dir, self.shf.get())
        items.sort()

        self.main_list.delete(0, tk.END)
        if self.current_dir != "/": 
            index = 1
            self.main_list.insert(0, "../")
        else:
            self.current_dir = ""
        
        for item in items:
            self.main_list.insert(index, item)
            index += 1

    def createContextMenu(self):
        self.contextMenu = tk.Menu(self, tearoff=0)
        
        self.contextMenu.add_command(label="Copy", command=lambda: self.registerAction("copy"))
        self.contextMenu.add_command(label="Cut", command=lambda: self.registerAction("cut")) 
        self.contextMenu.add_command(label="Paste", command=self.execAction)
        self.contextMenu.add_command(label="Delete", command=self.deleteAction)
        self.contextMenu.add_separator()
        self.contextMenu.add_command(label="Reload", command=self.reloadMainList)

        self.main_list.bind("<Button-3>", self.openContextMenu)

    def openContextMenu(self, event):
        self.contextMenu.post(event.x_root, event.y_root)

    def closeContextMenu(self, event):
        self.contextMenu.unpost()

    def newFolderDialog(self):
        self.fn_dialog = tk.Toplevel()
        self.fn_dialog.title("Create folder")
        
        fn = tk.StringVar()
        fd_field = tk.Entry(self.fn_dialog, textvariable=fn)
        fd_field.pack(fill=tk.X)

        submit = tk.Button(self.fn_dialog, text="Create folder", command=lambda: self.submitNewFolder(fn.get()))
        submit.pack(side=tk.LEFT)

        cancel = tk.Button(self.fn_dialog, text="Close", command=self.fn_dialog.destroy)
        cancel.pack(side=tk.RIGHT)
 
        self.fn_dialog.mainloop()
 
    def getSelection(self):
        selection = self.main_list.curselection()
        
        items_selected = []
        for index in selection:
            basename = self.main_list.get(int(index))
            if not basename.startswith("../"): 
                item = self.current_dir + "/" + basename
                items_selected.append(item)
        
        return items_selected
   
    def registerAction(self, action, display_info = True):
        self.items_selected = self.getSelection()
        self.action = action
        self.main_list.selection_clear(0, tk.END)
     
    def execAction(self):
        if not self.action is None:
            action = getattr(self.controller, self.action)     
            location = self.current_dir
            
            selection = self.getSelection()
            if len(selection) > 0:
                location = selection[0]
            if len(self.items_selected) > 0:
                if tkMessageBox.askokcancel(self.action.capitalize(), "Are you sure? This action can be permanent"): 
                    if action(self.items_selected, location):
                        self.action = None
                    else:
                        tkMessageBox.showerror("Ops", "An error occurred :(")            
                    self.reloadMainList()

    def submitNewFolder(self, folder_name):
        folder = self.current_dir + "/" + folder_name
        if not self.controller.createFolder(folder):
            self.statusbar_content.set("Error ocurred creating '"+folder_name+"' folder.")
        else:
            self.reloadMainList()       
 
        self.fn_dialog.destroy()

    def deleteAction(self): 
        if self.main_list.curselection():
            self.registerAction("delete")
            self.execAction() 
