import numpy as np
from numba import njit, prange

class Motor:

    def __init__(self, width, height):
        self.rg = np.random.default_rng()
        self.width = width
        self.height = height
    
    def inicializa_terreno(self):
        self.terreno = self.rg.integers(low=0, high=255, size=(self.width, self.height))

    def get_terreno(self):
        return self.terreno

    @njit(parallel=True)
    def _procesa(terreno):

        ori = terreno.copy()

        for i in prange(ori.shape[0]):
            for j in prange(ori.shape[1]):
                x = (i+1) % ori.shape[0]
                y = (j+1) % ori.shape[1]
                terreno[i][j] = ori[x][y]

        return terreno
            
    def procesa(self):
        return Motor._procesa(self.terreno)
