import os
import numpy as np
from himage import imread, imwrite, normalize


def test_imread_write():
    im_yellow = np.ones((20, 10, 3))*.9
    im_yellow[:,:,2] = 0

    imwrite(im_yellow, 'test.png')
    assert os.path.exists('test.png')

    written_im = imread('test.png')
    os.remove('test.png')
    assert np.allclose(normalize(written_im, method = 'limits'), im_yellow, atol=.5/255, rtol=0)

    imwrite(im_yellow, 'test.jpg')
    assert os.path.exists('test.jpg')

    written_im = imread('test.jpg')
    os.remove('test.jpg')
    assert np.allclose(normalize(written_im, method = 'limits'), im_yellow, atol=.1, rtol=0)
    


    im_yellow = np.random.uniform(0, 1, (20, 10, 3))
    im_yellow[:,:,2] = 0

    imwrite(im_yellow, 'test.png')
    assert os.path.exists('test.png')

    written_im = imread('test.png')
    os.remove('test.png')
    assert np.allclose(normalize(written_im, method = 'limits'), im_yellow, atol=.5/255, rtol=0)

    imwrite(im_yellow, 'test.jpg')
    assert os.path.exists('test.jpg')

    written_im = imread('test.jpg')
    os.remove('test.jpg')
    # jpg is distorting the values so if we try to compare them directly we will have to use a very large tolerance
    # (we didn't have this problem with the image made of ones because the values were all the same, so the compression didn't change them)
    assert np.allclose(normalize(written_im, method = 'limits').mean(), im_yellow.mean(), atol=.03, rtol=0)
    assert np.allclose(normalize(written_im, method = 'limits').mean(axis = (0,1)), im_yellow.mean(axis = (0,1)), atol=.1, rtol=0)
