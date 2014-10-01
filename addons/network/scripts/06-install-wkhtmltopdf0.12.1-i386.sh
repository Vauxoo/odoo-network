#!/bin/bash
# file: 06-install-wkhtmltopdf0.12.1-i386.sh
apt-get install -y  libfontconfig1.
apt-get install -y  libfreetype6.
apt-get install -y  libpng12-0.
apt-get install -y  zlib1g.
apt-get install -y  libjpeg-turbo8.
apt-get install -y  libssl1.0.0.
apt-get install -y  libx11-6.
apt-get install -y  libxext6.
apt-get install -y  libxrender1.
apt-get install -y  libstdc++6.
apt-get install -y  libc6.
cd /tmp
wget http://ufpr.dl.sourceforge.net/project/wkhtmltopdf/0.12.1/wkhtmltox-0.12.1_linux-trusty-i386.deb
sudo dpkg -i wkhtmltox-0.12.1_linux-trusty-i386.deb
rm wkhtmltox-0.12.1_linux-trusty-i386.deb
apt-get -f -y install #dependencies above will fail and will stay unsinstalled until we run this.
