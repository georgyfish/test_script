#!/bin/bash
# set -e

component_kmd=0
component_umd=0
checkdeb=0
summary=0 
component=0
branch=0
commitID=0
oss_url="https://oss.mthreads.com"
# commit_type_kmd=0
# commit_type_umd=0
# install_kmd_flag=0
# install_umd_flag=0

# ./download_driver.py -c umd -b develop -i 0d610f8ad
# modules=(pvrsrvkm mtgpu_kms mtgpu)
modules=(mtgpu)
# files_dir=(etc lib usr)
#remove kmd modules

function net_check() {
	ip_addr=$(ip addr |grep inet|grep -vE "docker0|wl|\<lo"|grep "192.168"|awk '{print $2}'|awk -F/ '{print $1}')
	if [ $ip_addr != "127.0.0.1" ];then 
		echo $ip_addr
	else
		echo "ip=$ip_addr,未检测到DHCP分配ip"
		exit 1
	fi
	test_ip=$(echo $oss_url |awk -F "https://" '{print $NF}')
    # test_ip="www.baidu.com"
    echo $test_ip
	#检查是否有网络
	ping_result=$(ping -c1 -W1 $test_ip > ping.txt 2>&1)
	#ping一次，超时时间1秒，ping的通返回0，echo up，ping失败打印down
	if [ $? -eq 0 ]
	then   
    	echo "可以ping通$test_ip..."
	else
    	echo "无法ping通$test_ip..."
    	exit 1
	fi
}

function download_all() {
    echo download_all
}

function download_kmd() {
    # kmd_url=oss/release-ci/gr-kmd/develop/${commitID}_1050u3_uos_arm64-mtgpu_linux-xorg-release-hw.tar.gz
    #KMD更换地址后 2023-12-18之后
    kmd_url="${oss_url}/sw-build/gr-kmd/${branch}/${commitID}/${commitID}_${arch}-mtgpu_linux-xorg-release-hw.tar.gz"
    # dkms_kmd_deb_url="${oss_url}/${commitID}/${commitID}_${arch}-mtgpu_linux-xorg-release-hw.deb"
    wget $kmd_url -O KMD_${commitID}.tar.gz
    mkdir KMD_$commitID && tar -xvf KMD_${commitID}.tar.gz -C "KMD_${commitID}/"
    KMD_tar_kernel=$(find KMD_${commitID}/ -name mtgpu.ko |awk -F/ '{print $(NF-2)}')
    if [[ $KMD_tar_kernel != $(uname -r) ]];then
        echo "KMD_${commitID}.tar.gz内核${KMD_tar_kernel}与系统内核$(uname -r)不匹配,下载dkms KMD_${commitID}.deb"
        kmd_url="${oss_url}/${commitID}/${commitID}_${arch}-mtgpu_linux-xorg-release-hw.deb"
        wget $kmd_url -O KMD_${commitID}.deb
        rm -rf KMD_${commitID}.tar.gz
    fi
}

function download_umd() {
    umd_url="${oss_url}/release-ci/gr-umd/${branch}/${commitID}_${arch}-mtgpu_linux-xorg-release-hw${glvnd}.tar.gz"
    wget $umd_url -O UMD_${commitID}${glvnd}.tar.gz
    mkdir UMD_$commitID && tar -xvf UMD_${commitID}${glvnd}.tar.gz -C UMD_${commitID}
}

# 安装KMD
function install_kmd() {
    echo "sudo systemctl stop lightdm"
    sudo systemctl stop lightdm
    sudo rmmod mtgpu
    if [ -e "/lib/modules/`uname -r`/updates/dkms/mtgpu.ko" ];then 
        sudo mv /lib/modules/`uname -r`/updates/dkms/mtgpu.ko /lib/modules/`uname -r`/updates/dkms/mtgpu.ko.bak
    fi
    sudo mkdir -p /lib/modules/`uname -r`/extra/
    #下载的KMD内核版本与系统内核版本一致就直接替换安装，否则使用dkms deb安装
    if find ./ -name KMD_${commitID}.tar.gz;
    then 
        echo "直接替换KMD"
        sudo cp $(find KMD_${commitID}/${arch}-mtgpu_linux-xorg-release/ -name mtgpu.ko) /lib/modules/`uname -r`/extra/
        sudo depmod
        sudo update-initramfs -u -k `uname -r`
    else
        echo "安装dkms mtgpu deb"
        while :
        do
            sudo dpkg -i ${commitID}_${arch}-mtgpu_linux-xorg-release-hw.deb
            if [ $? -ne 0 ];then 
                echo "安装KMD mtgpu dkms deb失败...musa包与kmd dkms deb mtgpu包冲突，需卸载musa包"
                dpkg -s musa
                if [ $? != 1 ];then
                    sudo dpkg -P musa;
                fi
            else
                break
            fi
        done
    fi
    # 重启机器
    read -p "kmd安装完成，是否要重启机器？ [yY/nN]" answer
    if [[ $answer == 'Y' ]] || [[ $answer = 'y' ]];then
        echo "30秒内重启机器"
        sleep 30
        sudo reboot
    elif [[ $answer == 'N' ]] || [[ $answer = 'n' ]];then
        exit 0
    else
        echo "input error!"
    fi
}



