#!/bin/bash
set -e 
INPUT="/home/Modbus/template.csv"
IFS=',' 
#OLDIFS=$IFS
#Internal Field Separator
arr_csv=()
count=0
[ ! -f $INPUT ] && { echo "$INPUT file not found"; exit 99; }
{
read
while IFS=',' read -r VendorName ProductCode VendorUrl ProductName ModelName Version 
do
	arr_csv+=($((++count)) "$VendorName") 
done }< $INPUT

clear
#IFS=$OLDIFS
HEIGHT=15
WIDTH=40
CHOICE_HEIGHT=4
BACKTITLE="LOGistICS"
TITLE="Modbus Honeypot"
MENU="Choose the Modbus PLC template to deploy (sudo):"

OPTIONS=(${arr_csv[@]})
CHOICE1=$(dialog --clear \
                --backtitle "$BACKTITLE" \
                --title "$TITLE" \
                --menu "$MENU" \
                $HEIGHT $WIDTH $CHOICE_HEIGHT \
                "${OPTIONS[@]}" \
                2>&1 >/dev/tty)
clear

case $CHOICE1 in
    1|2|3|4)
    export Modbus=$CHOICE1
        ;;
    esac

HEIGHT=15
WIDTH=40
CHOICE_HEIGHT=4
BACKTITLE="LOGistICS"
TITLE="PLC Siemens Honeypot"
MENU="Choose the PLC to deploy (sudo):"

S7_PATH="/home/S7comm/build/bin/x86_64-linux"
OPTIONS=(1 "Simatic S7-300"
         2 "Simatic S7-400"
         3 "Simatic S7-1200")

CHOICE2=$(dialog --clear \
                --backtitle "$BACKTITLE" \
                --title "$TITLE" \
                --menu "$MENU" \
                $HEIGHT $WIDTH $CHOICE_HEIGHT \
                "${OPTIONS[@]}" \
                2>&1 >/dev/tty)

clear
case $CHOICE2 in
        1)
            cp $S7_PATH/libsnap7_300.so /usr/local/lib/libsnap7.so;
            cp $S7_PATH/libsnap7_300.so /usr/lib/libsnap7.so;
	    echo "Copied";;
        2)
            echo "Copying library..."
            cp $S7_PATH/libsnap7_400.so /usr/local/lib/libsnap7.so;
            cp $S7_PATH/libsnap7_400.so /usr/lib/libsnap7.so;
            echo "Copied";;
        3)
            cp $S7_PATH/libsnap7_1200.so /usr/local/lib/libsnap7.so;
            cp $S7_PATH/libsnap7_1200.so /usr/lib/libsnap7.so;
	    echo "Copied";;
		
esac

S7_SERVER_PATH="$PWD/S7comm/examples/cpp/x86_64-linux"


dialog --title "Would you like to start the honeypot?" \
  --backtitle "LOGistICS" \
  --yesno "Yes: Start, No:Later." 0 0
dialog_status=$?

# Do something

if [ "$dialog_status" -eq 0 ]; then
	clear
	echo "Starting Honeypot..."
	#$S7_SERVER_PATH/server 
	setcap 'cap_net_bind_service=+ep' $S7_SERVER_PATH/server
	#$S7_SERVER_PATH/server  
	setcap 'cap_net_bind_service=+ep' Modbus/LOGistICS.py
	#screen -s "modbus" python3 Modbus/LOGistICS.py -H 0.0.0.0 -T $Modbus 
	#service supervisor stop
	#sleep 5
	sleep 3
    #locate pymodbus
    #service supervisor start
    #/usr/bin/supervisord -c /etc/supervisor/supervisord.conf
    #sleep 3
    #cat /var/log/logistics/logistics.log
    #cat /tmp/supervisord.log
	#supervisorctl stop all
	#sleep 3
	#supervisorctl start all

else
	clear
  	echo "Quitting..."
        exit 0
fi 

exec "$@"
