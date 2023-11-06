#!/bin/sh

script_dir=$(realpath $(dirname "$0"))
nsfv_dir=$script_dir/noise-suppression-for-voice
bin_dir=$nsfv_dir/build-x64/bin/
cd $nsfv_dir
cmake -Bbuild-x64 -H. -GNinja -DCMAKE_BUILD_TYPE=Release
ninja -C build-x64
ln -s $bin_dir $script_dir/../../dotfiles/.local/bin/noise-suppression-for-voice
