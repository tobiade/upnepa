#!/bin/bash
set -euo pipefail
./register_service.sh "/home/tobi/Development/upnepa/systemd/mediamtx.service"
./register_service.sh "/home/tobi/Development/upnepa/systemd/socket_server.service"