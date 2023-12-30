#!/bin/sh

script_dir=$(realpath $(dirname "$0"))
pipewire_conf_dir=$script_dir/../../dotfiles/.config/pipewire/pipewire.conf.d
template_path=$script_dir/00-quantum-limits-template.conf
config_path=$pipewire_conf_dir/00-quantum-limits.conf
mkdir -p $pipewire_conf_dir
cp $template_path $config_path
source $script_dir/config.sh
sed -i "s|<min>|$min|;s|<max>|$max|" $config_path
