# yuxin_helpers/color_utils.py

import matplotlib.pyplot as plt
import numpy as np

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



def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=100):
    """
    Truncate a colormap to a specified range of values.

    Parameters
    ----------
    cmap : matplotlib.colors.Colormap
        The colormap to be truncated.
    minval : float, optional
        The starting value of the colormap range (default is 0.0).
    maxval : float, optional
        The ending value of the colormap range (default is 1.0).
    n : int, optional
        The number of colors in the truncated colormap (default is 100).

    Returns
    -------
    matplotlib.colors.LinearSegmentedColormap
        The truncated colormap.

    Notes
    -----
    The function uses the `np.linspace` to create an evenly spaced array 
    of color values between the specified `minval` and `maxval`.
    """
    new_cmap = plt.cm.colors.LinearSegmentedColormap.from_list(
        'trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name, a=minval, b=maxval),
        cmap(np.linspace(minval, maxval, n)))

    return new_cmap
