import sys, os

class Controller():

    def copy(self):
        return
 
    def cut(self):
        return

    def delete(self, path):
        if os.path.exists(path):
            if os.path.isdir(path):
                for (i, basename) in enumerate(os.listdir(path)):
                    item = path + "/" + basename
                    if os.path.isfile(item):
                        os.unlink(item)
                    else:
                        if not self.delete(item):
                            return False
                os.rmdir(path)    
            else:
                os.unlink(path)
            
            return True    
        return False

    def createFolder(self, folder):
        if not os.path.exists(folder):
            try:
                os.makedirs(folder)
                return True
            except:
                return False

        return False
 
    def loadFolder(self, folder, show_hidden_files):
        items = [] 
        for (i, item) in enumerate(os.listdir(folder)):
            if show_hidden_files is 0 and item.startswith("."): continue
            items.append(item)

        return items
