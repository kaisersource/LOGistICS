FROM ubuntu:20.04
ENV TERM xterm

ARG LOGDIR=/var/log/logistics
COPY /rootfs/home/Modbus/requirements.txt /home/Modbus/requirements.txt
WORKDIR /home/Modbus/
RUN apt update \
    && apt install -y gcc python python3-pip python-setuptools dialog screen supervisor wireshark libcap2-bin \
    && pip3 install -r "requirements.txt" && mkdir -p $LOGDIR \
    && chmod -R 777 /tmp /var/log/ 
COPY rootfs /
#Kernel capabilities basedir
WORKDIR /home/
#RUN apt install mlocate && updatedb
ENTRYPOINT ["bash","gui.sh"]
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/supervisord.conf"]

EXPOSE 502 102
