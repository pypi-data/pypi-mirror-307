
import matplotlib.pyplot as plt
import numpy as np
from warnings import warn
from himage.utils import deduce_limits, normalize_manual
from himage.types import Image, Real
from himage.plot.utils import parse_cmap, parse_limits, parse_figsize


def imshow( im: Image, title: str | None = None,
            figsize: Real | tuple[Real, Real] | None = None,
            cmap: str | None = None,
            limits: tuple[Real, Real] | None = None,
            dpi:int | None = None,
            axis_on: bool = False
            ) -> None:
    """shows an image with matplotlib
    Parameters
    ----------
    im : ndarray
    title : string, optional
    figsize : tuple, of floats, representing the dimensions of the plot int or float represntig the desired width of the output, the heigth will be calculated automatically
    cmap : string, possible values are the same as in matplotlib.pyplot.imshow. 
            If None is provided and the image have a single channel, the cmap is set to 'gray' instead of matplotlib's default cmap for single channel images.
    limits : (vmin, vmax) a pair of int or float values representig the minimal pixel intensity of the plot.
    dpi : int, dots per inch
    axis_on : turn on and of the axis of the plots
    """

    _cmap = parse_cmap(cmap, im)
    _limits = parse_limits(limits, im)
    _figsize = parse_figsize(figsize, im)

    plt.figure(figsize=_figsize, dpi=dpi, frameon=False)

    if not axis_on:
        plt.axis('off')

    plt.tight_layout()
    plt.imshow(normalize_manual(im, *_limits), cmap=_cmap, vmin = 0, vmax=1)
    if title is not None:
        plt.title(str(title))
    plt.show()
    
    return None



def multimshow(images: list[Image],
               titles: list[str] | None=None, 
               n_cols: int = 2,
               figsize: Real | tuple[Real, Real] | None  =10,
               colwidth: Real| None = None,
               cmap: str | None=None,
               limits: tuple[Real, Real] | None=None,
               dpi: int | None = None,
               axis_on: bool = False ):
    """shows mutiple images in one plot
    Parameters
    ----------
    images : list or tuple of images
    titles : list or tuple of titles
    n_cols : int, number of columns of the resulting plot
    figsize : tuple, of floats, representing the dimensions of the plot
              int or float represntig the desired width of the output, the heigth will be calculated automatically
    colwidth : int or float representig the width of the column, can be given instead of a figsize. n_cols = 3 and colwidth = 5 will give the same output as colwidth = 3 and figsize = 15
    cmap : string, the cmap for single channel images. Possible values are the same as in matplotlib.pyplot.imshow.
            If None is provided and the image have a single channel, the cmap is set to 'gray' instead of 
            matplotlib's default cmap for single channel images.
            If the color images are mixed with single channel images, the cmap will be ignored for the color images.
    dpi : int, dots per inch
    axis_on : turn on and of the axis of the plots
    Returns
    -------
    None
    """


    n_ims = len(images)
    n_rows = int(np.ceil(n_ims/n_cols))
    if colwidth is not None:
        if figsize is not None:
            warn("If colwidth is not None, figsize is being deduced automatically. The user provided figsize is ignored.")
        figsize = colwidth * n_cols


    if type(figsize)==float or type(figsize) == int:
        figsize = (figsize, figsize/n_cols * n_rows)


    if cmap is None:
        cmap = 'gray'

    fig = plt.figure(figsize=figsize, dpi=dpi, frameon=False)

    for i, im in enumerate(images):

        fig.add_subplot(n_rows, n_cols, i+1)

        # it isnt very efficient to repetedly do this tests for values that don't change
        # but since nobody is going to plot thousands of images, it's better to keep the code simple
        if not axis_on: 
            plt.axis('off')
        if titles is not None: 
            plt.title(str(titles[i]))

        plt.imshow(normalize_manual(im, *deduce_limits(im)), cmap=cmap, vmin=0, vmax=1)
        plt.tight_layout()

    plt.show()
    
    return None