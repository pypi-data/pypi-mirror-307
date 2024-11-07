from typing import Union

import inspect


def variable_is_type(variable, type):
    """
    Checks if the type of the provided 'variable' is the also provided
    'type', returning True if yes or False if not.
    """
    # TODO: Maybe let this accept array of types to check if one of 
    # them (?)
    # Check this to validate 'type' is array to treat it like an array:
    # https://stackoverflow.com/a/16807050
    if isinstance(variable, type):
        return True
    
    return False

def variable_is_number(variable: Union[int, float, str]):
    """
    This method checks if the provided 'variable' is a numeric type,
    or tries to cast it as a float number if string provided, and
    returns True in the only case that the 'variable' is actual a
    number by itself or as a string.
    """
    if not isinstance(variable, (int, float, str)):
        return False
    
    if isinstance(variable, str):
        try:
            float(variable)
        except:
            return False
        
    return True

def variable_is_positive_number(variable: Union[int, float, str], do_include_zero = True):
    """
    This method checks if the provided 'variable' is a numeric type,
    or tries to cast it as a float number if string provided, and
    returns True in the only case that the 'variable' is actual a
    number by itself or as a string and it is 0 or above it. If 
    'do_include_zero' is set to False it won't be included.
    """        
    if not variable_is_number(variable):
        return False
        
    variable = float(variable)

    if do_include_zero:
        return variable >= 0

    return variable > 0

def variable_is_number_between(variable: Union[int, float, str], lower_limit: Union[int, float, str], upper_limit: Union[int, float, str], do_include_lower_limit: bool = True, do_include_upper_limit: bool = True):
    """
    This methods returns True if the provided 'variable' is a valid number
    that is between the also provided 'lower_limit' and 'upper_limit'. It
    will return False in any other case.
    """
    if not variable_is_number(variable):
        return False

    if not variable_is_number(lower_limit) or not variable_is_number(upper_limit):
        return False
    
    # if upper_limit < lower_limit:
    #     raise Exception(f'The provided "upper_limit" parameter {str(upper_limit)} is lower than the "lower_limit" parameter {str(lower_limit)} provided.')

    if do_include_lower_limit and do_include_upper_limit:
        return float(lower_limit) <= float(variable) <= float(upper_limit)
    elif do_include_lower_limit:
        return float(lower_limit) <= float(variable) < float(upper_limit)
    elif do_include_upper_limit:
        return float(lower_limit) < float(variable) <= float(upper_limit)
    else:
        return float(lower_limit) < float(variable) < float(upper_limit)

def code_file_is(parameter, filename):
    """
    Checks if the provided parameter code is contained in the also
    provided 'filename'. This method is useful to check Enum objects
    or classes as we know the name we use for the files.

    This method was created to be able to check if a function that
    was passed as parameter was part of a custom Enum we created
    and so we could validate the was actually that custom Enum.
    Working with classes was not returning the custom Enum class
    created, so we needed this.
    """
    if inspect.getfile(parameter).endswith(filename):
        return True
    
    return False

def is_class(parameter, class_names: Union[str, list[str]]):
    """
    Checks if the provided 'parameter' is of one of the also provided
    'class_names'.
    """
    # TODO: Improve this checking and transforming
    if isinstance(class_names, str):
        class_names = [class_names]

    return type(parameter).__name__ in class_names