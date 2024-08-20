import  subprocess,os,sys

class IP_Config:
    def  __init__(self,ip_address=None) -> None:
        self.netplan_yaml = "/etc/netplan/00-installer-config.yaml"
        self.ethernet_ID = self.eth()
        
        self.ip_address = ip_address
        pass

    def eth(self):
        eth = subprocess.Popen("ip address|grep BROADCAST|grep -v docker|awk -F: '{print $2}'",stdin=None,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
        eth = eth.stdout.readlines()[0].decode().strip()
        return eth
    
    def config(self):
        if os.path.exists(self.netplan_yaml):
            if self.ip_address:
                config = self.static_IP_config()
            else:
                config = self.dhcp_config()
            with open(self.netplan_yaml,'w',encoding='utf-8') as file:
                file.write(config)
            rs = subprocess.Popen("sudo netplan apply", stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            stdout,stderr = rs.communicate()
            print(f"{stdout.decode().strip()=}")
            print(f"{stderr.decode().strip()=}")
        else:
            print(f"Cant find {self.netplan_yaml}!")

    def static_IP_config(self):
        config = f"""
network:
  ethernets:
    {self.ethernet_ID}:
      dhcp4: no
      dhcp6: no
      addresses: [{self.ip_address}/24]
      gateway4: 192.168.115.254
      nameservers:
        addresses: [192.168.98.111]
  version: 2
        """
        print(config)
        return config

    def dhcp_config(self):
        config = f"""
network:
  ethernets:
    {self.ethernet_ID}:
      dhcp-identifier: mac
      dhcp4: true
      nameservers:
        addresses:
        - 192.168.98.111
  version: 2
        """
        print(config)
        return config




if __name__ == "__main__":
    if len(sys.argv) == 1:
        ip_addr = None
    else:
        ip_addr = sys.argv[1]
    ip = IP_Config(ip_addr)
    ip.config()
