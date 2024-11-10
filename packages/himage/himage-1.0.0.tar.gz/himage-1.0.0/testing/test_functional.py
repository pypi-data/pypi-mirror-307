from himage import imshow, multimshow, imread

im = imread("tulips.png")

imshow(im)
multimshow([im, im, im], titles = ['title 1', 'title 2', 'title 3'], n_cols=3)