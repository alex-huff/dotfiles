#!/bin/sh

script_dir=$(realpath $(dirname "$0"))
pipewire_conf_dir=$script_dir/../../dotfiles/.config/pipewire/pipewire.conf.d
template_path=$script_dir/01-roc-sink-template.conf
config_path=$pipewire_conf_dir/01-roc-sink.conf
mkdir -p $pipewire_conf_dir
cp $template_path $config_path
source $script_dir/config.sh
sed -i "s|<remote-ip>|$remote_ip|;s|<remote-source-port>|$remote_source_port|;s|<remote-repair-port>|$remote_repair_port|;s|<remote-control-port>|$remote_control_port|" $config_path
