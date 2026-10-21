# Workspace setup

The mecanum rUBot and ROSbot XL use separate ROS 2 distributions and separate
workspaces. The sensor repositories share source code, but each workspace has
its own `build`, `install`, and `log` directories.

## Mecanum workspace: Ubuntu 22.04 and ROS 2 Humble

```bash
mkdir -p ~/my_rUBot_sensor_ws/src
cd ~/my_rUBot_sensor_ws/src
git clone https://github.com/manelpuig/my_rUBot_mecanum.git
git clone https://github.com/manelpuig/ENS160_air_quality.git
git clone https://github.com/manelpuig/my_rUBot_sensors.git

cd ~/my_rUBot_sensor_ws
source /opt/ros/humble/setup.bash
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash
```

Start the physical mecanum robot and sensor:

```bash
ros2 launch rubot_sensor_bringup ens160_robot.launch.py \
  robot:=mecanum \
  mode:=hardware \
  start_sensor:=true
```

Mecanum simulation is not yet provided through this combined launch.

## ROSbot workspace: Ubuntu 24.04 and ROS 2 Jazzy

First install the official Husarion source workspace by following
`my_rUBot_rosbot/Documentation/01_rosbot_setup.md`. Then add the custom
repositories:

```bash
cd ~/rosbot_ws/src
git clone https://github.com/manelpuig/my_rUBot_rosbot.git
git clone https://github.com/manelpuig/ENS160_air_quality.git
git clone https://github.com/manelpuig/my_rUBot_sensors.git

cd ~/rosbot_ws
source /opt/ros/jazzy/setup.bash
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash
```

Start the official ROSbot XL simulation without physical ENS160 hardware:

```bash
ros2 launch rubot_sensor_bringup ens160_robot.launch.py \
  robot:=rosbot \
  mode:=simulation \
  start_sensor:=false
```

Start the physical ROSbot XL and ENS160 driver:

```bash
ros2 launch rubot_sensor_bringup ens160_robot.launch.py \
  robot:=rosbot \
  mode:=hardware \
  start_sensor:=true
```

The hardware command requires the official ROSbot and ENS160 device setup to
be complete. Test movement with the wheels raised or in a clear area.

## Useful launch arguments

Common arguments:

| Argument | Values | Default |
| --- | --- | --- |
| `robot` | `mecanum`, `rosbot` | `mecanum` |
| `mode` | `hardware`, `simulation` | `hardware` |
| `start_sensor` | `true`, `false` | `true` |
| `sensor_port` | Serial device path | `/dev/ens160` |
| `sensor_baud_rate` | Integer baud rate | `9600` |

ROSbot-specific arguments:

| Argument | Purpose | Default |
| --- | --- | --- |
| `rosbot_configuration` | Official Husarion configuration | `basic` |
| `rosbot_arm_activate` | Activate the manipulator | `False` |
| `rviz` | Start RViz in simulation | `True` |

The workspace directory is not a Git repository. Run Git commands from the
individual repositories below `src/`.
