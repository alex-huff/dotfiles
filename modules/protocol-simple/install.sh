#!/bin/sh

script_dir=$(realpath $(dirname "$0"))
pipewire_conf_dir=$script_dir/../../dotfiles/.config/pipewire/pipewire.conf.d
template_path=$script_dir/03-protocol-simple-template.conf
config_path=$pipewire_conf_dir/03-protocol-simple.conf
mkdir -p $pipewire_conf_dir
cp $template_path $config_path
source $script_dir/config.sh
sed -i "s|<ip>|$ip|;s|<port>|$port|;s|<capture-sink>|$capture_sink|;s|<rate>|$rate|;s|<format>|$format|" $config_path
