import math

import videoscrapper
import preprocessing
import postprocessing
import png_to_rgb
import secrets
from bitstring import BitStream


def create_generator():
    def create_iterator(selectSecretModule=False):
        if(selectSecretModule == False and videoscrapper.get_image()):
            r1, g1, b1 = png_to_rgb.png_to_rgb("images/img0.png")
            r2, g2, b2 = png_to_rgb.png_to_rgb("images/img1.png")
            print("preprocessing")
            z = preprocessing.preprocess_rgb(r1, g1, b1, r2, g2, b2)
            z = z[0:math.floor(len(z))]
            print("postprocessing")
            return postprocessing.postprocess(
                z[0:math.floor(len(z) / 4)], 6, 3.9+0/(10.01 * 3))
        else:
            def wrapper(bits):
                yield bits[1:]
            print("Użyto modułu secrets")
            bs = BitStream(int=secrets.randbits(32), length=33)
            return wrapper(bs)

    generator = create_iterator()

    while True:
        try:
            xorbytearray = generator.__next__()
            yield xorbytearray
        except StopIteration:
            generator = create_iterator()
        except ZeroDivisionError:
            print("ZeroDivisionError, sprawdź poprawność kamery")
            generator = create_iterator(True)
            xorbytearray = generator.__next__()
            yield xorbytearray
    print("finito")


# test = create_generator()
# test.__next__()
