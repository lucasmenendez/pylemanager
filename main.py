# -*- conding: utf-8 -*-

import view

class Filemanager():
    
    instance = None  

    def __init__(self):
        self.instance = view.View()


filemanager = Filemanager()
