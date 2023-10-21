#!/bin/python

from enum import Enum, auto
import math
import sys
import subprocess
import argparse

DECODE_MASK = 2**0
ENCODE_MASK = 2**1
INDIVIDUAL_MASK = 2**0
MIXED_MASK = 2**1
HW_DEVICE_NAME = "hadev"
DEFAULT_VAAPI_DEVICE = "/dev/dri/renderD128"
DEFAULT_VLC_FILE_CACHING = 3000
DEFAULT_FILE_PATH = "output.mkv"
DEFAULT_TARGET_WIDTH = 1920
DEFAULT_TARGET_HEIGHT = 1080


class HWAccelType(Enum):
    none = None
    vaapi = "vaapi"

    def should_hwaccel(self):
        return self != HWAccelType.none

    def get_api_name(self):
        return self.value

    def get_hw_format(self):
        return self.get_api_name()

    def get_upload_format(self):
        match self:
            case HWAccelType.vaapi:
                return "nv12"

    def get_encode_codec(self):
        match self:
            case HWAccelType.vaapi:
                return "hevc_vaapi"


DEFAULT_HWACCEL_TYPE = HWAccelType.vaapi


class HWAccelMode(Enum):
    none = 0
    d = DECODE_MASK
    e = ENCODE_MASK
    de = DECODE_MASK | ENCODE_MASK

    def should_decode(self):
        return self.value & DECODE_MASK

    def should_encode(self):
        return self.value & ENCODE_MASK


DEFAULT_HWACCEL_MODE = HWAccelMode.de


class OutputMode(Enum):
    file = auto()
    stdout = auto()
    vlc = auto()
    ffplay = auto()

    def is_player(self):
        match self:
            case OutputMode.vlc | OutputMode.ffplay:
                return True
        return False

    def get_player_name(self):
        if self.is_player():
            return self.name
        return None


DEFAULT_OUTPUT_MODE = OutputMode.ffplay


class AudioMode(Enum):
    none = 0
    i = INDIVIDUAL_MASK
    m = MIXED_MASK
    im = INDIVIDUAL_MASK | MIXED_MASK

    def should_include_individual_tracks(self):
        return self.value & INDIVIDUAL_MASK

    def should_include_mixed_track(self):
        return self.value & MIXED_MASK


DEFAULT_AUDIO_MODE = AudioMode.im


class Settings:
    def __init__(
        self,
        target_width,
        target_height,
        hwaccel_type,
        hwaccel_mode,
        audio_mode,
        output_mode,
        vaapi_device,
        vlc_file_caching,
        file_path,
    ):
        self.target_width = target_width
        self.target_height = target_height
        self.hwaccel_type = hwaccel_type
        self.hwaccel_mode = hwaccel_mode
        self.audio_mode = audio_mode
        self.output_mode = output_mode
        self.vaapi_device = vaapi_device
        self.vlc_file_caching = vlc_file_caching
        self.file_path = file_path

    def get_hwaccel_device(self):
        match self.hwaccel_type:
            case HWAccelType.vaapi:
                return self.vaapi_device


def get_grid_dimensions_for_num_inputs(settings, num_inputs):
    intermediate_dim = 1 + math.sqrt(4 * num_inputs - 3) / 2
    row, col = math.floor(intermediate_dim - 0.5), math.floor(intermediate_dim)
    downscale_ratio = max(row, col)
    grid_tile_width, grid_tile_height = math.floor(
        settings.target_width / downscale_ratio
    ), math.floor(settings.target_height / downscale_ratio)
    return row, col, grid_tile_width, grid_tile_height


def ffmpeg_build_hwaccel_device_args(command, settings):
    command.append("-init_hw_device")
    command.append(
        f"{settings.hwaccel_type.get_api_name()}={HW_DEVICE_NAME}:{settings.get_hwaccel_device()}"
    )


def ffmpeg_build_inputs(
    command, settings, input_files, grid_size, grid_tile_width, grid_tile_height
):
    should_decode = settings.hwaccel_mode.should_decode()
    should_encode = settings.hwaccel_mode.should_encode()
    for input_file in input_files:
        if should_decode:
            command.append("-hwaccel")
            command.append(settings.hwaccel_type.get_api_name())
            command.append("-hwaccel_device")
            command.append(HW_DEVICE_NAME)
            if should_encode:
                command.append("-hwaccel_output_format")
                command.append(settings.hwaccel_type.get_api_name())
        command.append("-i")
        command.append(input_file)
    if len(input_files) < grid_size:
        command.append("-f")
        command.append("lavfi")
        command.append("-i")
        command.append(
            f"color=size={grid_tile_width}x{grid_tile_height}:duration=1us:color=black"
        )


