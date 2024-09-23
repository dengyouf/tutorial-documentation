# NFS安装

- 准备NFS动态存储

```
apt install nfs-kernel-server -y
mkdir -pv  /data/nfsdata
echo  "/data/nfsdata  *(rw,no_root_squash)" >> /etc/exports
systemctl  restart nfs-server
```

- 所有k8s节点安装nfs客户端

```
apt install nfs-client
```

- 获取csi资源清单

```
 wget https://raw.githubusercontent.com/kubernetes-sigs/nfs-subdir-external-provisioner/master/deploy/class.yaml
wget https://raw.githubusercontent.com/kubernetes-sigs/nfs-subdir-external-provisioner/master/deploy/deployment.yaml
wget https://raw.githubusercontent.com/kubernetes-sigs/nfs-subdir-external-provisioner/master/deploy/rbac.yaml
wget https://raw.githubusercontent.com/kubernetes-sigs/nfs-subdir-external-provisioner/master/deploy/test-claim.yaml
```

- 部署nfs csi

```
~/nfsclass# kubectl  apply -f rbac.yaml

~/nfsclass# vim deployment.yaml
...

  template:
    metadata:
      labels:
        app: nfs-client-provisioner
    spec:
      serviceAccountName: nfs-client-provisioner
      containers:
        - name: nfs-client-provisioner
          image: dengyouf/nfs-subdir-external-provisioner:v4.0.2
          volumeMounts:
            - name: nfs-client-root
              mountPath: /persistentvolumes
          env:
            - name: PROVISIONER_NAME
              value: k8s-sigs.io/nfs-subdir-external-provisioner
            - name: NFS_SERVER
              value: 192.168.122.250
            - name: NFS_PATH
              value: /data/nfsdata
      volumes:
        - name: nfs-client-root
          nfs:
            server: 192.168.122.250
            path: /data/nfsdata

kubectl apply -f deployment.yaml
~/nfsclass# kubectl  get pod
NAME                                      READY   STATUS    RESTARTS   AGE
nfs-client-provisioner-5949749997-49kgk   1/1     Running   0          2m17s


~/nfsclass# kubectl  apply -f class.yaml
~/nfsclass# kubectl   get sc
NAME         PROVISIONER                                   RECLAIMPOLICY   VOLUMEBINDINGMODE   ALLOWVOLUMEEXPANSION   AGE
nfs-client   k8s-sigs.io/nfs-subdir-external-provisioner   Delete          Immediate           false                  47s
```