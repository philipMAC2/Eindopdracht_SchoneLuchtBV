import functies as f
import datetime
import numpy as np
from tqdm import tqdm
import time
import matplotlib.pyplot as plt

import curses
import time
from colorama import Fore, Back, Style, init
init(autoreset=True)


def main(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_YELLOW)

    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        stdscr.addstr(0, 0, " " * width, curses.color_pair(1))
        center_text = "SchoneLucht BV"
        center_x = (width - len(center_text)) // 2
        stdscr.addstr(0, center_x, center_text, curses.color_pair(1) | curses.A_BOLD)

        stdscr.refresh()
        time.sleep(1)


curses.wrapper(main)


