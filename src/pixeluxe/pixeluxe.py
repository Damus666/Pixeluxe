"""Library to abstract numpy vectorized array operations for pygame surfaces to mimic shader code"""
import pygame
import numpy
import typing

__all__ = [
    "R",
    "G",
    "B",
    "ALL",
    "PixeluteError",
    "correct_type",
    "PixelsType",
    "PShader",
    "PSurface"
]

R, G, B, ALL = 0, 1, 2, None


class PixeluteError(Exception):
    ...


def _no_get_error(name: str, oname: str):
    raise PixeluteError(
        f"The pixels attribute '{name}' is meant for assign only, use '{oname}' instead")
    

def correct_type(arr:numpy.ndarray):
    """Convert an array to be of type numpy.uint8 as required by pygame surfaces"""
    return arr.astype(numpy.uint8)


class _PPixels:
    """
    An object containing the surface pixels arrays, the uv arrays and properties to modify the pixels. Don't instantiate manually
    
    Property rules:
        - for r, g, b the slicing works like so: 'array[row, column, 0/1/2]' and can be get and set
        
        - if the property starts with s (f.e. s_rgb) it means it's assigning the value to a slice of the pixels like so: 'array[row, col, :] = value' which doesn't mean it's making all the components the same value and so it needs a particular numpy shaped array
        
        - if the property has underscores in it, when get it returns the needed values as a tuple and when set it assigns to each value a value from a tuple of the user, f.e. 'pixels.r_g_b = [0, 255, 0]' # all green
        
        - if the property has no underscores then it can't be get and when set it assigns to the respective components the same value, f.e. 'pixels.rgb = 255' # all white
    """
    def __init__(self, side:int, pg_surface:pygame.Surface, original: "_PPixels" = None):
        self.size = self.w, self.h = self.width, self.height = side, side
        self.array: numpy.ndarray = pygame.surfarray.array3d(pg_surface)
        """Numpy array containing pixel values of shape (side, side, 3)"""
        if original:
            self.o = self.original = original
            """Contains a copy of the array that will not be modified by this object's properties"""
        self.y = (
            numpy.linspace(0, 255, side * side, endpoint=False, dtype=int)
            .reshape((side, side))
            .transpose()
        )
        """UV coordinates ranging from 0 to 255 along the Y axis in a numpy array of shape (side, side)"""
        self.x = numpy.linspace(0, 255, side * side, endpoint=False, dtype=int).reshape(
            (side, side)
        )
        """UV coordinates ranging from 0 to 255 along the X axis in a numpy array of shape (side, side)"""
        
        self._c = slice(ALL)
        self._r = slice(ALL)

    def slice(self, row=(ALL,), column=(ALL,)):
        """Apply the slices for row and column to the next array assignments and return self"""
        self._r, self._c = slice(*row), slice(*column)
        return self

    # RGB
    @property
    def s_rgb(self): return self.array[self._r, self._c, :]
    @s_rgb.setter
    def s_rgb(self, v): self.array[self._r, self._c, :] = v

    @property
    def r_g_b(self): return (
        self.array[self._c, self._r, R],
        self.array[self._c, self._r, G],
        self.array[self._c, self._r, B]
    )

    @r_g_b.setter
    def r_g_b(self, v):
        self.array[self._c, self._r, R], self.array[self._c,
                                                    self._r, G], self.array[self._c, self._r, B] = v

    @property
    def rgb(self): _no_get_error("rgb", "r_g_b")

    @rgb.setter
    def rgb(self, v):
        self.array[self._c, self._r, R] = self.array[self._c,
                                                     self._r, G] = self.array[self._c, self._r, B] = v

    # RG
    @property
    def s_rg(self): return self.array[self._c, self._r, :B]
    @s_rg.setter
    def s_rg(self, v): self.array[self._c, self._r, :B] = v

    @property
    def r_g(self): return (
        self.array[self._c, self._r, R],
        self.array[self._c, self._r, G]
    )

    @r_g.setter
    def r_g(self, v):
        self.array[self._c, self._r, R], self.array[self._c, self._r, G] = v

    @property
    def rg(self): _no_get_error("rg", "r_g")

    @rg.setter
    def rg(self, v):
        self.array[self._c, self._r, R] = self.array[self._c, self._r, G] = v

    # RB
    @property
    def s_rb(self): return self.array[self._c, self._r, :B]
    @s_rb.setter
    def s_rb(self, v): self.array[self._c, self._r, R::2] = v

    @property
    def r_b(self): return (
        self.array[self._c, self._r, R],
        self.array[self._c, self._r, B]
    )

    @r_b.setter
    def r_b(self, v):
        self.array[self._c, self._r, R], self.array[self._c, self._r, B] = v

    @property
    def rb(self): _no_get_error("rb", "r_b")

    @rb.setter
    def rb(self, v):
        self.array[self._c, self._r, R] = self.array[self._c, self._r, B] = v

    # GB
    @property
    def s_gb(self): return self.array[self._c, self._r, 1::]
    @s_gb.setter
    def s_gb(self, v): self.array[self._c, self._r, 1::] = v

    @property
    def g_b(self): return (
        self.array[self._c, self._r, G],
        self.array[self._c, self._r, B]
    )

    @g_b.setter
    def g_b(self, v):
        self.array[self._c, self._r, G], self.array[self._c, self._r, B] = v

    @property
    def gb(self): _no_get_error("gb", "g_b")

    @gb.setter
    def gb(self, v):
        self.array[self._c, self._r, G] = self.array[self._c, self._r, B] = v

    # R
    @property
    def r(self): return self.array[self._c, self._r, R]
    @r.setter
    def r(self, v): self.array[self._c, self._r, R] = v

    # G
    @property
    def g(self): return self.array[self._c, self._r, G]
    @g.setter
    def g(self, v): self.array[self._c, self._r, G] = v

    # B
    @property
    def b(self): return self.array[self._c, self._r, B]
    @b.setter
    def b(self, v): self.array[self._c, self._r, B] = v


