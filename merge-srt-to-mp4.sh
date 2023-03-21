#!/bin/bash

if [ $# -ne 2 ]; then
  echo "Usage: $0 <video_file.mp4> <subtitle_file.srt>"
  exit 1
fi

if [ ! -f "$1" ]; then
  echo "Error: File $1 not found."
  exit 1
fi

if [ ! -f "$2" ]; then
  echo "Error: File $2 not found."
  exit 1
fi

output_file="${1%.*}_subtitled.mp4"

ffmpeg -i "$1" -vf subtitles="$2:force_style='Fontsize=28'" -c:a copy "$output_file"

echo "Done. Subtitled video saved as: $output_file"

