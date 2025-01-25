FROM ubuntu:22.04

RUN apt update && apt upgrade -y
RUN apt-get update && apt-get install -y systemd wget openssh-server
RUN wget https://github.com/tsl0922/ttyd/releases/download/1.7.4/ttyd.x86_64
RUN chmod +x ttyd.x86_64 && mv ttyd.x86_64 /usr/local/bin/ttyd
RUN sed -i "s/#PermitRootLogin prohibit-password/PermitRootLogin yes/" /etc/ssh/sshd_config
RUN service ssh restart

CMD [ "bash" ]