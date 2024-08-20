import subprocess


class Xrandr:
    def __init__(self) -> None:
        self.display_var = self.get_display_var()
        pass

    def get_display_var(self):
        rs = subprocess.Popen(r"who | grep -o '(:[0-9]\+)' | sed 's/[()]//g' |head -n 1",stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        display_var = rs.stdout.readlines()[0].decode()
        if not display_var:
            rs = subprocess.Popen(r"w -h  | awk '{print $3}'|grep -o '^:[0-9]\+' |head -n 1",stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            display_var = rs.stdout.readlines()[0].decode()
            if not display_var:
                display_var=':0'
                rs = subprocess.Popen(f"export DISPLAY={display_var} ; xrandr 2>&1",stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                if "Can't open display" in rs.stdout.readlines()[0].decode():
                    display_var = ':1'
                    rs = subprocess.Popen(f"export DISPLAY={display_var} ; xrandr 2>&1",stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                    if "Can't open display" in rs.stdout.readlines()[0].decode():
                        print("xrandr failed to run with both :0 and :1")
                        return None
        return display_var


    # 获取显卡接口
    def get_vga_support(self):
        pass
    
    # 获取显示支持的接口、分辨率信息
    def get_display_support():
        pass
    
    # 获取当前接口、分辨率信息
    def get_current_display():
        pass

    def before_test(config):
        '''
        before test set mode max resolution
        '''
        cmd = f"export DISPLAY=:0 "
        modes = list(config.keys())
        for i in range(len(modes)):
            cmd += f"&& xrandr --output {modes[i]} --auto "
        print(cmd)
        rs = subprocess.Popen(cmd, shell=True, close_fds=True, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE, preexec_fn = os.setsid)
        stdout,stderr = rs.communicate(timeout=10)
        if rs.returncode == 0 :
            # print(f"\"{cmd}\" executed successfully.")
            time.sleep(10)
            if not check_status:
                return False
        else:
            print(f"\"{cmd}\" executed failed.")
            return False

    def after_test():
        '''
        check dmesg & HWR
        '''

    def get_best_display_mode():
        '''
        get best resolution
        '''

    def set_display_config(device_name, mode, rate):
        cmd = f"export DISPLAY=:0.0 && xrandr --output {device_name} --mode {mode} --rate {rate}"
        print(cmd)
        rs = subprocess.Popen(cmd, shell=True, close_fds=True, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE, preexec_fn = os.setsid)
        stdout,stderr = rs.communicate(timeout=10)

    def check_status():
        rs = subprocess.Popen("export DISPLAY=:0.0 xgles3test1", shell=True, close_fds=True, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE, preexec_fn = os.setsid)
        stdout,stderr = rs.communicate(timeout=10)
        if rs.returncode != 0:
            print("display error")
            return False
        else:
            return True

    def run_display_resolution(config, times, random_flag):
        para_list = []
        for device_name in config.keys():
            for mode in config[device_name].keys():
                for rate in config[device_name][mode]:
                    para_list.append([device_name, mode, rate])
        para_list_size = len(para_list)
        if times == None:
            times = para_list_size
        for i in range(times):
            index = i % para_list_size
            if random_flag == 'true':
                random.shuffle(para_list)
            device_name, mode, rate = para_list[index]
            set_display_config(device_name, mode, rate)
            time.sleep(10)
            if not check_status():
                return False

    # 
    def run_display_mode(config, times):
        modes = list(config.keys())
        if times == None:
            times = 2
        for i in range(times):
            if i %2 == 0:
                rs = subprocess.Popen(f"export DISPLAY=:0.0 && xrandr --output {modes[0]} --same-as {modes[1]}", shell=True)
            else:
                rs = subprocess.Popen(f"export DISPLAY=:0.0 && xrandr --output {modes[0]} --right-of {modes[1]} --auto", shell=True)
            time.sleep(10)
            if not check_status():
                return False


class Test:
    def __init__(self) -> None:
        pass

    def test_duplicate(self):
        pass

    def test_extend(self):
        pass

    def test_only(self):
        pass

