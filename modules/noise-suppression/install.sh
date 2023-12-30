#!/bin/sh

script_dir=$(realpath $(dirname "$0"))
pipewire_conf_dir=$script_dir/../../dotfiles/.config/pipewire/pipewire.conf.d
nsfv_dir=$script_dir/noise-suppression-for-voice
bin_dir=$nsfv_dir/build-x64/bin
plugin_path=$bin_dir/ladspa/librnnoise_ladspa.so
template_path=$script_dir/99-input-denoising-template.conf
config_path=$pipewire_conf_dir/99-input-denoising.conf
cd $nsfv_dir
cmake -Bbuild-x64 -H. -GNinja -DCMAKE_BUILD_TYPE=Release
ninja -C build-x64
mkdir -p $pipewire_conf_dir
cp $template_path $config_path
sed -i "s|<path-to-plugin>|$plugin_path|" $config_path
