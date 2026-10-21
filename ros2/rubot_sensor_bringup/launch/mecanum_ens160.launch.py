"""Launch the physical mecanum rUBot and the optional ENS160 driver."""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    robot_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory("my_robot_bringup"),
                "launch",
                "my_robot_bringup_robust_hw.launch.py",
            )
        ),
        launch_arguments={
            "robot_model": LaunchConfiguration("robot_model"),
            "mecanum_serial_port": LaunchConfiguration("robot_port"),
            "rplidar_serial_port": LaunchConfiguration("lidar_port"),
            "rplidar_frame_id": LaunchConfiguration("lidar_frame_id"),
            "usb_video_device": LaunchConfiguration("camera_device"),
            "camera_width": LaunchConfiguration("camera_width"),
            "camera_height": LaunchConfiguration("camera_height"),
            "camera_pixel_format": LaunchConfiguration("camera_pixel_format"),
            "camera_output_encoding": LaunchConfiguration(
                "camera_output_encoding"
            ),
        }.items(),
    )

    sensor_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory("ens160_air_quality_ros"),
                "launch",
                "air_quality.launch.py",
            )
        ),
        condition=IfCondition(LaunchConfiguration("start_sensor")),
        launch_arguments={
            "port": LaunchConfiguration("sensor_port"),
            "baud_rate": LaunchConfiguration("sensor_baud_rate"),
        }.items(),
    )

    return LaunchDescription(
        [
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
            DeclareLaunchArgument("sensor_port", default_value="/dev/ens160"),
            DeclareLaunchArgument("sensor_baud_rate", default_value="9600"),
            DeclareLaunchArgument(
                "start_sensor", default_value="true", choices=["true", "false"]
            ),
            robot_launch,
            sensor_launch,
        ]
    )
