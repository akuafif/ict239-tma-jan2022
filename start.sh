#!/bin/bash

green="\e[0;92m"
reset="\e[0m"

echo ""
echo -e "${green}Entering virtual environment...${reset}"
echo ". q1venv/bin/activate"
. q1venv/bin/activate

echo ""
echo -e "${green}Setting up flask enviroment variables...${reset}"
echo "export FLASK_APP=./app.py"
echo "export PYTHONPATH=."
echo "export FLASH_ENV=development"
export FLASK_APP=./app.py
export PYTHONPATH=.
export FLASH_ENV=development

echo ""
echo -e "Executing ${green}'flask run'${reset}..."
flask run