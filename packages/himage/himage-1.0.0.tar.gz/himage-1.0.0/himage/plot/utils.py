from himage.types import Image, Real
from himage.utils import deduce_limits

def parse_cmap(cmap: str | None, im: Image):
    if cmap is None and im.ndim == 2:
        _cmap = 'gray'
    elif cmap is None:
        _cmap = 'viridis'
    else:
        _cmap = cmap
    return _cmap


def parse_limits(limits: tuple[Real, Real] | None, im: Image):
    if limits is None:
        _limits = deduce_limits(im)
    else:
        _limits = limits
    return _limits

def parse_figsize(figsize: Real | tuple[Real, Real] | None, im: Image) -> tuple[Real, Real] | None:
    _figsize: tuple[Real, Real] | None
    if type(figsize)==float or type(figsize)==int:
        w, h = im.shape
        _figsize = (h/w * figsize, figsize)
    else:
        _figsize = figsize # type: ignore

    return _figsize
