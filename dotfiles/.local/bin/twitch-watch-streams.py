#!/bin/python3

import sys
import subprocess
import os
import tempfile

XDG_RUNTIME_DIR = "XDG_RUNTIME_DIR"


def get_fifo_dir():
    xdg_runtime_dir = os.environ.get(XDG_RUNTIME_DIR)
    if xdg_runtime_dir:
        fifo_dir_path = xdg_runtime_dir
    else:
        fifo_dir_path = tempfile.gettempdir()
    return os.path.join(fifo_dir_path, "twitch-viewer")


def unlink_fifos(stream_fifos):
    for stream_fifo in stream_fifos:
        try:
            os.unlink(stream_fifo)
        except OSError:
            pass


def make_fifos(stream_fifos):
    for stream_fifo in stream_fifos:
        os.mkfifo(stream_fifo)


def start_streamlinks(streams, stream_fifos):
    return [
        subprocess.Popen(
            (
                "streamlink",
                "--twitch-disable-ads",
                "--output",
                stream_fifo,
                f"https://www.twitch.tv/{stream}",
                "best"
            )
        )
        for stream, stream_fifo in zip(streams, stream_fifos)
    ]


streams = list(map(str.rstrip, sys.stdin.readlines()))
num_streams = len(streams)
if num_streams < 2:
    if not num_streams:
        sys.exit(0)
    subprocess.run(("streamlink", "--player", "mpv", f"https://www.twitch.tv/{streams[0]}", "best"))
    sys.exit(0)
fifo_dir_path = get_fifo_dir()
try:
    os.makedirs(fifo_dir_path)
except FileExistsError:
    pass
stream_fifos = [f"{fifo_dir_path}/{stream}" for stream in streams]
unlink_fifos(stream_fifos)
make_fifos(stream_fifos)
streamlink_processes = start_streamlinks(streams, stream_fifos)
ffmpeg_grid_view_process = subprocess.Popen(
    ("ffmpeg-grid-view.py", "--hwaccel_type", "none"), stdin=subprocess.PIPE
)
ffmpeg_grid_view_process.stdin.write("\n".join(stream_fifos).encode("utf-8"))
ffmpeg_grid_view_process.stdin.close()
ffmpeg_grid_view_process.wait()
for streamlink_process in streamlink_processes:
    streamlink_process.kill()
for streamlink_process in streamlink_processes:
    streamlink_process.wait()
unlink_fifos(stream_fifos)
