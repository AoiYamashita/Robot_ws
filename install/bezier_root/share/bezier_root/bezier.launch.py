import launch
import launch.actions
import launch.substitutions
import launch_ros.actions

def generate_launch_description():
    web = launch_ros.actions.Node(
            package = 'rosbridge_server',
            executable = 'rosbridge_websocket.py',
            parameters=[{'port': 9090}],
            output = 'screen',
            )
    bezier = launch_ros.actions.Node(
            package = 'bezier_root',
            executable = 'bezierRoot',
            output = 'screen',
            )
    return launch.LaunchDescription([web,bezier])