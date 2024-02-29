#!/bin/bash
set -e

checkkmd=0
checkumd=0
checkdeb=0
summary=0 
commit_type_kmd=0
commit_type_umd=0
install_kmd_flag=0
install_umd_flag=0

# ./download_driver.py -c umd -b develop -i 0d610f8ad
# modules=(pvrsrvkm mtgpu_kms mtgpu)
modules=(mtgpu)
# files_dir=(etc lib usr)
#remove kmd modules
# function rmmmod_kmd() {
#   for m in ${modules[@]}
#   do
#       if lsmod |grep ${m} > /dev/null 2>&1
#       then
#           rmmod ${m}
#           echo "[info] rmmod ${m} done."
#       else
#           echo "[INFO] ${m} was not loaded"  
#       fi
#   done
# }

function download_kmd() {
    # kmd_url=oss/release-ci/gr-kmd/develop/${commitID}_1050u3_uos_arm64-mtgpu_linux-xorg-release-hw.tar.gz
    #KMD更换地址后 2023-12-18之后
    kmd_url="https://oss.mthreads.com/sw-build/gr-kmd/develop"
    none_dkms_kmd_url="${kmd_url}/${commitID}/${commitID}_${arch}-mtgpu_linux-xorg-release-hw.tar.gz"
    dkms_kmd_deb_url="${kmd_url}/develop/${commitID}/${commitID}_${arch}-mtgpu_linux-xorg-release-hw.deb"
    wget $none_dkms_kmd_url -O KMD_${commitID}.tar.gz
    mkdir KMD_$commitID && tar -xvf KMD_${commitID}.tar.gz -C "KMD_${commitID}/"
    KMD_tar_kernel=$(find KMD_${commitID}/ -name mtgpu.ko |awk -F/ '{print $(NF-2)}')
    if [[ $KMD_tar_kernel != $(uname -r) ]];
        echo "KMD_${commitID}.tar.gz内核${KMD_tar_kernel}与系统内核$(uname -r)不匹配,下载dkms KMD_${commitID}.deb"
        wget $dkms_kmd_deb_url -O KMD_${commitID}.deb
    fi
}

function download_umd() {
    
    commitID=$1 
    umd_url="https://oss.mthreads.com/release-ci/gr-umd/develop/${commitID}_${arch}-mtgpu_linux-xorg-release-hw${glvnd}.tar.gz"
    wget $umd_url -O UMD_${commitID}.tar.gz
    mkdir UMD_$commitID && tar -xvf UMD_${commitID}.tar.gz -C UMD_${commitID} && cd UMD_${commitID}/${arch}-mtgpu_linux-xorg-release/
}


arch=$(uname -m)
if [ $arch = 'aarch64' ];then 
   arch='arm64'
fi
glvnd="-glvnd"
# os是Kylin就使用非glvnd的umd；
if [ $os_type = "Kylin" ];then 
    glvnd=''
fi

function show_deb_info() {
    echo "show_deb_info"
    musa_info=$(dpkg -s musa  2>/dev/null|grep Version |awk -F: '{print $NF}')
    mtgpu_info=$(dpkg -s mtgpu  2>/dev/null|grep Version |awk -F: '{print $NF}')
    if [[ $musa_info == '' ]]
    then   
        echo "[INFO] run 'dpkg -s musa' failed! Please check musa deb is installed."
    else
        ehco "[INFO] dpkg -s musa"
        dpkg -s musa 
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
            kmd_commit=$(grep "Driver Version" /sys/kernel/debug/musa/version|awk -F[ '{print $NF}'|awk -F] '{print $1}')
            echo "[INFO] KMD commitID : $kmd_commit"

        else
            echo "[INFO] $m not loaded"
            
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
        echo "[INFO] 无法查询到umd info, please check Xorg status;"
    fi

}

function check_commit_type() {
    check_commit_kmd $commitID
    if [ commit_type_kmd -eq 1 ] ;then 
        echo "$commitID 为KMD"
        install_kmd $commitID
    else
        check_commit_umd $commitID
        if [ commit_type_umd -eq 1 ] ;then 
            echo "$commitID 为UMD"
            install_umd $commitID
        else
            "未识别到commitID，请重新检查commit拼写！"
            exit 1
        fi
    fi
    
}
function check_commit_kmd() {
    commit_type_kmd=1
}
function check_commit_umd() {
    commit_type_umd=1
}


function usage() {
    echo in usage
    # 实现效果：
    # $0  功能：检查出当前环境的commit，包括kmd和umd；安装指定commitID的kmd或umd；
    # $0 -s                                         #检查当前环境的驱动信息，KMD、UMD commit信息；
    # $0 -b  <daily/release/master/haiguang/kylin>  # 指定branch
    # $0 -c  <all|kmd|umd>                          # 指定component ; all---->all in one;
    # $0 -i  <commitID>  #检查commitID是kmd还是umd, 安装；
    # $0 -s | [-c all|kmd|umd ] -b branch [-i commitID ] |-h 
    echo "Usage: $0 -s | [-c all|kmd|umd ] | [-i commitID ] | -h"
    echo "
-s      # show driver info summary;
-c      # kmd: check kmd commit info;
        # umd: check umd commit info;
-i      # install kmd/umd commit;
-h      # --help"
     
}

function parse_args() {
    while getopts :sc:i:h option
    do 
        case "$option" in
            s)
                echo "-s"
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
                commitID=$OPTARG
                check_commit_type $commitID
                
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
    fi
}
function main() {
    echo in main
    parse_args "$@"
    if [ $summary -eq 1 ];then 
        show_deb_info
        show_kmd_info
        show_umd_info
        exit 0
    elif [ $checkkmd -eq 1 ];then 
        show_kmd_info
        exit 0 
    elif [ $checkumd -eq 1 ];then 
        show_umd_info
        exit 0 
    else
        exit 0
    fi
    
    
}

main "$@"