#!/bin/bash

input_filepath="1T2G_icon_1024.png"
output_iconset_name="1T2G.iconset"
sips -z 16 16     $input_filepath --out ".${output_iconset_name}/icon_16x16.png"
sips -z 32 32     $input_filepath --out ".${output_iconset_name}/icon_16x16@2x.png"
sips -z 32 32     $input_filepath --out ".${output_iconset_name}/icon_32x32.png"
sips -z 64 64     $input_filepath --out ".${output_iconset_name}/icon_32x32@2x.png"
sips -z 128 128   $input_filepath --out ".${output_iconset_name}/icon_128x128.png"
sips -z 256 256   $input_filepath --out ".${output_iconset_name}/icon_128x128@2x.png"
sips -z 256 256   $input_filepath --out ".${output_iconset_name}/icon_256x256.png"
sips -z 512 512   $input_filepath --out ".${output_iconset_name}/icon_256x256@2x.png"
sips -z 512 512   $input_filepath --out ".${output_iconset_name}/icon_512x512.png"

