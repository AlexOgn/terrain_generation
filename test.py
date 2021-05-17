import random
from PIL import Image

sizeX = 1025
sizeY = 1025

grid = [[-1 for x in range(sizeX)] for y in range(sizeY)]
bgrid = [[-1 for x in range(sizeX)] for y in range(sizeY)]
grid[0][0] = 128
grid[sizeX-1][0] = 128
grid[0][sizeY-1] = 128
grid[sizeX-1][sizeY-1] = 128

index = 120

def smooth():
    for x in range(sizeX):
        for y in range(sizeY):
            sum = grid[x][y]
            cells=1
            if x<sizeX-1:
                sum += grid[x+1][y]
                cells+= 1
            if x>0:
                sum += grid[x-1][y]
                cells+= 1
            if y<sizeY-1:
                sum += grid[x][y+1]
                cells+= 1
            if y>0:
                sum += grid[x][y-1]
                cells+= 1
            bgrid[x][y]=sum//cells

    for x in range(sizeX):
        for y in range(sizeY):
            grid[x][y]=bgrid[x][y]

def ds(sx, sy, size, grid, index):
    c1 = grid[sx][sy]
    c2 = grid[sx+size-1][sy]
    c3 = grid[sx][sy+size-1]
    c4 = grid[sx+size-1][sy+size-1]

    hx = sx + size//2
    hy = sy + size//2

    grid[hx][hy] = (c1 + c2 + c3 + c4) / 4 + random.randint(-index/2, index/2)
    d = grid[hx][hy]

    if grid[hx][sy] == -1:
        grid[hx][sy] = (c1 + c2 + d) / 3 + random.randint(-index/2, index/2)

    if grid[sx + size - 1][hy] == -1:
        grid[sx + size - 1][hy] = (c2 + c4 + d) / 3 + random.randint(-index/2, index/2)

    if grid[hx][sy + size - 1] == -1:
        grid[hx][sy + size - 1] = (c3 + c4 + d) / 3 + random.randint(-index/2, index/2)

    if grid[sx][hy] == -1:
        grid[sx][hy] = (c1 + c3 + d) / 3 + random.randint(-index/2, index/2)


    # ne e tuka bratan
    if size != 3:
        ds(sx, sy, size // 2 + 1, grid, index)
        ds(hx, sy, size // 2 + 1, grid, index)
        ds(sx, hy, size // 2 + 1, grid, index)
        ds(hx, hy, size // 2 + 1, grid, index)
        pass



img = Image.new('RGB', (sizeX, sizeY), "black")

pixels = img.load()

ds(0, 0, sizeX, grid, index)
for i in range(4):
    smooth()
for i in range(sizeX):
    for j in range(sizeY):
        grid[i][j] = abs(grid[i][j])

for i in range(img.size[0]):
    for j in range(img.size[1]):
        height = int(grid[i][j])
        if height > 255:
            height = 255
        if height < 120:  # voda
            pixels[i, j] = (0, 0, abs(255-height))
        elif height < 170:  # treva
            pixels[i, j] = (0, height, 0)
        elif height < 240:  # planina
            pixels[i, j] = (height-30, height//2-30, 0)
        else:  # snqg
            pixels[i, j] = (height, height, height)

img.show()
