#!/bin/sh

script_dir=$(realpath $(dirname "$0"))
pipewire_conf_dir=$script_dir/../../dotfiles/.config/pipewire/pipewire.conf.d
config_path=$pipewire_conf_dir/02-setup-sinks.conf
cd $script_dir
mkdir -p $pipewire_conf_dir
./generate-config > $config_path
