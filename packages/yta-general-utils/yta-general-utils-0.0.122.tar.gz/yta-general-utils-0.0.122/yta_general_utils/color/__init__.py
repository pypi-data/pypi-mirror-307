from yta_general_utils.color.utils import is_string_color, is_hexadecimal_color, parse_rgba_color, parse_rgb_color
from yta_general_utils.color.converter import ColorConverter
from yta_general_utils.programming.parameter_validator import PythonValidator
from yta_general_utils.color.enums import ColorString
from typing import Union


class Color:
    """
    Class that represents a color, stored as RGBA, makes
    easy the way we interact with color and provide them as
    parameters and simplify the color conversion. The color
    is stored as a not-normalized color, but values can be
    normalized through the methods that allow it (those 
    including the 'normalized' bool parameter).
    """
    r: int
    """
    Red color, from 0 to 255, where 0 is no value and 255
    is everything.
    """
    g: int
    """
    Green color, from 0 to 255, where 0 is no value and 255
    is everything.
    """
    b: int
    """
    Blue color, from 0 to 255, where 0 is no value and 255
    is everything.
    """
    a: int
    """
    Alpha (transparency), from 0 to 255, where 0 is no
    value and 255 is everything.
    """
    def __init__(self, r, g, b, a):
        self.r, self.g, self.b, self.a = r, g, b, a

    def to_rgb(self, normalized: bool = False):
        if normalized:
            return self.r / 255.0, self.g / 255.0, self.b / 255.0
        
        return self.r, self.g, self.b
    
    def to_rgba(self, normalized:bool = False):
        if normalized:
            return self.r / 255.0, self.g / 255.0, self.b / 255.0, self.a / 255.0
        
        return self.r, self.g, self.b, self.a
    
    def to_hex(self, do_include_alpha: bool = False):
        return ColorConverter.rgba_to_hex(self.to_rgba(), do_include_alpha)
    
    def to_hsl(self):
        return ColorConverter.rgba_to_hsl(self.to_rgba())
    
    def to_cymk(self):
        return ColorConverter.rgba_to_cymk(self.to_rgba())
    
    # TODO: Use the cv2 library to make other changes
    @staticmethod
    def parse(color: Union[list, tuple, str, 'ColorString']):
        """
        Parse the provided 'color' parameter and return the
        color as r,g,b,a values or raises an Exception if it
        is not a valid and parseable color.

        This method accepts string colors (if names are
        registered in our system), hexadecimal colors (than
        can also include alpha value), RGB array or tuples
        (that can be normalized, with float values between
        0.0 and 1.0, or not normalized, with int values
        between 0 and 255), or RGBA array or tuples, similar
        to RGB but including a 4h alpha value.
        """
        string_color = None
        try:
            string_color = ColorString.to_enum(color)
        except:
            pass

        color_array = None
        if string_color is not None:
            color_array = ColorConverter.hex_to_rgba(string_color.value)
        elif PythonValidator.is_string(color) and is_hexadecimal_color(color):
            color_array = ColorConverter.hex_to_rgba(color)
        else:
            try:
                color_array = parse_rgba_color(color)
            except:
                pass

            try:
                color_array = *parse_rgb_color(color), 0
            except:
                pass

            if color_array is None:
                raise Exception(f'The provided "color" parameter is not parseable.')
        
        return Color(*color_array)
