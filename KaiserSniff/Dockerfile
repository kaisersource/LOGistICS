FROM ubuntu:22.04

LABEL KaiserSource <pgiatasti>
USER root

RUN apt update -y \
    && apt -y install mlocate 

RUN apt install -y python3-pip \
    && pip3 install trollius pyshark tqdm requests 

#Fix permissions dumpcap for tshask/pyshark
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y tshark 

RUN addgroup wireshark \
&& setcap 'CAP_NET_RAW+eip CAP_NET_ADMIN+eip' /usr/bin/dumpcap \
&& chgrp wireshark /usr/bin/dumpcap \
&& chmod 750 /usr/bin/dumpcap

WORKDIR /home
RUN mkdir Captures
COPY Sniffer.py constants.py ./ 
ENTRYPOINT ["python3","Sniffer.py"]


