# Architecture

## Repository boundaries

`my_rUBot_sensors` integrates other projects without copying their source
code. Each repository remains independently versioned and synchronized.

```text
my_rUBot_mecanum (Humble) ──┐
                            ├── rubot_sensor_bringup
ROSbot XL stack (Jazzy) ────┘             │
                                          ▼
ENS160_air_quality ──────────────> rubot_ens160_mapping
```

`rubot_sensor_bringup` provides one public selector and two
platform-specific launch files:

- `ens160_robot.launch.py`: selects `robot:=mecanum` or `robot:=rosbot`.
- `mecanum_ens160.launch.py`: starts the physical mecanum robot.
- `rosbot_ens160.launch.py`: starts the physical or simulated ROSbot XL.

The two ROS distributions are never sourced in the same terminal. The shared
sensor repositories are compiled independently in each workspace.

## ENS160 data flow

```text
ENS160 array
    │ I2C through TCA9548A
    ▼
Arduino Nano 33 IoT
    │ USB serial
    ▼
ens160_air_quality_ros
    │ /ens160/readings
    ▼
rubot_ens160_mapping
    ├── TF map → base_link
    ├── positioned measurements
    ├── CSV datasets
    └── PointCloud2 / heatmaps
```

The generic ENS160 node reads and publishes measurements without depending on
the robot. The integration package adds robot pose and map context.

## Design rules

- Do not duplicate robot or sensor drivers.
- Keep hardware ports, frames, topics and output paths configurable.
- Use timestamps when associating measurements with TF transforms.
- Do not store generated logs in Git by default.
- Keep small, documented example datasets for repeatable tests.
