from yta_general_utils.programming.enum import YTAEnum as Enum

import re


class RegularExpression(Enum):
    """
    Enum class to encapsulate useful regular expressions for our system
    and to simplify the way we check those regular expressions with some
    provided parameters.
    """
    FILENAME_WITH_EXTENSION = r'^[\w,\s-]+\.[a-zA-Z0-9]{2,}$'
    """
    Check if the string is a filename with a valid extension (which must
    be a common filename with a dot '.' and at least two
    alphanumeric characters). Something valid would be 'filename.mp3'.
    """

    def check(self, string: str):
        """
        Check this Regular Expression with the provided 'string'. It returns
        True if valid or False if not.
        """
        if not isinstance(string, str):
            raise Exception(f'The provided "string" parameter "{string}" is not a string.')
        
        return bool(re.match(self, string))