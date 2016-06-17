import sys, os

class Controller():

    def copyFile(self, file, location):
        dest = open(location+"/"+self.basename(file), "w+")
        
        if os.path.exists(file) and os.path.isfile(file):

            buffer = None
            with open(file, "r") as content:
                buffer = content.read()

            dest.write(buffer)
            return True
        return False

    def copy(self, selection, location):
        if os.path.exists(location):
            if len(selection) > 0:    
                for item in selection:
                    if os.path.exists(item):
                        if os.path.isdir(item):
                            dest = location+"/"+self.basename(item)
                            try:
                                os.mkdir(dest, 0755)                           
                            except:
                                return False

                            new_selection = []
                            for basename in os.listdir(item):
                                new_selection.append(item+"/"+basename)

                            if not self.copy(new_selection, dest):
                                return True
                        else:
                            if not self.copyFile(item, location):
                                return False
                return True
        return False
 
    def cut(self):
        return

    def delete(self, path):
        if os.path.exists(path):
            if os.path.isdir(path):
                for (i, basename) in enumerate(os.listdir(path)):
                    item = path + "/" + basename
                    if os.path.isfile(item):
                        try:
                            os.unlink(item)
                        except:
                            return False
                    else:
                        if not self.delete(item):
                            return False
                try:
                     os.rmdir(path)    
                except:
                    return False
            else:
                try:
                    os.unlink(path)
                except:
                    return False
            
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

    def basename(self, item):
        parts = item.split("/")
        index = len(parts)-1
        return parts[index]
