from math import gcd


# TODO: Maybe I can refactor this with the new method below
def resize_to_fit_on_region(element_size: tuple, region_size: tuple):
    """
    This method calculates the size that the 'element_size' must be
    resized to in order to fit the provided 'region_size'. Fitting 
    means that the element will cover the whole region.

    This method is useful to resize images or videos that will be
    placed behind alpha (transparent) areas of images so they will
    fit perfectly.

    This method returns a group of two values that are the expected
    element width and height (w, h).
    """
    # TODO: Check that the format is ok and the values are also ok
    if len(element_size) != 2 or len(region_size) != 2:
        raise Exception('The provided "element_size" and "region_size" parameters are not tuples of (w, h) values.')

    element_width, element_height = element_size
    region_width, region_height = region_size

    great_common_divisor = gcd(element_width, element_height)
    step_x = element_width / great_common_divisor
    step_y = element_height / great_common_divisor

    # Make sure they are even numbers to be able to move at least
    # one pixel on each side
    if step_x % 2 != 0 or step_y % 2 != 0:
        step_x *= 2
        step_y *= 2

    # If element is larger than region, we need to make it smaller.
    # In any other case, bigger
    if element_width > region_width and element_height > region_height:
        step_x = -step_x
        step_y = -step_y
    
    do_continue = True
    tmp_size = [element_width, element_height]
    while (do_continue):
        tmp_size = [tmp_size[0] + step_x, tmp_size[1] + step_y]

        if step_x < 0 and (tmp_size[0] < region_width or tmp_size[1] < region_height):
            # The previous step had the right dimensions
            tmp_size[0] += abs(step_x)
            tmp_size[1] += abs(step_y)
            do_continue = False
        elif step_x > 0 and (tmp_size[0] > region_width and tmp_size[1] > region_height):
            # This step is ok
            do_continue = False

    return tmp_size[0], tmp_size[1]

def adjust_to_aspect_ratio(width, height, aspect_ratio):
    """
    This method will adjust the provided 'width' and 'height'
    to fit the provided 'aspect_ratio' using, as maximum, the
    provided 'width' or 'height' values.

    For example, if width = 900 and height = 900 and 
    aspect_ratio = 16/9, the result will be 900, 506.25 that
    are the values that fit the 'aspect_ratio' by using the
    'width' as it is (because it is the 'height' the one that
    has to be changed).

    This is useful when we need to fit some region of an 
    specific aspect ratio so we first adjust it and then resize
    it as needed.
    """
    if width / height > aspect_ratio:
        new_height = height
        new_width = new_height * aspect_ratio
        
        if new_width > width:
            new_width = width
            new_height = new_width / aspect_ratio
    else:
        new_width = width
        new_height = new_width / aspect_ratio
        
        if new_height > height:
            new_height = height
            new_width = new_height * aspect_ratio

    return new_width, new_height