def ffmpeg_build_maps_and_metadata(command, settings, input_files):
    should_include_individual_tracks = settings.audio_mode.should_include_individual_tracks()
    should_include_mixed_track = settings.audio_mode.should_include_mixed_track()
    if should_include_mixed_track:
        command.append("-map")
        command.append("[mixed]")
        command.append("-metadata:s:a:0")
        command.append("title=mixed")
    if should_include_individual_tracks:
        for i in range(len(input_files)):
            input_file = input_files[i]
            metadata_offset = i + 1 if should_include_mixed_track else i
            command.append("-map")
            command.append(f"{i}:a:0")
            command.append(f"-metadata:s:a:{metadata_offset}")
            command.append(f"title={input_file}")
    command.append("-map")
    command.append("[grid]")


def ffmpeg_build_filtergraph(
    command, settings, num_inputs, row, col, grid_tile_width, grid_tile_height
):
    should_decode = settings.hwaccel_mode.should_decode()
    should_encode = settings.hwaccel_mode.should_encode()
    should_include_mixed_track = settings.audio_mode.should_include_mixed_track()
    upload_format = settings.hwaccel_type.get_upload_format()
    hw_format = settings.hwaccel_type.get_hw_format()
    pix_fmts = (
        "yuv420p"
        if not should_encode
        else (f"{upload_format}|{hw_format}" if should_decode else f"{upload_format}")
    )
    xstack_preperation_filter = (
        "hwupload"
        if should_encode
        else f"scale=width={grid_tile_width}:height={grid_tile_height}"
    )
    grid_size = row * col
    filtergraph_builder = []
    if should_include_mixed_track:
        for i in range(num_inputs):
            filtergraph_builder.append(f"[{i}:a:0]")
        filtergraph_builder.append(f"amix=inputs={num_inputs}[mixed];")
    if should_encode:
        command.append("-filter_hw_device")
        command.append(HW_DEVICE_NAME)
    command.append("-filter_complex")
    input_filterchain = f"format=pix_fmts={pix_fmts},{xstack_preperation_filter}"
    i = 0
    for i in range(num_inputs):
        filtergraph_builder.append(f"[{i}:v:0]{input_filterchain}[tile:{i}];")
    i += 1
    for n in range(i, grid_size):
        filtergraph_builder.append(f"[{i}:v:0]{input_filterchain}[tile:{n}];")
    for u in range(grid_size):
        filtergraph_builder.append(f"[tile:{u}]")
    filtergraph_builder.append(
        f"{'xstack_vaapi' if should_encode else 'xstack'}=grid={col}x{row}{f':grid_tile_size={grid_tile_width}x{grid_tile_height}' if should_encode else ''}[grid]"
    )
    command.append("".join(filtergraph_builder))


def ffmpeg_build_output(command, settings):
    if settings.hwaccel_mode.should_encode():
        command.append("-c:v")
        command.append(settings.hwaccel_type.get_encode_codec())
    if settings.output_mode != OutputMode.file:
        command.append("-flush_packets")
        command.append("1")
    command.append("-f")
    command.append("matroska")
    match settings.output_mode:
        case OutputMode.file:
            command.append(settings.file_path)
        case _:
            command.append("pipe:1")


def ffmpeg_build_command(
    command, settings, input_files, row, col, grid_tile_width, grid_tile_height
):
    command.append("ffmpeg")
    command.append("-nostdin")
    command.append("-y")
    if settings.hwaccel_type.should_hwaccel():
        ffmpeg_build_hwaccel_device_args(command, settings)
    ffmpeg_build_inputs(
        command, settings, input_files, row * col, grid_tile_width, grid_tile_height
    )
    ffmpeg_build_maps_and_metadata(command, settings, input_files)
    ffmpeg_build_filtergraph(
        command, settings, len(input_files), row, col, grid_tile_width, grid_tile_height
    )
    ffmpeg_build_output(command, settings)


