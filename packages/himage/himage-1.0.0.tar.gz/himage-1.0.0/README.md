A set of various convenient functions useful in image processing, written in python.

## Example of usage

```py
from himage import imshow, multimshow, imread

im = imread("image.png")

imshow(im)
multimshow([im, im, im], titles = ['title 1', 'title 2', 'title 3'], n_cols=3)
```