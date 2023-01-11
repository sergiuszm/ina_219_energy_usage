#!/bin/bash

#rsync -av --delete --exclude '.vscode' --exclude '.git' --exclude 'data' /home/serchio/Documents/COAT/master-election-experiments/ pi@ou_con_1:/home/pi/master-election-experiments/
#rsync -av --delete --exclude '.vscode' --exclude '.git' --exclude 'data' /home/serchio/Documents/COAT/master-election-experiments/ pi@ou_con_4:/home/pi/master-election-experiments/
# rsync -av --delete --exclude '.vscode' --exclude '.git' --exclude 'data' /home/serchio/Documents/COAT/master-election-experiments/ pi@ou_con_2:/home/pi/master-election-experiments/
# rsync -av --delete --exclude '.vscode' --exclude '.git' --exclude 'data' --exclude '.vscode' --exclude 'venv' --exclude '.ipynb_checkpoints' \
# /home/serchio/Documents/COAT/master-election-experiments/ pi@rpi_ina219_1.cpsl.lan:/home/pi/master-election-experiments/



#rsync -av --delete --exclude '.vscode' --exclude '.git' --exclude 'data' --exclude '.vscode' --exclude 'venv' --exclude '.ipynb_checkpoints' \
#/home/serchio/Documents/COAT/master-election-experiments/ pi@192.168.100.1:/home/pi/master-election-experiments/
rsync -av --delete --exclude '.vscode' --exclude '.git' --exclude 'data' --exclude '.vscode' --exclude 'venv' --exclude '.ipynb_checkpoints' \
/home/serchio/Documents/COAT/master-election-experiments/ pi@10.128.0.190:/home/pi/master-election-experiments/

