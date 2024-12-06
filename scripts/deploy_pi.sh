#!/bin/bash
set -euo pipefail
./register_service.sh "/home/tobi/Development/upnepa/systemd/led_controller.service"
./register_service.sh "/home/tobi/Development/upnepa/systemd/video_feed.service"