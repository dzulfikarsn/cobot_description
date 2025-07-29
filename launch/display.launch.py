from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution

from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    package = FindPackageShare('cobot_description')
    urdf_path = PathJoinSubstitution([package, 'urdf', 'cobot.urdf.xacro'])
    rviz_config = PathJoinSubstitution([package, 'rviz', 'urdf.rviz'])

    # declare argument
    argument_list = [
        DeclareLaunchArgument(
            name='jsp_gui',
            default_value='true',
            choices=['true', 'false'],
            description='Flag to enable joint_state_publisher_gui'
        ),
        DeclareLaunchArgument(
            name='urdf',
            default_value=urdf_path,
            description='Path to the URDF file'
        ),
        DeclareLaunchArgument(
            name='rviz_cfg',
            default_value=rviz_config,
            description='Absolute path to rviz config file'
        )
    ]

    # joint state publisher node
    jsp_gui_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        output='screen',
        condition=IfCondition(LaunchConfiguration('jsp_gui'))
    )

    jsp_node = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        output='screen',
        condition=UnlessCondition(LaunchConfiguration('jsp_gui'))
    )

    # robot state publisher node
    xacro_script = Command(['xacro ', LaunchConfiguration('urdf')])

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
        arguments=['-d', LaunchConfiguration('rviz_cfg')]
    )

    # add nodes
    node_list = [
        jsp_gui_node,
        jsp_node,
        robot_state_publisher_node,
        rviz2_node,
    ]

    return LaunchDescription(argument_list + node_list)