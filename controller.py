import sys, os

class Controller():

    def cp(self, file, location):
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
                            return False
                    else:
                        if not self.cp(item, location):
                            return False
            return True
        return False
 
    def cut(self, selection, location):
        if os.path.exists(location):
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

                        if self.cut(new_selection, dest):
                            try:
                                os.rmdir(item)
                            except:
                                return False
                        else:
                            return False
                    else:
                        if self.cp(item, location):
                            try:
                                os.unlink(item)
                            except:
                                return False
                        else:
                            return False
            return True
        return False
 
    def delete(self, selection, location):
        for path in selection:
            if os.path.exists(path):
                if os.path.isdir(path):
                    for src in os.listdir(path):
                        item = path + "/" + src
                        if os.path.isdir(item):
                            new_selection = []
                            for basename in os.listdir(item):
                                new_selection.append(item)

                            if not self.delete(new_selection, item):
                                return False
                        else:
                            try:
                                os.unlink(item)
                            except:
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
