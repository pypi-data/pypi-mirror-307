class listNode:
    def __init__(self, size):
        self.cells = []
        self.size = size
        listSize = 2**size
        for i in range(listSize):
            self.cells.append({bin(i)[2:].zfill(size): [0, None]})
    
    def setCounter(self, cell):
        if type(cell) != str:
            cellToBinary = bin(cell)[2:].zfill(self.size)
            self.data.cells[cell][cellToBinary][0] += 1
        else:
            self.data.cells[int(cell, 2)][cell][0] += 1

    def setPointer(self, cell, pointer):
        if type(cell) != str:
            cellToBinary = bin(cell)[2:].zfill(self.size)
            self.data.cells[cell][cellToBinary][1] = pointer
        else:
            self.data.cells[int(cell, 2)][cell][1] = pointer