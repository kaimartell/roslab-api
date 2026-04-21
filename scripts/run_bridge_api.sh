#!/usr/bin/env bash

set -euo pipefail

if ! command -v ros2 >/dev/null 2>&1; then
  echo "ros2 is not available in the current shell."
  echo "Source your ROS environment and workspace first."
  exit 1
fi

exec ros2 launch roslab_api bridge_api.launch.py "$@"
