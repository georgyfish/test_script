import os
import subprocess
import time
import paramiko


# def find_file_formats(directory):
#     file_formats = {}
#
#     for root, dirs, files in os.walk(directory):
#         # 忽略目录
#         dirs[:] = [d for d in dirs if not d.endswith('.txt')]
#
#         # 获取当前目录的层级
#         level = root[len(directory) + 1:].count(os.sep) + 1
#
#         for file in files:
#             # 检查文件的扩展名
#             extension = os.path.splitext(file)[1]
#
#             # 将格式添加到对应目录的列表中
#             if level not in file_formats:
#                 file_formats[level] = []
#             file_formats[level].append(extension)
#
#     return file_formats

def check_mpv():
    command = f"dpkg -l |grep -i mpv"
    result = subprocess.check_output(command, shell=True).decode('utf-8').split('\n')
    if not result:
        print('install mpv...')
        os.system('sudo apt install mpv -y')

def scp_testdata(remote_host, remote_user, remote_pass,remote_path,local_path):

    # # 远程服务器的信息
    # remote_host = '192.168.100.242'
    # remote_port = 22
    # remote_user = 'user'
    # remote_pass = 'gfx123456'
    # remote_path = '/var/www/data/testdata/'

    # # 本地服务器的信息
    # local_path = '/home/swqa/'

    # 创建SSH客户端对象
    # ssh = paramiko.SSHClient()
    # ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # # 连接远程服务器
    # ssh.connect(remote_host, remote_port, remote_user, remote_pass)

    # # 执行SCP命令，将文件从远程服务器复制到本地
    # stdin, stdout, stderr = ssh.exec_command(f'scp {remote_path} {local_path}')

    # # 关闭SSH连接
    # ssh.close()
    os.system('sudo apt-get -y install sshpass')
    
    os.system(f" sshpass -p '{remote_pass}' scp -r {remote_user}@{remote_host}:{remote_path} {local_path} ")

def find_files(directory):
    file_formats = {}

    for root, dirs, files in os.walk(directory):
        for file in files:
            # 获取文件的扩展名
            extension = os.path.splitext(file)[1]

            # 将格式添加到对应列表中
            if extension not in file_formats:
                file_formats[extension] = []
            file_formats[extension].append(os.path.join(root, file))

    return file_formats

def get_encode_files(directory):
    file_formats = {} 
    # 视频文件：编码格式
    for file in os.path(directory):
        cmd = f"ffprobe -v error -select_streams v:0 -show_entries stream=codec_name -of default=noprint_wrappers=1:nokey=1 {file}"
        file_code = subprocess.Popen(cmd,shell=True)    
        file_formats[file] = file_code
    return file_formats


def hard_decode_video(video_file,time):
    try:
        #os.system('killall mpv')
        #command = f" export DISPLAY=:0.0 && timeout 30  mpv --hwdec=vaapi --vo=gpu '{video_file}' --fs --loop &"
        command = f" export DISPLAY=:0.0 && timeout {time}  deepin-movie  '{video_file}' &"
        subprocess.run(command, shell=True, check=True)
        decode_status_command = "sudo cat /sys/kernel/debug/mtvpu0/info |grep fps"
        os.system('sleep 5')
        result = subprocess.check_output(decode_status_command, shell=True).decode('utf-8').split('\n')
        print(result)
        if result:
            return True
        else:
            return False
    except subprocess.CalledProcessError:
        return False

def main():
    directory = '/home/swqa/testdata/mm_video/1080P/'  # 替换为你的视频文件夹路径
    file_formats = find_files(directory)
    check_mpv()
    print("\n找到的文件格式如下：")
    for extension, files in file_formats.items():
        print("扩展名为 %s 的文件:" % extension)
        for file in files:
            print("  %s" % file)
    # formats = get_video_formats(directory)
    # print("Detected video formats:", formats)
    for extension in file_formats.keys():
        print(f"Try Hard decoding videos in format {extension}...")
        # files = [f for f in os.listdir(directory) if f.endswith(extension)]
        files = file_formats[extension]
        success_count = 0
        fail_count = 0
        for file in files:
            print(f"Hard decoding video:{file}")
            file_path = f"{os.path.join(directory, file)}"
            # print(file_path)
            result = hard_decode_video(file_path,20)
            print(result)
            time.sleep(20)
            if result:
                success_count += 1
            else:
                fail_count += 1
                print(f"Failed hard decoding {extension} video: {os.path.join(directory, file)}")
        print(f"Hard decoding of {extension} videos finished. Successful count: {success_count}")
        print(f"Hard decoding of {extension} videos finished. Failed count: {fail_count}")
        print('--'*50)

if __name__ == "__main__":
    main()