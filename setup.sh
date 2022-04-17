#!/bin/bash

green="\e[0;92m"
reset="\e[0m"

echo ""
echo -e "${green}Creating virtual environment...${reset}"
echo "python3 -m venv q2venv"
python3 -m venv q2venv

echo ""
echo -e "${green}Entering virtual environment...${reset}"
echo ". q2venv/bin/activate"
. q2venv/bin/activate

echo ""
echo -e "${green}Installing requirement.txt...${reset}"
echo "pip install -r requirement.txt"
pip install -r requirement.txt

echo ""
chmod +x ./start.sh
echo -e "${green}Setup completed...${reset}"
while true; do
    read -p "Do you wish to run the ./start.sh? [Y/n] " n
    case $n in
        [Nn]* ) exit;;
        * ) ./start.sh;break;; 
    esac
done