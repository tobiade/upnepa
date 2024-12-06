#!/bin/bash
set -euo pipefail
./register_service.sh "mediamtx.service" "/home/tobi/Development/upnepa/systemd/mediamtx.service"
./register_service.sh "socket_server.service" "/home/tobi/Development/upnepa/systemd/socket_server.service"