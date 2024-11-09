class ColorConverter:
    """
    Class to simplify and encapsulate the functionality related
    to color conversion.
    """
    @staticmethod
    def rgb_to_hex(red, green, blue):
        """
        Returns the provided RGB color as a hex color. The 'red', 'green' and
        'blue' parameters must be between 0 and 255.
        """
        return '#{:02x}{:02x}{:02x}'.format(red, green, blue)