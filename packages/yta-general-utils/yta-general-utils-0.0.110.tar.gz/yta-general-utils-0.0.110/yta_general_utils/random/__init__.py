from random import choice as random_choice


def randrangefloat(start: float, end: float, step: float):
    """
    Calculate and return a random float number between the provided
    'start' and 'end' limits using the also provided float 'step'.
    """
    # Swap limits if needed
    if end < start:
        start, end = end, start

    # TODO: What if 'start' and 'end' are the same (?)
    return random_choice([round(start + i * step, 4) for i in range(int((end - start) / step) + 1) if start + i * step <= end])