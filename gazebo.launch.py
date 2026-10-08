import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node


def generate_launch_description():

    pkg_share = get_package_share_directory('hand_gesture_control')

    urdf_file = os.path.join(
        pkg_share,
        'urdf',
        'arm_hand.urdf'
    )

    with open(urdf_file, 'r') as infp:
        robot_desc = infp.read()

    # =========================
    # Gazebo Harmonic
    # =========================

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('ros_gz_sim'),
                'launch',
                'gz_sim.launch.py'
            )
        ),
        launch_arguments={
            'gz_args': '-r empty.sdf'
        }.items()
    )

    # =========================
    # Robot State Publisher
    # =========================

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[
            {
                'robot_description': robot_desc,
                'use_sim_time': True
            }
        ]
    )

    # =========================
    # Spawn robot in Gazebo
    # =========================

    spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-topic',
            'robot_description',
            '-name',
            'arm_hand_robot'
        ],
        output='screen'
    )

    return LaunchDescription([
        gazebo,
        robot_state_publisher,
        spawn_entity
    ])