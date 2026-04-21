from __future__ import annotations


def build_system_metadata() -> dict[str, object]:
    return {
        "packages": {
            "rosbridge_server": {
                "display_name": "rosbridge_server",
                "description": "Bridges the ROS graph to browser clients over WebSocket.",
            },
            "rosapi": {
                "display_name": "rosapi",
                "description": "Provides graph introspection services such as nodes, topics, services, and message types.",
            },
            "roslab_api": {
                "display_name": "roslab_api",
                "description": "Small helper package that launches rosbridge, rosapi, and a lightweight HTTP API for the frontend.",
            },
        },
        "nodes": {
            "rosbridge_websocket": {
                "display_name": "Browser Bridge",
                "package_name": "rosbridge_server",
                "description": "Accepts browser WebSocket connections and forwards ROS traffic.",
            },
            "rosapi_node": {
                "display_name": "Graph Introspection",
                "package_name": "rosapi",
                "description": "Answers browser questions about the live ROS graph.",
            },
            "bridge_api_server": {
                "display_name": "Bridge API",
                "package_name": "roslab_api",
                "description": "Serves health and metadata endpoints for the frontend.",
            },
        },
        "topics": {},
        "services": {},
        "actions": {},
        "topic_details": {},
        "service_details": {},
        "action_details": {},
    }
