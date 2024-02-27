#!/bin/bash

checkkmd=0
checkumd=0
checkdeb=0
summary=0 
commit_type_kmd=0
commit_type_umd=0
install_kmd_flag=0
install_umd_flag=0


function show_deb_info() {
    echo "show_deb_info"
}

function show_kmd_info() {
    echo "show kmd info"
}
function show_umd_info() {
    echo "shwo umd info "
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
    # commit.sh  功能：检查出当前环境的commit，包括kmd和umd；安装指定commitID的kmd或umd；
    # commit.sh -s  #检查当前环境的驱动信息，commit信息；
    # commit.sh -c  kmd | umd  #检查当前环境的kmd或umd commitID信息
    # commit.sh -i  commitID  #检查commitID是kmd还是umd, 安装；
    # commit.sh -s | [-c kmd|umd ] | [-i commitID ] |-h 
    echo "Usage: $0 -s | [-c kmd|umd ] | [-i commitID ] | -h"
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
                if 
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