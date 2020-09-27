"""
  ----------------------------------------------------------------------------
    This module returns the text from a screenshot of a terminal window.

    The module uses pixel matching technology from OpenCV "Match Template"
    so the operating system must be Ubuntu Mate with a screen resolution
    of 1920x1080 and the Terminal application must on its Defaults; 80
    columns by 24 rows and also be configured to use non-colourised
    Monospace Regular 12 font.

    Version: 1.0

    TODO:
        different resolutions
        variable starting location
        blank lines
        multiple spaces and tabs
        line wrapping
        underlined characters
        black on white characters
"""

from common_opencv import match_template
from common_opencv import preview_window
import cv2 as cv
import numpy as np
import argparse
import time
import os


# ---------------------------------------------------------------------------- #


def monospace_regular_12(image, progress=False, display=False, preview=False):
    """
      ----------------------------------------------------------------------------
        args:
            image (numpy.ndarray):  OpenCV image array
            progress (bool):        Display '...' progress on the terminal
            display (bool):         Echo the text to the terminal and display
                                    the source image with rectangles for all
                                    fonts found.

        returns:
            image (numpy.ndarray):
                An OpenCV image with rectangles around each font found.

            text_array (list):
                A two dimensional array containing the rows of text, with each
                element being a single character. If no characters are found,
                an empty array is returned.
    """

    # print(f'image.shape:{image.shape}')
    if len(image.shape) == 3:
        image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    monospace_dictionary = _load_monospace_dictionary()

    image_width = len(image[0])
    image_height = len(image)
    start_row = 29      # EXPECTED pixel starting location for line one
    start_cell = 2      # could/should change this to be the result of
    block_height = 18   # the first character location from a search.
    block_width = 9
    results = []

    start = time.perf_counter()
    for r in range(start_row, (image_height - block_height), block_height):
        for c in range(start_cell, (image_width - block_width), block_width):

            if progress:
                print('.', end='')

            # print(f'[{r}:{r+18}, {c}:{c+9}] ', end='')
            #                 rows  elements
            block = image[r:r + 18, c:c + 9]
            # preview_window(block, 0)

            block_result = _process_block(r, c, block, monospace_dictionary)
            if len(block_result) > 0:
                results.append(block_result)

        if progress:
            print('')

        # break     # only do the first row

    if progress:
        finish = time.perf_counter()
        print(f'Finished in {round(finish - start, 2)} second(s)')

    for r in results:
        image = cv.rectangle(image, (r[3]-9, r[0]), (r[3], r[0]+18), (255, 0, 0), thickness=1, lineType=cv.LINE_4)

    text_array = []
    for i in range(0, 60, 1):              # image has 30 rows, terminal has 24 rows
        _ = [''] * 80
        text_array.append(_)                     # 80 column

    row, column = 0, 0
    height = 0
    for index, result in enumerate(results, start=0):
        # print(f'[{row}]({column}){result[-1]}')

        if result[0] > height:              # carriage returns
            height = result[0]
            row += 1
            column = 0
            # print('')
            # print(f'\n[{row}] ', end='')

        # print(f'{result[-1]}', end='')
        # print(f'{result[-1]}({column}) ', end='')
        text_array[row][column] = result[-1]

        if index < len(results) - 1:        # space character(s)
            if results[index + 1][3] > results[index][3] + 9:
                column += 1
                text_array[row][column] = ' '
                # print(f' ', end='')
                # print(f'({column}) ', end='')

        if column == 79:    # carriage returns
            row += 1
            column = 0

        column += 1
    # print('')

    # remove blank lines
    blank_lines = []
    for index, row in enumerate(text_array, start=0):
        blank = True
        for column in row:
            if column != '':
                blank = False

        if blank:
            blank_lines.append(index)

    if len(blank_lines) > 0:
        blank_lines.sort(reverse=True)
        for index in blank_lines:
            text_array.pop(index)

    text_rows = []
    for row in text_array:
        _ = ''
        for cell in row:
            _ += cell
        text_rows.append(_)

    if display:
        print('')
        for i, r in enumerate(text_rows):
            print(f'{i:<3} {r}')

    if preview:
        preview_window(image, 0)

    return image, text_rows

# ---------------------------------------------------------------------------- #


