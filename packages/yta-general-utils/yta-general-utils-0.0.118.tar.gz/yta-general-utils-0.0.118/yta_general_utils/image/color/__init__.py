from yta_general_utils.programming.regular_expressions import RegularExpression
from yta_general_utils.programming.parameter_validator import PythonValidator
from yta_general_utils.programming.enum import YTAEnum as Enum
from typing import Union


class ColorRegularExpression(RegularExpression):
    HEX = r'^(#|0x|0X)[0-9a-fA-F]{6,8}$'
    """
    Accepts colors with or without alpha, that include the
    '#', '0x' or '0X' begining.
    """

class ColorString(Enum):
    WHITE = '#FFFFFF'
    BLACK = '#000000'
    RED = '#FF000000'
    GREEN = '#00FF00'
    BLUE = '#0000FF'
    # TODO: Add colors from Manim or other libraries

class Color:
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

    def normalized(self):
        """
        Returns the color as 4 elements (r, g, b, a) as
        normalized values (from 0 to 1).
        """
        return self.r / 255.0, self.g / 255.0, self.b / 255.0, self.a / 255.0
    
    def to_rgb(self):
        return self.r, self.g, self.b
    
    def to_rgba(self):
        return self.to_rgb(), self.a
    
    def to_hex(self, do_include_alpha: bool = False):
        return rgba_to_hex(self.to_rgba(), do_include_alpha)
    
    def to_hsl(self):
        return rgba_to_hsl(self.to_rgba())
    
    def to_cymk(self):
        return rgba_to_cymk(self.to_rgba())
    
    # TODO: Use the cv2 library to make other changes

    @staticmethod
    def parse(color):
        return ColorParser.parse(color)

class ColorParser:
    @staticmethod
    def parse(color):
        """
        Parse the provided 'color' parameter and return the
        color as r,g,b,a values or raises an Exception if it
        is not a valid and parseable color.
        """
        string_color = is_string_color(color)
        if is_hexadecimal_color(color):
            return hex_to_rgba(color)
        elif string_color:
            return ColorParser.parse(string_color.value)
        else:
            try:
                return parse_rgba_color(color)
            except:
                pass

            try:
                return *parse_rgb_color(color), 0
            except:
                pass

            raise Exception(f'The provided "color" parameter is not parseable.')
        
    @staticmethod
    def to_color(color):
        """
        Parse the provided 'color' and turn it into a Color
        class instance.
        """
        return Color(ColorParser.parse(color))

def hex_to_rgb(color: str):
    """
    Parse the provided hexadecimal 'color' parameter and
    turn it into an RGB color (returned as r,g,b) or
    raises an Exception if not.
    """
    r, g, b, _ = hex_to_rgba(color)

    return r, g, b

def hex_to_rgba(color: str):
    if not is_hexadecimal_color(color):
        raise Exception(f'The provided "color" parameter "{str(color)}" is not an hexadecimal color.')
    
    # Hex can start with '0x', '0X' or '#'
    hex = color.lstrip('#').lstrip('0x').lstrip('0X')
    if len(hex) == 6:
        # hex without alpha
        r, g, b, a = (int(hex[i:i+2], 16) for i in (0, 2, 4)), 0
    elif len(hex) == 8:
        # hex with alpha
        r, g, b, a = (int(hex[i:i+2], 16) for i in (0, 2, 4, 6))
    
    return r, g, b, a

def rgb_to_hex(color: Union[tuple, list], do_include_alpha: bool = False):
    """
    Parse the provided RGB 'color' parameter and turn it to
    a hexadecimal color if valid or raises an Exception if
    not. The result will be #RRGGBB if 'do_include_alpha' is
    False, or #RRGGBBAA if 'do_include_alpha' is True.
    """
    r, g, b = parse_rgb_color(color)

    hex = "#{:02x}{:02x}{:02x}".format(r, g, b)
    if do_include_alpha:
        hex = "#{:02x}{:02x}{:02x}{:02x}".format(r, g, b, 0)

    return hex
    
def rgba_to_hex(color: Union[tuple, list], do_include_alpha: bool = False):
    """
    Parse the provided RGBA 'color' parameter and turn it to
    a hexadecimal color if valid or raises an Exception if
    not. The result will be #RRGGBB if 'do_include_alpha' is
    False, or #RRGGBBAA if 'do_include_alpha' is True.
    """
    r, g, b, a = parse_rgba_color(color)

    hex = "#{:02x}{:02x}{:02x}".format(r, g, b)
    if do_include_alpha:
        hex = "#{:02x}{:02x}{:02x}{:02x}".format(r, g, b, a)

    return hex

def rgba_to_hsl(color: Union[tuple, list]):
    _, _, _, a = parse_rgba_color(color)
    
    return *rgb_to_hsl(color), a

