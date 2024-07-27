import launch
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, SetEnvironmentVariable, RegisterEventHandler
from launch.substitutions import LaunchConfiguration
from launch.conditions import IfCondition
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource
import os
from ament_index_python import get_package_share_directory
import xacro


def generate_launch_description():

    # robot_description = xacro.process_file(os.path.join(get_package_share_directory('rover_description'), 'urdf/bot/bot.xacro')).toxml()
    robot_description = xacro.process_file(os.path.join(get_package_share_directory('rover_description'), 'urdf/rover/rover.urdf')).toxml()
    config_file = os.path.join(get_package_share_directory('rover_gazebosim'), 'config', 'parameter_bridge.yaml')
    # camera_description = xacro.process_file(os.path.join(get_package_share_directory('rover_description'), 'urdf/rover/camera.urdf')).toxml()
    robot_controllers = os.path.join(get_package_share_directory("rover_wheel_control"),"config","diff_drive_controller.yaml")
    return LaunchDescription([

        DeclareLaunchArgument('gui', default_value='true', description='Flag to enable/disable GUI'),
        DeclareLaunchArgument('separate_cam', default_value='false', description='Flag to enable/disable separate camera'),

        # Set intial postion of rover..
        DeclareLaunchArgument('x', default_value='2', description='Initial x position of the rover'),
        DeclareLaunchArgument('y', default_value='2', description='Initial y position of the rover'),
        DeclareLaunchArgument('z', default_value='1', description='Initial z position of the rover'),

        # Set environment variables...
        SetEnvironmentVariable(name='IGN_GAZEBO_RESOURCE_PATH', value=os.path.join(get_package_share_directory('rover_description'), 'meshes') + ':' + os.path.join(get_package_share_directory('rover_description'), 'urdf', 'rover')),
        # Include the shapes world launch file from igniton gazebo package here..
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(get_package_share_directory("ros_gz_sim"), "launch", "gz_sim.launch.py")
                ),
                launch_arguments=[("gz_args", ["~/mrt_ws/src/rover_gazebosim/worlds/ign_rect_world.sdf"])],
        ),
    
        # Robot strcture publisher..
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            output='screen',
            parameters=[{"robot_description": robot_description}]
        ),
        # Joint State Publisher to send fake joint values..
        Node(
            package='joint_state_publisher',
            executable='joint_state_publisher',
            name='joint_state_publisher',
            parameters=[{'use_gui': LaunchConfiguration('gui')}]  
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
                "-x",
                LaunchConfiguration("x"),
                "-y",
                LaunchConfiguration("y"),
                "-z",
                LaunchConfiguration("z"),
            ],
        ),
        
        Node(
              package='ros_gz_bridge',
              executable='parameter_bridge',
              parameters=[{'config_file': config_file }],
              ),
        # Node(
        # package="controller_manager",
        # executable="ros2_control_node",
        # parameters=[robot_controllers],
        # output="both",
        # ),
        # Node(
        # package="controller_manager",
        # executable="spawner",
        # arguments=["joint_state_broadcaster", "--controller-manager", "/controller_manager"],
        # ),
        # Node(
        # package="controller_manager",
        # executable="spawner",
        # arguments=["forward_position_controller", "--controller-manager", "/controller_manager"],
        # ),

        ])
