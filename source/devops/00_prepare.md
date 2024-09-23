# 准备虚拟机

## 安装虚拟机

## 安装后得配置

- 允许root用户远程登陆

```
~# echo "PermitRootLogin yes" >> /etc/ssh/sshd_config
~# systemctl  restart sshd
~# passwd root
New password:
Retype new password:
passwd: password updated successfully
```

- 更新apt源为[阿里源](https://developer.aliyun.com/mirror/ubuntu?spm=a2c6h.13651102.0.0.3e221b1160qO5E)

- 关闭防火墙

```
~# ufw  disable
```

- 关闭selinux

- 关闭swap分区

```
~# sed  -ri  's@/.*swap.*@# &@' /etc/fstab && swapoff -a
```
- 调整时区

```
~# sudo cp /usr/share/zoneinfo/Asia/Shanghai  /etc/localtime
root@devops:~# date -R
Wed, 31 Jul 2024 19:04:19 +0800
```

- 时间同步

```
~# sudo apt update
~# sudo apt install -y ntpdate
~# /usr/sbin/ntpdate ntp.aliyun.com 2&>1 /dev/null

~# crontab -l
/usr/sbin/ntpdate ntp.aliyun.com 2&>1 /dev/null
```


- 打开内核转发

```
~# cat > /etc/sysctl.d/k8s.conf <<EOF
net.ipv4.ip_forward = 1
net.bridge.bridge-nf-call-iptables = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-arptables = 1
net.ipv4.tcp_tw_reuse = 0
net.core.somaxconn = 32768
net.netfilter.nf_conntrack_max=1000000
vm.swappiness = 0
vm.max_map_count=655360
fs.file-max=6553600
EOF

~# sysctl -p
```

- 关机

```
init 0
```

## 克隆虚拟机

- 查看模板机器状态，确保已经关机

```
~]# virsh  list --all
 Id    Name                           State
----------------------------------------------------
 -     ubuntu20.04                    shut off
```

- 克隆机器

```
~]# virt-clone --auto-clone -o ubuntu20.04 -n k8s-master01
~]# virt-clone --auto-clone -o ubuntu20.04 -n k8s-worker01
~]# virt-clone --auto-clone -o ubuntu20.04 -n k8s-worker02
~]# virt-clone --auto-clone -o ubuntu20.04 -n k8s-worker03
```

- 修改主机名和ip地址

```
~]# virt-sysprep  --operations defaults,machine-id,-ssh-userdir,-lvm-uuids --hostname k8s-master01 --run-command "sed -i 's@192.168.122.7@192.168.122.11@g' /etc/netplan/00-installer-config.yaml && dpkg-reconfigure openssh-server" -d k8s-master01
 ~]#  virt-sysprep  --operations defaults,machine-id,-ssh-userdir,-lvm-uuids --hostname k8s-worker01 --run-command "sed -i 's@192.168.122.7@192.168.122.21@g' /etc/netplan/00-installer-config.yaml && dpkg-reconfigure openssh-server" -d k8s-worker01

~]# virt-sysprep  --operations defaults,machine-id,-ssh-userdir,-lvm-uuids --hostname k8s-worker02 --run-command "sed -i 's@192.168.122.7@192.168.122.22@g' /etc/netplan/00-installer-config.yaml && dpkg-reconfigure openssh-server" -d k8s-worker02
~]# virt-sysprep  --operations defaults,machine-id,-ssh-userdir,-lvm-uuids --hostname k8s-worker03 --run-command "sed -i 's@192.168.122.7@192.168.122.23@g' /etc/netplan/00-installer-config.yaml && dpkg-reconfigure openssh-server" -d k8s-worker03
```

## 启动虚拟机

```
~]# virsh start k8s-master01
~]# virsh start k8s-worker01
~]# virsh start k8s-worker02
~]# virsh start k8s-worker03
```


## 准备其他机器

```
virt-clone --auto-clone -o ubuntu20.04 -n k8s-harbor
virt-sysprep  --operations defaults,machine-id,-ssh-userdir,-lvm-uuids --hostname reg.linux.io --run-command "sed -i 's@192.168.122.7@192.168.122.250@g' /etc/netplan/00-installer-config.yaml && dpkg-reconfigure openssh-server" -d k8s-harbor

virt-clone --auto-clone -o ubuntu20.04 -n k8s-jenkins
virt-sysprep  --operations defaults,machine-id,-ssh-userdir,-lvm-uuids --hostname jenkins.linux.io --run-command "sed -i 's@192.168.122.7@192.168.122.251@g' /etc/netplan/00-installer-config.yaml && dpkg-reconfigure openssh-server" -d k8s-jenkins

virt-clone --auto-clone -o ubuntu20.04 -n k8s-gitlab
virt-sysprep  --operations defaults,machine-id,-ssh-userdir,-lvm-uuids --hostname gitlab.linux.io --run-command "sed -i 's@192.168.122.7@192.168.122.252@g' /etc/netplan/00-installer-config.yaml && dpkg-reconfigure openssh-server" -d k8s-gitlab

virt-clone --auto-clone -o ubuntu20.04 -n k8s-sonarqube
virt-sysprep  --operations defaults,machine-id,-ssh-userdir,-lvm-uuids --hostname sonar.linux.io --run-command "sed -i 's@192.168.122.7@192.168.122.253@g' /etc/netplan/00-installer-config.yaml && dpkg-reconfigure openssh-server" -d k8s-sonarqube
```