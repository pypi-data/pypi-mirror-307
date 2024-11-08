from yta_general_utils.programming.error_message import ErrorMessage
# from yta_general_utils.file.filename import filename_is_type
# from yta_general_utils.checker.type import variable_is_positive_number
# from yta_general_utils.file.checker import file_exists
# from yta_general_utils.checker.url import url_is_ok
from enum import Enum
from typing import Union

import numpy as np


# TODO: Remove commented methods in PythonValidator for the next version
class PythonValidator:
    """
    Class to simplify and encapsulate the functionality related with
    parameters and variables validation.

    This class has been created to simplify the way it work and 
    replace the old ParameterValidator that was using too many 
    different methods being imported and generating cyclic import
    issues.

    We have some equivalent methods that do not need to pass the class
    as a parameter, so we can only work with the class name and avoid
    imports that can cause issues.
    """
    @staticmethod
    def is_instance(element, cls: Union[str, type]):
        """
        Check if the provided 'element' is an instance of the provided
        class 'cls'. An instance is not the same as a class. The 'cls'
        parameter can be the class or the string name of that class. 

        You can pass the string name of the class to avoid import in 
        the file where you are calling this method.
        """
        # TODO: Convert this to accept cls as array and check 
        # diferent classes
        if not PythonValidator.is_string(cls) and not PythonValidator.is_a_class(cls):
            raise Exception(f'The provided "cls" parameter "{str(cls)}" is not a string nor a class.')
        
        if PythonValidator.is_a_class(cls):
            return isinstance(element, cls)
        else:
            if PythonValidator.is_a_class(element):
                return False
        
            return getattr(type(element), '__name__', None) is cls
    
    @staticmethod
    def is_an_instance(element):
        """
        Check if the provided 'element' is an instance of any class.
        """
        return isinstance(element, object)
        # This below is just another alternative I want to keep
        return getattr(element, '__name__', None) is None
    
    @staticmethod
    def is_class(element, cls: Union[str, type]):
        """
        Check if the provided 'element' is the provided class 'cls'.
        A class is not the same as an instance of that class. The
        'cls' parameter can be the class or the string name of that
        class. 

        You can pass the string name of the class to avoid import in 
        the file where you are calling this method.
        """
        # TODO: Convert this to accept cls as array and check 
        # diferent classes
        if not PythonValidator.is_string(cls) and not PythonValidator.is_a_class(cls):
            raise Exception(f'The provided "cls" parameter "{str(cls)}" is not a string nor a class.')
        
        if PythonValidator.is_string(cls):
            return getattr(element, '__name__', None) is cls
        else:
            return PythonValidator.is_a_class(element) and element == cls

    @staticmethod
    def is_a_class(element):
        """
        Check if the provided 'element' is a class.
        """
        return isinstance(element, type)
        # This below is just another alternative I want to keep
        return getattr(element, '__name__', None) is not None
    
    @staticmethod
    def is_subclass(element: type, cls: Union[str, type]):
        """
        Check if the provided 'element' is a subclass of the provided
        class 'cls'. The 'cls' parameter can be the class or the
        string name of that class.

        You can pass the string name of the class to avoid import in 
        the file where you are calling this method.

        This method can return True if the provided 'element' is an
        instance or a class that inherits from Enum or YTAEnum class.
        Consider this above to check later if your 'element' is an
        instance or a class.
        """
        # TODO: Convert this to accept cls as array and check 
        # diferent classes
        if not PythonValidator.is_string(cls) and not PythonValidator.is_a_class(cls):
            raise Exception(f'The provided "cls" parameter "{str(cls)}" is not a string nor a class.')
        
        if not PythonValidator.is_a_class(element):
            # We want to know if it is a subclass, we don't
            # care if the provided one is an instance or a class,
            # so we try with both.
            if PythonValidator.is_an_instance(element):
                element = type(element)
            else:
                return False
            
        if PythonValidator.is_string(cls):
            return cls in [base_class.__name__ for base_class in element.__bases__]
        else: 
            issubclass(element, cls)
    
    @staticmethod
    def is_list(element):
        """
        Check if the provided 'element' is a list.
        """
        return type(element) == list
    
    @staticmethod
    def is_string(element):
        """
        Check if the provided 'element' is a string (str).
        """
        return isinstance(element, str)
    
    @staticmethod
    def is_boolean(element):
        """
        Check if the provided 'element' is a boolean (bool).
        """
        return isinstance(element, bool)
    
    @staticmethod
    def is_number(element, do_accept_string_number: bool = False):
        """
        Check if the provided 'element' is a numeric value. If
        'do_accept_string_number' is True, it will try to parse
        the 'element' as a float if a string is provided.
        """
        return NumberValidator.is_number(element, do_accept_string_number)

    @staticmethod
    def is_numpy_array(element):
        """
        Check if the provided 'element' is an instance of the
        numpy array np.ndarray.
        """
        return PythonValidator.is_instance(element, np.ndarray)
    
    @staticmethod
    def is_enum(element: Union['YTAEnum', Enum]):
        """
        Check if the provided 'element' is a subclass of an Enum or
        a YTAEnum.

        This method can return True if the provided 'element' is an
        instance or a class that inherits from Enum or YTAEnum class.
        Consider this above to check later if your 'element' is an
        instance or a class.
        """
        # TODO: I think it is 'EnumMeta' not Enum
        return PythonValidator.is_subclass(element, 'YTAEnum') or PythonValidator.is_subclass(element, 'Enum')
    
    @staticmethod
    def is_enum_instance(element: Union['YTAEnum', Enum]):
        """
        Check if the provided 'element' is a Enum (it is a subclass
        of an Enum or a YTAEnum) and it is an instance.
        """
        return PythonValidator.is_enum(element) and PythonValidator.is_an_instance(element)
    
    @staticmethod
    def is_enum_class(element: Union['YTAEnum', Enum]):
        """
        Check if the provided 'element' is a Enum (it is a subclass
        of an Enum or a YTAEnum) and it is a class.
        """
        return PythonValidator.is_enum(element) and PythonValidator.is_a_class(element)

