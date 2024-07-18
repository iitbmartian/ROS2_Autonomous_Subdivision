import os
from ament_index_python import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

from time import sleep
import xacro

package_name = 'rover_description'
world_file = 'living_room3.sdf'

def generate_launch_description():

    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')
    pkg_radu_simulation = get_package_share_directory('rover_description')
    rviz_config_path = os.path.join(pkg_radu_simulation, 'rviz/rover_description.rviz')

    robot_description_path =  os.path.join(
        pkg_radu_simulation,
        "urdf","rover",
        "rover.urdf",
    )

    robot_description = {"robot_description": xacro.process_file(robot_description_path).toxml()}

    print("MODEL %s" % robot_description['robot_description'])

    sleep(3)

    joint_state_publisher_node = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher'
    )

    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="both",
        parameters=[robot_description],
    )

    gazebo_node = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gazebo.launch.py'),
        )
    )

    robot_spawner = Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            name='urdf_spawner',
            output='screen',
            arguments=["-topic", "/robot_description", "-entity", "rover", "-x", "-3.0", "-y", "-1.5"])

    print("STARTING ALL NODES")

    sleep(3)

    # world_arg = DeclareLaunchArgument(
    #       'world',
    #       default_value=[os.path.join(pkg_radu_simulation, 'worlds', world_file), ''],
    #       description='SDF world file')    

    no_sim_time = DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation (Gazebo) clock if true')

    return LaunchDescription([
        # world_arg,
        no_sim_time,
        joint_state_publisher_node,
        robot_state_publisher_node,
        gazebo_node,
        robot_spawner
    ])
