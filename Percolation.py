import sys
import pygame
import pygame.draw
import numpy as np
import matplotlib.pyplot as plt

__screenSize__ = (1530,835)
__cellSize__ = 10
__gridDim__ = tuple(map(lambda x: int(x/__cellSize__), __screenSize__))

# limite réajustée en fonction de la taille de la grille
sys.setrecursionlimit(__gridDim__[0]*__gridDim__[1])

def getColorCell(n):
    if n == 1: #tree
        return (0,255,0)
    elif n == -1: #fire
        return (255,0,0)
    else: #nothing = 0
        return (255, 255, 255)

class Grid:
    """Classe représentant la forêt par une matrice contenant:
    Des arbres (1), du terrain vide (0) et du feu (-1)"""

    _grid= None
    def __init__(self, density):
        ratio = 1 - density
        print("Creating a grid of dimensions " + str(__gridDim__))
        randBase = np.random.random_sample(__gridDim__)
        randBase[randBase < ratio] = 0
        randBase[randBase >= ratio] = 1
        randBase[__gridDim__[0]//2, __gridDim__[1]//2] = -1 #feu sur la case centrale
        self._grid = randBase

        count = 0
        for i in range(__gridDim__[0]):
            for j in range(__gridDim__[1]):
                count += self._grid[i, j] == 1

        self._treeNumber = count

    def addBlockFromMouse(self, coord, w):
        x = int(coord[0] / __cellSize__)
        y = int(coord[1] / __cellSize__)
        self._grid[x,y] = w

    def drawMe(self):
        pass

    def inside(self, i, j):
        return i >= 0 and i < __gridDim__[0] and j >=0 and j < __gridDim__[1]

    def computeState(self, i, j):
        """Calcul l'état suivant d'une case de la matrice"""
        if(self._grid[i, j] == 0):
            return 0
        elif(self._grid[i, j] == -1):
            return 0
        else:
            if(self.inside(i+1, j) and self._grid[i+1, j] == -1):
                return -1
            elif(self.inside(i-1, j) and self._grid[i-1, j] == -1):
                return -1
            elif(self.inside(i, j+1) and self._grid[i, j+1] == -1):
                return -1
            elif(self.inside(i, j-1) and self._grid[i, j-1] == -1):
                return -1
            else:
                return 1


    def computeStep(self):
        """Calcul l'état suivant de l'incendie sur la matrice"""
        nextStep = np.zeros(__gridDim__)
        for i in range(__gridDim__[0]):
            for j in range(__gridDim__[1]):
                nextStep[i,j] = self.computeState(i, j)
        return nextStep

    def converge(self):
        """Fait dérouler l'incendie jusqu'à son terme"""
        isChanging = True
        count = 0
        while(isChanging):
            nextStep = self.computeStep()
            if(np.array_equal(nextStep, self._grid)):
                isChanging = False
            self._grid = nextStep

    def ratio(self):
        """Retourne le taux d'arbres ayant survécus à l'incendie"""
        count = 0
        for i in range(__gridDim__[0]):
            for j in range(__gridDim__[1]):
                count += self._grid[i,j] == 1

        if self._treeNumber == 0:
            return 1
        return count/self._treeNumber


    def recProp(self, i, j):
        """Propagation du feu aux arbres alentours en croix (Nord, Est, Ouest, Sud)"""
        self._grid[i, j] == 0

        if(self.inside(i+1, j) and self._grid[i+1, j] == 1):
            self._grid[i+1, j] = -1
            self.recProp(i+1, j)
        if(self.inside(i-1, j) and self._grid[i-1, j] == 1):
            self._grid[i-1, j] = -1
            self.recProp(i-1, j)
        if(self.inside(i, j+1) and self._grid[i, j+1] == 1):
            self._grid[i, j+1] = -1
            self.recProp(i, j+1)
        if(self.inside(i, j-1) and self._grid[i, j-1] == 1):
            self._grid[i, j-1] = -1
            self.recProp(i, j-1)


    def recSolve(self):
        """Méthode récurrente commençant la propagation du feu au centre.
        Cette méthode accélère le calcul car la matrice n'est parcourue qu'une seule fois.
        La méthode n'est cependant pas utilisable avec l'affichage car le calcul ne se fait pas frame par frame"""
        self.recProp(__gridDim__[0]//2, __gridDim__[1]//2)

    def iterSolve(self):
        """Méthode iterative commençant la propagation du feu au centre.
        Cette méthode accélère le calcul car la matrice n'est parcourue qu'une seule fois.
        Evite la limite de recursion atteinte avec la méthode précédente"""
        stack = []
        stack.append((__gridDim__[0]//2, __gridDim__[1]//2))

        while(stack):
            i, j = stack.pop()

            self._grid[i, j] == 0

            if (self.inside(i + 1, j) and self._grid[i + 1, j] == 1):
                self._grid[i + 1, j] = -1
                stack.append((i + 1, j))
            if (self.inside(i - 1, j) and self._grid[i - 1, j] == 1):
                self._grid[i - 1, j] = -1
                stack.append((i - 1, j))
            if (self.inside(i, j + 1) and self._grid[i, j + 1] == 1):
                self._grid[i, j + 1] = -1
                stack.append((i, j + 1))
            if (self.inside(i, j - 1) and self._grid[i, j - 1] == 1):
                self._grid[i, j - 1] = -1
                stack.append((i, j - 1))


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
        self._grid._grid = self._grid.computeStep()

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
    Tree = 1
    Fire = -1
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
                    scene._grid.addBlockFromMouse(event.dict['pos'], Tree)
                else:
                    scene.eventClic(event.dict['pos'],event.dict['button'])
            elif event.type == pygame.MOUSEMOTION:
                scene.recordMouseMove(event.dict['pos'])
    pygame.quit()


def display(n, rep, steps, results):
    plt.plot(steps, results)
    axes = plt.gca()
    axes.xaxis.set_ticks(np.linspace(0, 1, 11))
    axes.yaxis.set_ticks(np.linspace(0, 1, 11))
    plt.grid(True)
    plt.xlabel('Densité initiale de la forêt')
    plt.ylabel('Densité finale de la forêt')
    plt.title('Evolution de la densité post-incendie de la forêt en fonction de la densité initiale ' + '(' + str(
        n) + ' points, ' + str(rep) + ' répétitions)')
    plt.show()


def plotPercoDumb(n, rep):
    """Affiche un graphique représentant le taux d'arbres ayant
    survécus à l'incendie en fonction de la densité de la forêt au départ.
    Méthode itérative:
    n: nombre de points pour tracer la courbe
    rep: nombre de répétition de l'expérience pour chaque point (moyenne à l'issue)
    """
    steps = np.linspace(0,1,n)
    results = np.zeros(n)
    for k in range(n):
        for i in range(rep):
            print(str(k*rep+i+1) + "/" + str(rep*n))
            perco = Grid(steps[k]) #création de la grille
            perco.converge() #convergence de la methode iterative
            results[k] += perco.ratio()
        results[k] /= rep

    display(n, rep, steps, results)


def plotPercoRec(n, rep):
    """Affiche un graphique représentant le taux d'arbres ayant
    survécus à l'incendie en fonction de la densité de la forêt au départ.
    Méthode récursive:
    n: nombre de points pour tracer la courbe
    rep: nombre de répétition de l'expérience pour chaque point (moyenne à l'issue)
    """
    steps = np.linspace(0,1,n)
    results = np.zeros(n)
    for k in range(n):
        for i in range(rep):
            print(str(k*rep+i+1) + "/" + str(rep*n))
            perco = Grid(steps[k]) #création de la grille
            perco.recSolve() #résolution récursive
            results[k] += perco.ratio()
        results[k] /= rep

    display(n, rep, steps, results)


def plotPercoIter(n, rep):
    """Affiche un graphique représentant le taux d'arbres ayant
    survécus à l'incendie en fonction de la densité de la forêt au départ.
    Méthode itérative finale:
    n: nombre de points pour tracer la courbe
    rep: nombre de répétition de l'expérience pour chaque point (moyenne à l'issue)
    """
    steps = np.linspace(0,1,n)
    results = np.zeros(n)
    for k in range(n):
        for i in range(rep):
            print(str(k*rep+i+1) + "/" + str(rep*n))
            perco = Grid(steps[k]) #création de la grille
            perco.iterSolve() #résolution itérative
            results[k] += perco.ratio()
        results[k] /= rep

    display(n, rep, steps, results)


# Première version du tracé de courbe:
# Ne pas utiliser avec de trop grosses valeurs (Très lent)
# plotPercoDumb(20, 10)

# Version récursive du tracé de courbe
# Beaucoup plus rapide (réajustage de la limite de récursion dans le code)
# plotPercoRec(30, 10)

# Version itérative finale du tracé de courbe
# Aussi rapide que la méthode récursive mais sans le défaut de la limite de récursion
# plotPercoIter(50, 10)

# Pour l'affichage graphique
# (utilise la version itérative pour pouvoir avoir des représentations étape par étape)
density = 0.61 # Réglage de la densité initiale de la forêt
if not sys.flags.interactive: main(density)