class NumberValidator:
    """
    Class to simplify and encapsulate the functionality related
    to validate numeric values.
    """
    @staticmethod
    def is_number(element: Union[int, float, str], do_accept_string_number: bool = False):
        """
        Check if the provided 'element' is a numeric value. If
        'do_accept_string_number' is True, it will try to parse
        the 'element' as a float if a string is provided.
        """
        if not PythonValidator.is_instance(element, int) and not PythonValidator.is_instance(element, float) and not PythonValidator.is_instance(element, str):
            return False
        
        if PythonValidator.is_instance(element, str):
            if do_accept_string_number:
                try:
                    float(element)
                except:
                    return False
            else:
                return False
            
        return True
    
    @staticmethod
    def is_positive_number(element: Union[int, float, str], do_include_zero: bool = True):
        """
        This method checks if the provided 'element' is a numeric type,
        or tries to cast it as a float number if string provided, and
        returns True in the only case that the 'element' is actual a
        number by itself or as a string and it is 0 or above it. If 
        'do_include_zero' is set to False it won't be included.
        """        
        if not NumberValidator.is_number(element):
            return False
            
        variable = float(variable)

        if do_include_zero:
            return variable >= 0

        return variable > 0
    
    @staticmethod
    def is_number_between(element: Union[int, float, str], lower_limit: Union[int, float, str], upper_limit: Union[int, float, str], do_include_lower_limit: bool = True, do_include_upper_limit: bool = True):
        """
        This methods returns True if the provided 'variable' is a valid number
        that is between the also provided 'lower_limit' and 'upper_limit'. It
        will return False in any other case.
        """
        if not NumberValidator.is_number(element, True):
            return False
        
        if not NumberValidator.is_number(lower_limit) or not NumberValidator.is_number(upper_limit):
            return False
        
        element = float(element)
        lower_limit = float(lower_limit)
        upper_limit = float(upper_limit)
        
        # TODO: Should we switch limits if unordered (?)
        # if upper_limit < lower_limit:
        #     raise Exception(f'The provided "upper_limit" parameter {str(upper_limit)} is lower than the "lower_limit" parameter {str(lower_limit)} provided.')

        if do_include_lower_limit and do_include_upper_limit:
            return lower_limit <= element <= upper_limit
        elif do_include_lower_limit:
            return lower_limit <= element < upper_limit
        elif do_include_upper_limit:
            return lower_limit < element <= upper_limit
        else:
            return lower_limit < element < upper_limit
    
class ParameterValidator:
    @staticmethod
    def validate_mandatory_parameter(name: str, value):
        """
        Validates if the provided 'value' parameter with the also
        provided 'name' has a value, raising an Exception if not.

        This method returns the provided 'value' if everything is
        ok.
        """
        if not value:
            raise Exception(ErrorMessage.parameter_not_provided(name))

        return value

    @staticmethod
    def validate_string_parameter(name: str, value):
        """
        Validates if the provided 'value' parameter with the also
        provided 'name' is a string value, raising an Exception if
        not.

        This method returns the provided 'value' if everything is
        ok.
        """
        if not PythonValidator.is_string(value):
            raise Exception(ErrorMessage.parameter_is_not_string(name))

        return value
    
    @staticmethod
    def validate_bool_parameter(name: str, value: bool):
        """
        Validates if the provided 'value' parameter with the also
        provided 'name' is a boolean value, raising and Exception 
        if not.

        This method returns the provided 'value' if everything is
        ok.
        """
        if not PythonValidator.is_boolean(value):
            raise Exception(ErrorMessage.parameter_is_not_boolean(name))

        return value
    
# class ParameterValidator:
#     @classmethod
#     def validate_mandatory_parameter(cls, name: str, value):
#         """
#         Validates if the provided 'value' parameter with the also
#         provided 'name' has a value, raising an Exception if not.

