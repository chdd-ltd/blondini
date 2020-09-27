"""
  ----------------------------------------------------------------------------
    This module ...


"""

import cv2 as cv
import sys
from random import randint


def match_template(haystack, needle):

    result = cv.matchTemplate(haystack, needle, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

    return min_val, max_val, min_loc, max_loc


def preview_window(image, window=0):

    # 16:9 aspect ratio resolutions:
    resolutions = [[0, 0], [1024, 576], [1152, 648], [1280, 720], [1366, 768], [1600, 900], [1920, 1080]]

    print('\nQ or Esc to exit window')
    print('S to save image to img/image...\n')

    while True:
        key = cv.waitKey(1)
        if window > 0:
            cv.namedWindow('preview', 0)
            cv.resizeWindow('preview', resolutions[window][0], resolutions[window][1])
        cv.imshow('preview', image)

        if key == ord('s'):
            height, width, *_ = image.shape
            number = randint(100, 999)
            filename = f'img/image_{width}x{height}_{number}.jpg'
            print(f'saving: {filename}')
            cv.imwrite(filename, image)

        if key == ord('q') or key == 27:   # 27 = Esc
            break


# ---------------------------------------------------------------------------- #
if __name__ == '__main__':

    print('\n#', '-' * 76, '#')
    print('{}'.format(sys.argv[0]))

