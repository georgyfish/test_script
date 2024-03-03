#!/usr/bin/env bash

project=$1

function init_common() {
    sudo apt install libvulkan-dev -y
    sudo apt install libassimp-dev -y
}

function set_work_path() {
    project=$1
    rm -rf ${project}.tgz
    wget http://192.168.114.118/tool/UE/sample/${project}.tgz
    rm -rf $project
    tar xvf ${project}.tgz
    cd $project
}
function install_vulkan_sdk() {
    wget https://sdk.lunarg.com/sdk/download/1.3.275.0/linux/vulkansdk-linux-x86_64-1.3.275.0.tar.xz
    
}

function check_board(){
    result=$(sudo dmidecode | grep Version)
    #sudo dmidecode | grep -i Version
    if [[ $result == *"Phytium"* ]];then
        board_type="Phytium"
    elif [[ $result == *"Hygon"* ]];then
        board_type="Hygon"
    fi 
}

if [[ $project == 'Vulkan-Samples' ]];then
    init_common
    sudo apt install cmake g++ xorg-dev libglu1-mesa-dev -y
    set_work_path $project
    cmake -G "Unix Makefiles" -Bbuild/linux -DCMAKE_BUILD_TYPE=Release
    cmake --build build/linux --config Release --target vulkan_samples -j16
elif [[ $project == 'Vulkan-master' ]];then
    init_common
    sudo apt-get install libglm-dev -y
    set_work_path $project
    cmake -S . -B build
    cmake --build build
elif [[ $project == 'VulkanDemos-master' ]];then
    check_board
    init_common
    set_work_path $project
    if [[ $board_type == "Phytium" ]];then
        #wget https://github.com/DLTcollab/sse2neon/blob/master/sse2neon.h
        wget http://192.168.114.118/tool/UE/sample/src/sse2neon.h
        sudo cp sse2neon.h /usr/include/
        sudo mv sse2neon.h /usr/local/include/
        sed -i "s|emmintrin.h|sse2neon.h|g" Engine/Monkey/Loader/stb_image.h
        sed -i "s|emmintrin.h|sse2neon.h|g" examples/72_MeshLOD/vertexfilter.cpp
        sed -i "s|emmintrin.h|sse2neon.h|g" external/assimp/contrib/stb_image/stb_image.h
        sed -i "s|emmintrin.h|sse2neon.h|g" external/assimp/contrib/rapidjson/include/rapidjson/writer.h
        sed -i "s|emmintrin.h|sse2neon.h|g" external/assimp/contrib/rapidjson/include/rapidjson/reader.h
        sed -i "s|xmmintrin.h|sse2neon.h|g" Engine/Monkey/Math/Linux/LinuxPlatformMath.h
    fi
    # replace code all emmintrin.h to sse2neon.h
    cmake -S . -B build
    cmake --build build
elif [[ $project == 'Vulkan-glTF-PBR' ]];then
    init_common
    set_work_path $project
    sed -i '1159s/BoundingBox&/BoundingBox/' base/VulkanglTFModel.cpp
    
    cmake .
    make
elif [[ $project == 'vulkan-basic-samples' ]];then
    check_board
    init_common
    #set_work_path $VulkanSamples
    #mkdir build
    #cd build
    #chmod +x ../scripts/update_deps.py
    #python3 ../scripts/update_deps.py
    #cmake -C helper.cmake ..
    #cmake --build .

    #cd
    set_work_path $project
    cp ./API-Samples/android/ShaderHeaders/spirv_assembly.vert.h API-Samples/spirv_assembly.vert.h
    if [[ $board_type == "Hygon" ]];then
        wget http://192.168.114.118/tool/UE/sample/src/util.hpp
        cp util.hpp ./API-Samples/utils/
    fi
    sudo apt install spirv-tools -y
    sudo apt-get install git build-essential libx11-xcb-dev \
        libxkbcommon-dev libwayland-dev libxrandr-dev -y
    mkdir build
    cd build
    cmake -DCMAKE_BUILD_TYPE=Debug \
          -DVULKAN_HEADERS_INSTALL_DIR=absolute_path_to_install_dir \
          -DVULKAN_LOADER_INSTALL_DIR=absolute_path_to_install_dir \
          -DCMAKE_INSTALL_PREFIX=install ..
    #直接拷贝现成的glslang二进制，两个方法二选一,飞腾+kylin用这种，已经调试过了
    if [[ $board_type == "Phytium" ]];then
        wget http://192.168.114.118/tool/UE/sample/src/glslang
        cp glslang ../glslang/bin/glslangValidator
        cp glslang ../glslang/bin/
    fi
    #glslang源码编译二进制，耗时很长，和上面方法二选一，新arm主机方法一不适用可以选择这种
    #if [[ $board_type == "Phytium" ]];then
    #wget http://192.168.114.118/tool/UE/sample/glslang.tgz
    #wget http://192.168.114.118/tool/UE/sample/src/cmake
    #wget http://192.168.114.118/tool/UE/sample/src/cmake-3.17.tgz
    #tar xvf cmake-3.17.tgz
    #sudo chmod +x cmake
    #sudo cp cmake /usr/bin/
    #sudo cp -r cmake-3.17 /usr/share  
    #tar xvf glslang.tgz
    #cd glslang 
    #mkdir build
    #cd build
    #cmake ..
    #make
    #cp StandAlone/glslang ../glslang/bin/glslangValidator
    #cp StandAlone/glslang ../glslang/bin/
    #cd ../../
    #fi
    make -j4
elif [[ $project == 'gl_vk_chopper' ]];then
    init_common
    set_work_path nvpro_core
    cd
    set_work_path $project
    mv ../nvpro_core .
    vulkaninfo
    if [[ $? != 0 ]];then
        install_vulkan_sdk
    else
        cmake .
        make
    fi
elif [[ $project == 'nvpro_samples' ]];then
    init_common
    set_work_path $project
    sudo apt-get install libx11-dev libxcb1-dev libxcb-keysyms1-dev libxcursor-dev libxi-dev libxinerama-dev libxrandr-dev libxxf86vm-dev libvulkan-dev libglm-dev libfreeimage-dev -y
    sudo apt-get install libglfw3-dev -y

    wget -qO - https://oss.mthreads.com/product-release/tmp/lunarg-signing-key-pub.asc | sudo apt-key add -
    sudo wget -qO /etc/apt/sources.list.d/lunarg-vulkan-focal.list http://packages.lunarg.com/vulkan/lunarg-vulkan-focal.list
    sudo apt-get update
    sudo apt-get install vulkan-sdk -y
    
    cd build_all
    cp ../nvpro_core/extensions_vk.cpp ../nvpro_core/nvvk/extensions_vk.cpp
    cmake -S . -B build
    cmake --build build

else
    echo "support project: Vulkan-Samples、Vulkan-master、VulkanDemos-master、vulkan-basic-samples、Vulkan-glTF-PBR、nvpro_samples"
fi

