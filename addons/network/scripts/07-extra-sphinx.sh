#!/bin/bash
# file: 07-extra-sphinx.sh

cd /tmp
git clone https://github.com/thewtex/sphinx-contrib.git
cd sphinx-contrib/youtube
sudo python setup.py install
