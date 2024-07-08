## Getting Started
```console
mkdir -p mrt_ws/src && cd mrt_ws/src
git clone git@github.com:iitbmartian/ROS2_Autonomous_Subdivision.git .
cd ..
colcon build --symlink-install
source install/setup.zsh
```
## Packages
- `rover_description`: URDF descriptions + rviz visualization of the rover
## Guidelines
- Pull the changes of the main branch to your own branch and make changes
- Then create a pull request of your branch into the main branch  
- When committing new code, please follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification.

