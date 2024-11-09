# yuxin_helpers/color_utils.py

def rgb_to_hex(r: int, g: int, b: int) -> str:
    '''
    Convert an RGB color to a hexadecimal color.
    
    Parameters
    ----------
    r : int
        The red component.
    g : int
        The green component.
    b : int
        The blue component. 
    
    Returns
    -------
    str
        The hexadecimal color.
    '''
    return '#%02x%02x%02x' % (r, g, b)


def hex_to_rgb(hex: str) -> tuple[int, int, int]:
    '''
    Convert a hexadecimal color to an RGB color.
    
    Parameters
    ----------
    hex : str
        The hexadecimal color.
    
    Returns
    -------
    tuple[int, int, int]
        The RGB color.
    '''
    hex = hex.lstrip('#')
    return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))
