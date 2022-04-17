echo "Creating virtual environment..."
echo "python3 -m venv q1venv"
python3 -m venv q1venv

echo ""
echo "Entering virtual environment..."
echo ". q1venv/bin/activate"
. q1venv/bin/activate

echo ""
echo "Installing requirement.txt..."
echo "pip install -r requirement.txt"
pip install -r requirement.txt

echo ""
chmod +x ./start.sh
while true; do
    read -p "Setup completed. Do you wish to run the start.sh? [Y/n] " n
    case $n in
        [Nn]* ) exit;;
        * ) ./start.sh;break;; 
    esac
done