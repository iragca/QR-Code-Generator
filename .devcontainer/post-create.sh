#!/bin/bash

sudo apt update
sudo apt upgrade -y
pip install virtualenv
virtualenv .venv
