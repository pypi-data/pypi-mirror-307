import ctypes
import dataclasses
import subprocess
from ctypes import wintypes
from enum import Enum
from pathlib import Path
from typing import Callable

import Xlib
import cv2
import numpy as np
from ..frame_reader import LocalVideoFileReader, LocalDirReader, FrameReader
from ..recorder import AbstractRecorder, SimpleRecorder


class SupportedOS(Enum):
    LINUX = "Linux"
    WINDOWS = "Windows"


@dataclasses.dataclass
class KeyFunction:
    key: str
    func: Callable
    description: str


def get_frame_reader(video_source):
    if isinstance(video_source, (str, Path)):
        path = Path(video_source)
        if path.is_file():
            frame_reader = LocalVideoFileReader(video_source)
        elif path.is_dir():
            frame_reader = LocalDirReader
        else:
            raise IOError(f"{video_source} not found")
    elif isinstance(video_source, FrameReader):
        frame_reader = video_source
    else:
        raise ValueError(
            "video_source can needs to be one of {path to a video file, path to frame folder,"
            " an object of a class that implements FrameReader}"
        )
    return frame_reader


def get_recorder(record):
    if isinstance(record, AbstractRecorder):
        recorder = record
    elif isinstance(record, bool):
        recorder = SimpleRecorder() if record else None
    else:
        raise ValueError(
            "record can needs to be one of {True, False," " an object of a class that implements AbstractRecorder}"
        )
    return recorder


def get_foreground_window_pid():
    h_wnd = ctypes.windll.user32.GetForegroundWindow()
    pid = ctypes.wintypes.DWORD()
    ctypes.windll.user32.GetWindowThreadProcessId(h_wnd, ctypes.byref(pid))
    return pid.value


def hist_eq_uint16(img):
    hist, bins = np.histogram(img.flatten(), 65536, (0, 65536))  # Collect 16 bits histogram (65536 = 2^16).
    cdf = hist.cumsum()

    cdf_m = np.ma.masked_equal(cdf, 0)  # Find the minimum histogram value (excluding 0)
    cdf_m = (cdf_m - cdf_m.min()) * 65535 / (cdf_m.max() - cdf_m.min())
    cdf = np.ma.filled(cdf_m, 0).astype("uint16")

    # Now we have the look-up table...
    hist_eq_img = cdf[img]
    return hist_eq_img


def get_screen_size_linux():
    try:
        screen_size_str = (
            subprocess.check_output('xrandr | grep "\*" | cut -d" " -f4', shell=True).decode().strip().split("\n")[0]
        )
        screen_w, screen_h = screen_size_str.split("x")
        screen_w = 0.9 * int(screen_w)
        screen_h = 0.9 * int(screen_h)
        return screen_w, screen_h
    except (ValueError, TypeError, subprocess.CalledProcessError, IndexError):
        return None, None


def get_screen_size_windows():
    user32 = ctypes.windll.user32
    screensize = 0.9 * user32.GetSystemMetrics(0), 0.9 * user32.GetSystemMetrics(1)
    return screensize


def get_screen_adjusted_frame_size(screen_size, frame_width, frame_height):
    screen_w, screen_h = screen_size
    if screen_w is None:
        return frame_width, frame_height

    adjusted_w = screen_w
    adjusted_h = screen_h
    if screen_w != frame_width:
        w_ratio = screen_w / frame_width
        adjusted_w = screen_w
        adjusted_h = frame_height * w_ratio
    if screen_h < adjusted_h:
        h_ratio = screen_h / adjusted_h
        adjusted_h = screen_h
        adjusted_w *= h_ratio

    return int(adjusted_w), int(adjusted_h)


def is_window_closed_by_mouse_click(window_name):
    return cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1


def get_in_focus_window_id(os: SupportedOS):
    if os == SupportedOS.LINUX:
        window = Xlib.display.Display().get_input_focus().focus
        if isinstance(window, int):
            return ""
        return window.get_wm_name()
    if os == SupportedOS.WINDOWS:
        return get_foreground_window_pid()
    else:
        raise NotImplementedError(f"{os=} not supported")


def get_screen_size(os: SupportedOS):
    if os == SupportedOS.LINUX:
        return get_screen_size_linux()
    if os == SupportedOS.WINDOWS:
        return get_screen_size_windows()
    else:
        raise NotImplementedError(f"{os=} not supported")
