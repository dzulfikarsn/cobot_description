from launch import LaunchDescription
from launch.substitutions import Command, PathJoinSubstitution

from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    package = FindPackageShare('cobot_description')
    urdf_path = PathJoinSubstitution([package, 'urdf', 'cobot.urdf.xacro'])
    rviz_config = PathJoinSubstitution([package, 'config', 'urdf.rviz'])

    # joint state publisher gui node
    jsp_gui_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        output='screen'
    )

    # robot state publisher node
    xacro_script = Command(['xacro ', urdf_path])
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': ParameterValue(xacro_script, value_type=str)
        }]
    )

    # rviz2 node
    rviz2_node = Node(
        package='rviz2',
        executable='rviz2',
        output='screen',
        arguments=['-d', rviz_config]
    )

    # add nodes
    node_list = [
        jsp_gui_node,
        robot_state_publisher_node,
        rviz2_node,
    ]

    return LaunchDescription(node_list)