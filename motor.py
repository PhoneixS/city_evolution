from datetime import datetime, timedelta
import numpy as np
from numba import njit, prange
import pygame
from pygame import Surface

from modelo import Dibujable, Procesable, Terreno

class Motor:

    def __init__(self, width, height):
        self.rg = np.random.default_rng()
        self.width = width
        self.height = height
        self.zoom = 7
        self.desplazamiento = [0, 0]
        self.desp_inc = [0, 0]

        self.procesables: list[Procesable] = []
        self.dibujables: list[Dibujable] = []

        self.fecha_actual: datetime = datetime(1, 1, 1)
    
    def inicializa_terreno(self):
        self.terreno = self.rg.integers(low=0, high=255, size=(self.width, self.height))

    def get_terreno(self):
        return self.terreno
    
    def generar_terreno_vacio(self) -> np.ndarray:
        return np.zeros((self.width, self.height))

    @njit(parallel=True)
    def _procesa(terreno):

        ori = terreno.copy()

        for i in prange(ori.shape[0]):
            for j in prange(ori.shape[1]):
                x = (i+1) % ori.shape[0]
                y = (j+1) % ori.shape[1]
                terreno[i][j] = ori[x][y]

        return terreno
            
    def procesa(self, time: timedelta):

        self.procesa_teclas_continuas()

        self.desplazamiento[0] += self.desp_inc[0]
        self.desplazamiento[1] += self.desp_inc[1]

        superficie = Motor._procesa(self.terreno)

        self.fecha_actual += time

        for procesable in self.procesables:
            procesable.procesa(time, self)
        return superficie
    
    def dibuja(self, pantalla: Surface) -> None:
        for dibujable in self.dibujables:
            dibujable.dibuja(pantalla, self.zoom, self.desplazamiento)

    def on_event(self, event) -> None:

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_KP_PLUS or event.key == pygame.K_PLUS:
                self.zoom += 1
            if event.key == pygame.K_KP_MINUS or event.key == pygame.K_MINUS:
                self.zoom -= 1
                if self.zoom < 1:
                    self.zoom = 1

    def procesa_teclas_continuas(self) -> None:
    
        teclas = pygame.key.get_pressed()
    
        if teclas[pygame.K_RIGHT] and not teclas[pygame.K_LEFT]:
            self.desp_inc[0] = -5
        elif teclas[pygame.K_LEFT] and not teclas[pygame.K_RIGHT]:
            self.desp_inc[0] = 5
        else:
            self.desp_inc[0] = 0

        if teclas[pygame.K_UP] and not teclas[pygame.K_DOWN]:
            self.desp_inc[1] = 5
        elif teclas[pygame.K_DOWN] and not teclas[pygame.K_UP]:
            self.desp_inc[1] = -5
        else:
            self.desp_inc[1] = 0
        
        
        