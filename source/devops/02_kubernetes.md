# 安装Kubernetes集群

## 主机名解析

```
cat  >> /etc/hosts <<EOF
192.168.122.11 k8s-master01
192.168.122.21 k8s-worker01
192.168.122.22 k8s-worker02
192.168.122.23 k8s-worker03

192.168.122.11 k8s.linux.io
EOF
```
## 配置kubernetes仓库

```
apt-get update && apt-get install -y apt-transport-https
curl https://mirrors.aliyun.com/kubernetes/apt/doc/apt-key.gpg | apt-key add - 

cat <<EOF >/etc/apt/sources.list.d/kubernetes.list
deb https://mirrors.aliyun.com/kubernetes/apt/ kubernetes-xenial main
EOF
apt-get update
```

## 安装软件

- 安装kubeadm

```
apt install -y kubeadm=1.23.5-00 kubelet=1.23.5-00 kubectl=1.23.5-00

systemctl  enable kubelet
```

- 拉取镜像

```
kubeadm config images pull --image-repository=registry.cn-hangzhou.aliyuncs.com/google_containers --kubernetes-version=1.23.5
```

## 初始化集群

```
# 所有节点需要解析 k8s.linux.io, 此域名用于后续扩展集群为高可用集群
kubeadm init --kubernetes-version=v1.23.5 \
    --control-plane-endpoint=k8s.linux.io \
    --apiserver-advertise-address=0.0.0.0 \
    --pod-network-cidr=10.244.0.0/16   \
    --service-cidr=10.96.0.0/12 \
    --image-repository=registry.cn-hangzhou.aliyuncs.com/google_containers \
    --ignore-preflight-errors=Swap | tee kubeadm-init.log
```

## 配置kubectl命令

```
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

## Join工作节点

```
kubeadm join k8s.linux.io:6443 --token ib2mri.l36ju6sma8mx0789 \
        --discovery-token-ca-cert-hash sha256:96fdccd0ce69686181fbc53e31a1ccfaec584af096ac1bded792fbcc2cbe1b9c
```

## 安装CNI

- flannel 
```
wget  https://github.com/flannel-io/flannel/releases/latest/download/kube-flannel.yml
kubectl apply -f kube-flannel.yml
```

## 验证集群

```
~# kubectl  create deployment myapp --image=ikubernetes/myapp:v1 --replicas=3
~# kubectl  expose deployment myapp --port=80 --target-port=80
```

```
~# kubectl  get pods -o wide
NAME                    READY   STATUS    RESTARTS   AGE    IP           NODE     NOMINATED NODE   READINESS GATES
myapp-9cbc4cf76-7cgwt   1/1     Running   0          103s   10.244.1.4   k8s-w1   <none>           <none>
myapp-9cbc4cf76-qzghs   1/1     Running   0          103s   10.244.2.2   k8s-w2   <none>           <none>
myapp-9cbc4cf76-xmgxt   1/1     Running   0          103s   10.244.2.3   k8s-w2   <none>           <none>
root@k8s-m1:~# kubectl  get svc
NAME         TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)   AGE
kubernetes   ClusterIP   10.96.0.1      <none>        443/TCP   15m
myapp        ClusterIP   10.97.183.10   <none>        80/TCP    53s
root@k8s-m1:~# for i in `seq 4`;do curl 10.97.183.10/hostname.html;done
myapp-9cbc4cf76-7cgwt
myapp-9cbc4cf76-7cgwt
myapp-9cbc4cf76-qzghs
myapp-9cbc4cf76-7cgwt
```

## 安装Kuborad

- 启动Kuboard容器

