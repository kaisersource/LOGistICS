cd /home/emanuele/Desktop/LOGICS/s7comm/snap7-full-1.4.0/build/unix/
make -f x86_64_linux.mk clean;
make -f x86_64_linux.mk;
sudo cp /home/emanuele/Desktop/LOGICS/s7comm/snap7-full-1.4.0/build/bin/x86_64-linux/libsnap7.so /usr/lib;
sudo cp /home/emanuele/Desktop/LOGICS/s7comm/snap7-full-1.4.0/build/bin/x86_64-linux/libsnap7.so /usr/local/lib;
cd /home/emanuele/Desktop/LOGICS/s7comm/snap7-full-1.4.0/examples/cpp/x86_64-linux/;
make clean;
make;
sudo ./server