#         This method returns the provided 'value' if everything is
#         ok.
#         """
#         if not value:
#             raise Exception(ErrorMessage.parameter_not_provided(name))

#         return value
        
#     @classmethod
#     def validate_string_parameter(cls, name: str, value: str):
#         """
#         Validates if the provided 'value' parameter with the also
#         provided 'name' is a string value, raising an Exception if
#         not.

#         This method returns the provided 'value' if everything is
#         ok.
#         """
#         if not isinstance(value, str):
#             raise Exception(ErrorMessage.parameter_is_not_string(name))

#         return value

#     @classmethod
#     def validate_bool_parameter(cls, name: str, value: bool):
#         """
#         Validates if the provided 'value' parameter with the also
#         provided 'name' is a boolean value, raising and Exception 
#         if not.

#         This method returns the provided 'value' if everything is
#         ok.
#         """
#         if not isinstance(value, bool):
#             raise Exception(ErrorMessage.parameter_is_not_boolean(name))

#         return value
        
#     @classmethod
#     def validate_file_exists(cls, name: str, value: str):
#         """
#         Validates if the provided 'value' parameter with the also
#         provided 'name' is a file that actually exists, raising
#         an Exception if not.

#         This method returns the provided 'value' if everything is
#         ok.
#         """
#         if not file_exists(value):
#             raise Exception(ErrorMessage.parameter_is_file_that_doesnt_exist(name))

#         return value
        
#     @classmethod
#     def validate_filename_is_type(cls, name: str, value: str, file_type: 'FileType'):
#         """
#         Validates if the provided 'value' parameter with the also
#         provided 'name' is a filename of the given 'file_type',
#         raising an Exception if not.

#         This method returns the provided 'value' if everything is
#         ok.
#         """
#         if not filename_is_type(value, file_type):
#             raise Exception(ErrorMessage.parameter_is_not_file_of_file_type(name, file_type))

#         return value
        
#     @classmethod
#     def validate_url_is_ok(cls, name: str, value: str):
#         """
#         Validates if the provided 'value' parameter with the also
#         provided 'name' is a valid url (the url is accessible),
#         raising an Exception if not.

#         This method returns the provided 'value' if everything is
#         ok.
#         """
#         if not url_is_ok(value):
#             raise Exception(ErrorMessage.parameter_is_not_valid_url(name))

#         return value
        
#     @classmethod
#     def validate_positive_number(cls, name: str, value: Union[int, float]):
#         """
#         Validates if the provided 'value' parameter with the also
#         provided 'name' is a positive number (0 or greater),
#         raising an Exception if not.

#         This method returns the provided 'value' as it is if 
#         everything is ok.
#         """
#         if not variable_is_positive_number(value):
#             raise Exception(ErrorMessage.parameter_is_not_positive_number(name))

#         return value

#     @classmethod
#     def validate_is_class(cls, name: str, value, class_names: Union[list[str], str]):
#         """
#         Validates if the provided 'value' is one of the provided 'class_names'
#         by using the 'type(value).__name__' checking.

#         This method returns the 'value' as it is if everything is ok.
#         """
#         if isinstance(class_names, str):
#             class_names = [class_names]

#         if not type(value).__name__ in class_names:
#             raise Exception(ErrorMessage.parameter_is_not_class(name, class_names))
        
#         return value
        
#     # Complex ones below
#     @classmethod
#     def validate_string_mandatory_parameter(cls, name: str, value: str):
#         """
#         Validates if the provided 'value' is a valid and non
#         empty string.
#         """
#         cls.validate_mandatory_parameter(name, value)
#         cls.validate_string_parameter(name, value)

#         return value

#     @classmethod
#     def validate_numeric_positive_mandatory_parameter(cls, name: str, value: str):
#         """
#         Validates if the provided 'value' is a positive numeric
#         value.
#         """
#         cls.validate_mandatory_parameter(name, value)
#         cls.validate_positive_number(name, value)

#         return value
    
#     @classmethod
#     def validate_is_enum_class(cls, enum: Union['YTAEnum', Enum]):
#         """
#         Validates if the provided 'value' is a valid Enum
#         class or subclass.

#         This method will raise an Exception if the provided
#         'value' is not a valid Enum class or subclass, or
#         will return it as it is if yes.
#         """
#         if not isinstance(enum, Enum) and not issubclass(enum, Enum):
#             raise Exception(f'The parameter "{enum}" provided is not an Enum class or subclass.')
        
#         return enum

#     @classmethod
#     def validate_enum(cls, value: Union['YTAEnum', str], enum: 'YTAEnum'):
#         """
#         Validates if the provided 'value' value is a valid
#         Enum or Enum value of the also provided 'enum' class.

#         This method will raise an Exception if something is
#         wrong or will return the 'value' as an 'enum' Enum.
#         instance if everything is ok.
#         """
#         cls.validate_mandatory_parameter('value', value)
#         cls.validate_is_enum_class(enum)
#         cls.validate_is_class('value', value, [enum.__class__.__name__, 'str'])

#         return enum.to_enum(value)