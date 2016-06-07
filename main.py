import view

class Filemanager():
    
    instance = None  

    def __init__(self):
        self.instance = view.View()
        self.instance.master.title("Pylemanager")
        self.instance.mainloop()


filemanager = Filemanager()
