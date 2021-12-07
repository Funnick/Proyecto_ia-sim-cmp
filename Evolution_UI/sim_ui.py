import time, os, random as rd, pygame, math
from pygame.locals import *
  

class Game:
    def __init__(self, width=1000, height=1000, agents = 30):
        self._agents = [Agent(Coordinate(rd.randint(0, width), rd.randint(0, height))) for _ in range(20)]
        self._width = width
        self._height = height
        
    def neighborhood(self):
        neighbors = 0
        for ag in self._agents:
            pass
        
    def cicle(self):
        for ag in self._agents:
            try_move = ag.move()
            if len(ag._neighborhood) > 0:
                ag._paststate[0] = True
            else: ag._paststate[0] = False
            
            if in_range(try_move, self._width, self._height):
                ag._paststate[1] = Coordinate(ag._pos.X, ag._pos.Y)
                ag._pos.X = try_move[0]
                ag._pos.Y = try_move[1]
                for agn in self._agents:
                    dist = math.sqrt(math.pow(ag._pos.X - agn._pos.X, 2) + math.pow(ag._pos.Y - agn._pos.Y, 2))
                    if dist != 0 and dist <= ag._vision + agn._vision and agn not in ag._neighborhood:
                        ag._neighborhood.append(agn)
                    elif agn in ag._neighborhood: ag._neighborhood.remove(agn)
            ag._paststate[2] = ag._size, ag._vision
            ag.mut()    
    
    def delete(self, surface):
        for ag in self._agents:
            if ag._paststate[0] is not None:
                pygame.draw.circle(surface, (0,100,0), (ag._paststate[1].X, ag._paststate[1].Y), ag._paststate[2][0], 100)
                if ag._paststate[2]:
                    pygame.draw.circle(surface, (0,100,0), (ag._paststate[1].X, ag._paststate[1].Y), ag._paststate[2][1], 2)
    
    def paint(self, surface):
        self.delete(surface)
        for ag in self._agents:
            x = ag._pos.X
            y = ag._pos.Y
            colorB = (ag._size%100,ag._speed%100,ag._vision%100)
            ag._figure = pygame.draw.circle(surface, colorB, (x, y), ag._size, 100)
            if len(ag._neighborhood) > 0:
                pygame.draw.circle(surface, (100,0,100), (x, y), ag._vision, 2)
            
        
class Agent:
    def __init__(self, coord):
        self._age = 0
        self._state = 0
        self._size = 10
        self._pos = coord
        self._vision = 50
        self._speed = 10
        self._paststate = [None, None, None]
        self._neighborhood = []
        self._figure = None
        
    def mut(self):
        var = rd.random()
        if var > 0.8:
            self._size += rd.randint(-2, 2)
            self._vision += rd.randint(-2, 2)
            self._speed += rd.randint(-2, 2)
                
        
    def see(self):
        return
        
    def move(self):
        movement = [1,0,-1]
        next_posX = self._pos.X + self._speed*movement[rd.randint(0, 2)]
        next_posY = self._pos.Y + self._speed*movement[rd.randint(0, 2)]
        return next_posX,next_posY

class Coordinate:
    def __init__(self, x, y):
        self.X = x
        self.Y = y

def in_range(coord, w, h):
    if coord[0] <= w and coord[0] >= 0 and coord[1] <= h and coord[1] >= 0:
        return True
    else: return False

def main(width, height, iterations):
    screen = pygame.display.set_mode((width, height))
    screen.fill((0,100,0))
    pygame.display.set_caption("Evolution")
     
    game = Game(width=width, height=height)     
    clock = pygame.time.Clock()
     
    while iterations:
        clock.tick(30)
         
        game.paint(screen)
        game.cicle()
        time.sleep(0.10)
         
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                break
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                break
         
        pygame.display.flip()
        iterations -= 1
    pygame.quit()
    return game._agents
