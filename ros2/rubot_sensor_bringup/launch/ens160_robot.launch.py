"""Select the robot-specific ENS160 bringup."""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, OpaqueFunction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def _select_robot_launch(context):
    robot = LaunchConfiguration("robot").perform(context)
    mode = LaunchConfiguration("mode").perform(context)

    if robot == "mecanum" and mode != "hardware":
        raise RuntimeError("The mecanum bringup currently supports mode:=hardware only")

    launch_file = f"{robot}_ens160.launch.py"
    return [
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(
                    get_package_share_directory("rubot_sensor_bringup"),
                    "launch",
                    launch_file,
                )
            )
        )
    ]


def generate_launch_description():
    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "robot",
                default_value="mecanum",
                choices=["mecanum", "rosbot"],
                description="Robot platform to start.",
            ),
            DeclareLaunchArgument(
                "mode",
                default_value="hardware",
                choices=["hardware", "simulation"],
                description="Run physical hardware or a simulator.",
            ),
            DeclareLaunchArgument(
                "start_sensor",
                default_value="true",
                choices=["true", "false"],
                description="Start the physical ENS160 serial driver.",
            ),
            DeclareLaunchArgument("sensor_port", default_value="/dev/ens160"),
            DeclareLaunchArgument("sensor_baud_rate", default_value="9600"),
            DeclareLaunchArgument(
                "robot_model", default_value="rubot_arm/my_simple_robot.urdf"
            ),
            DeclareLaunchArgument("robot_port", default_value="/dev/robot_arduino"),
            DeclareLaunchArgument("lidar_port", default_value="/dev/robot_lidar"),
            DeclareLaunchArgument("lidar_frame_id", default_value="base_scan"),
            DeclareLaunchArgument("camera_device", default_value="/dev/robot_camera"),
            DeclareLaunchArgument("camera_width", default_value="640"),
            DeclareLaunchArgument("camera_height", default_value="480"),
            DeclareLaunchArgument("camera_pixel_format", default_value="YUYV"),
            DeclareLaunchArgument("camera_output_encoding", default_value="rgb8"),
            DeclareLaunchArgument("rosbot_configuration", default_value="basic"),
            DeclareLaunchArgument(
                "rosbot_arm_activate",
                default_value="False",
                choices=["True", "False"],
            ),
            DeclareLaunchArgument(
                "rviz", default_value="True", choices=["True", "False"]
            ),
            OpaqueFunction(function=_select_robot_launch),
        ]
    )
