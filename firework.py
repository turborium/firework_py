# pip install pyxel
import pyxel
import math
import random

FIREWORK_PALETTE_LIST = [
    [7, 14, 8, 2, 1],
    [7, 11, 5],
    [7, 6, 12, 5, 1],
    [15, 10, 9, 4],
]
GRAVITY = 0.09
RESISTANCE = 0.02
FIREWORK_COUNT = 10
BOUNDS = 40

class Spark:
    def __init__(self, x, y, palette):
        self.palette = palette 
        self.x = x
        self.y = y
        angle = math.pi * random.random() * 2
        speed = random.random() * 2 + 0.1
        self.dx = math.cos(angle) * speed
        self.dy = math.sin(angle) * speed
        self.fade = 0
        self.dfade = 0.025 + random.random() * 0.05 

    def update(self):
        self.x = self.x + self.dx
        self.y = self.y + self.dy
        self.fade = self.fade + self.dfade
        self.dy = self.dy + GRAVITY
        self.dx = self.dx * (1 - RESISTANCE)

    def draw(self):
        color_index = self.palette[min(len(self.palette) - 1, int(self.fade * len(self.palette)))]
        pyxel.pset(int(self.x), int(self.y), color_index)

    def is_dead(self):
        return self.fade > 1.0

class Firework:
    def __init__(self, x, y, palette):
        self.spark_list = []
        self.skip_frames = random.randint(0, 50)
        for _ in range(200):
            self.spark_list.append(Spark(x, y, palette))

    def update(self):
        if self.skip_frames > 0:
            self.skip_frames = self.skip_frames - 1
            return

        for spark in self.spark_list:
            spark.update()   

    def draw(self):
        if self.skip_frames > 0:
            return

        for spark in self.spark_list:
            spark.draw()   

    def is_dead(self):
        result = True
        for spark in self.spark_list:
            if not spark.is_dead():
                result = False
                break
        return result
            
def make_firework():
    return Firework(
        random.randint(0 + BOUNDS, pyxel.width - BOUNDS), 
        random.randint(0 + BOUNDS, pyxel.height - BOUNDS), 
        random.choice(FIREWORK_PALETTE_LIST),
    )

class App:
    def __init__(self):
        pyxel.init(256, 256)

        self.firework_list = []
        for _ in range(FIREWORK_COUNT):
            self.firework_list.append(make_firework())    
        
        pyxel.run(self.update, self.draw)
        

    def update(self):
        for i in range(len(self.firework_list)):
            self.firework_list[i].update()
            if self.firework_list[i].is_dead():
                self.firework_list[i] = make_firework()      

    def draw(self):
        pyxel.cls(0)
        for firework in self.firework_list:
            firework.draw()

App()