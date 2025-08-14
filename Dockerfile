FROM ubuntu:22.04

# Impostazioni di ambiente (best practice: raggruppare all'inizio)
ENV TERM=xterm \
    TZ=Europe/Rome \
    PATH="/opt/venv/bin:$PATH"

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ARG LOGDIR=/var/log/logistics
WORKDIR /home/Modbus/

# copy requirements in order to leverage cache
COPY /rootfs/home/Modbus/requirements.txt ./requirements.txt

# venv - deps - reqs all-in-one
RUN apt-get update && \
    echo "wireshark-common wireshark-common/install-setuid boolean true" | debconf-set-selections && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3 \
    python3-pip \
    python3-venv \
    dialog \
    screen \
    supervisor \
    libcap2-bin \
    tshark && \
    python3 -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir -r "requirements.txt" && \
    rm -rf /var/lib/apt/lists/*

# Copia il resto dei file e finalizza la configurazione
COPY rootfs /
RUN mkdir -p $LOGDIR && \
    chmod -R 777 /tmp /var/log/

WORKDIR /home/

ENTRYPOINT ["bash", "gui.sh"]
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/supervisord.conf"]

EXPOSE 502 102