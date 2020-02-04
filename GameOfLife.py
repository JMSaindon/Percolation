import sys
import pygame
import pygame.draw
import numpy as np

__screenSize__ = (1530,835)
__cellSize__ = 20
__gridDim__ = tuple(map(lambda x: int(x/__cellSize__), __screenSize__))


def getColorCell(n):
    if n == 0: #alive
        return (255,255,255)
    else:#dead
        return (0, 0, 0)

class Grid:
    """Classe représentant le plateau de jeu par une matrice.
    Une case vivante est représentée par 0 et une morte par 1"""

    _grid= None
    def __init__(self, density):
        ratio = 1 - density
        print("Creating a grid of dimensions " + str(__gridDim__))
        randBase = np.random.random_sample(__gridDim__)
        randBase[randBase < ratio] = 0
        randBase[randBase >= ratio] = 1
        self._grid = randBase

    def addBlockFromMouse(self, coord, w):
        x = int(coord[0] / __cellSize__)
        y = int(coord[1] / __cellSize__)
        self._grid[x,y] = w

    def drawMe(self):
        pass

    def inside(self, i, j):
        return i >= 0 and i < __gridDim__[0] and j >=0 and j < __gridDim__[1]


    def computeState(self, i, j):
        count = 0
        for x in range(-1,2):
            for y in range(-1,2):
                if(self.inside(i+x, j+y) and (x!=0 or y!=0)):
                    count += self._grid[i+x, j+y]
        if(count == 3):
            return 1
        elif(count == 2):
            return self._grid[i,j]
        else:
            return 0


    def computeStep(self):
        nextStep = np.zeros(__gridDim__)
        for i in range(__gridDim__[0]):
            for j in range(__gridDim__[1]):
                nextStep[i,j] = self.computeState(i, j)
        self._grid = nextStep


class Scene:
    _mouseCoords = (0,0)
    _grid = None
    _font = None

    def __init__(self, density):
        pygame.init()
        self._screen = pygame.display.set_mode(__screenSize__)
        self._font = pygame.font.SysFont('Arial',25)
        self._grid = Grid(density)

    def drawMe(self):
        if self._grid._grid is None:
            return
        self._screen.fill((128,128,128))
        for x in range(__gridDim__[0]):
            for y in range(__gridDim__[1]):
                pygame.draw.rect(self._screen,
                        getColorCell(self._grid._grid.item((x,y))),
                        (x*__cellSize__ + 1, y*__cellSize__ + 1, __cellSize__-2, __cellSize__-2))


    def drawText(self, text, position, color = (255,64,64)):
        self._screen.blit(self._font.render(text,1,color),position)

    def update(self):
        # time.sleep(1)
        self._grid.computeStep()

    def eventClic(self,coord,b):
        pass

    def recordMouseMove(self, coord):
        pass


def main(density):
    buildingGrid = False # True if the user can add / remove walls / weights
    scene = Scene(density)
    done = False
    clock = pygame.time.Clock()
    buildingTrack = True
    Life = 0
    while done == False:
        clock.tick(20)
        scene.update()
        scene.drawMe()
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Exiting")
                done=True
            if event.type == pygame.KEYDOWN:
                if event.unicode in [str(i) for i in range (10)]:
                    wallWeight = min(1, .1 + 1 - int(event.unicode)/10)
                    break
                if event.key == pygame.K_q or event.key==pygame.K_ESCAPE: # q
                    print("Exiting")
                    done = True
                    break
                if event.key == pygame.K_s: # s
                    np.save("matrix.npy",scene._grid._grid)
                    print("matrix.npy saved")
                    break
                if event.key == pygame.K_l: # l
                    print("matrix.npy loaded")
                    scene._grid._grid = np.load("matrix.npy")
                    break
                if event.key == pygame.K_n:
                    buildingTrack = False
                    break
                if event.key == pygame.K_b :
                    buildingTrack = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if buildingTrack:
                    scene._grid.addBlockFromMouse(event.dict['pos'], Life)
                else:
                    scene.eventClic(event.dict['pos'],event.dict['button'])
            elif event.type == pygame.MOUSEMOTION:
                scene.recordMouseMove(event.dict['pos'])
    pygame.quit()


LifeDensity = 0.5
if not sys.flags.interactive: main(LifeDensity)
