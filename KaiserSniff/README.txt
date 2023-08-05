# docker build -t kaisersource/kaisersniff . 
# docker run --rm -it -v /home/emanuele/Desktop/LOGICS/Captures/:/home/Captures kaisersource/kaisersniff –cap-add=NET_RAW –cap-add=NET_ADMIN


# By using entrypoint, pass -I <interface> as an argument while running the cointainer
# docker run --cap-add=NET_RAW --cap-add=NET_ADMIN sniffer -I eth0