#安装umd
function install_umd() {
    sudo systemctl stop lightdm
    commitID=$1
    cd UMD_${commitID}/${arch}-mtgpu_linux-xorg-release/

    if [[ $glvnd == "-glvnd" ]];then 
        #glvnd umd安装方式
        #卸载UMD
        sudo ./install.sh -g -n -u .
        #安装UMD
        sudo ./install.sh -g -n -s .
    else
        #非glvnd umd安装方式
        sudo set -i 's/basedir=/usr/lib/xorg/basedir=/usr/local/bin/g' /usr/bin/X
        #卸载UMD
        sudo ./install.sh -u .
        #安装UMD
        sudo ./install.sh -s .
    fi

    sudo systemctl start lightdm
}

function show_deb_info() {
    echo "show_deb_info"
    musa_info=$(dpkg -s musa  musa_all_in_one 2>/dev/null|grep Version |awk -F: '{print $NF}')
    mtgpu_info=$(dpkg -s mtgpu  2>/dev/null|grep Version |awk -F: '{print $NF}')
    if [[ $musa_info == '' ]] && [[ $mtgpu_info == '' ]];then   
        echo "[INFO] run 'dpkg -s musa musa_all_in_one mtgpu' failed! Please check musa deb is installed."
    elif [[ $musa_info != '' ]];then
        ehco "[INFO] dpkg -s musa"
        dpkg -s musa 
    elif [[ $mtgpu_info != '' ]];then
        ehco "[INFO] dpkg -s mtgpu"
        dpkg -s mtgpu
    else 
        echo "[ERROR] musa、mtgpu cannot install at the same time; Please check musa or mtgpu install status." 
    fi
}

function show_kmd_info() {
    echo "show kmd info"
    for m in ${modules[@]}
    do 
        if lsmod |grep "$m" > /dev/null 2>&1 
        then 
            echo "[INFO] $m loaded"
            # kmd_commit=$(grep "MTGPU Driver Version" /var/log/kern.log |tail -n 1 |awk -F: '{print $NF}' |awk '{print $1}')
            kmd_commit=$(sudo grep "Driver Version" /sys/kernel/debug/musa/version|awk -F[ '{print $NF}'|awk -F] '{print $1}')
            # kmd commit 只显示7位；检查安装成功时只能对比前7位字母数字；
            echo "[INFO] KMD commitID : $kmd_commit"
        else
            echo "[ERROR] $m not loaded, Please check mtgpu.ko is loaded!"
            exit 1
            
        fi
    done
}

function show_umd_info() {
    echo "shwo umd info "
    umd_commit=$(export DISPLAY=:0.0 && glxinfo -B |grep -i "OpenGL version string"|awk '{print $NF}'|awk -F "@" '{print $1}')
    if [[ $umd_commit != "" ]]
    then
        echo "[INFO] UMD commitID : $umd_commit"
    else
        echo "[ERROR] 无法查询到umd info, please check Xorg status;"
    fi

}



function usage() {
    # echo in usage
    # 实现效果：检查出当前环境的commit，包括kmd和umd；安装指定commitID的kmd或umd；
    # $0 -s | [-c all|kmd|umd ] -b branch [-i commitID ] |-h 
    echo "Usage: $0 -s | -b <daily/release/master/haiguang/kylin> -c <all|kmd|umd>  -i commitID | -h"
    echo "
-s      # show driver info summary,include KMD/UMD COMMIT INFO;
-b      # --branch  <develop/release/master/haiguang/kylin>
-c      # component all/kmd/umd ;
-i      # install commit;
-h      # --help"
     
}

function parse_args() {
    while getopts :sb:c:i:h option
    do 
        case "$option" in
            s)
                # echo "-s"
                summary=1
                ;;
            b) 
                branch=$OPTARG
                ;;
            c)
                if [ "$OPTARG" = "kmd" ];
                then 
                    component=kmd
                elif [ "$OPTARG" = "umd" ];
                then 
                    component=kmd
                elif [ "$OPTARG" = "all" ]    
                then
                    component=all
                else
                    usage
                    exit 1
                fi
                ;;
            i)
                commitID=$OPTARG
                ;;
            h)
                usage
                exit 0 
                ;;
            # *) 
            #     echo "[Error] Illegal option -${option}"
            #     usage
            #     ;;
            :)
                echo "选项-$OPTARG后面需要一个参数值"
                usage
                exit 1
                ;;
            ?)
                echo "Unknown args -$OPTARG!"
                usage
                exit 1
                ;; 
        esac

        
    done

    if [ $# -eq 0 ]
    then 
        echo "缺少参数"
        usage
        exit 1
    fi
}
function main() {
    # echo in main
    parse_args "$@"
    if [ $summary -eq 1 ];then 
        show_deb_info
        show_kmd_info
        show_umd_info
        exit 0
    else    
        if [[ $component == '0' ]] || [[ $branch == '0' ]]
        then
            echo "You need set component and branch!"
            usage
            exit 1
        elif [ $component = 'all' ];then 
            commitID=''
        else
            commitID=$commitID
            if [ $commitID = '0' ];then 
                echo "You need input a commitID!"
                usage
                exit 1
            fi
        fi
        net_check
        download_${component} $commitID
        #install_${component}
    fi
    
    
}


os_type=$(cat /etc/os-release |grep 'NAME'|grep -v "PRETTY_NAME"|grep -v  "CODENAME"|awk -F\" '{print $(NF-1)}')
arch=$(uname -m)
if [ $arch = 'aarch64' ];then 
   arch='arm64'
fi
glvnd="-glvnd"
# os是Kylin就使用非glvnd的umd；
if [ $os_type = "Kylin" ];then 
    glvnd=''
fi
 
main "$@"


    
