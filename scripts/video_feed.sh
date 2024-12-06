#!/bin/bash
set -euo pipefail
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <host to send video feed>"
    exit 1
fi

HOST=$1
rpicam-vid -t 0 --camera 0 --nopreview --codec yuv420 --width 1280 --height 720 --inline --listen -o - | ffmpeg -f rawvideo -pix_fmt yuv420p -s:v 1280x720 -i /dev/stdin -c:v libx264 -preset ultrafast -tune zerolatency -f rtsp rtsp://${HOST}:8554/picam