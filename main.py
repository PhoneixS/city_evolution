
import numpy as np

# import the pygame module, so you can use it
import pygame
from pygame import surfarray

from motor import Motor


# define a main function
def main(width: int, height: int):

    motor = Motor(width, height)
    motor.inicializa_terreno()
     
    # initialize the pygame module
    pygame.init()
    # load and set the logo
    logo = pygame.image.load("arbolserpiente.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("minimal program")
     
    # create a surface on screen that has the size of 240 x 180
    screen = pygame.display.set_mode((width,height), vsync=1)
     
    # define a variable to control the main loop
    running = True

    surfarray.blit_array(screen, motor.get_terreno())
    pygame.display.flip()
     
    # main loop
    while running:
        
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
        
        motor.procesa()

        surfarray.blit_array(screen, motor.get_terreno())
        pygame.display.flip()



if __name__ == "__main__":

    print("Inciando aplicación")

    width = 1280
    height = 720

    # Ejecutar el juego
    main(width, height)