#!/usr/bin/env bash
#
# This script updates a systemd unit file from a specified location, 
# reloads systemd, and ensures the service is enabled and running.
#
# Usage: ./update_service.sh <unit-file-name> <source-path>
#
# Example:
# ./update_service.sh my_service.service /tmp/my_service.service

UNIT_NAME="$1"
SOURCE_PATH="$2"
SYSTEMD_PATH="/etc/systemd/system"

# Check arguments
if [ -z "$UNIT_NAME" ] || [ -z "$SOURCE_PATH" ]; then
    echo "Usage: $0 <unit-file-name> <source-path>"
    exit 1
fi

# Ensure the source file exists
if [ ! -f "$SOURCE_PATH" ]; then
    echo "Error: Source file $SOURCE_PATH not found."
    exit 1
fi

echo "Updating $UNIT_NAME from $SOURCE_PATH..."

# Copy unit file into systemd directory
sudo cp "$SOURCE_PATH" "$SYSTEMD_PATH/$UNIT_NAME"

# Set proper permissions
sudo chmod 644 "$SYSTEMD_PATH/$UNIT_NAME"

# Reload systemd to pick up changes
sudo systemctl daemon-reload

# Enable the service so it starts on boot
sudo systemctl enable "$UNIT_NAME"

# Start (or restart) the service
sudo systemctl restart "$UNIT_NAME"

# Print the status for verification
systemctl status "$UNIT_NAME"

echo "$UNIT_NAME has been updated and (re)started successfully."
