#! /bin/bash

primary_gpu=$1
card_cnt=$(lspci |grep -Ei "vga|3D|1ed5|MTT"|grep -v audio|grep -v NVMe|awk '{print $1}'|wc -l)
function check_para() {
    primary_gpu=$1
    if [[ $# != 1 ]];then 
        echo "请使用合法参数:$0 card0/card1"
        exit 1
    fi
    # 识别以card或Card开头的字符串
    typeset -u name
    name=$primary_gpu
    if [[ ${name:0:4} != "CARD" ]];then
        echo "请使用合法参数:$0 card0/card1"
        echo $name
        exit 1
    fi
    if [[ ${primary_gpu:(-1)} =~ ^[0-9]+$ ]];then
        primary_gpu="Card${primary_gpu:(-1)}"
    else
        echo "请使用合法参数:$0 card0/card1"
        exit 1
    fi
    # 边界值，Card0-n应当小于显卡数量
    cardID=`echo $primary_gpu |awk -F 'Card' '{print $2}'`
    if [ $cardID -gt $(expr $card_cnt - 1) ];then 
        echo "GPU序号错误"
        exit 1
    fi
    if [ -e /etc/X11/xorg.conf ];then 
        sudo mv /etc/X11/xorg.conf /etc/X11/xorg.conf.bak
    fi
}

function xorg_config() {
    # 配置mtgpu
    #mt_pcie_addr=$(lspci |grep -Ei "3D|1ed5|MTT"|awk '{print $1}')
    mtgpu_config=""
    layout=""
    layout_config=""
    for pcie_addr in $(lspci |grep -Ei "vga|3D|1ed5|MTT"|grep -v audio|grep -v NVMe|awk '{print $1}');do
        #echo $pcie_addr
        mt_bus_id=$((16#$(echo $pcie_addr|cut -d ':' -f1)))
        bus_id_1=$(echo $pcie_addr|awk -F':' '{print $2}')
        b=$((16#$(echo $pcie_addr|awk -F':' '{print $2}'|awk -F'.' '{print $1}')))
        c=$((16#$(echo $pcie_addr|awk -F':' '{print $2}'|awk -F'.' '{print $2}')))
        mt_bus_id="$mt_bus_id:$b:$c"
        #echo $mt_bus_id
        device_id=$(find /sys/devices -name drm|grep $pcie_addr|xargs -n1 ls|grep card|grep -oE '[0-9]+')
        echo "Card$device_id : $(lspci |grep $pcie_addr)"
        driver=$(lspci -k |grep $pcie_addr -A3|grep "driver in use" |awk -F ": " '{print $2}')
        mtgpu_config_base=''

        # echo $device_id
        if [[ $device_id != '' || $device_id != ' ' ]];then 
            mtgpu_config_base="
Section \"Device\"
        Identifier      \"Card$device_id\"
        Driver          \"$driver\"
        BusID           \"PCI:$mt_bus_id\"
EndSection

Section \"Screen\"
        Identifier      \"Card$device_id\"
        #Monitor         \"Monitor$device_id\"
        Device          \"Card$device_id\"
EndSection
"
            if [[ "Card$device_id" != $primary_gpu ]]
            then 
                layout="Inactive \"Card$device_id\"
        "
                layout_config="$layout_config$layout"
            fi
        fi
        mtgpu_config="$mtgpu_config$mtgpu_config_base"
    done
    echo $layout_config
    layout_config="$layout_config
EndSection
    "
    
    # Screen 0 card decide which discrete card is PrimaryGPU; inactive card is the secondary gpu
    server_layout="Section \"ServerLayout\"
        Identifier \"layout\"
        Screen 0 \"$primary_gpu\"
        $layout_config
    "
    #echo "$server_layout"    
    xorg="$server_layout$mtgpu_config"
    echo "echo xorg.conf"
    echo "#########################################################################"
    echo "$xorg"
    echo "#########################################################################"
    echo "测试完毕如需恢复环境，请将/etc/X11/xorg.conf文件移除"
    echo "$xorg" > ~/xorg.conf
}

function check_primarygpu() {
    cardID=`echo $primary_gpu |awk -F 'Card' '{print $2}'`
    for pcie_addr in $(lspci |grep -Ei "vga|3D|1ed5|MTT"|grep -v audio|grep -v NVMe|awk '{print $1}');do
        #echo $pcie_addr
        mt_bus_id=$((16#$(echo $pcie_addr|cut -d ':' -f1)))
        b=$((16#$(echo $pcie_addr|awk -F':' '{print $2}'|awk -F'.' '{print $1}')))
        c=$((16#$(echo $pcie_addr|awk -F':' '{print $2}'|awk -F'.' '{print $2}')))
        mt_bus_id="$mt_bus_id:$b:$c"
        #echo $mt_bus_id
        device_id=$(find /sys/devices -name drm|grep $pcie_addr|xargs -n1 ls|grep card|grep -oE '[0-9]+')
        # echo "Card$device_id : $(lspci |grep $pcie_addr)"
        
        if [ $device_id -eq $cardID ];then
            c=$(lspci -nn |grep $pcie_addr|awk -F: '{print $4}')
            set_primarygpu_deviceID=${c%%]*}
        fi
    done
    current_primarygpu_deviceID=`grep "\<PCI:\*" /var/log/Xorg.0.log |awk  '{print $5}'|awk -F: '{print $2}'`
    echo "set_primarygpu_deviceID=$set_primarygpu_deviceID"
    echo "current_primarygpu_deviceID=$current_primarygpu_deviceID"
    if [ $set_primarygpu_deviceID -ne $current_primarygpu_deviceID ];then 
        echo "检查deviceID失败，boot_vga=$current_primarygpu_deviceID"
    else
        echo "检查deviceID正确, boot_vga=$current_primarygpu_deviceID"
    fi

}

check_para $primary_gpu
xorg_config
# sudo systemctl stop lightdm
# sudo ps -ef |grep Xorg|awk '{print $2}'|xargs -n1 kill -9

sudo cp ~/xorg.conf /etc/X11
echo "sudo cp ~/xorg.conf /etc/X11"
echo "sudo systemctl restart lightdm "
sudo systemctl restart lightdm 
sleep 5
# check_primarygpu

#check Primary GPU set status
#check Xorg status
# systemctl status lightdm
# sudo cat /var/log/Xorg.0.log |grep -i error -v "\(EE\)"  
# sudo cat /var/log/Xorg.0.log |awk -F ' ' '{print $4}'|grep -iE "^PCI:\*"
# sudo find  /sys/devices/pci0000\:00/ -name boot_vga
# 修改xorg.conf后 /var/log/Xorg.0.log 查找出来结果不对，boot_vga 可能与显示器插在哪张显卡上有关。
#测试完毕恢复默认，需要将/etc/X11/xorg.conf文件移除；

