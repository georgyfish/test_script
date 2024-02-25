#!/bin/bash

arch=$(uname -m)
kernel_version=$(uname -r)
kernel_flag=True
#检查下载的KMD内核版本与系统内核版本是否一致
function check_kernel_version() {
    commitID=$1
    if [ "$(find KMD_${commitID}/${arch}-mtgpu_linux-xorg-release/ -name mtgpu.ko |cut -d "/" -f 5)" = "$kernel_version" ];then 
        echo "下载KMD驱动与内核匹配，可以直接替换安装";
        kernel_flag=True
    else
        echo "下载KMD驱动与内核不匹配，需使用dkms deb安装KMD"
        kernel_flag=False
    fi
    echo $kernel_flag
}

function download_kmd() {
    commitID=$1 
    #kmd_url=oss/release-ci/gr-kmd/develop/${commitID}_1050u3_uos_arm64-mtgpu_linux-xorg-release-hw.tar.gz
    #KMD更换地址后 2023-12-18之后
    #只有ubuntu、20.04.1 kernel 5.4.0-42内核可以直接使用tar包替换kmd?

    kmd_url="https://oss.mthreads.com/sw-build/gr-kmd/develop/${commitID}/${commitID}_${arch}-mtgpu_linux-xorg-release-hw.tar.gz"
    kmd_deb_url="https://oss.mthreads.com/sw-build/gr-kmd/develop/${commitID}/${commitID}_${arch}-mtgpu_linux-xorg-release-hw.deb"
    rm -rf KMD_${commitID}.tar.gz
    wget $kmd_url -O KMD_${commitID}.tar.gz
    rm -rf KMD_$commitID
    mkdir KMD_$commitID
    tar -xvf KMD_${commitID}.tar.gz -C KMD_${commitID}
    check_kernel_version $commitID
    if [ $kernel_flag != "True" ];then 
        rm -rf ${commitID}_${arch}-mtgpu_linux-xorg-release-hw.deb
        wget $kmd_deb_url;
    fi
}

function download_umd() {
    glvnd="-glvnd"
    commitID=$1 
    umd_url="https://oss.mthreads.com/release-ci/gr-umd/develop/${commitID}_${arch}-mtgpu_linux-xorg-release-hw${glvnd}.tar.gz"
    wget $umd_url -O UMD_${commitID}.tar.gz
    mkdir UMD_$commitID
    tar -xvf UMD_${commitID}.tar.gz -C UMD_${commitID}
}




# 安装KMD
function install_kmd() {
    commitID=$1
    echo "sudo systemctl stop lightdm"
    sudo systemctl stop lightdm
    sudo rmmod mtgpu
    if [ -e "/lib/modules/`uname -r`/updates/dkms/mtgpu.ko" ];then 
        sudo mv /lib/modules/`uname -r`/updates/dkms/mtgpu.ko /lib/modules/5.4.0-42-generic/updates/dkms/mtgpu.ko.bak
    fi
    sudo mkdir -p /lib/modules/`uname -r`/extra/
    #下载的KMD内核版本与系统内核版本一致就直接替换安装，否则使用dkms deb安装
    if [ $kernel_flag = "True" ];then 
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
    echo "kmd安装完成，30秒内重启机器。"
    sleep 30
    sudo reboot
}



#安装umd
function install_umd() {
    sudo systemctl stop lightdm
    commitID=$1
    cd UMD_${commitID}/${arch}-mtgpu_linux-xorg-release/
    #卸载UMD
    sudo ./install.sh -g -n -u .
    #安装UMD
    sudo ./install.sh -g -n -s .
    sudo systemctl restart lightdm
}

# kmd_umd=$1
# commit=$2

checkkmd=0
checkumd=0
checkdeb=0
summary=0 

#实现效果：
# commit.sh  功能：检查出当前环境的commit，包括kmd和umd；安装指定commitID的kmd或umd；
# commit.sh -s  #检查当前环境的驱动信息，commit信息；
# commit.sh -c  kmd | umd  #检查当前环境的kmd或umd commitID信息
# commit.sh -i  commitID  #检查commitID是kmd还是umd, 安装；
# commit.sh -s | [-c kmd|umd ] | [-i commitID ] |-h 


function parse_args() {
    echo in parse_args
    while getopts ":sc:i:h" option;do 
        case $option in 
        s)
            summary=1
            ;;
        c)
            if [ "$OPTARG" = "kmd" ];
            then 
                checkkmd=1
            elif [ "$OPTARG" = "umd" ];
            then 
                checkumd=1
            else
                usage
                exit 1
            fi
            ;;
        i)
            $commitID = $OPTARG
            
            if [ $commitID = $OPTARG ];
            then 
                checkkmd=1
            elif [ "$2" = "umd" ];
            then 
                checkumd=1
            else
                usage
                exit 1
            fi
            ;;
        h)
            usage
            exit 0
            ;;
        ?)
            echo "Unknown args $OPTARG!"
            usage
            exit 1
        esac
    done 
}


function main() {
    echo in main
    parse_args
    echo "$@"
    # download_${kmd_umd} $commit
    # install_${kmd_umd} $commit   

}

### main starts here ! ###
main "$@"
