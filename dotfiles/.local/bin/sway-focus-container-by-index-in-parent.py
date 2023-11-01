#!/bin/python

import argparse
import subprocess
import json
import sys

NODES = "nodes"
FOCUSED = "focused"
ID = "id"
SWAYMSG = "swaymsg"

def get_siblings_of_focused_container(tree):
	children = tree[NODES]
	for container in children:
		if container[FOCUSED]:
			return children
	for container in children:
		siblings_of_focused_container = get_siblings_of_focused_container(container)
		if siblings_of_focused_container:
			return siblings_of_focused_container

parser = argparse.ArgumentParser(
	prog="sway-focus-container-by-index-in-parent",
	description="Focus a container by its index in its parent",
)
parser.add_argument(
	"index",
	type=int,
	help=f"the index of the container to focus",
)
arguments = parser.parse_args()
swaymsg_process = subprocess.Popen((SWAYMSG, "-t", "get_tree"), stdout=subprocess.PIPE)
tree_json = json.load(swaymsg_process.stdout)
siblings_of_focused_container = get_siblings_of_focused_container(tree_json)
index = arguments.index
if index < 0 or index >= len(siblings_of_focused_container):
	print("invalid index", file=sys.stderr)
	sys.exit(1)
container_id = siblings_of_focused_container[index][ID]
subprocess.run((SWAYMSG, f"[con_id = {container_id}] focus"))
swaymsg_process.wait()
