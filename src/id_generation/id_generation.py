import numpy as np

def generate_ids(quantity: int = 2000) -> map:
    """Generate a sequence of unique identifiers.

    This function creates a map object containing a sequence of string identifiers
    in the format 'MP_XXXXX', where XXXXX is a zero-padded number from 00001 to the specified quantity.

    Args:
        quantity (int): The number of identifiers to generate. Defaults to 2000.

    Returns:
        map: A map object containing the generated identifiers as strings.
    """
    try:
        digits = np.arange(1, quantity + 1, 1)
        return map(lambda x: f"MP_{str(x).zfill(5)}", digits)
    except Exception as e:
        return f"Please use numbers: {e}"