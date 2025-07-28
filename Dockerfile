FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
RUN ln -fs /usr/share/zoneinfo/Etc/UTC /etc/localtime && \
    apt-get update && \
    apt-get install -y openssh-server sudo ntp python3 && \
    dpkg-reconfigure --frontend noninteractive tzdata
RUN apt-get update && apt-get install -y \
    openssh-server sudo python3 python3-pip && \
    useradd -m -s /bin/bash ansible && \
    echo "ansible:ansible" | chpasswd && \
    echo 'ansible ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/ansible && \
    mkdir /var/run/sshd

CMD ["/usr/sbin/sshd","-D"]

