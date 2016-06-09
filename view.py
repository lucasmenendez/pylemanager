from os import path 
import controller
import Tkinter as tk

class View(tk.Frame):

    controller          = None

    current_dir         = "~"
    items_selected      = []

    main_list           = None
    statusbar_content   = None
    fn_dialog           = None
    shf                 = None
    buttons             = {}

    def __init__(self, master = None):
        self.controller = controller.Controller()
        self.current_dir = path.expanduser(self.current_dir)

        tk.Frame.__init__(self, master)
        self.grid(sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.createWidgets()
    
    def createWidgets(self):
        self.createToolbar()
        self.createMainList()        
        self.createStatusbar()

    def createToolbar(self):
        self.buttons["copy"] = tk.Button(self, text="Copy", command=lambda: self.registerAction("copy"))
        self.buttons["copy"].grid(row=0, column=0);
        self.buttons["cut"] = tk.Button(self, text="Cut", command=lambda: self.registerAction("cut"))
        self.buttons["cut"].grid(row=0, column=1);
        self.buttons["paste"] = tk.Button(self, text="Paste", command=self.execAction)
        self.buttons["paste"].grid(row=0, column=2);
        self.buttons["new_file"] = tk.Button(self, text="New file")
        self.buttons["new_file"].grid(row=0, column=3);
        self.buttons["delete"] = tk.Button(self, text="Delete", command=self.deleteFolder)
        self.buttons["delete"].grid(row=0, column=4);
        self.buttons["new_folder"] = tk.Button(self, text="New folder", command=self.newFolderDialog)
        self.buttons["new_folder"].grid(row=0, column=5);
        self.buttons["reload"] = tk.Button(self, text="Reload", command=self.reloadMainList)
        self.buttons["reload"].grid(row=0, column=6);
 
    def createMainList(self):
        if self.main_list is None:
            self.main_list = tk.Listbox(self, selectmode=tk.MULTIPLE)
    
        self.main_list.grid(row=1, column=0, columnspan=7, sticky="nsew")
        
        self.reloadMainList()       
        self.main_list.bind("<Double-Button-1>", self.reloadMainList) 

    def reloadMainList(self, event = None):
        if not event is None and self.main_list.curselection(): 
            folder_index = self.main_list.curselection()[0]
            folder = self.main_list.get(int(folder_index))

            if folder == "../":
                folder = self.current_dir.split("/")
                del folder[len(folder) - 1]
                if len(folder) > 1:
                    self.current_dir = "/".join(folder)
                else:
                    self.current_dir = "/"
            else:
                self.current_dir += "/" + folder
            
        index = 0
        if self.shf is None:
            self.shf = tk.IntVar()
            self.shf.set(0)
        
        items = self.controller.loadFolder(self.current_dir, self.shf.get())

        self.main_list.delete(0, tk.END)
        if self.current_dir != "/": 
            index = 1
            self.main_list.insert(0, "../")

        for item in items:
            self.main_list.insert(index, item)
            index += 1

    def createStatusbar(self):
        shf_checkbutton = tk.Checkbutton(self.master, text="Show hidden files", variable=self.shf, command=self.reloadMainList)
 
        shf_checkbutton.grid(row=2, column=0, columnspan=7)

        self.statusbar_content = tk.StringVar()
        statusbar = tk.Label(self, textvariable=self.statusbar_content)
        
        self.statusbar_content.set("")
        statusbar.grid(row=3, column=0, columnspan=7)

    def newFolderDialog(self):
        self.fn_dialog = tk.Toplevel()
        self.fn_dialog.title("Create folder")
        
        self.fn_dialog.grid()
        self.fn_dialog.grid_rowconfigure(0, weight=1)
        self.fn_dialog.grid_columnconfigure(0, weight=1)
    
        fn = tk.StringVar()
        fd_field = tk.Entry(self.fn_dialog, textvariable=fn)
        fd_field.grid(row=0, column=0, columnspan=2)

        submit = tk.Button(self.fn_dialog, text="Create folder", command=lambda: self.submitNewFolder(fn.get()))
        submit.grid(row=1, column=0)

        cancel = tk.Button(self.fn_dialog, text="Close", command=self.fn_dialog.destroy)
        cancel.grid(row=1, column=1)
 
        self.fn_dialog.mainloop()
 
    def getSelection(self):
        selection = self.main_list.curselection()
        
        items_selected = []
        for index in selection:
            item = self.current_dir + "/" + self.main_list.get(int(index))
            items_selected.append(item)
        
        return items_selected
   
    def registerAction(self, action):
        self.items_selected = self.getSelection()
        self.statusbar_content.set(str(len(self.items_selected)) + " selected.")
        self.action = action
        self.main_list.selection_clear(0, tk.END)
     
    def execAction(self):
        self.statusbar_content.set("")
        print self.items_selected
        print self.action

    def submitNewFolder(self, folder_name):
        folder = self.current_dir + "/" + folder_name
        if not self.controller.createFolder(folder):
            self.statusbar_content.set("Error ocurred creating '"+folder_name+"' folder.")
        else:
            self.reloadMainList()       
 
        self.fn_dialog.destroy()

    def deleteFolder(self): 
        if self.main_list.curselection(): 
            index = self.main_list.curselection()[0]
            basename = self.main_list.get(int(index))
            path = self.current_dir + "/" + basename

            if self.controller.delete(path):
                self.statusbar_content.set("'"+basename+"' deleted succesfully.")
                self.reloadMainList()
            else:
                self.statusbar_content.set("Error deleting '"+basename+"' folder.")
