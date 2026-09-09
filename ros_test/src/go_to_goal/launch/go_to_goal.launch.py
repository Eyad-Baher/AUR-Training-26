import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    # Find the path to the installed YAML file
    pkg_share = get_package_share_directory('go_to_goal')
    param_file = os.path.join(pkg_share, 'config', 'parameter.yaml')

    # Define the node execution
    demo_node = Node(
        package='go_to_goal',
        executable='go_to_goal',
        name='go_to_goal',
        output='screen',
        parameters=[param_file]
    )

    turtle_node = Node(
        package='turtlesim',
        executable='turtlesim_node',
        name='turtlesim_node',
        output='screen'
    )

    return LaunchDescription([
        turtle_node,
        demo_node
    ])