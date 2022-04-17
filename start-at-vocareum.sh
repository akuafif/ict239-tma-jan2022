echo "Starting Mongodb.."
echo "/opt/suss/mongodbfiles/manualMongo.sh >> /dev/null"
nohup /opt/suss/mongodbfiles/manualMongo.sh >> /dev/null &

echo ""
echo "Activating virtual environment..."
echo ". q1venv/bin/activate"
. q1venv/bin/activate

echo ""
echo "Setting up enviroment variables..."
echo "export FLASK_APP=./app.py"
echo "export PYTHONPATH=."
echo "export FLASH_ENV=development"
export FLASK_APP=./app.py
export PYTHONPATH=.
export FLASH_ENV=development

echo ""
echo "Executing 'flask run'..."
flask run