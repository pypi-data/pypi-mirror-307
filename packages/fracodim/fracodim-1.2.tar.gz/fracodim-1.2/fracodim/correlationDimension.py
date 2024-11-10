from .TreeNode import TreeNode
from scipy.stats import linregress
import math

def CorrelationDimension(points):
    
    try:
        dimension = getDatasetDimension(points)
    except ValueError as e:
        print(e)

    hypergridSideSize = getHyperSize(points)
    root = TreeNode(dimension)
    sidesizeValues = [math.log(hypergridSideSize, 10)]
    sumSquaredOccupancies = []
    myTree = {i: [] for i in range(2**dimension)}

    for point in points:
        cellSize = hypergridSideSize
        
        if(root.getCounter(0) == 0):
            root.setRootCounter()
            currentNode = root.addChild(0)
            myTree[0].append(root)
        else:
            root.setRootCounter()
            currentNode = root.getPointer(0)

        for i in range(1, (2**dimension)):
            cellSize = cellSize / 2

            if math.log(cellSize, 10) not in sidesizeValues:
                sidesizeValues.append(math.log(cellSize, 10))

            cell = cellPicker(point, cellSize)

            if currentNode not in myTree[i]:
                myTree[i].append(currentNode)

            if currentNode.getCounter(cell) == 0 and i != (2**dimension - 1):
                currentNode.setCellCounter(cell)
                currentNode.addChild(cell)
                currentNode = currentNode.getPointer(cell)
            else:
                currentNode.setCellCounter(cell)
                currentNode = currentNode.getPointer(cell)
    
    for level in myTree:
        level_counter = 0
        for node in myTree[level]:
            level_counter += node.getNodeSquareCounter()
        sumSquaredOccupancies.append(math.log(level_counter, 10))

    return linregress(sidesizeValues, sumSquaredOccupancies).slope

def cellPicker(point, sideSize):
    cell = []

    for i, coordinate in enumerate(point):      
        if coordinate <= sideSize:
            cell.append(0)
        else:
            cell.append(1)
            point[i] -= sideSize
        
    return "".join([str(x) for x in cell])

def getDatasetDimension(dataset):
    if not dataset:
        raise ValueError("Dataset cannot be empty.")
    
    first_point_dimension = len(dataset[0])
    
    for point in dataset:
        if len(point) != first_point_dimension:
            raise ValueError("Dataset contains points with different dimensions.")
    
    return first_point_dimension

def getHyperSize(dataset):
    flattened_coords = [coordinate for point in dataset for coordinate in point]

    return max(flattened_coords)
