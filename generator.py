import math

import videoscrapper
import preprocessing
import postprocessing
import png_to_rgb


def create_generator():
    def create_iterator():
        videoscrapper.get_image()
        r1, g1, b1 = png_to_rgb.png_to_rgb("images/img0.png")
        r2, g2, b2 = png_to_rgb.png_to_rgb("images/img1.png")
        z = preprocessing.preprocess_rgb(r1, g1, b1, r2, g2, b2)
        z = z[0:math.floor(len(z))]
        return postprocessing.postprocess(z[0:math.floor(len(z) / 4)], 6, 3.9+0/(10.01 * 3))

    generator = create_iterator()

    while True:
        try:
            xorbytearray = generator.__next__()
            yield xorbytearray.int
        except StopIteration:
            generator = create_iterator()
    print("finito")


# test = create_generator()
# test.__next__()
