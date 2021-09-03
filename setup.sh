#!/bin/bash

echo ""
read -p "System Has Already Upgraded [y/n]: " UPGRADE
read -p "System Has Already Install python3 & pip3 Install [y/n]: " CHECK

if [ $UPGRADE = n ] || [ $UPGRADE = N ];
then
	sudo apt-get update && apt-get upgrade -y
	
	if [ $CHECK = n ] || [ $CHECK = N ];
	then
		sudo apt-get install python3
		sudo apt-get install python3-pip

	elif [ $CHECK = y ] || [ $CHECK = Y ];
	then
		echo "System Already Have python3 & pip3"
	else
		echo "Invalid Input"
	fi
		 
		
elif [ $UPGRADE = y ] || [ $UPGRADE = Y ];
then
	if [ $CHECK = n ] || [ $CHECK = N ];
	then
		sudo apt-get install python3
		sudo apt-get install python3-pip

	elif [ $CHECK = y ] || [ $CHECK = Y ];
	then
		echo "System Already Have python3 & pip3"
	else
		echo -e $'\n\t'"\e[1;91m Invalid Input \e[0m"
	fi
else
	echo -e $'\n\t'"\e[1;91m Invalid Input \e[0m"
fi	
	
sudo pip3 install requests
sudo pip3 install argparse
sudo pip3 install bs4

sudo chmod +x finder.py	
mkdir /usr/share/finder
cp advance.txt /usr/share/finder/
sudo cp finder.py /usr/bin/finder

echo -e $'\n\t'"\e[1;92m ^^ Installation Complete Successfully ^^ \e[0m"

echo -e $'\n'"\e[1;97m Run 'finder' File With The Help Of 'finder --help' \e[0m"	