PixelsType = _PPixels
"""Exports _PPixels which should not be instantiated manually"""


class PShader:
    """
    Keeps the reference to two user functions representing the setup shader and the loop shader.
    
    - The setup shader function should accept one parameter which is the pixels object of the PSurface and then any setup uniform
    - The loop shader function should accept the pixels object parameter and any uniform parameters passed to the PSurface
    
    The setup is meant to be called once or very few times to initialize the array pixels while the loop is meant to be called every frame
    """
    def __init__(self, setup_func: typing.Callable[[PixelsType], None]|None, loop_func: typing.Callable[[PixelsType], None]|None):
        self.setup_func, self.loop_func = setup_func, loop_func

    def setup(self, psurf: "PSurface", *setup_uniforms):
        """Call the setup function, if any, passing the pixels object of psurf and the specified setup_uniforms"""
        if self.setup_func is None: return
        self.setup_func(psurf._pixels, *setup_uniforms)

    def loop(self, psurf: "PSurface", *uniforms):
        """Call the loop function, if any, passing the pixels object of psurf and the specified uniforms"""
        if self.loop_func is None: return
        self.loop_func(psurf._pixels, *uniforms)


class PSurface:
    """Object holding a pygame surface, a shader object and a pixels object. The width and the height are the same, to make it a rectangle use the scaling functions"""
    def __init__(self, side:int, shader: PShader):
        self.set_size(side)
        self.set_shader(shader)

    def set_shader(self, shader: PShader):
        """Set the PSurface shader"""
        self.shader: PShader = shader

    def set_size(self, side:int):
        """Set the PSurface size and creates the pixels object"""
        self.size = self.w, self.h = self.width, self.height = side, side
        self.pg_surface: pygame.Surface = pygame.Surface(self.size)
        self.output_surface: pygame.Surface = self.pg_surface
        self._opixels = _PPixels(side, self.pg_surface)
        self._pixels = _PPixels(side, self.pg_surface, self._opixels)

    def shader_setup(self, *setup_uniforms):
        """Call shader.setup passing the setup_uniforms to it"""
        self.shader.setup(self, *setup_uniforms)

    def shader_loop(self, *uniforms):
        """Call shader.loop passing the uniforms to it"""
        self.shader.loop(self, *uniforms)

    def apply_to_surface(self):
        """Blit the pixels array to the pg_surface which is the same as output_surface"""
        pygame.surfarray.blit_array(self.pg_surface, self._pixels.array)
        self.output_surface = self.pg_surface
        
    def apply_sized(self, width: int, height: int):
        """Blit the pixels array to the pg_surface and then scales it into output_surface using width and height"""
        pygame.surfarray.blit_array(self.pg_surface, self._pixels.array)
        self.output_surface = pygame.transform.scale(self.pg_surface, (width, height))
        
    def apply_scaled(self, scale: float | tuple[float, float]):
        """Blit the pixels array to the pg_surface and then scales it into output_surface using a scale factor"""
        pygame.surfarray.blit_array(self.pg_surface, self._pixels.array)
        self.output_surface = pygame.transform.scale_by(self.pg_surface, scale)
