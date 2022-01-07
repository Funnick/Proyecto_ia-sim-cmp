import time, os, random as rd, pygame, math, Evolution_Frame.evolution as evo
from pygame.locals import *
  

class View:
    """
    Clase encargada de mostrar en una interfaz visual la simulación en tiempo real.
    """
    def __init__(self, map_=None):
        """
        
        """
        self._width = (map_.dimension_x) * 40
        self._heigth = (map_.dimension_y) * 40
        self._world = map_
        self._screen = None
        self._days = 0
        
    def save_state(self):
        return [obj for obj in self._world]
        
    def neighborhood(self):
        neighbors = 0
        for ag in self._agents:
            pass
        
    def cicle(self, surface):
        self.paint_objects(surface)
    
    
    def paint_objects(self, surface):
        for space_x in self._world.map:
            for space_y in space_x:
                for obj in space_y:
                    x = obj.pos_x * 40
                    y = obj.pos_y * 40
                    if str(obj) == "Nothing":
                        color = (0,80,0)
                        pygame.draw.rect(surface, color, [x,y, 40,40], 0)
                    elif str(obj) == "Edge":
                        color = (100,50,50)
                        pygame.draw.rect(surface, color, [x,y, 40,40], 0)
                    elif str(obj) == "Food":
                        color = (100,0,0)
                        pygame.draw.circle(surface, color, [x+20, y+20], 5, 0)
                    elif str(obj) == "Agent":
                        color = (0,80,80)
                        pygame.draw.circle(surface, color, [x+20, y+20], 20, 0)
    def start_simulation(self, days):
        self._screen = pygame.display.set_mode((self._width, self._heigth))
        self._screen.fill((0,80,0))
        pygame.display.set_caption("Evolution")
        self._days = days
    
    def update_map(self, new_world):
        self._world = new_world
    
    def simulate_one_agent(self, agent):
        agent
    
    def simulate_one_round(self):
        clock = pygame.time.Clock()
        clock.tick(50)
        time.sleep(0.20)
        self.paint_objects(self._screen)
        
        pygame.display.flip()
        self._days -= 1
        if self._days == 0:
            pygame.quit()
            