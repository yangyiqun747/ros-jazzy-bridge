# ros-jazzy-bridge
基于小鱼和gazebo官网的ros-jazzy版本的桥接案例
然后运行命令的话
colcon build
source install/setup.bash
最后一个命令跟小鱼的不一样
ros2 launch 你功能包的名字 gazebo.launch.py bridge_name:=ros_gz_bridge config_file:=这里直接在vscode里复制gazebo_bridge.yaml文件的路径就行
