# For interacting with the os
import os
# For interacting with the system
import sys
# For reading individual character inputs (depends on operating system)
if os.name == "nt":
    import msvcrt
else:
    import tty
    import termios


redstyle = "\033[91m"
greenstyle = "\033[92m"
bluestyle = "\033[94m"
yellowstyle = "\033[93m"
violetstyle = "\033[95m"
stylereset = "\033[0m"
dim = "\033[2m"
bold = "\033[1m"


def _get_char():
    """ Reads individual characters """
    if os.name == "nt":
        return msvcrt.getch().decode("utf-8", "ignore")
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
    return ch


def color_input(prompt, color="\033[97m"):
    """ Colors the characters and prints them """
    sys.stdout.write(prompt)
    sys.stdout.flush()
    chars = []
    while True:
        ch = _get_char()
        if ch in ("\r", "\n"):
            sys.stdout.write("\n")
            break
        if ch == "\x03":
            raise KeyboardInterrupt
        if ch in ("\x08", "\x7f"):
            if chars:
                chars.pop()
                sys.stdout.write("\b \b")
                sys.stdout.flush()
            continue
        chars.append(ch)
        sys.stdout.write(color + ch + stylereset)
        sys.stdout.flush()
    return "".join(chars)


def clear_console():
    os.system("cls" if os.name == "nt" else "clear")