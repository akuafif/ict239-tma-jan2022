echo "Creating virtual environment..."
echo "python3 -m venv q2venv"
python3 -m venv q2venv

echo ""
echo "Entering virtual environment..."
echo ". q2venv/bin/activate"
. q2venv/bin/activate

echo ""
echo "Installing requirement.txt..."
echo "pip install -r requirement.txt"
pip install -r requirement.txt

echo ""
chmod +x ./start.sh
while true; do
    read -p "Setup completed. Do you wish to run the start.sh? [Y/N] " yn
    case $yn in
        [Yy]* ) ./start.sh; break;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes or no.";; 
    esac
done