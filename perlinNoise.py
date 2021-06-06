import noise
import random
from PIL import Image
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np


class PerlinNoise():
    def __init__(self, _sizeX, _sizeY, _octaves=5, _frequency=150):
        if not isinstance(_sizeX, int):
            raise Exception("First argument (sizeX) is not integer")
        if not isinstance(_sizeY, int):
            raise Exception("Second argument (sizeY) is not integer")
        if not isinstance(_octaves, int):
            raise Exception("First argument (octaves) is not integer")
        if not isinstance(_frequency, int):
            raise Exception("Second argument (frequency) is not integer")

        self.octaves = _octaves
        self.frequency = _frequency
        self.sizeX = _sizeX
        self.sizeY = _sizeY
        self.grid = self.grid = [[-1 for x in range(self.sizeX)]
                                 for y in range(self.sizeY)]
        self.seed = random.uniform(-10000, 10000)
        self.img = Image.new('RGB', (self.sizeX, self.sizeY), "black")
        self.pixels = self.img.load()

    def compute(self):
        for i in range(self.img.size[0]):
            for j in range(self.img.size[1]):
                height = int(noise.snoise3(i/self.frequency, j /
                                           self.frequency, self.seed, self.octaves) * 127 + 128)
                self.grid[i][j] = height
                if height < 110:  # voda
                    self.pixels[i, j] = (0, 0, abs(255-height))
                elif height < 140:  # treva
                    self.pixels[i, j] = (0, height, 0)
                elif height < 190:  # planina
                    self.pixels[i, j] = (height-30, int(height/2-30), 0)
                else:  # snqg
                    self.pixels[i, j] = (height, height, height)

    def show(self):
        self.img.show()

    def show3D(self):
        # trqq da e po-maluk grid
        z = np.array(self.grid)
        x, y = np.meshgrid(range(z.shape[0]), range(z.shape[1]))

        # show hight map in 3d
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(x, y, z)
        plt.title('Perlin noise height map')
        plt.show()

    def run(self):
        self.compute()
        self.show()

    def run3D(self):
        self.compute()
        self.show3D()
