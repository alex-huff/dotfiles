#!/bin/python

from subprocess import run

state_prefix = "/home/alex/.config/midi-macros/state/eww-slider-"
with open(f"{state_prefix}r") as rFile, open(f"{state_prefix}g") as gFile, open(f"{state_prefix}b") as bFile:
    light_r = int(rFile.readline())
    light_g = int(gFile.readline())
    light_b = int(bFile.readline())
max_color_component = max(light_r, light_g, light_b)
if not max_color_component:
    adjusted_light_r = adjusted_light_g = adjusted_light_b = 255
else:
    adjusted_light_r = round((light_r / max_color_component) * 255)
    adjusted_light_g = round((light_g / max_color_component) * 255)
    adjusted_light_b = round((light_b / max_color_component) * 255)
run(["eww", "update", f'adjusted-color=rgb({adjusted_light_r}, {adjusted_light_g}, {adjusted_light_b})'])
