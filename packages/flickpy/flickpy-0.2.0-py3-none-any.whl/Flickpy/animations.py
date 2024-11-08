import sys
import time
import threading
import shutil
import re

stop_event = threading.Event()

def get_terminal_width():
    return shutil.get_terminal_size().columns

def progress_bar_fill():
    width = get_terminal_width() - 2
    for i in range(width + 1):
        if stop_event.is_set():
            break
        sys.stdout.write(f"\r{'█' * i}{' ' * (width - i)}")
        sys.stdout.flush()
        time.sleep(0.05)

def rotating_bar():
    width = get_terminal_width() - 2
    frames = "|/-\\"
    while not stop_event.is_set():
        for frame in frames:
            sys.stdout.write(f"\r{frame}" + " " * (width - 10))
            sys.stdout.flush()
            time.sleep(0.1)

def expanding_blocks():
    width = get_terminal_width() - 2
    for i in range(1, width // 2):
        if stop_event.is_set():
            break
        sys.stdout.write(f"\r{'█' * i} " + " " * (width - i))
        sys.stdout.flush()
        time.sleep(0.1)

def bouncing_bar():
    width = get_terminal_width() - 2
    for i in range(width):
        if stop_event.is_set():
            break
        sys.stdout.write(f"\r{' ' * i}█{' ' * (width - i - 1)}")
        sys.stdout.flush()
        time.sleep(0.05)

def sliding_dots():
    width = get_terminal_width() - 2
    while not stop_event.is_set():
        for i in range(width):
            sys.stdout.write(f"\r{' ' * i}." + ' ' * (width - i - 1))
            sys.stdout.flush()
            time.sleep(0.05)

def pulse_blocks():
    width = get_terminal_width() - 2
    for i in range(width):
        if stop_event.is_set():
            break
        sys.stdout.write(f"\r{'█' * (i % width)}" + ' ' * (width - (i % width)))
        sys.stdout.flush()
        time.sleep(0.07)

def loading_wave():
    width = get_terminal_width() - 2
    wave = ['.   ', '..  ', '... ', '....']
    while not stop_event.is_set():
        for i in wave:
            sys.stdout.write(f"\r{i}" + " " * (width - len(i)))
            sys.stdout.flush()
            time.sleep(0.15)

def blinking_blocks():
    width = get_terminal_width() - 2
    while not stop_event.is_set():
        sys.stdout.write("\r" + "█" * width)
        sys.stdout.flush()
        time.sleep(0.2)
        sys.stdout.write("\r" + " " * width)
        sys.stdout.flush()
        time.sleep(0.2)

animations = {
    "Progress Bar Fill": progress_bar_fill,
    "Rotating Bar": rotating_bar,
    "Expanding Blocks": expanding_blocks,
    "Bouncing Bar": bouncing_bar,
    "Sliding Dots": sliding_dots,
    "Pulse Blocks": pulse_blocks,
    "Loading Wave": loading_wave,
    "Blinking Blocks": blinking_blocks
}

def run_animation(animation_name, duration_str):
    global stop_event
    stop_event.clear()
    animation_func = animations.get(animation_name)
    if animation_func:
        duration = parse_duration(duration_str)
        animation_thread = threading.Thread(target=animation_func)
        animation_thread.start()
        time.sleep(duration)
        stop_event.set()
        animation_thread.join()
        sys.stdout.write("\r" + " " * 40 + "\r")

def list_animations():
    return list(animations.keys())

def parse_duration(duration_str):
    pattern = re.compile(r'(?P<value>\d+)(?P<unit>[smh])')
    match = pattern.match(duration_str.lower())
    if match:
        value = int(match.group('value'))
        unit = match.group('unit')
        if unit == 's':
            return value
        elif unit == 'm':
            return value * 60
        elif unit == 'h':
            return value * 3600
    else:
        raise ValueError(f"Invalid time format: {duration_str}")
