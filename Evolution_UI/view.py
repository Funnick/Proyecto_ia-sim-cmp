import time, os, random as rd, pygame, math, Evolution_Frame.evolution as evo
from pygame.locals import *
  

class View:
    """
    Clase encargada de mostrar en una interfaz visual la simulación en tiempo real.
    """
    def __init__(self, map_=None):
        """
        
        """
        self._width = map_.dimension_x * 80
        self._height = map_.dimesion_y * 80
        self._world = map_
        
    def save_state(self):
        return [obj for obj in self._world]
        
    def neighborhood(self):
        neighbors = 0
        for ag in self._agents:
            pass
        
    def cicle(self, surface):
        self.paint_objects(surface)
    
    
    def paint_objects(self, surface):
        for space in self._world:
            for obj in space:
                x = obj.pos_x + 80
                y = obj.pos_y + 80
                if str(obj) == "Nothing":
                    color = (0,100,0)
                    pygame.draw.rect(surface, color, (x,y, 80,80), 100)
                if str(obj) == "Edge":
                    color = (100,50,50)
                    pygame.draw.rect(surface, color, (x,y, 80,80), 100)
                if str(obj) == "Food":
                    color = (100,0,0)
                    pygame.draw.circle(surface, color, (x, y), 10, 100)
                if str(obj) == "Agent":
                    color = (100,100,obj.sense_gene*5%100)
                    pygame.draw.circle(surface, color, (x, y), 40, 100)

def in_range(coord, w, h):
    if coord[0] <= w and coord[0] >= surface0 and coord[1] <= h and coord[1] >= 0:
        return True
    else: return False

def main(width, height, iterations):
    screen = pygame.display.set_mode((width, height))
    screen.fill((0,100,0))
    pygame.display.set_caption("Evolution")
     
    game = View(width=width, height=height)     
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
