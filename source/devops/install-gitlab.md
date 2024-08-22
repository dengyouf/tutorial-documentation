# GitLab

## Install GitLab On Ubuntu

1. 信任 GitLab 的 GPG 公钥
```shell
curl https://packages.gitlab.com/gpg.key 2> /dev/null | apt-key add - &>/dev/null
```
2. 将下方内容写入 /etc/apt/sources.list.d/gitlab-ce.listd/gitlab-ce.list`
```shell
echo "deb https://mirrors.tuna.tsinghua.edu.cn/gitlab-ce/ubuntu focal main" > /etc/apt/sources.list.d/gitlab-ce.list
```

3. 安装 gitlab
```shell
apt update
apt install gitlab-ce 
```



## Install GitLab By Docker

