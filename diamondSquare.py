import noise
import random
from PIL import Image

class DiamondSquare():
    def __init__(self, _sizeX, _sizeY):
        self.sizeX = _sizeX
        self.sizeY = _sizeY
        self.img = Image.new('RGB', (self.sizeX, self.sizeY), "black")
        self.pixels = self.img.load()

        self.grid = [[-1 for x in range(self.sizeX)] for y in range(self.sizeY)]
        self.bgrid = self.grid
        self.grid[0][0] = 128
        self.grid[self.sizeX-1][0] = 128
        self.grid[0][self.sizeY-1] = 128
        self.grid[self.sizeX-1][self.sizeY-1] = 128

        self.index = 120

    def ds(self, sx, sy, size, grid, index):
        c1 = self.grid[sx][sy]
        c2 = self.grid[sx+size-1][sy]
        c3 = self.grid[sx][sy+size-1]
        c4 = self.grid[sx+size-1][sy+size-1]

        hx = sx + size//2
        hy = sy + size//2

        self.grid[hx][hy] = (c1 + c2 + c3 + c4) / 4 + random.randint(-self.index/2, self.index/2)
        d = self.grid[hx][hy]

        if self.grid[hx][sy] == -1:
            self.grid[hx][sy] = (c1 + c2 + d) / 3 + random.randint(-self.index/2, self.index/2)

        if self.grid[sx + size - 1][hy] == -1:
            self.grid[sx + size - 1][hy] = (c2 + c4 + d) / 3 + random.randint(-self.index/2, self.index/2)

        if self.grid[hx][sy + size - 1] == -1:
            self.grid[hx][sy + size - 1] = (c3 + c4 + d) / 3 + random.randint(-self.index/2, self.index/2)

        if self.grid[sx][hy] == -1:
            self.grid[sx][hy] = (c1 + c3 + d) / 3 + random.randint(-self.index/2, self.index/2)

        if size != 3:
            self.ds(sx, sy, size // 2 + 1, self.grid, self.index)
            self.ds(hx, sy, size // 2 + 1, self.grid, self.index)
            self.ds(sx, hy, size // 2 + 1, self.grid, self.index)
            self.ds(hx, hy, size // 2 + 1, self.grid, self.index)
            ####
            pass
    
    def smooth(self):
        for x in range(self.sizeX):
            for y in range(self.sizeY):
                sum = self.grid[x][y]
                cells=1
                if x<self.sizeX-1:
                    sum += self.grid[x+1][y]
                    cells+= 1
                if x>0:
                    sum += self.grid[x-1][y]
                    cells+= 1
                if y<self.sizeY-1:
                    sum += self.grid[x][y+1]
                    cells+= 1
                if y>0:
                    sum += self.grid[x][y-1]
                    cells+= 1
                self.bgrid[x][y]=sum//cells

        for x in range(self.sizeX):
            for y in range(self.sizeY):
                self.grid[x][y]=abs(self.bgrid[x][y])

    def compute(self):
        self.ds(0, 0, self.sizeX, self.grid, self.index)
        for i in range(4):
            self.smooth()
            
        for i in range(self.img.size[0]):
            for j in range(self.img.size[1]):
                height = int(self.grid[i][j])
                if height > 255:
                    height = 255
                if height < 120:  # voda
                    self.pixels[i, j] = (0, 0, abs(255-height))
                elif height < 170:  # treva
                    self.pixels[i, j] = (0, height, 0)
                elif height < 240:  # planina
                    self.pixels[i, j] = (height-30, height//2-30, 0)
                else:  # snqg
                    self.pixels[i, j] = (height, height, height)

    def show(self):
        self.img.show()
         