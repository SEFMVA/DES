import cv2


def get_image():
    camera = cv2.VideoCapture(0)
    for i in range(2):
        return_value, image = camera.read()
        try:
            cv2.imwrite('images/img' + str(i) + '.png', image)
        except:
            print("Błąd komery")
            del camera
            return False
    del camera
    return True
