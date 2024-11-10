#!/bin/sh

original_dir=$(pwd)
cd ~/.lol-data
archive_path="ddragon.tgz"
data_dir="data"
output_dir="ddragon-data"
newest_version=$(curl "https://ddragon.leagueoflegends.com/api/versions.json" 2>/dev/null | jq -r ".[0]")
data_url="https://ddragon.leagueoflegends.com/cdn/dragontail-${newest_version}.tgz"
certificate_path="riotgames.pem"
certificate_url="https://static.developer.riotgames.com/docs/lol/riotgames.pem"

rm -rf $data_dir/*
wget -O $certificate_path $certificate_url
wget -O $archive_path $data_url
tar -C $data_dir -xzf $archive_path
rm $archive_path
mv $data_dir/$newest_version $data_dir/$output_dir
cd $original_dir
