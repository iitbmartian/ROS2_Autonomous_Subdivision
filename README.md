## Getting Started
```console
mkdir -p mrt_ws/src && cd mrt_ws/src
git clone git@github.com:iitbmartian/ROS2_Autonomous_Subdivision.git .
cd ..
colcon build --symlink-install
source install/setup.zsh
```
Use [setuptools 58.2.0](https://pypi.org/project/setuptools/58.2.0/) to remove warning while building python based ROS packages
## Packages
- `rover_description`: URDF descriptions + RViz visualization of the rover
-  `rover_gazebosim` : Ignition Fortress simulation of the rover
## Guidelines
- Pull the changes of the main branch to your own branch and make changes
- Then create a pull request of your branch into the main branch  
- When committing new code, please follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification.



