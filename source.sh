#!/bin/bash

# 1. 
# 换20.04 apt 源
# 2. 
# sudo apt update 
# sudo apt remove libavutil56
# sudo apt install openscenegraph
# sudo apt install openscenegraph-plugin-osgearth osgearth-data osgearth -y
# 3. 换22.04 apt 源
# sudo apt updae
# sudo sed -i 's@//.*archive.ubuntu.com@//mirrors.ustc.edu.cn@g' /etc/apt/sources.list
# sudo sed -i 's/jammy/focal/g' /etc/apt/sources.list

set -e
sudo cp /etc/apt/sources.list  /etc/apt/sources.list.bak

cat > sources.list <<EOF
deb http://mirrors.ustc.edu.cn/ubuntu/ focal main restricted
deb http://mirrors.ustc.edu.cn/ubuntu/ focal-updates main restricted
deb http://mirrors.ustc.edu.cn/ubuntu/ focal universe
deb http://mirrors.ustc.edu.cn/ubuntu/ focal-updates universe
deb http://mirrors.ustc.edu.cn/ubuntu/ focal multiverse
deb http://mirrors.ustc.edu.cn/ubuntu/ focal-updates multiverse
deb http://mirrors.ustc.edu.cn/ubuntu/ focal-backports main restricted universe multiverse
deb http://security.ubuntu.com/ubuntu focal-security main restricted
deb http://security.ubuntu.com/ubuntu focal-security universe
deb http://security.ubuntu.com/ubuntu focal-security multiverse
EOF
sudo cp sources.list /etc/apt/
sudo apt update 
sudo apt remove libavutil56 -y
sudo apt install openscenegraph -y
sudo apt install openscenegraph-plugin-osgearth osgearth-data osgearth -y

sudo cp /etc/apt/sources.list.bak /etc/apt/sources.list
sudo apt update
# remove libavutil56会卸载mpv ffmpeg等工具和video依赖包
./init_xc_env.sh 

