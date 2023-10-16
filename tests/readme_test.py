# You'll most likely need this
import pygame, sys
import pixeluxe
import numpy as np
import math as m

# pygame simple setup
pygame.init()
screen = pygame.display.set_mode((1200,800)) 
clock = pygame.Clock()

# First, define your shader functions

# This is meant to run once or few times, to initialize the pixels values. Custom setup uniforms are allowed
def shader_hello_world_setup(pixels: pixeluxe.PixelsType):
    # Use the pixels property to make a common shader 'Hello World'. Use the PixelsType's docstring to know more about those properties
    # This will be overridden by shader_hello_world_loop, this is just an example
    pixels.r_g_b = [pixels.x, pixels.y, 255]


# Here are 2 functions that should be called every frame, one of them needs a 'time' uniform. 
def shader_noise_loop(pixels: pixeluxe.PixelsType):
    pixels.rgb = pixeluxe.correct_type(np.random.rand(pixels.w,pixels.h)*255)

def shader_hello_world_loop(pixels: pixeluxe.PixelsType, time):
    sin = m.sin(time/500)
    if sin > 0:
        pixels.r_g_b = [pixels.x, pixels.y, (sin+1)/2*255]
    else:
        pixels.r_g_b = [pixels.x, (sin+1)/2*255, pixels.y/2]


# Use those functions to make 2 shaders:
hello_world_shader = pixeluxe.PShader(shader_hello_world_setup, shader_hello_world_loop)
noise_shader = pixeluxe.PShader(None, shader_noise_loop)

# Now let's create 2 surfaces that will use those shaders. Only one dimention is needed as the shaders only work for quads. Use the scaling functions for rectangles
hello_world_surf = pixeluxe.PSurface(400, hello_world_shader)
noise_surf = pixeluxe.PSurface(400, noise_shader)

# Setup should be called after the surface is created
hello_world_surf.shader_setup()

while True:
    [(pygame.quit(), sys.exit()) for e in pygame.event.get() if e.type == pygame.QUIT]
    
    screen.fill("black")
    
    # Call the shader loops on this surface to apply them, passing the correct uniforms
    hello_world_surf.shader_loop(pygame.time.get_ticks())
    noise_surf.shader_loop()
    
    # Tell the PSurface to blit the array onto the output surface. use apply_sized and apply_scaled to change the output surface size
    # We are also making rects for blitting
    hello_world_surf.apply_to_surface()
    rect = hello_world_surf.output_surface.get_rect(midright=(600,400))
    noise_surf.apply_to_surface()
    rect2 = noise_surf.output_surface.get_rect(midleft=(600,400))
    
    # Blit the surface output_surface onto the screen and watch the result!
    screen.blit(hello_world_surf.output_surface, rect)
    screen.blit(noise_surf.output_surface, rect2)
    
    clock.tick(0)
    pygame.display.flip()
    # Let's check our performance
    pygame.display.set_caption(f"{clock.get_fps():.0f}")