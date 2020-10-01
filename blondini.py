from common_opencv import match_template
from common_opencv import preview_window

from monospace_regular_12 import monospace_regular_12

# from parser import parse_cat
# from parser import parse_ls
# from parser import parse_pwd
# from terminal_parser import parse
# from terminal_parser import parse_id
# from terminal_parser import parse_ifconfig
# from terminal_parser import parse_list
# from terminal_parser import parse_netstat
# from terminal_parser import parse_ps
# from terminal_parser import parse_resolv
# from terminal_parser import parse_uname

from terminal_parser import terminal_parser

import cv2 as cv
import numpy as np
import pyautogui
import time
import json
import sys


def pre_requisites(pre_requisite):

    if pre_requisite == 'minimise_idea':
        pyautogui.moveTo(38, 42, duration=0)
        pyautogui.click()
        # TODO: conformation that it worked else error and exit!

    if pre_requisite == 'coordinates':
        coordinates = find_terminal_window()
        session.append({'coordinates': coordinates})
        # TODO: conformation that it worked else error and exit!

    if pre_requisite == 'focus':
        pass
        # TODO: conformation that it worked else error and exit!

    if pre_requisite == 'prompt':
        pil_image = pyautogui.screenshot(region=(session[0]["coordinates"][0][0], session[0]["coordinates"][0][1],
                                                 session[0]["coordinates"][4][0], session[0]["coordinates"][4][1]))
        image = cv.cvtColor(np.array(pil_image), cv.COLOR_RGB2BGR)
        _, text_rows = monospace_regular_12(image, progress=False, display=False, preview=False)
        for row in text_rows:
            if '#' in row:
                _ = row.split('#')
                prompt = _[0] + '#'
                break
            if '$' in row:
                _ = row.split('$')
                prompt = _[0] + '$'
                break

        # print(f'prompt : {prompt}')
        if len(prompt) > 0:
            session.append({'prompt': prompt})
        else:
            print(f'error: pre_requisites(prompt) = {prompt}')
            exit(1)


def post_requisites(post_requisite):
    pass

    # if post_requisite == 'coordinates':
    #     coordinates = session[0]
    #     # TODO: conformation that it worked else error and exit!


def run_terminal_command(command, progress=False, display=False, preview=False):

    if command == 'enter':
        pyautogui.press('enter')
    else:
        type_string(command, True)

    if command != 'clear' and command != 'enter':
        terminal_window = 1
        terminal_output = {}

        while True:
            pil_image = pyautogui.screenshot(region=(session[0]["coordinates"][0][0], session[0]["coordinates"][0][1],
                                                     session[0]["coordinates"][4][0], session[0]["coordinates"][4][1]))
            image = cv.cvtColor(np.array(pil_image), cv.COLOR_RGB2BGR)
            image_result, text_rows = monospace_regular_12(image, progress=progress, display=display, preview=preview)
            terminal_output[terminal_window] = text_rows

            if 'less' in command:
                if len(text_rows) > 0 and text_rows[-1] == ':':
                    terminal_window += 1
                    pyautogui.press('pagedown')
                    time.sleep(.25)
                else:
                    pyautogui.press('q')
                    break
            else:
                break

        terminal_rows = parse_terminal_output(terminal_output, display=display)

        return terminal_rows


def parse_terminal_output(terminal_output, display=False):
    row_count = 0
    for _, v in terminal_output.items():
        row_count += len(v)
    terminal_rows = [None] * row_count
    # print(f'row_count:{row_count}')
    # print(f'terminal_rows:{len(terminal_rows)}')

    z = 0
    p = 0
    for key, value in terminal_output.items():

        if key == 1:
            for i, e in enumerate(value):
                terminal_rows[i] = e
                z += 1
                # print(f'{z:>2}:{i:<2} {e}')
        else:
            for i, e in enumerate(value):
                if e in terminal_rows and z <= p:
                    # print(f'\t{z:>2}:{i:<2} {e}')
                    pass
                else:
                    # print(f'{z:>2}:{i:<2} {e}')
                    terminal_rows[z] = e
                    z += 1

        p += len(terminal_output[key])

    pop_list = []
    # print(f'\nterminal_rows:{len(terminal_rows)}')
    for i, e, in enumerate(terminal_rows):
        # print(f'{i:>2} : {e}')
        if e == ':':
            pop_list.append(i)
        if e is None:
            pop_list.append(i)

    pop_list.reverse()
    # print(f'pop_list:{pop_list}')
    for i in pop_list:
        terminal_rows.pop(i)

    if display:
        print(f'\nparse_terminal_output -> terminal_rows:{len(terminal_rows)}')
        for i, e, in enumerate(terminal_rows):
            print(f'{i:>2} : {e}')

    return terminal_rows


