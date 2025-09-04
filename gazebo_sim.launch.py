import launch
import launch_ros
from ament_index_python.packages import get_package_share_directory
import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, Command
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ros_gz_bridge.actions import RosGzBridge


def generate_launch_description():
    # 获取功能包的share路径
    urdf_packages_path = get_package_share_directory('ybot_description')
    default_xacro_path = os.path.join(urdf_packages_path, 'urdf', 'ybot', 'ybot.urdf.xacro')
    default_world_path = os.path.join(urdf_packages_path, 'world', 'custom_room_ping.sdf')
    
    # 声明一个urdf目录的参数，方便修改
    declare_model_arg = DeclareLaunchArgument(
        name='model', default_value=str(default_xacro_path), description='加载的模型文件路径'
    )

    # 通过文件路径，获取内容，并转换成参数数值对象
    robot_description_content = Command(['xacro ', LaunchConfiguration('model')])
    robot_description = {'robot_description': robot_description_content}

    robot_state_publisher = launch_ros.actions.Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[robot_description, {'use_sim_time': True}],
        output='screen'
    )

    # 启动 Gazebo 并加载世界文件
    launch_gazebo = launch.actions.IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={
            'gz_args': f'-r {default_world_path}'
        }.items()
    )


    # 在 Gazebo 中生成机器人实体
    spawn_entity = launch_ros.actions.Node(
        package='ros_gz_sim',
        executable='create',
        arguments=['-name', 'ybot', '-topic', '/robot_description'],
        output='screen'
    )
    


    # 声明桥接参数
    declare_bridge_name = DeclareLaunchArgument(
        'bridge_name', default_value='ros_gz_bridge',
        description='Name of ros_gz_bridge node'
    )

    declare_config_file = DeclareLaunchArgument(
        'config_file',
        default_value='gazebo_bridge.yaml',
        description='YAML config file'
    )

    # 创建桥接
    bridge = RosGzBridge(
        bridge_name=LaunchConfiguration('bridge_name'),
        config_file=LaunchConfiguration('config_file'),
    )

    # 创建并填充启动描述
    ld = LaunchDescription()

    # 添加所有声明参数
    ld.add_action(declare_model_arg)
    ld.add_action(declare_bridge_name)
    ld.add_action(declare_config_file)

    # 添加基本节点
    ld.add_action(robot_state_publisher)
    ld.add_action(launch_gazebo)
    ld.add_action(spawn_entity)
    ld.add_action(bridge)

    return ld