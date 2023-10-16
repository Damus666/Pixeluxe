import pygame, sys
import numpy as np
import math as m
import pixeluxe
#import perlin_numpy

pygame.init()
screen = pygame.display.set_mode((1200,800))
clock = pygame.Clock()

def setup(p: pixeluxe.PixelsType):
    p.rgb = pixeluxe.correct_type(np.random.rand(p.w,p.h)*255)
    
def loop_noise(p: pixeluxe.PixelsType, time):
    p.rgb = pixeluxe.correct_type(np.random.rand(p.w,p.h)*255)
    
#def setup_perlin(p: pixeluxe.PixelsType):
#    p.rgb = (perlin_numpy.generate_fractal_noise_2d((p.w, p.h), (10,10), 1, 1))*255
        
def loop_default(p: pixeluxe.PixelsType, time):
    sin = m.sin(time/500)
    if sin > 0:
        p.r_g_b = [p.x, p.y, (sin+1)/2*255]
    else:
        p.r_g_b = [p.x, (sin+1)/2*255, p.y/2]
    
shader = pixeluxe.PShader(None, loop_noise)
surface = pixeluxe.PSurface(600, shader)
surface.shader_setup()

while True:
    [(pygame.quit(), sys.exit()) for e in pygame.event.get() if e.type == pygame.QUIT]
    
    screen.fill("black")
    
    surface.shader_loop(pygame.time.get_ticks())
    surface.apply_scaled(2)
    rect = surface.output_surface.get_rect(center=(600,400))
    screen.blit(surface.output_surface, rect)
            
    clock.tick(0)
    pygame.display.flip()
    pygame.display.set_caption(f"{clock.get_fps():.0f}")