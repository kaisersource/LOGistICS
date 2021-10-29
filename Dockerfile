FROM ubuntu:20.04
ENV TERM xterm
RUN apt update \
&& apt install -y gcc python python3-pip python-setuptools dialog screen supervisor

RUN pip3 install pymodbus twisted numpy pandas service_identity 

COPY . /home 
COPY supervisord.conf /etc/supervisor/conf.d/logistics.conf
WORKDIR /home
CMD ["bash","gui.sh"]

EXPOSE 502 102
