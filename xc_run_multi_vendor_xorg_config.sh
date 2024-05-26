#! /bin/bash

function check_para() {
    primary_gpu=$1
    if [[ $# == 0 ]];then 
        check_current
    fi
    if [[ $# > 1 ]];then 
        echo "请使用合法参数:$0 card0/card1"
        exit 1
    fi
    # 识别以card或Card开头的字符串
    typeset -u name
    name=$primary_gpu
    if [[ ${name:0:4} != "CARD" ]];then
        echo "切换PrimaryGPU请使用合法参数:$0 card0/card1"
        # echo $name
        exit 1
    fi
    if [[ ${primary_gpu:(-1)} =~ ^[0-9]+$ ]];then
        primary_gpu="card${primary_gpu:(-1)}"
    else
        echo "切换PrimaryGPU请使用合法参数:$0 card0/card1"
        exit 1
    fi
    # 边界值，card0-n应当小于显卡数量;显卡数量应大于等于2；
    if (( $card_cnt < 2));then
        echo "识别显卡数量大于1才可切换"
        exit 1
    fi
    cardID=`echo $primary_gpu |awk -F 'card' '{print $2}'`
    if [[ $cardID -gt $(expr $card_cnt - 1) ]] ;then 
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
    for pcie_addr in $(lspci |grep -Ei "VGA compatible controller|3D controller|1ed5|MTT"|grep -v audio|grep -v NVMe|awk '{print $1}');do
        #echo $pcie_addr
        mt_bus_id=$((16#$(echo $pcie_addr|cut -d ':' -f1)))
        bus_id_1=$(echo $pcie_addr|awk -F':' '{print $2}')
        b=$((16#$(echo $pcie_addr|awk -F':' '{print $2}'|awk -F'.' '{print $1}')))
        c=$((16#$(echo $pcie_addr|awk -F':' '{print $2}'|awk -F'.' '{print $2}')))
        mt_bus_id="$mt_bus_id:$b:$c"
        #echo $mt_bus_id
        device_id=$(find /sys/devices/ -name drm|grep $pcie_addr|xargs -n1 ls|grep card|grep -oE '[0-9]+')
        echo "card$device_id : $(lspci |grep $pcie_addr)"
        driver=$(lspci -k |grep $pcie_addr -A3|grep "driver in use" |awk -F ": " '{print $2}')
        mtgpu_config_base=''

        # echo $device_id
        if [[ $device_id != '' || $device_id != ' ' ]];then 
            mtgpu_config_base="
Section \"Device\"
        Identifier      \"card$device_id\"
        Driver          \"$driver\"
        BusID           \"PCI:$mt_bus_id\"
EndSection

Section \"Screen\"
        Identifier      \"card$device_id\"
        #Monitor         \"Monitor$device_id\"
        Device          \"card$device_id\"
EndSection
"
            if [[ "card$device_id" != $primary_gpu ]]
            then 
                layout="Inactive \"card$device_id\"
        "
                layout_config="$layout_config$layout"
            fi
        fi
        mtgpu_config="$mtgpu_config$mtgpu_config_base"
    done
    # echo $layout_config
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

# """
# 多卡环境下如何检查哪张显卡是primary gpu呢；
#     查看Xorg日志：
#     lightdm Xorg log path: "/var/log/Xorg.0.log"
#     gdm3 Xorg log path: "~/.local/share/xorg/Xorg.0.log"
# 	MTGPU(0) 对应的card应该才是 primary GPU；如果是集显、A卡、N卡？
#     MTGPU(G0) 对应的card才是 secondary gpu; 
# 当前机器上的card0 \card1 分别是哪张显卡呢，输出对应的显卡信息；
# 当前机器上的primary gpu？
# """



function check_primarygpu() {
    # 检查 $primary_gpu 和 $current_PrimaryGPU的值是否相同；
    current_PrimaryGPU=`grep "(0): using drv /dev/dri/card" /var/log/Xorg.0.log |awk  -F"/dev/dri/" '{print $2}'`
    secondaryGPU=`grep "(G0): using drv /dev/dri/card" /var/log/Xorg.0.log |awk  -F"/dev/dri/" '{print $2}'`

    if [[ $primary_gpu -eq $current_PrimaryGPU ]];then
        echo "Set $primary_gpu PrimaryGPU success!"
    else
        echo "Set $primary_gpu PrimaryGPU fail! Current PrimaryGPU is $current_PrimaryGPU"
    fi

}
function check_current() {
    current_PrimaryGPU=`grep "(0): using drv /dev/dri/card" $Xorg_log_path |awk  -F"/dev/dri/" '{print $2}'`
    secondaryGPU=`grep "(G0): using drv /dev/dri/card" $Xorg_log_path |awk  -F"/dev/dri/" '{print $2}'`
    current_PrimaryGPU_busID=$(find  /sys/devices/ -name $current_PrimaryGPU |grep drm |awk -F"/" '{print $(NF-2)}'|awk -F: '{print $2":"$3}')
    current_PrimaryGPU_info=$(lspci |grep $current_PrimaryGPU_busID)
    secondaryGPU_busID=$(find  /sys/devices -name $secondaryGPU |grep drm |awk -F"/" '{print $(NF-2)}'|awk -F: '{print $2":"$3}')
    secondaryGPU_info=$(lspci |grep $secondaryGPU_busID)
    echo "当前PrimaryGPU是 $current_PrimaryGPU : $current_PrimaryGPU_info"
    echo "当前SecondaryGPU是 $secondaryGPU : $secondaryGPU_info"
}

dm=$(cat /etc/X11/default-display-manager |awk -F/ '{print $NF}') 
#检查dm为lightdm还是gdm，如果是lightdm，Xorg的日志地址是"/var/log/Xorg.0.log",\
#如果是gdm3,Xorg的日志地址是"~/.local/share/xog/Xorg.0.log"
if [ $dm = 'lightdm' ];then
    Xorg_log_path="/var/log/Xorg.0.log";
elif [ $dm = 'gdm3' ];then
    Xorg_log_path="$HOME/.local/share/xorg/Xorg.0.log";
else
    echo "check dm"
fi

echo "Xorg_log_path=$Xorg_log_path"
primary_gpu=$1
card_cnt=$(lspci |grep -Ei "VGA compatible controller|3D controller|1ed5|MTT"|grep -v audio|grep -v NVMe|awk '{print $1}'|wc -l)
check_para $primary_gpu
xorg_config
# sudo systemctl stop lightdm
# sudo ps -ef |grep Xorg|awk '{print $2}'|xargs -n1 kill -9
sudo cp ~/xorg.conf /etc/X11
echo "sudo cp ~/xorg.conf /etc/X11"
echo "sudo systemctl restart $dm "
sudo systemctl restart $dm 
sleep 5
check_primarygpu
