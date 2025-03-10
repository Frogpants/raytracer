import json

class ToDo:
    def __init__(self):
        self.lst = self.loadList()
    def addItem(self, item):
        self.lst.append(item)
        self.saveList()
    def removeItem(self, item):
        self.lst.remove(item)
        self.saveList()
    def saveList(self):
        with open("ToDo.json", "w") as file:
            json.dump(self.lst, file, indent=4)
    def loadList(self):
        with open("ToDo.json", "r") as file:
            loaded = json.load(file)
        return loaded