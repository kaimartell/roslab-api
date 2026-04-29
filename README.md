# roslab-api

This package exposes an existing ROS 2 graph to the ROS Lab frontend through rosbridge and rosapi.

It is a small generic connector. Clone it into a ROS 2 workspace that already contains, sources, or can discover the robot nodes and interfaces you want ROS Lab to inspect and interact with.

## Purpose

`roslab_api` launches:

- `rosbridge_server`'s `rosbridge_websocket` on `ws://<host>:9090` by default
- `rosapi`'s `rosapi_node` for graph introspection used by roslib.js

Through rosbridge and rosapi, the frontend can list nodes, topics, topic types, services, node publishers/subscribers/services, and service types. Action support is best-effort; the frontend may infer actions from `/_action/` topics and services when explicit action-server listing is unavailable.

## Install

From an existing ROS 2 workspace:

```bash
cd ~/ros2_ws/src
git clone https://github.com/kaimartell/roslab-api.git
cd ~/ros2_ws
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash
```

If your ROS graph uses custom message, service, or action types, source the workspace that provides those interfaces before launching this bridge.

## Run

Start the connector with the default WebSocket endpoint:

```bash
ros2 launch roslab_api frontend_bridge.launch.py
```

Bind to a custom address or port:

```bash
ros2 launch roslab_api frontend_bridge.launch.py address:=127.0.0.1 port:=9091
```

Launch arguments:

- `address`, default `0.0.0.0`
- `port`, default `9090`
- `enable_rosapi`, default `true`

`rosapi_node` provides ROS graph metadata over rosbridge, such as nodes, topics, services, and type information. Keep it enabled when using ROS Lab's Explore view or other browser tools that need graph introspection; disable it only if you want a narrower bridge that allows topic/service interaction without rosapi metadata services.

## Connect Frontend

Use these rosbridge WebSocket URLs in roslab, hosted at https://kaimartell.github.io/roslab/:

- Local browser and ROS host: `ws://localhost:9090`
- Browser on another machine: `ws://<host-ip>:9090`

The frontend subscribes to selected topics using their reported message type, publishes raw JSON messages to selected topics, calls selected services with raw JSON requests, and can send raw JSON action goals when action name/type information is available.

## Validation

After launch:

```bash
ros2 node list
```

The node list should include `rosbridge_websocket` and `rosapi_node` when `enable_rosapi:=true`.

In the browser or frontend:

- ROS Lab should show `connected`
- The Explore view should list nodes, topics, and services from the running ROS graph

## Network Notes

- Port `9090` must be reachable from the browser machine.
- If using the GitHub Pages HTTPS-hosted frontend, browsers may block plain `ws://`; use a local HTTP-served frontend or provide a `wss://` TLS reverse proxy.
- This connector does not authenticate rosbridge. Use it only on trusted networks unless you add your own network security.

## Scope

This repository is the generic ROS Lab connector only.

It does not start robot demos, manage launch files, provide curated lesson metadata, or serve node code excerpts. The optional ROS Lab HTTP API at `http://<same-host>:8000` is intentionally omitted, so demo controls and curated code panels are unavailable in this generic connector.

## Repository Layout

```text
roslab-api/
├── launch/
│   └── frontend_bridge.launch.py
├── roslab_api/
│   └── __init__.py
├── package.xml
├── setup.cfg
└── setup.py
```

## License

Apache-2.0