def _process_block(r, c, block, monospace_dictionary):
    block_result = []

    count = 0
    # print('')
    for x in block:
        for y in x:
            # print(f'{y}', end=' ')
            count += y
        # print('')
    # print(f'count:{count}')

    if count > 8748:  # non-blank block!
        top = [0, '']
        for key, value in monospace_dictionary.items():
            # print(key, value)
            _, max_val, _, max_loc = match_template(block, value[1])

            if max_val > top[0]:
                top[0] = max_val
                top[1] = key

            # if r == 209 and max_val > .75:
            #     print(f'{r:<3}:{r+18:<3} {c:<3}:{c+9:<3} {value[0]} max_val:{round(max_val, 4):<4}')

            if max_val > .99:
                # print(f'{r:<3}:{r+18:<3} {c:<3}:{c+9:<3} {value[0]} max_val:{round(max_val, 4):<4}')
                block_result = [r, r + 18, c, c + 9, value[0]]
                break

        # to ENSURE we get a character for a non-blank block we take the highest max_val
        # from all tried, with a sanity check at .60
        if max_val < .99 and top[0] > .60:
            # print(f'+ {r:<3}:{r+18:<3} {c:<3}:{c+9:<3} {top[1]} max_val:{round(top[0], 4):<4}')
            _, max_val, _, max_loc = match_template(block, monospace_dictionary[top[1]][1])
            block_result = [r, r + 18, c, c + 9, monospace_dictionary[top[1]][0]]

    # if len(block_result) > 0:
    #     print(f'block_result:{block_result}')

    return block_result

# ---------------------------------------------------------------------------- #


