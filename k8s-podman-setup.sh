#!/bin/bash

# 更新系統
sudo apt-get update
sudo apt-get upgrade -y

# 安裝必要的系統工具
sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common gnupg2

# 安裝 Podman
. /etc/os-release
echo "deb https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/xUbuntu_${VERSION_ID}/ /" | sudo tee /etc/apt/sources.list.d/devel:kubic:libcontainers:stable.list
curl -L "https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/xUbuntu_${VERSION_ID}/Release.key" | sudo apt-key add -
sudo apt-get update
sudo apt-get -y install podman

# 安裝 Kubernetes 必要組件
# 添加 Kubernetes apt 倉庫
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list

# 安裝 kubelet, kubeadm 和 kubectl
sudo apt-get update
sudo apt-get install -y kubelet kubeadm kubectl
sudo apt-mark hold kubelet kubeadm kubectl

# 禁用 swap
sudo swapoff -a
# 永久禁用 swap，註釋掉 /etc/fstab 中的 swap 行
sudo sed -i '/ swap / s/^\(.*\)$/#\1/g' /etc/fstab

# 配置系統參數
cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
overlay
br_netfilter
EOF

sudo modprobe overlay
sudo modprobe br_netfilter

# 設置必要的 sysctl 參數
cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-iptables  = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.ipv4.ip_forward                 = 1
EOF

# 應用 sysctl 參數
sudo sysctl --system

# 配置 Podman 作為 CRI
cat <<EOF | sudo tee /etc/containers/containers.conf
[engine]
cgroup_manager = "cgroupfs"
events_logger = "file"
runtime = "crun"
EOF

# 初始化 Kubernetes 集群
# 注意：請替換 <your-pod-network-cidr> 為你想使用的 Pod 網路 CIDR
echo "現在你可以運行以下命令來初始化 Kubernetes 集群："
echo "sudo kubeadm init --pod-network-cidr=10.244.0.0/16"

# 設置 kubectl 配置
echo "集群初始化後，運行以下命令設置 kubectl："
echo "mkdir -p \$HOME/.kube"
echo "sudo cp -i /etc/kubernetes/admin.conf \$HOME/.kube/config"
echo "sudo chown \$(id -u):\$(id -g) \$HOME/.kube/config"
