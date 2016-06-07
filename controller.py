import sys
from os import listdir 

class Controller():

    def copy(self):
        return
 
    def cut(self):
        return
    
    def loadFolder(self, folder):
        items = [] 
        for (i, item) in enumerate(listdir(folder)):
            if item.startswith("."): continue
            items.append(item)

        return items
