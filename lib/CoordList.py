
class CoordList(object):
    def __init__(self, grid, *args, **kwargs):
        self.grid = grid
        self.empty()
    
    def empty(self):
        self.elements = []

    def pop(self):
        return self.elements.pop()

    def insert(self, idx, coord):
        return self.elements.insert(idx, coord)

    def append(self, coord):
        return self.elements.append(coord)

    def remove(self, coord):
        return self.elements.remove(coord)

    def len(self):
        return len(self.elements)

    def getField(self, coord):
        x, y = coord
        return self.grid.itemAtPosition(y, x).widget()

    def exists(self, coord):
        return (coord in self.elements)

    def first(self):
        return self.elements[0]

    def last(self):
        return self.elements[-1]
