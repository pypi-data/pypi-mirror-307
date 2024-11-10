import numpy as np
from himage.utils import deduce_limits, normalize_manual, normalize_min_max, normalize_limits, normalize, clip


im_int_gray = np.ones((5, 5), dtype=np.uint8)
im_int_rgb = np.ones((5, 5, 3), dtype=np.uint8)
im_float_gray = np.ones((5, 5), dtype=np.float32)
im_float_rgb = np.ones((5, 5, 3), dtype=np.float32)

def test_deduce_limits():
    assert deduce_limits(im_int_gray) == (0, 255)
    assert deduce_limits(im_int_rgb) == (0, 255)
    
    assert deduce_limits(im_int_gray*0) == (0, 255)
    assert deduce_limits(im_int_rgb*0) == (0, 255)

    assert deduce_limits(im_int_gray*42) == (0, 255)
    assert deduce_limits(im_int_rgb*42) == (0, 255)

    assert deduce_limits(im_float_gray) == (0, 1)
    assert deduce_limits(im_float_rgb) == (0, 1)

    assert deduce_limits(im_float_gray*0) == (0, 1)
    assert deduce_limits(im_float_rgb*0) == (0, 1)

    assert deduce_limits(im_float_gray*42) == (0, 255)
    assert deduce_limits(im_float_rgb*42) == (0, 255)


def test_normalize_manual():
    assert np.allclose(normalize_manual(im_int_gray, 0, 255), 1/255, atol=1e-7, rtol=0)
    assert np.allclose(normalize_manual(im_int_rgb, 0, 255), 1/255, atol=1e-7, rtol=0)

    assert np.allclose(normalize_manual(im_int_gray*0, 0, 255), 0, atol=1e-7, rtol=0)
    assert np.allclose(normalize_manual(im_int_rgb*0, 0, 255), 0, atol=1e-7, rtol=0)

    assert np.allclose(normalize_manual(im_int_gray*42, 0, 255), 42/255, atol=1e-7, rtol=0)
    assert np.allclose(normalize_manual(im_int_rgb*42, 0, 255), 42/255, atol=1e-7, rtol=0)

    assert np.allclose(normalize_manual(im_float_gray, 0, 1), 1, atol=1e-7, rtol=0)
    assert np.allclose(normalize_manual(im_float_rgb, 0, 1), 1, atol=1e-7, rtol=0)

    assert np.allclose(normalize_manual(im_float_gray*0, 0, 1), 0, atol=1e-7, rtol=0)
    assert np.allclose(normalize_manual(im_float_rgb*0, 0, 1), 0, atol=1e-7, rtol=0)

    assert np.allclose(normalize_manual(im_float_gray*42, 0, 255), 42/255, atol=1e-7, rtol=0)
    assert np.allclose(normalize_manual(im_float_rgb*42, 0, 255), 42/255, atol=1e-7, rtol=0)


def test_normalize_min_max():
    assert np.allclose(normalize_min_max(im_int_gray), 1, atol=1e-7, rtol=0)
    assert np.allclose(normalize_min_max(im_int_rgb), 1, atol=1e-7, rtol=0)

    assert np.allclose(normalize_min_max(im_int_gray*0), 0, atol=1e-7, rtol=0)
    assert np.allclose(normalize_min_max(im_int_rgb*0), 0, atol=1e-7, rtol=0)

    assert np.allclose(normalize_min_max(im_int_gray*42), 1, atol=1e-7, rtol=0)
    assert np.allclose(normalize_min_max(im_int_rgb*42), 1, atol=1e-7, rtol=0)

    assert np.allclose(normalize_min_max(im_float_gray), 1, atol=1e-7, rtol=0)
    assert np.allclose(normalize_min_max(im_float_rgb), 1, atol=1e-7, rtol=0)

    assert np.allclose(normalize_min_max(im_float_gray*0), 0, atol=1e-7, rtol=0)
    assert np.allclose(normalize_min_max(im_float_rgb*0), 0, atol=1e-7, rtol=0)

    assert np.allclose(normalize_min_max(im_float_gray*42), 1, atol=1e-7, rtol=0)
    assert np.allclose(normalize_min_max(im_float_rgb*42), 1, atol=1e-7, rtol=0)


def test_normalize_limits():
    assert np.allclose(normalize_limits(im_int_gray), 1/255, atol=1e-7, rtol=0)
    assert np.allclose(normalize_limits(im_int_rgb), 1/255, atol=1e-7, rtol=0)

    assert np.allclose(normalize_limits(im_int_gray*0), 0, atol=1e-7, rtol=0)
    assert np.allclose(normalize_limits(im_int_rgb*0), 0, atol=1e-7, rtol=0)

    assert np.allclose(normalize_limits(im_int_gray*42), 42/255, atol=1e-7, rtol=0)
    assert np.allclose(normalize_limits(im_int_rgb*42), 42/255, atol=1e-7, rtol=0)

    assert np.allclose(normalize_limits(im_float_gray), 1, atol=1e-7, rtol=0)
    assert np.allclose(normalize_limits(im_float_rgb), 1, atol=1e-7, rtol=0)

    assert np.allclose(normalize_limits(im_float_gray*0), 0, atol=1e-7, rtol=0)
    assert np.allclose(normalize_limits(im_float_rgb*0), 0, atol=1e-7, rtol=0)

    assert np.allclose(normalize_limits(im_float_gray*42), 42/255, atol=1e-7, rtol=0)
    assert np.allclose(normalize_limits(im_float_rgb*42), 42/255, atol=1e-7, rtol=0)


