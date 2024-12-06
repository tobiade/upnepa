#!/bin/bash
set -euo pipefail
scripts/register_service.sh "led_controller.service" "/home/tobi/Development/upnepa/systemd/led_controller.service"
scripts/register_service.sh "video_feed.service" "/home/tobi/Development/upnepa/systemd/video_feed.service"