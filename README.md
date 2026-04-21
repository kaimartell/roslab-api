# roslab-api

This folder is a minimal ROS 2 connector package you can publish as its own GitHub repository.

It does not include any demo nodes or teaching packages. It only provides:

- `rosbridge_websocket` on a configurable port
- `rosapi_node` for browser-side graph introspection
- a small HTTP API on a configurable port so the frontend has stable health and metadata endpoints

The goal is to let you clone one package into any ROS 2 environment, build it, run it, and expose that environment to the frontend.

## What this package does

When launched, it starts:

- `rosbridge_websocket`
- `rosapi_node`
- `roslab_api` HTTP server

It does not start or manage demos.
It exposes the ROS graph that is already running in your environment and ROS domain.

## What this package does not do

- no learner demo packages
- no launch catalog
- no demo start/stop manager
- no concept-code session runner

The HTTP API is intentionally minimal. Launch-related endpoints return empty data or "not configured" responses.

## Recommended use

Clone this repository into the `src/` directory of the ROS workspace you want to expose.

That keeps the bridge in the same environment as your real nodes, custom message packages, and launch files.

## Existing workspace flow

If you already have a workspace such as `~/my_ros_ws`:

```bash
cd ~/my_ros_ws/src
git clone <your-repo-url> roslab_api_repo
cd ..
source /opt/ros/humble/setup.bash
rosdep install --from-paths src/roslab_api_repo --ignore-src -r -y --rosdistro humble
colcon build --packages-select roslab_api
source install/setup.bash
ros2 launch roslab_api bridge_api.launch.py
```

Then point the frontend at:

- `ws://<host>:9090`
- `http://<host>:8000`

## Standalone workspace flow

If you want a small standalone bridge workspace:

```bash
mkdir -p ~/ros2_bridge_ws/src
cd ~/ros2_bridge_ws/src
git clone <your-repo-url> roslab_api_repo
cd ..
source /opt/ros/humble/setup.bash
rosdep install --from-paths src --ignore-src -r -y --rosdistro humble
colcon build --packages-select roslab_api
source install/setup.bash
ros2 launch roslab_api bridge_api.launch.py
```

## Important runtime note

If the target environment has custom message, service, or action types, source that environment before launching the bridge so `rosbridge` and `rosapi` can resolve those interfaces.

Typical order:

```bash
source /opt/ros/humble/setup.bash
source /path/to/your/main_ws/install/setup.bash
source /path/to/bridge_ws/install/setup.bash
ros2 launch roslab_api bridge_api.launch.py
```

If you clone this package directly into the target workspace and build it there, that is already handled.

## Ports

Default ports:

- rosbridge: `9090`
- HTTP API: `8000`

Override them at launch:

```bash
ros2 launch roslab_api bridge_api.launch.py rosbridge_port:=9091 api_port:=8001
```

Bind addresses can also be changed:

```bash
ros2 launch roslab_api bridge_api.launch.py rosbridge_address:=0.0.0.0 api_host:=0.0.0.0
```

## Helper scripts

Two optional helper scripts are included:

- `scripts/install_dependencies.sh`
- `scripts/run_bridge_api.sh`

`install_dependencies.sh` installs `rosdep` and package dependencies for this package.

`run_bridge_api.sh` launches the bridge after your ROS environment is already sourced.

## HTTP API

Exposed endpoints:

- `GET /api/health`
- `GET /api/launch/demos`
- `GET /api/launch/status`
- `GET /api/system/metadata`

Behavior:

- `/api/launch/demos` returns an empty list
- `/api/launch/status` returns an empty list
- `/api/system/metadata` returns lightweight metadata for the bridge nodes only

## Push to GitHub

If you want to publish this folder as its own repository:

```bash
cd /Users/kaimartell/Desktop/Tufts/MSME/Thesis/spring/ros2-education-platform/roslab-api
git init
git add .
git commit -m "Add roslab API bridge package"
git branch -M main
git remote add origin https://github.com/<your-user>/roslab-api.git
git push -u origin main
```

If you prefer creating the repo first in the GitHub UI:

1. Create a new empty repository named `roslab-api`
2. Do not initialize it with a README, `.gitignore`, or license
3. Run the commands above

If you use GitHub CLI instead:

```bash
cd /Users/kaimartell/Desktop/Tufts/MSME/Thesis/spring/ros2-education-platform/roslab-api
git init
git add .
git commit -m "Add roslab API bridge package"
gh repo create roslab-api --public --source=. --remote=origin --push
```

## Files to publish

Publish the contents of this folder as the GitHub repository root:

```text
roslab-api/
```

## Summary

This package is the generic connector layer only. It is meant to sit inside an arbitrary ROS 2 workspace and expose that live ROS environment to the web frontend over standard ports.
