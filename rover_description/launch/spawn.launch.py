import launch
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, SetEnvironmentVariable
from launch.substitutions import LaunchConfiguration
from launch.conditions import IfCondition
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource
import os
from ament_index_python import get_package_share_directory
from ament_index_python import get_package_share_directory
import xacro


def generate_launch_description():

    robot_description = xacro.process_file(os.path.join(get_package_share_directory('rover_description'), 'urdf/rover.urdf')).toxml()
    # camera_description = xacro.process_file(os.path.join(get_package_share_directory('rover_description'), 'urdf/camera.urdf')).toxml()

    return LaunchDescription([

        DeclareLaunchArgument('gui', default_value='true', description='Flag to enable/disable GUI'),
        DeclareLaunchArgument('separate_cam', default_value='false', description='Flag to enable/disable separate camera'),

        # Set intial postion of rover..
        DeclareLaunchArgument('x', default_value='0', description='Initial x position of the rover'),
        DeclareLaunchArgument('y', default_value='0', description='Initial y position of the rover'),
        DeclareLaunchArgument('z', default_value='0.5', description='Initial z position of the rover'),

        # Set intial postion of camera..
        DeclareLaunchArgument('x_cam', default_value='-0.06421885520658', description='Initial x position of the camera'),
        DeclareLaunchArgument('y_cam', default_value='-0.526119109974194', description='Initial y position of the camera'),
        DeclareLaunchArgument('z_cam', default_value='1.203679693338444', description='Initial z position of the camera'),


        # Set environment variables...
        SetEnvironmentVariable(name='GAZEBO_MODEL_PATH', value=os.path.join(get_package_share_directory('rover_description'),  'meshes') + ':' + os.path.join(get_package_share_directory('rover_description'), 'urdf')),
        SetEnvironmentVariable(name='GAZEBO_MODEL_DATABASE_URI', value='/'),
        SetEnvironmentVariable(name='GAZEBO_RESOURCE_PATH', value=os.path.join(get_package_share_directory('gazebo_envs'), 'media/materials')),

        # Include the shapes world launch file from igniton gazebo package here..
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(get_package_share_directory("ros_gz_sim"), "launch", "gz_sim.launch.py")
            ),
                launch_arguments=[("gz_args", ["shapes.sdf"])],
        ),

        # Robot strcture publisher..
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            output='screen',
            parameters=[{"robot_description": robot_description}]
        ),

        # Camera strcture publisher..
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            output='screen',
            parameters=[{"camera_description": camera_description}]
        ),

        # Joint State Publisher to send fake joint values..
        Node(
            package='joint_state_publisher',
            executable='joint_state_publisher',
            name='joint_state_publisher',
            parameters=[{'use_gui': LaunchConfiguration('gui')}]  
        ),

        # Combine joint values..
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher'
        ),

        # Spawn the rover in gazebo..
        Node(
            package="ros_gz_sim",
            executable="create",
            output="screen",
            name="rover_spawn",
            arguments = [
                "-string",
                robot_description,
                "-name",
                "rover",
                "x",
                LaunchConfiguration("x"),
                "y",
                LaunchConfiguration("y"),
                "z",
                LaunchConfiguration("z"),
            ],
        ),

        # Spawn the camera conditionally..
        Node(
            condition = IfCondition(LaunchConfiguration('separate_cam')),
            package="ros_gz_sim",
            executable="create",
            name='camera_spawn',
            output='screen',
            arguments = [
                "-string",
                camera_description,
                "-name",
                "camera",
                "x",
                LaunchConfiguration("x_cam"),
                "y",
                LaunchConfiguration("y_cam"),
                "z",
                LaunchConfiguration("z_cam"),
                ],
            ),
    ])

