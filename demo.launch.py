import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
  pkg_share = get_package_share_directory('hand_gesture_control')
  # Apunta al nuevo URDF que incluye la mano completa
  urdf_file = os.path.join(pkg_share, 'urdf', 'arm_hand.urdf')

  with open(urdf_file, 'r') as infp:
    robot_desc = infp.read()

  robot_state_publisher_node = Node(
      package='robot_state_publisher',
      executable='robot_state_publisher',
      name='robot_state_publisher',
      output='screen',
      parameters=[{'robot_description': robot_desc}],
  )

  gesture_detector_node = Node(
      package='hand_gesture_control',
      executable='gesture_detector',
      name='gesture_detector',
      output='screen',
  )

  hand_controller_node = Node(
      package='hand_gesture_control',
      executable='hand_controller',
      name='hand_controller',
      output='screen',
  )

  rviz_node = Node(
      package='rviz2',
      executable='rviz2',
      name='rviz2',
      output='screen',
  )

  return LaunchDescription([
      robot_state_publisher_node,
      gesture_detector_node,
      hand_controller_node,
      rviz_node,
  ])