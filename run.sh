# create a virtual environment
python3 -m venv env

# activate the virtual environment
source env/bin/activate

# install Flask
pip install -r requirements.txt

# run the Flask app
python entrypoint.py