def test_normlize():
    assert np.allclose(normalize(im_int_gray, 'minmax'), 1, atol=1e-7, rtol=0)
    assert np.allclose(normalize(im_int_rgb, 'minmax'), 1, atol=1e-7, rtol=0)

    assert np.allclose(normalize(im_int_gray*0, 'minmax'), 0, atol=1e-7, rtol=0)
    assert np.allclose(normalize(im_int_rgb*0, 'minmax'), 0, atol=1e-7, rtol=0)

    assert np.allclose(normalize(im_int_gray*42, 'minmax'), 1, atol=1e-7, rtol=0)
    assert np.allclose(normalize(im_int_rgb*42, 'minmax'), 1, atol=1e-7, rtol=0)

    assert np.allclose(normalize(im_float_gray, 'minmax'), 1, atol=1e-7, rtol=0)
    assert np.allclose(normalize(im_float_rgb, 'minmax'), 1, atol=1e-7, rtol=0)

    assert np.allclose(normalize(im_float_gray*0, 'minmax'), 0, atol=1e-7, rtol=0)
    assert np.allclose(normalize(im_float_rgb*0, 'minmax'), 0, atol=1e-7, rtol=0)

    assert np.allclose(normalize(im_float_gray*42, 'minmax'), 1, atol=1e-7, rtol=0)
    assert np.allclose(normalize(im_float_rgb*42, 'minmax'), 1, atol=1e-7, rtol=0)


    assert np.allclose(normalize(im_int_gray, 'limits'), 1/255, atol=1e-7, rtol=0)
    assert np.allclose(normalize(im_int_rgb, 'limits'), 1/255, atol=1e-7, rtol=0)

    assert np.allclose(normalize(im_int_gray*0, 'limits'), 0, atol=1e-7, rtol=0)
    assert np.allclose(normalize(im_int_rgb*0, 'limits'), 0, atol=1e-7, rtol=0)

    assert np.allclose(normalize(im_int_gray*42, 'limits'), 42/255, atol=1e-7, rtol=0)
    assert np.allclose(normalize(im_int_rgb*42, 'limits'), 42/255, atol=1e-7, rtol=0)

    assert np.allclose(normalize(im_float_gray, 'limits'), 1, atol=1e-7, rtol=0)
    assert np.allclose(normalize(im_float_rgb, 'limits'), 1, atol=1e-7, rtol=0)

    assert np.allclose(normalize(im_float_gray*0, 'limits'), 0, atol=1e-7, rtol=0)
    assert np.allclose(normalize(im_float_rgb*0, 'limits'), 0, atol=1e-7, rtol=0)

    assert np.allclose(normalize(im_float_gray*42, 'limits'), 42/255, atol=1e-7, rtol=0)
    assert np.allclose(normalize(im_float_rgb*42, 'limits'), 42/255, atol=1e-7, rtol=0)


def test_clip():
    print(im_int_gray)
    print(clip(im_int_gray))
    assert np.allclose(clip(im_int_gray), 1/255, atol=1e-7, rtol=0)
    assert np.allclose(clip(im_int_rgb), 1/255, atol=1e-7, rtol=0)

    assert np.allclose(clip(im_int_gray*0), 0, atol=1e-7, rtol=0)
    assert np.allclose(clip(im_int_rgb*0), 0, atol=1e-7, rtol=0)

    assert np.allclose(clip(im_int_gray*42), 42/255, atol=1e-7, rtol=0)
    assert np.allclose(clip(im_int_rgb*42), 42/255, atol=1e-7, rtol=0)

    assert np.allclose(clip(im_float_gray), 1, atol=1e-7, rtol=0)
    assert np.allclose(clip(im_float_rgb), 1, atol=1e-7, rtol=0)

    assert np.allclose(clip(im_float_gray*0), 0, atol=1e-7, rtol=0)
    assert np.allclose(clip(im_float_rgb*0), 0, atol=1e-7, rtol=0)

    assert np.allclose(clip(im_float_gray*42), 42/255, atol=1e-7, rtol=0)
    assert np.allclose(clip(im_float_rgb*42), 42/255, atol=1e-7, rtol=0)

    assert np.allclose(clip(im_float_gray*8), 1, atol=1e-7, rtol=0)
    assert np.allclose(clip(im_float_rgb*8), 1, atol=1e-7, rtol=0)

    assert np.allclose(clip(im_float_gray*0.9), 0.9, atol=1e-7, rtol=0)
    assert np.allclose(clip(im_float_rgb*0.9), 0.9, atol=1e-7, rtol=0)