def player_build_command(command, settings):
    command.append(settings.output_mode.get_player_name())
    match settings.output_mode:
        case OutputMode.vlc:
            command.append(f"--file-caching={settings.vlc_file_caching}")
        case OutputMode.ffplay:
            command.append("-infbuf")
    command.append("-")


parser = argparse.ArgumentParser(
    prog="ffmpeg-grid-view",
    description="Assemble multiple video files from stdin into a grid view",
)
parser.add_argument(
    "--target_width",
    default=DEFAULT_TARGET_WIDTH,
    type=int,
    help=f"Target width for output video. Default: {DEFAULT_TARGET_WIDTH}",
)
parser.add_argument(
    "--target_height",
    default=DEFAULT_TARGET_HEIGHT,
    type=int,
    help=f"Target height for output video. Default: {DEFAULT_TARGET_HEIGHT}",
)
parser.add_argument(
    "--hwaccel_type",
    choices=[hwaccel_type.name for hwaccel_type in HWAccelType],
    default=DEFAULT_HWACCEL_TYPE.name,
    help=f"Which hardware acceleration api to use if any. Default: {DEFAULT_HWACCEL_TYPE.name}",
)
parser.add_argument(
    "--hwaccel_mode",
    choices=[hwaccel_mode.name for hwaccel_mode in HWAccelMode],
    default=DEFAULT_HWACCEL_MODE.name,
    help=f"Whether hardware acceleration should be used for decode and encode. Default: {DEFAULT_HWACCEL_MODE.name}",
)
parser.add_argument(
    "--audio_mode",
    choices=[audio_mode.name for audio_mode in AudioMode],
    default=DEFAULT_AUDIO_MODE.name,
    help=f"Which audio tracks to include if any. 'i' stands for individual tracks, 'm' stands for mixed track. Default: {DEFAULT_AUDIO_MODE.name}",
)
parser.add_argument(
    "--output_mode",
    choices=[output_mode.name for output_mode in OutputMode],
    default=DEFAULT_OUTPUT_MODE.name,
    help=f"Where the video should be sent. Default: {DEFAULT_OUTPUT_MODE.name}",
)
parser.add_argument(
    "--vaapi_device",
    default=DEFAULT_VAAPI_DEVICE,
    help=f"The render node to use for vaapi hardware acceleration. Default: {DEFAULT_VAAPI_DEVICE}",
)
parser.add_argument(
    "--vlc_file_caching",
    default=DEFAULT_VLC_FILE_CACHING,
    type=int,
    help=f"How many milliseconds of video VLC should cache. Default: {DEFAULT_VLC_FILE_CACHING}",
)
parser.add_argument(
    "--file_path",
    default=DEFAULT_FILE_PATH,
    help=f"Output filepath for 'file' output mode. Default: {DEFAULT_FILE_PATH}",
)
arguments = parser.parse_args()
hwaccel_type = HWAccelType[arguments.hwaccel_type]
hwaccel_mode = (
    HWAccelMode[arguments.hwaccel_mode]
    if hwaccel_type.should_hwaccel()
    else HWAccelMode.none
)
settings = Settings(
    arguments.target_width,
    arguments.target_height,
    hwaccel_type,
    hwaccel_mode,
    AudioMode[arguments.audio_mode],
    OutputMode[arguments.output_mode],
    arguments.vaapi_device,
    arguments.vlc_file_caching,
    arguments.file_path,
)
input_files = list(map(str.rstrip, sys.stdin.readlines()))
num_inputs = len(input_files)
if num_inputs < 2:
    print("a minimum of 2 inputs is required", file=sys.stderr)
    exit(1)
ffmpeg_command = []
ffmpeg_build_command(
    ffmpeg_command,
    settings,
    input_files,
    *get_grid_dimensions_for_num_inputs(settings, num_inputs),
)
output_is_player = settings.output_mode.is_player()
ffmpeg_process = subprocess.Popen(
    ffmpeg_command, stdout=subprocess.PIPE if output_is_player else None
)
if output_is_player:
    player_command = []
    player_build_command(player_command, settings)
    player_process = subprocess.Popen(player_command, stdin=ffmpeg_process.stdout)
    player_process.wait()
    ffmpeg_process.kill()
ffmpeg_process.wait()
