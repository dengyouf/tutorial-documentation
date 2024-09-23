# 安装容器运行时

## 准备软件仓库

- 安装必要的一些系统工具

```
sudo apt-get remove docker docker-engine docker.io
sudo apt-get install apt-transport-https ca-certificates curl gnupg2 software-properties-common
```

- 导入信任Docker的GPG公钥

```
curl -fsSL https://mirrors.huaweicloud.com/docker-ce/linux/ubuntu/gpg | sudo apt-key add -
```

- 添加软件仓库

```
sudo add-apt-repository "deb [arch=amd64] https://mirrors.huaweicloud.com/docker-ce/linux/ubuntu $(lsb_release -cs) stable"
````

- 安装docker

```
sudo apt-get update
apt-cache madison docker-ce
apt install docker-ce=5:20.10.22~3-0~ubuntu-focal
```

- 配置docker

```
mkdir -pv /etc/docker
sudo tee /etc/docker/daemon.json <<-'EOF'
{
    "exec-opts": ["native.cgroupdriver=systemd"],
    "registry-mirrors": [
        "https://docker.rainbond.cc"
    ]

}
EOF
systemctl restart docker
```


