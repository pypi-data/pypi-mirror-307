import numpy as np
from himage.types import Image
from typing import Literal


def deduce_limits(im: Image, tolerance_factor: float = 1):
    """
    deduces the limits for the imshow function. 
    returns 0, 1 if the image is a float in the range [0, tolerance_factor] and 0, 255 otherwise
    """
    vmin = 0
    if isinstance(im.flat[0], np.floating) and im.max() <= tolerance_factor:
        vmax = 1
    else:
        vmax = 255
    return vmin, vmax

def normalize_manual(im: Image, vmin: float, vmax: float):
    """normalizes an image to be in the range [0, 1] relative to the provided values"""
    return (im - vmin) / (vmax - vmin)

def normalize_min_max(im: Image):
    """normalizes an image to be in the range [0, 1] relative to its maximum and minimum values"""
    vmin, vmax = im.min(), im.max()

    if vmax == vmin:
        if vmin == 0:
            return im
        else:
            return im/vmin
    else:
        return (im - vmin) / (vmax - vmin)

def normalize_limits(im: Image):
    """normalizes an image to be in the range [0, 1] relative to its limit values"""
    _, vmax = deduce_limits(im) 
    return im/vmax

def normalize(im:Image, method: str = 'limits', ):
    """normalizes an image to be in the range [0, 1] relative to its maximum and minimum values
    Parameters
    ----------
    im : ndarray, the image
    method : string, possible values are 'minmax' and 'limits'
            'minmax' : normalize the image relative to its maximum and minimum values
            'limits' : normalize the image relative to its limit values
                ex.: if the image is uint8 or a flaot with values greater than 1, the limits will 
                be 0 and 255 hence the image will be divided by 255. Otherwise, the limits will be
                0 and 1 so the image will not be changed
    Returns
    -------
    ndarray, the normalized image
    """

    if method == 'minmax':
        return normalize_min_max(im)
    elif method == 'limits':
        return normalize_limits(im)
    else:
        raise ValueError('method must be either minmax or limits')

def clip(im: Image, vmax: Literal['auto'] | float = 'auto'):
    if vmax == 'auto':
        vmin, vmax = deduce_limits(im, 10)
    else:
        vmin = 0
    return np.clip(im, vmin, vmax)/vmax