def _load_monospace_dictionary():
    """
      ----------------------------------------------------------------------------
        create a dictionary that is used to identify monospace font filenames,
        ascii characters and loads OpenCV greyscale image array's
    """

    monospace_dictionary = {}

    monospace_dictionary['0'] = ['0']
    monospace_dictionary['1'] = ['1']
    monospace_dictionary['2'] = ['2']
    monospace_dictionary['3'] = ['3']
    monospace_dictionary['4'] = ['4']
    monospace_dictionary['5'] = ['5']
    monospace_dictionary['6'] = ['6']
    monospace_dictionary['7'] = ['7']
    monospace_dictionary['8'] = ['8']
    monospace_dictionary['9'] = ['9']

    monospace_dictionary['A'] = ['A']
    monospace_dictionary['B'] = ['B']
    monospace_dictionary['C'] = ['C']
    monospace_dictionary['D'] = ['D']
    monospace_dictionary['E'] = ['E']
    monospace_dictionary['F'] = ['F']
    monospace_dictionary['G'] = ['G']
    monospace_dictionary['H'] = ['H']
    monospace_dictionary['I'] = ['I']
    monospace_dictionary['J'] = ['J']
    monospace_dictionary['K'] = ['K']
    monospace_dictionary['L'] = ['L']
    monospace_dictionary['M'] = ['M']
    monospace_dictionary['N'] = ['N']
    monospace_dictionary['O'] = ['O']
    monospace_dictionary['P'] = ['P']
    monospace_dictionary['Q'] = ['Q']
    monospace_dictionary['R'] = ['R']
    monospace_dictionary['S'] = ['S']
    monospace_dictionary['T'] = ['T']
    monospace_dictionary['U'] = ['U']
    monospace_dictionary['V'] = ['V']
    monospace_dictionary['W'] = ['W']
    monospace_dictionary['X'] = ['X']
    monospace_dictionary['Y'] = ['Y']
    monospace_dictionary['Z'] = ['Z']

    monospace_dictionary['a'] = ['a']
    monospace_dictionary['b'] = ['b']
    monospace_dictionary['c'] = ['c']
    monospace_dictionary['d'] = ['d']
    monospace_dictionary['e'] = ['e']
    monospace_dictionary['f'] = ['f']
    monospace_dictionary['g'] = ['g']
    monospace_dictionary['h'] = ['h']
    monospace_dictionary['i'] = ['i']
    monospace_dictionary['j'] = ['j']
    monospace_dictionary['k'] = ['k']
    monospace_dictionary['l'] = ['l']
    monospace_dictionary['m'] = ['m']
    monospace_dictionary['n'] = ['n']
    monospace_dictionary['o'] = ['o']
    monospace_dictionary['p'] = ['p']
    monospace_dictionary['q'] = ['q']
    monospace_dictionary['r'] = ['r']
    monospace_dictionary['s'] = ['s']
    monospace_dictionary['t'] = ['t']
    monospace_dictionary['u'] = ['u']
    monospace_dictionary['v'] = ['v']
    monospace_dictionary['w'] = ['w']
    monospace_dictionary['x'] = ['x']
    monospace_dictionary['y'] = ['y']
    monospace_dictionary['z'] = ['z']

    monospace_dictionary['#'] = ['#']
    monospace_dictionary['%'] = ['%']
    monospace_dictionary['+'] = ['+']
    monospace_dictionary[','] = [',']
    monospace_dictionary['-'] = ['-']
    monospace_dictionary['@'] = ['@']
    monospace_dictionary['_'] = ['_']
    monospace_dictionary['~'] = ['~']

    monospace_dictionary['ampersand'] = ['&']
    monospace_dictionary['asterisk'] = ['*']
    monospace_dictionary['backslash'] = ['\\']
    monospace_dictionary['brace_close'] = ['}']
    monospace_dictionary['brace_open'] = ['{']
    monospace_dictionary['bracket_close'] = [')']
    monospace_dictionary['bracket_open'] = ['(']
    monospace_dictionary['caret'] = ['^']
    monospace_dictionary['colon'] = [':']
    monospace_dictionary['dollar'] = ['$']
    monospace_dictionary['double_quotes'] = ['"']
    monospace_dictionary['equals'] = ['=']
    monospace_dictionary['exclamation_mark'] = ['!']
    monospace_dictionary['forwardslash'] = ['/']
    monospace_dictionary['fullstop'] = ['.']
    monospace_dictionary['grave_accent'] = ['`']
    monospace_dictionary['greaterthan'] = ['>']
    monospace_dictionary['lessthan'] = ['<']
    monospace_dictionary['question_mark'] = ['?']
    monospace_dictionary['semicolon'] = [';']
    monospace_dictionary['single_quote'] = ["'"]
    monospace_dictionary['square_close'] = [']']
    monospace_dictionary['square_open'] = ['[']
    monospace_dictionary['vertical_bar'] = ['|']

    # monospace_dictionary['space'] = [' ']
    # we DON'T want search for 'BLANK' blocks because there is hundreds of them...

    monospace_pop = []
    for key, value in monospace_dictionary.items():
        character_file = f'img/monospace/monospace_regular_12_{key}.png'

        try:
            character = cv.imread(character_file, cv.IMREAD_UNCHANGED)
            character = cv.cvtColor(character, cv.COLOR_BGR2GRAY)
            value.append(character)
        except cv.error:
            print(f'Can\'t find {character_file}')
            monospace_pop.append(key)

    if len(monospace_pop) > 0:
        for p in monospace_pop:
            monospace_dictionary.pop(p)

    if len(monospace_dictionary) == 0:
        print(f'Can\'t work without any font files!')
        exit(1)

    return monospace_dictionary

# ---------------------------------------------------------------------------- #


if __name__ == '__main__':

    # $ python monospace_regular_12.py img/test_image_man_bash.jpg
    # $ python monospace_regular_12.py img/test_image_syslog.jpg

    progress = True
    display = True
    preview = True

    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="terminal image file")
    parser.add_argument('-p', help="turn OFF ... progress bars", action="store_true")
    parser.add_argument('-d', help="turn OFF displaying the text", action="store_true")
    parser.add_argument('-w', help="turn OFF previewing the image", action="store_true")

    args = parser.parse_args()

    if args.p:
        progress = False

    if args.d:
        display = False

    if args.w:
        preview = False

    if args.file:
        if not os.path.isfile(args.file):
            print(f'Can\'t find {args.file}')
            exit(2)
        else:
            image_file = args.file

    # print(f'\nargs:{args}\n')

    print(__doc__)

    try:
        image = cv.imread(image_file)
        image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        print(f'file: {image_file}')
    except cv.error as e:
        print(f'OpenCV error: {e}')
        exit(2)

    image, text_rows = monospace_regular_12(image, progress=progress, display=display, preview=preview)

    cv.destroyAllWindows()
