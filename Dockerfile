FROM ubuntu:24.04 as builder

# Impostazioni di ambiente (best practice: raggruppare all'inizio)
ENV TERM=xterm \
    TZ=Europe/Rome \
    PATH="/opt/venv/bin:$PATH"

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

#ARG LOGDIR=/var/log/logistics
#WORKDIR /home/Modbus/
# copy requirements in order to leverage cache
#COPY /rootfs/home/Modbus/requirements.txt ./requirements.txt
# venv - deps - reqs all-in-one
RUN apt-get update \
    && apt-get upgrade -y \
    # Combine all installations into a single command
    # Removed redundant packages like make, g++, gcc (included in build-essential)
    && apt-get install -y software-properties-common \
    && add-apt-repository ppa:ubuntu-toolchain-r/test \
    && echo "wireshark-common wireshark-common/install-setuid boolean true" | debconf-set-selections \
    && apt-get install -y --no-install-recommends \
    ca-certificates \
    gcc-13 \
    g++ \
    make \
    git
# Copia il resto dei file e finalizza la configurazione
COPY rootfs /
# Compila solamente la versione di default (s7 300) all'interno del container.
# Then compile server.cpp binaries linking snap7 library copied to /usr/lib
RUN cd /home/S7comm/build/unix/ \
    && make -f x86_64_linux.mk  clean \
    && make -f x86_64_linux.mk \
    && make -f x86_64_linux.mk install \
    && cd /home/S7comm/examples/cpp/x86_64-linux \
    && make clean && make \
    && rm -rf /var/lib/apt/lists/*


FROM ubuntu:24.04

# Continua per tutti gli altri eseguibili...

# Reinstalla le librerie runtime di cui gli eseguibili hanno bisogno.
# Ad esempio, libstdc++6.
RUN apt-get update && apt-get install -y --no-install-recommends \
    libstdc++6 \
    libcap2-bin \
    tshark \
    python3 \
    python3-pip \
    python3-venv \
    git \
    dialog \
    screen \
    ca-certificates \
    supervisor \
    && python3 -m venv /opt/venv \
    && rm -rf /var/lib/apt/lists/*

ARG LOGDIR=/var/log/logistics
WORKDIR /home/Modbus/

# Copia le configurazioni e i file essenziali
# Copia gli eseguibili compilati dallo stage precedente
COPY --from=builder /etc/supervisor /etc/supervisor
COPY --from=builder /home/Modbus/requirements.txt ./requirements.txt
COPY --from=builder /home /home
COPY --from=builder /usr/bin/gui.sh /usr/bin
RUN /opt/venv/bin/pip install --no-cache-dir -r "requirements.txt" \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p $LOGDIR && \
    chmod -R 777 /tmp /var/log/

WORKDIR /home/

ENTRYPOINT ["bash", "gui.sh"]
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/supervisord.conf"]

EXPOSE 502 102



#    RUN mkdir -p $LOGDIR && \
#    chmod -R 777 /tmp /var/log/
#
#WORKDIR /home/
#
#ENTRYPOINT ["bash", "gui.sh"]
#CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/supervisord.conf"]
#
#EXPOSE 502 102