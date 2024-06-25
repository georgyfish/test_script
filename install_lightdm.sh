#!/bin/bash

# apt安装lightdm并设置lightdm为X11默认启动display manager
sudo DEBIAN_FRONTEND=noninteractive apt install lightdm -y;
echo "/usr/sbin/lightdm" |sudo tee /etc/X11/default-display-manager
sudo DEBIAN_FRONTEND=noninteractive DEBCONF_NONINTERACTIVE_SEEN=true dpkg-reconfigure lightdm    

# 配置lightdm自动登录
lightdm_autologin_cmd="[SeatDefaults]\nautologin-user=swqa\n[LightDM]\nlogind-check-graphical=true" 
echo -e $lightdm_autologin_cmd |sudo tee /etc/lightdm/lightdm.conf  