def rgb_to_hsl(color: Union[tuple, list]):
    r, g, b = parse_rgb_color(color)
    # Normalizamos los valores de r, g, b de 0-255 a 0-1
    r /= 255.0
    g /= 255.0
    b /= 255.0
    
    # Encuentra los valores máximos y mínimos de los componentes RGB
    cmax = max(r, g, b)
    cmin = min(r, g, b)
    delta = cmax - cmin

    # Calcular el tono (H)
    if delta == 0:
        h = 0  # Si no hay diferencia, el tono es indefinido (gris)
    elif cmax == r:
        h = (60 * ((g - b) / delta) + 360) % 360
    elif cmax == g:
        h = (60 * ((b - r) / delta) + 120) % 360
    else:  # cmax == b
        h = (60 * ((r - g) / delta) + 240) % 360
    
    # Calcular la luminosidad (L)
    l = (cmax + cmin) / 2
    
    # Calcular la saturación (S)
    if delta == 0:
        s = 0  # Si no hay diferencia, la saturación es 0 (gris)
    else:
        s = delta / (1 - abs(2 * l - 1)) if l != 0 and l != 1 else delta / (2 - (cmax + cmin))

    return round(h, 2), round(s * 100, 2), round(l * 100, 2)

def rgba_to_cymk(color: Union[tuple, list]):
    # TODO: Is there a way to handle alpha transparency
    # with a cymk (?)
    return rgb_to_cymk(color)

def rgb_to_cymk(color: Union[tuple, list]):
    r, g, b = parse_rgb_color(color)
    r, g, b = r / 255.0, g / 255.0, b / 255.0

    k = 1 - max(r, g, b)

    if k == 1:
        c = m = y = 0
    else:
        c = (1 - r - k) / (1 - k)
        m = (1 - g - k) / (1 - k)
        y = (1 - b - k) / (1 - k)

    return round(c * 100, 2), round(m * 100, 2), round(y * 100, 2), round(k * 100, 2)

def parse_rgb_color(color):
    """
    Parse the provided 'color' as RGB and returns it as
    r,g,b values.
    """
    if is_array_or_tuple_without_alpha_normalized(color):
        return color[0] * 255, color[1] * 255, color[2] * 255
    elif is_array_or_tuple_without_alpha(color):
        return color[0], color[1], color[2]
    else:
        raise Exception(f'The provided "color" parameter is not an RGB color.')

def parse_rgba_color(color):
    """
    Parse the provided 'color' as RGBA and returns it as
    r,g,b,a values.
    """
    if is_array_or_tuple_with_alpha(color):
        return color[0], color[1], color[2], color[3]
    elif is_array_or_tuple_with_alpha_normalized(color):
        return color[0] * 255, color[1] * 255, color[2] * 255, color[3] * 255
    else:
        raise Exception(f'The provided "color" parameter is not an RGBA color.')

def is_hexadecimal_color(color):
    """
    Check that the 'color' parameter is an hexadecimal
    color.
    """
    return ColorRegularExpression.HEX.check(color)

def is_string_color(color):
    """
    Check that the 'color' parameter is an string 
    color accepted by our system, whose value is an
    hexadecimal value.
    """
    return ColorString.to_enum(color)

def is_array_or_tuple_without_alpha_normalized(color):
    """
    Check that the 'color' parameter is an array or a
    tuple of 3 elements that are float values between
    0 and 1 (normalized value).
    """
    return is_array_or_tuple_without_alpha and all(PythonValidator.is_instance(c, float) and 0 <= c <= 1 for c in color)

def is_array_or_tuple_with_alpha_normalized(color):
    """
    Check that the 'color' parameter is an array or a
    tuple of 4 elements that are float values between
    0 and 1 (normalized value).
    """
    return is_array_or_tuple_with_alpha and all(PythonValidator.is_instance(c, float) and 0 <= c <= 1 for c in color)

def is_array_or_tuple_without_alpha(color):
    """
    Check that the 'color' parameter is an array or a
    tuple of 3 elements that are int values between 0
    and 255.
    """
    return PythonValidator.is_instance(color, tuple) or PythonValidator.is_instance(color, list) and len(color) == 3 and all(PythonValidator.is_instance(c, int) and 0 <= c <= 255 for c in color)

def is_array_or_tuple_with_alpha(color):
    """
    Check that the 'color' parameter is an array or a
    tuple of 4 elements that are int values between 0
    and 255.
    """
    return PythonValidator.is_instance(color, tuple) or PythonValidator.is_instance(color, list) and len(color) == 4 and all(PythonValidator.is_instance(c, int) and 0 <= c <= 255 for c in color)
