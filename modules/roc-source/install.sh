#!/bin/sh

script_dir=$(realpath $(dirname "$0"))
pipewire_conf_dir=$script_dir/../../dotfiles/.config/pipewire/pipewire.conf.d
template_path=$script_dir/03-roc-source-template.conf
config_path=$pipewire_conf_dir/03-roc-source.conf
mkdir -p $pipewire_conf_dir
cp $template_path $config_path
source $script_dir/config.sh
sed -i "s|<local-ip>|$local_ip|;s|<local-source-port>|$local_source_port|;s|<local-repair-port>|$local_repair_port|;s|<local-control-port>|$local_control_port|;s|<target-latency-ms>|$target_latency_ms|;s|<playback-sink>|$playback_sink|" $config_path
