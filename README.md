## Getting Started
Once in HOME directory, paste the following commands
```console
mkdir -p mrt_ws/src && cd mrt_ws/src
git clone git@github.com:iitbmartian/ROS2_Autonomous_Subdivision.git .
cd ..
colcon build --symlink-install
source install/setup.zsh
```
- Use [setuptools 58.2.0](https://pypi.org/project/setuptools/58.2.0/) to remove warning while building python based ROS packages
- For spawning ArUco markers and arrows in classic Gazebo, add the following lines to your bashrc (or zshrc), and then source it
```
export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:${HOME}/mrt_ws/src/rover_gazebosim/model_editor_models
export GAZEBO_RESOURCE_PATH=$GAZEBO_RESOURCE_PATH:/usr/share/gazebo-11:${HOME}/mrt_ws/src/rover_gazebosim/media/materials
```
## Packages
- `rover_description`: URDF descriptions + RViz visualization of the rover
- `rover_gazebosim` : Ignition Fortress simulation of the rover
## Guidelines
- Pull the changes of the main branch to your own branch and make changes
- Then create a pull request of your branch into the main branch  
- When committing new code, please follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification
## Resources
- [Spreadsheet of important links for learning Fortress][https://docs.google.com/spreadsheets/d/1Vd0YYC5ROk6MPMOKjW5itqq75i41R3NcYcKld-Sgi4g/edit?gid=0#gid=0]



