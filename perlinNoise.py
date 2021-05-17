import noise
import random
from PIL import Image
class PerlinNoise():
    def __init__(self, _octaves, _frequency, _sizeX, _sizeY):
        self.octaves = _octaves
        self.frequency = _frequency
        self.sizeX = _sizeX
        self.sizeY = _sizeY
        self.seed = random.uniform(-10000, 10000)
        self.img = Image.new('RGB', (self.sizeX, self.sizeY), "black")
        self.pixels = self.img.load()

    def compute(self):
        for i in range(self.img.size[0]):
            for j in range(self.img.size[1]):
                height = int(noise.snoise3(i/self.frequency, j /
                                        self.frequency, self.seed, self.octaves) * 127 + 128)
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
    
    def run(self):
        self.compute()
        self.show()