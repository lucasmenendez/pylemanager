from os import path 
import controller
import Tkinter as tk

class View(tk.Frame):

    controller = None

    current_dir = "~"
    items_selected = []
    
    main_list = None
    statusbar_content = None
    buttons = {}

    def __init__(self, master = None):
        self.controller = controller.Controller()
        self.current_dir = path.expanduser(self.current_dir)

        tk.Frame.__init__(self, master)
        self.grid()
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
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
 
    def createMainList(self):
        if self.main_list is None:
            self.main_list = tk.Listbox(self, selectmode=tk.MULTIPLE)
    
        self.main_list.grid(row=1, column=0, columnspan=3)
        
        self.fillMainList()       
        self.main_list.bind("<Double-Button-1>", self.fillMainList) 

    def fillMainList(self, event = None):
        if self.main_list.curselection():
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
        items = self.controller.loadFolder(self.current_dir)

        self.main_list.delete(0, tk.END)
        
        if self.current_dir != "/": 
            index = 1
            self.main_list.insert(0, "../")

        for item in items:
            self.main_list.insert(index, item)
            index += 1

    def createStatusbar(self):
        self.statusbar_content = tk.StringVar()
        statusbar = tk.Label(self, textvariable=self.statusbar_content, justify=tk.RIGHT)
        
        self.statusbar_content.set("")
        statusbar.grid(row=2, column=0, columnspan=3)

    def getSelection(self):
        selection = self.main_list.curselection()
        
        items_selected = []
        for index in selection:
            item = self.current_dir + "/" + self.main_list.get(int(index))
            items_selected.append(item)
        
        return items_selected
   
    def registerAction(self, action):
        self.items_selected = self.getSelection()
        self.statusbar_content.set(str(len(self.items_selected)) + " items to " + action + ".")
        self.action = action
        self.main_list.selection_clear(0, tk.END)
     
    def execAction(self):
        self.statusbar_content.set("")
        print self.items_selected
        print self.action
