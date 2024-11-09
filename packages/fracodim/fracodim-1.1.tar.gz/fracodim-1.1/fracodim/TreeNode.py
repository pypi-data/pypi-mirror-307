from .listNode import listNode

nodeIndex = 0

class TreeNode(listNode):
    def __init__(self, size, index = 0):
        global nodeIndex
        self.size = size
        self.index = nodeIndex
        self.data = listNode(size)
        nodeIndex += 1

    def addChild(self, cell = 0):
        global nodeIndex
        new_child = TreeNode(self.size, nodeIndex + 1)
        self.setPointer(cell, new_child)
        
        return new_child
    
    def setCellCounter(self, cell):    
        self.setCounter(cell)

    def setRootCounter(self):
        self.setCounter(0)

    def getIndex(self):
        return self.index
    
    def getCounter(self, cell):
       if type(cell) != str:
            cellToBinary = bin(cell)[2:].zfill(self.size)
            return self.data.cells[cell][cellToBinary][0]
       else:
            return self.data.cells[int(cell, 2)][cell][0]
       
    def getPointer(self, cell):
       if type(cell) != str:
            cellToBinary = bin(cell)[2:].zfill(self.size)
            return self.data.cells[cell][cellToBinary][1]
       else:
            return self.data.cells[int(cell, 2)][cell][1]
       
    def getNodeSquareCounter(self,):
        totalSum = 0
        for cell in self.data.cells:
            for key in cell:
                totalSum += (cell[key][0]**2)
        return totalSum