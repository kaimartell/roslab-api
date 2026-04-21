from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description() -> LaunchDescription:
    launch_args = [
        DeclareLaunchArgument("enable_rosbridge", default_value="true"),
        DeclareLaunchArgument("rosbridge_address", default_value="0.0.0.0"),
        DeclareLaunchArgument("rosbridge_port", default_value="9090"),
        DeclareLaunchArgument("api_host", default_value="0.0.0.0"),
        DeclareLaunchArgument("api_port", default_value="8000"),
    ]

    rosbridge_node = Node(
        package="rosbridge_server",
        executable="rosbridge_websocket",
        name="rosbridge_websocket",
        output="screen",
        condition=IfCondition(LaunchConfiguration("enable_rosbridge")),
        parameters=[
            {
                "address": LaunchConfiguration("rosbridge_address"),
                "port": ParameterValue(LaunchConfiguration("rosbridge_port"), value_type=int),
            }
        ],
    )

    rosapi_node = Node(
        package="rosapi",
        executable="rosapi_node",
        name="rosapi_node",
        output="screen",
        condition=IfCondition(LaunchConfiguration("enable_rosbridge")),
    )

    api_node = Node(
        package="roslab_api",
        executable="bridge_api_server",
        name="bridge_api_server",
        output="screen",
        arguments=[
            "--host",
            LaunchConfiguration("api_host"),
            "--port",
            LaunchConfiguration("api_port"),
        ],
    )

    return LaunchDescription(launch_args + [rosbridge_node, rosapi_node, api_node])