def open_terminal_menu():
    # open terminal windows using the Menu search functionality

    # move to "Menu" and click on it
    pyautogui.moveTo(33, 9, duration=0)
    pyautogui.click()

    string = 'Terminal'
    type_string(string, True)
    time.sleep(.33)


def find_terminal_window(focus=True, preview=False):

    tl, tr, bl, br, wh = [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]

    pil_image = pyautogui.screenshot()
    haystack = cv.cvtColor(np.array(pil_image), cv.COLOR_RGB2BGR)

    needle_file = f'img/mate/mate_1920x1080_window_terminal_724x27.png'
    needle = cv.imread(needle_file, cv.IMREAD_UNCHANGED)
    height, width, _ = needle.shape
    _, max_val, _, max_loc = match_template(haystack, needle)
    # print(f'{needle_file} \t\t\t{round(max_val, 2):<4} {max_loc[0]}x{max_loc[1]} \t{width}:{height}')
    if max_val >= 0.7:
        tl[0] = max_loc[0]
        tl[1] = max_loc[1]
        pyautogui.moveTo(tl[0], tl[1], duration=0)

        tr[0] = tl[0] + width
        tr[1] = tl[1]
        pyautogui.moveTo(tr[0], tr[1], duration=0)

        needle_file = f'img/mate/mate_1920x1080_window_bottomleft_dark_12x12.png'
        needle = cv.imread(needle_file, cv.IMREAD_UNCHANGED)
        height, width, _ = needle.shape
        _, max_val, _, max_loc = match_template(haystack, needle)
        # print(f'{needle_file} \t{round(max_val, 2):<4} {max_loc[0]}x{max_loc[1]} \t{width}:{height}')
        if max_val >= 0.9:
            bl[0] = max_loc[0]
            bl[1] = max_loc[1] + 11
            pyautogui.moveTo(bl[0], bl[1], duration=0)

            needle_file = f'img/mate/mate_1920x1080_window_bottomright_dark_12x12.png'
            needle = cv.imread(needle_file, cv.IMREAD_UNCHANGED)
            height, width, _ = needle.shape
            _, max_val, _, max_loc = match_template(haystack, needle)
            # print(f'{needle_file} \t{round(max_val, 2):<4} {max_loc[0]}x{max_loc[1]} \t{width}:{height}')
            if max_val >= 0.9:
                br[0] = max_loc[0] + (width - 1)
                br[1] = max_loc[1] + (height - 1)
                pyautogui.moveTo(br[0], br[1], duration=0)

                wh = [(br[0] - (tl[0] - 1)), (br[1] - (tl[1] - 1))]

    if focus and sum(tl) > 0:
        pyautogui.moveTo(tl[0] + (wh[0] // 2), tl[1] + 10, duration=0)
        pyautogui.click()

    if preview and sum(tl) > 0:
        # pil_image = pyautogui.screenshot()
        # haystack = cv.cvtColor(np.array(pil_image), cv.COLOR_RGB2BGR)
        # cv.drawMarker(haystack, (tl[0], tl[1]), (0, 0, 255), cv.MARKER_CROSS, markerSize=20, thickness=2, line_type=cv.LINE_AA)
        # cv.drawMarker(haystack, (tr[0], tr[1]), (0, 0, 255), cv.MARKER_CROSS, markerSize=20, thickness=2, line_type=cv.LINE_AA)
        # cv.drawMarker(haystack, (bl[0], bl[1]), (0, 0, 255), cv.MARKER_CROSS, markerSize=20, thickness=2, line_type=cv.LINE_AA)
        # cv.drawMarker(haystack, (br[0], br[1]), (0, 0, 255), cv.MARKER_CROSS, markerSize=20, thickness=2, line_type=cv.LINE_AA)
        # preview_window(haystack, 1)

        pil_image = pyautogui.screenshot(region=(tl[0], tl[1], wh[0], wh[1]))
        haystack = cv.cvtColor(np.array(pil_image), cv.COLOR_RGB2BGR)
        preview_window(haystack, 0)

    return [tl, tr, bl, br, wh]


def type_string(string, enter):
    # TODO: what is the default delay between presses?
    for c in string:
        if c.isupper():
            pyautogui.keyDown('shift')
            pyautogui.press(c)
            pyautogui.keyUp('shift')
        else:
            pyautogui.press(c)

    if enter:
        pyautogui.press('enter')

# ---------------------------------------------------------------------------- #


if __name__ == '__main__':

    print('\n#', '-' * 76, '#')
    print('{}'.format(sys.argv[0]))

    print('open "Terminal" -> run some commands...')

    # Fail-Safes, mode is True, moving the mouse to the upper-left
    # will raise a pyautogui.FailSafeException that can abort your program:
    # pyautogui.FAILSAFE = True
    # pyautogui.PAUSE = 0.250
    # TODO: find out how this works

    # TODO: set these automatically
    # os = 'mate'
    # dir = f'img/{os}'
    # print(f'\n{os} {dir}')

    # screen resolution, width x height
    screen_resolution = pyautogui.size()
    print(f'screen_resolution:{screen_resolution}')

    # open terminal window
    # open_terminal_menu()

    # commands = ['uname -a', 'id', 'pwd', 'ls -la #less']
    # commands = ['ifconfig #less', 'cat /etc/resolv.conf', 'netstat -netapl #less']   # network
    # commands = ['cat /etc/passwd #less', 'ps -ef #less']    # running processes
    # cat /etc/ssh/sshd_config
    # commands = ['find / -type f -perm -4000 -print 2>/dev/null #less']
    # commands = ['uname -a']

    session = []
    coordinates = []

    actions = []
    action = {'name': 'setup',
              'pre_requisites': ['minimise_idea', 'coordinates'],
              'commands': [],
              'post_requisites': []}
    actions.append(action)
    action = {'name': 'printenv',
              'pre_requisites': ['focus', 'prompt'],
              'commands': ['enter', 'clear', 'printenv |less'],
              'post_requisites': ['printenv']}
    actions.append(action)

    output = []
    users = []
    flag = False

    for action in actions:
        print(f'\naction : {action["name"]}')

        for pre_requisite in action["pre_requisites"]:
            print(f'\tpre_requisite : {pre_requisite}')
            pre_requisites(pre_requisite)

        for command in action["commands"]:
            print(f'\tcommand : {command}')

            # TODO:
            # `1234567890-=[];'#\,./ shift ¬!"£$%^&*()_+{}:@~|<>?   # UK keyboard layout output
            # `1234567890-=[];'|<,./ shift  !@ $%^&*()_+{}:"|><>?   # .press(key) output
            #                  ^^          ^ ^^            ^^^      # dif
            command = command.replace('|', '#')

            terminal_rows = run_terminal_command(command, progress=False, display=False, preview=False)
            if terminal_rows:
                terminal_parser(command, terminal_rows, session, display=False)

        for post_requisite in action["post_requisites"]:
            print(f'\tpost_requisite : {post_requisite}')
            post_requisites(post_requisite)





            # for i, row in enumerate(terminal_rows):
        # print(f'{i:>2} : {row}')

    # print(f'\noutput : {len(output)}')
    # for i, e in enumerate(output):
    #     for k, v, in e.items():
    #         print(f'\n{i} : {k}')
    #         if isinstance(v, dict):
    #             for key, value, in v.items():
    #                 print(f'{key:>20} : {value}')

    print(f'\nsession : {len(session)}')
    for i, e in enumerate(session):
        for key, value in e.items():
            print(f'{i} {key} : {value}')

    # TODO: try block
    with open('output.json', 'w') as write_file:
        json.dump(session, write_file)     # Python to JSON


cv.destroyAllWindows()

