from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description() -> LaunchDescription:
    address = LaunchConfiguration("address")
    port = LaunchConfiguration("port")
    enable_rosapi = LaunchConfiguration("enable_rosapi")

    rosbridge_node = Node(
        package="rosbridge_server",
        executable="rosbridge_websocket",
        name="rosbridge_websocket",
        output="screen",
        parameters=[
            {
                "address": address,
                "port": ParameterValue(port, value_type=int),
            }
        ],
    )

    rosapi_node = Node(
        package="rosapi",
        executable="rosapi_node",
        name="rosapi_node",
        output="screen",
        condition=IfCondition(enable_rosapi),
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "address",
                default_value="0.0.0.0",
                description="Address rosbridge_websocket binds to.",
            ),
            DeclareLaunchArgument(
                "port",
                default_value="9090",
                description="Port rosbridge_websocket listens on.",
            ),
            DeclareLaunchArgument(
                "enable_rosapi",
                default_value="true",
                description="Start rosapi_node for ROS graph introspection.",
            ),
            rosbridge_node,
            rosapi_node,
        ]
    )
