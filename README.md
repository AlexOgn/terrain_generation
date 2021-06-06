# Terrain generation
Alex Ognyanov project

Generates terrain pseudo-random terrain and has 3D visualisation options

# Algorithms implemented:
  - Diamond Square
  - Perlin Noise

# Documentation
## Diamond Square (ds)
### How does it work
![Image of DS](https://upload.wikimedia.org/wikipedia/commons/thumb/b/bf/Diamond_Square.svg/2560px-Diamond_Square.svg.png)
At it's essense it's a recursive algorithm that has 2 steps:
- Diamond step
  - Takes four corners and averages it then adds a random value
- Square step
  - Averages each edge and adds a random value

The next step is to do the same thing until the whole grid is filled with values

## Code
### Initialization
Arguments and `__init__` function
```python
def __init__(self, _sizeX, _sizeY):
```
We check if every argument is valid and then we initializise everything
```python
if not isinstance(_sizeX, int):
    raise Exception("First argument (sizeX) is not integer")
if not isinstance(_sizeY, int):
    raise Exception("Second argument (sizeY) is not integer") 
```
We then initialize every needed variable
```python
self.sizeX = _sizeX
self.sizeY = _sizeY
self.img = Image.new('RGB', (self.sizeX, self.sizeY), "black")
self.pixels = self.img.load()
```
After that we fill the whole grid with `-1` and we initialize the four initial corners
```python
self.grid = [[-1 for x in range(self.sizeX)]
                     for y in range(self.sizeY)]
self.bgrid = self.grid
self.grid[0][0] = 128
self.grid[self.sizeX-1][0] = 128
self.grid[0][self.sizeY-1] = 128
self.grid[self.sizeX-1][self.sizeY-1] = 128

self.index = 120
```
### Diamond-Square function

We initialize the funcion and get arguments
```python
def ds(self, sx, sy, size, grid, index):
```

We get the initial variables so it's easier to do calculations
```python
c1 = self.grid[sx][sy]
c2 = self.grid[sx+size-1][sy]
c3 = self.grid[sx][sy+size-1]
c4 = self.grid[sx+size-1][sy+size-1]

hx = sx + size//2
hy = sy + size//2

d = self.grid[hx][hy]
```

We then calculate and assign values
```python
self.grid[hx][hy] = (c1 + c2 + c3 + c4) / 4 + random.randint(-self.index/2, self.index/2)

if self.grid[hx][sy] == -1:
  self.grid[hx][sy] = (c1 + c2 + d) / 3 + random.randint(-self.index/2, self.index/2)

if self.grid[sx + size - 1][hy] == -1:
  self.grid[sx + size - 1][hy] = (c2 + c4 + d) / 3 + random.randint(-self.index/2, self.index/2)

if self.grid[hx][sy + size - 1] == -1:
  self.grid[hx][sy + size - 1] = (c3 + c4 + d) / 3 + random.randint(-self.index/2, self.index/2)

if self.grid[sx][hy] == -1:
  self.grid[sx][hy] = (c1 + c3 + d) / 3 + random.randint(-self.index/2, self.index/2)
```

Then we run the recursion part
```python
if size != 3:
  self.ds(sx, sy, size // 2 + 1, self.grid, self.index)
  self.ds(hx, sy, size // 2 + 1, self.grid, self.index)
  self.ds(sx, hy, size // 2 + 1, self.grid, self.index)
  self.ds(hx, hy, size // 2 + 1, self.grid, self.index)
  pass
```

### Smooth function
We initialize the funcion
```python
def smooth(self):
```

We then run a `for` loop that averages every cell based on the cells around it
```python
for x in range(self.sizeX):
    for y in range(self.sizeY):
        sum = self.grid[x][y]
        cells = 1
    if x < self.sizeX-1:
        sum += self.grid[x+1][y]
        cells += 1
    if x > 0:
        sum += self.grid[x-1][y]
        cells += 1
    if y < self.sizeY-1:
        sum += self.grid[x][y+1]
        cells += 1
    if y > 0:
        sum += self.grid[x][y-1]
        cells += 1
    self.bgrid[x][y] = sum//cells
```

After that we write to the original array
```python
for x in range(self.sizeX):
    for y in range(self.sizeY):
      self.grid[x][y] = abs(self.bgrid[x][y])
```
### 3D visualization using matlib
Initialization
```python
def show3D(self):
```
Create needed variables
```python
z = np.array(self.grid)
x, y = np.meshgrid(range(z.shape[0]), range(z.shape[1]))

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(x, y, z)
plt.title('Diamond square height map')
```
Visualize the height map
```python
plt.show()
```
