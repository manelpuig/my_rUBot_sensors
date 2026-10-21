"""Launch the ROSbot XL and the optional ENS160 driver."""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, OpaqueFunction
from launch.conditions import IfCondition
from launch.launch_description_sources import (
    AnyLaunchDescriptionSource,
    PythonLaunchDescriptionSource,
)
from launch.substitutions import LaunchConfiguration


def _robot_launch(context):
    mode = LaunchConfiguration("mode").perform(context)
    configuration = LaunchConfiguration("rosbot_configuration")
    arm_activate = LaunchConfiguration("rosbot_arm_activate")
    rviz = LaunchConfiguration("rviz")

    if mode == "simulation":
        source = AnyLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory("rosbot_gazebo"),
                "launch",
                "simulation.yaml",
            )
        )
        arguments = {
            "robot_model": "rosbot_xl",
            "use_sim": "True",
            "configuration": configuration,
            "arm_activate": arm_activate,
            "rviz": rviz,
        }
    else:
        source = AnyLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory("rosbot_bringup"),
                "launch",
                "rosbot_xl.yaml",
            )
        )
        arguments = {
            "configuration": configuration,
            "arm_activate": arm_activate,
        }

    return [
        IncludeLaunchDescription(source, launch_arguments=arguments.items())
    ]


def generate_launch_description():
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
                "mode",
                default_value="hardware",
                choices=["hardware", "simulation"],
            ),
            DeclareLaunchArgument("rosbot_configuration", default_value="basic"),
            DeclareLaunchArgument(
                "rosbot_arm_activate",
                default_value="False",
                choices=["True", "False"],
            ),
            DeclareLaunchArgument(
                "rviz", default_value="True", choices=["True", "False"]
            ),
            DeclareLaunchArgument("sensor_port", default_value="/dev/ens160"),
            DeclareLaunchArgument("sensor_baud_rate", default_value="9600"),
            DeclareLaunchArgument(
                "start_sensor", default_value="true", choices=["true", "false"]
            ),
            OpaqueFunction(function=_robot_launch),
            sensor_launch,
        ]
    )
