"""Este módulo contiene la diferente funcionalidad para los edificios"""

from datetime import datetime, timedelta
import random
from typing import Optional

import numpy as np
from numpy import ndarray
from pygame import Color, Surface, draw

from shapely.geometry import Polygon

from motor import Motor

class Procesable:

    def procesa(self, time: timedelta, motor: Motor) -> None:
        pass

class Dibujable:

    def dibuja(self, pantalla: Surface, zoom: int, desplazamiento: list) -> None:
        pass

class Persona(Procesable):

    def __init__(self, nacimiento: datetime) -> None:
        self.nacimiento = nacimiento
        self.edad: timedelta = timedelta()
        self.vivo: bool = True
        self.casa: Terreno = None
    
    def procesa(self, time: timedelta, motor: Motor):
        self.edad = self.edad + time

        if not self.casa:
            # Si no tiene casa, intentará comprar una
            motor.obten_terreno()
    



class Posesion(Procesable):

    def __init__(self, owner: Persona = None) -> None:
        self.owner = owner

class Terreno(Posesion, Dibujable):
    
    def __init__(self, perimetro: ndarray, owner: Persona = None) -> None:
        super().__init__(owner)
        if perimetro.shape[1] != 2:
            raise Exception
        self.perimetro: ndarray = perimetro
        self._area: Optional[float] = None
        self.color: Color = Color(0)
        self.color.hsla = (random.randint(0, 360), random.randint(50, 100), random.randint(25, 75), 100)
        self.color_texto: Color = Color(self.color)
        self.color_texto.hsla = ((self.color_texto.hsla[0] + 180) % 360, self.color_texto.hsla[1], self.color_texto.hsla[2], self.color_texto.hsla[3])
    
    @property
    def area(self) -> float:
        """
        Calcula el área del terreno.

        Calcula el área usando las coordenadas del perímetro mediante la formula Shoelace
        según viene indicado en https://stackoverflow.com/questions/24467972/calculate-area-of-polygon-given-x-y-coordinates
        """

        if self._area:
            return self._area
        
        x, y = self.perimetro.swapaxes(0,1)
        self._area = 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))

        return self._area
    
    @property
    def area(self) -> ndarray:
        return self._area

    def procesa(self, time: timedelta) -> None:
        pass
    
    def dibuja(self, pantalla: Surface, zoom: int, desplazamiento: list) -> None:
        draw.polygon(pantalla, self.color, (self.perimetro) * zoom + desplazamiento)
        myfont = pygame.font.Font(None, zoom*2)
        # TODO Poner un color que contraste
        label = myfont.render(f"Area: {self.area}", 1, self.color_texto)
        label_center = label.get_rect(center=(self.centro()) * zoom + desplazamiento)
        pantalla.blit(label, label_center)
    
    def centro(self) -> ndarray:
        return (np.max(self.perimetro, 0) - np.min(self.perimetro, 0)) / 2 + np.min(self.perimetro, 0)
