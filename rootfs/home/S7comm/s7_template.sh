#!/bin/sh

HEIGHT=15
WIDTH=40
CHOICE_HEIGHT=4
BACKTITLE="LOGtastICS"
TITLE="PLC Siemens Honeypot"
MENU="Choose the PLC to deploy (sudo):"

S7_300_PATH="/home/emanuele/Desktop/LOGICS/s7comm/snap7-full-1.4.0/build/bin/x86_64-linux/libsnap7_300.so"
S7_400_PATH="/home/emanuele/Desktop/LOGICS/s7comm/snap7-full-1.4.0/build/bin/x86_64-linux/libsnap7_400.so"
S7_1200_PATH="/home/emanuele/Desktop/LOGICS/s7comm/snap7-full-1.4.0/build/bin/x86_64-linux/libsnap7_1200.so"

OPTIONS=(1 "Simatic S7-300"
         2 "Simatic S7-400"
         3 "Simatic S7-1200")

CHOICE=$(dialog --clear \
                --backtitle "$BACKTITLE" \
                --title "$TITLE" \
                --menu "$MENU" \
                $HEIGHT $WIDTH $CHOICE_HEIGHT \
                "${OPTIONS[@]}" \
                2>&1 >/dev/tty)

clear
case $CHOICE in
        1)
            cp $S7_300_PATH /usr/local/lib/snap7.so;
            cp $S7_300_PATH /usr/lib/libsnap7.so;
	    echo "Copied";;
        2)
            echo "Copying library..."
            cp $S7_400_PATH /usr/local/lib/libsnap7.so;
            cp $S7_400_PATH /usr/lib/libsnap7.so;
            echo "Copied";;
        3)
            cp $S7_1200_PATH /usr/local/lib/libsnap7.so;
            cp $S7_1200_PATH /usr/lib/libsnap7.so;
	    echo "Copied";;
		
esac

SERVER_PATH="/home/emanuele/Desktop/LOGICS/s7comm/snap7-full-1.4.0/examples/cpp/x86_64-linux"


dialog --title "Would you like to start the honeypot?" \
  --backtitle "LOGistICS" \
  --yesno "Yes: Start, No:Later." 0 0
dialog_status=$?

# Do something

if [ "$dialog_status" -eq 0 ]; then
	clear
	echo "Starting Honeypot..."
	cd $SERVER_PATH
	./server
else
	clear
  	echo "Quitting..."
        exit 0
fi 
