#!/usr/bin/env bash

set -euo pipefail

PACKAGE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [[ -z "${ROS_DISTRO:-}" ]]; then
  echo "ROS_DISTRO is not set."
  echo "Source your ROS installation first, for example:"
  echo "  source /opt/ros/humble/setup.bash"
  exit 1
fi

if ! command -v apt-get >/dev/null 2>&1; then
  echo "This helper currently supports apt-based Ubuntu ROS environments."
  echo "Install rosdep and this package's dependencies manually on your platform."
  exit 1
fi

if ! command -v rosdep >/dev/null 2>&1 || ! command -v colcon >/dev/null 2>&1; then
  sudo apt-get update
  sudo apt-get install -y python3-colcon-common-extensions python3-rosdep
fi

if [[ ! -f /etc/ros/rosdep/sources.list.d/20-default.list ]]; then
  sudo rosdep init
fi

rosdep update
rosdep install \
  --from-paths "${PACKAGE_DIR}" \
  --ignore-src \
  -r \
  -y \
  --rosdistro "${ROS_DISTRO}"

echo
echo "Dependencies installed for roslab_api."
echo "Build it from your workspace root with:"
echo "  colcon build --packages-select roslab_api"
