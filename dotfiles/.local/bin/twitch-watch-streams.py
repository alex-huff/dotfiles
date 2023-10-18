#!/bin/python

import sys
import subprocess
import math
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
            [
                "streamlink",
                f"https://www.twitch.tv/{stream}",
                "best",
                "--output",
                stream_fifo,
            ]
        )
        for stream, stream_fifo in zip(streams, stream_fifos)
    ]


def get_grid_dimensions_for_num_stream(num_streams):
    intermediate_dim = 1 + math.sqrt(4 * num_streams - 3) / 2
    row, col = math.floor(intermediate_dim - 0.5), math.floor(intermediate_dim)
    downscale = max(row, col)
    grid_tile_width, grid_tile_height = math.floor(
        target_width / downscale
    ), math.floor(target_height / downscale)
    return row, col, grid_tile_width, grid_tile_height


def ffmpeg_build_hwaccel_device_args(command):
    command.append("ffmpeg")
    command.append("-init_hw_device")
    command.append("vaapi=vdev:/dev/dri/renderD129")


def ffmpeg_build_inputs(
    command, stream_fifos, grid_size, grid_tile_width, grid_tile_height
):
    for stream_fifo in stream_fifos:
        command.append("-i")
        command.append(stream_fifo)
    if len(stream_fifos) < grid_size:
        command.append("-f")
        command.append("lavfi")
        command.append("-i")
        command.append(f"color=size={grid_tile_width}x{grid_tile_height}:color=black")


def ffmpeg_build_maps_and_metadata(command, streams):
    for i in range(len(streams)):
        stream = streams[i]
        command.append("-map")
        command.append(f"{i}:a:0")
        command.append(f"-metadata:s:a:{i}")
        command.append(f"title={stream}")
    command.append("-map")
    command.append("[grid]")


def ffmpeg_build_filter(
    command, num_streams, row, col, grid_tile_width, grid_tile_height
):
    command.append("-filter_hw_device")
    command.append("vdev")
    command.append("-filter_complex")
    filter_builder = []
    i = 0
    grid_size = row * col
    for i in range(num_streams):
        filter_builder.append(f"[{i}:v:0]format=nv12,hwupload[uploaded:{i}];")
    i += 1
    for n in range(i, grid_size):
        filter_builder.append(f"[{i}:v:0]format=nv12,hwupload[uploaded:{n}];")
    for u in range(grid_size):
        filter_builder.append(f"[uploaded:{u}]")
    filter_builder.append(
        f"xstack_vaapi=grid={col}x{row}:grid_tile_size={grid_tile_width}x{grid_tile_height}[grid];"
    )
    command.append("".join(filter_builder))


def ffmpeg_build_output(command):
    command.append("-c:v")
    command.append("hevc_vaapi")
    command.append("-f")
    command.append("matroska")
    command.append("pipe:1")


def ffmpeg_build_command(
    command, streams, stream_fifos, row, col, grid_tile_width, grid_tile_height
):
    ffmpeg_build_hwaccel_device_args(command)
    ffmpeg_build_inputs(
        command, stream_fifos, row * col, grid_tile_width, grid_tile_height
    )
    ffmpeg_build_maps_and_metadata(command, streams)
    ffmpeg_build_filter(
        command, len(streams), row, col, grid_tile_width, grid_tile_height
    )
    ffmpeg_build_output(command)


def vlc_build_command(command):
    command.append("vlc")
    command.append("--file-caching=10000")
    command.append("-")


target_width, target_height = 1920, 1080
streams = list(map(str.rstrip, sys.stdin.readlines()))
num_streams = len(streams)

if num_streams == 1:
    subprocess.run(["streamlink", f"https://www.twitch.tv/{streams[0]}", "best"])
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
ffmpeg_command = []
ffmpeg_build_command(
    ffmpeg_command,
    streams,
    stream_fifos,
    *get_grid_dimensions_for_num_stream(num_streams),
)
vlc_command = []
vlc_build_command(vlc_command)
ffmpeg_process = subprocess.Popen(ffmpeg_command, stdout=subprocess.PIPE)
vlc_process = subprocess.Popen(vlc_command, stdin=ffmpeg_process.stdout)
vlc_process.wait()
ffmpeg_process.kill()
ffmpeg_process.wait()
for streamlink_process in streamlink_processes:
    streamlink_process.kill()
for streamlink_process in streamlink_processes:
    streamlink_process.wait()
unlink_fifos(stream_fifos)
