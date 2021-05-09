#pid!/bin/bash

sudo pip3 install psutil


# install rrdtool
sudo apt-get install librrd-dev libpython3-dev
sudo pip3 install rrdtool


#build Flask, jiaja, venv
sudo apt install python3-venv
mkdir flask_app && cd flask_app
python3 -m venv venv
source venv/bin/activate
pip3 install Flask


