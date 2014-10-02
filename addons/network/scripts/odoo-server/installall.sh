#!/bin/bash
# file: 00-installall.to07.sh 

wget -O- https://raw.githubusercontent.com/Vauxoo/odoo-network/master/addons/network/scripts/01-config-locales-v8.0.sh | sh 
wget -O- https://raw.githubusercontent.com/Vauxoo/odoo-network/master/addons/network/scripts/02-dependencies-odoo-v8.0.sh | sh 
wget -O- https://raw.githubusercontent.com/Vauxoo/odoo-network/master/addons/network/scripts/04-install-pip.sh | sh 
wget -O- https://raw.githubusercontent.com/Vauxoo/odoo-network/master/addons/network/scripts/05-install-dependencies-python-v80.sh | sh 
wget -O- https://raw.githubusercontent.com/Vauxoo/odoo-network/master/addons/network/scripts/06-install-wkhtmltopdf0.12.1-i386.sh | sh 
wget -O- https://raw.githubusercontent.com/Vauxoo/odoo-network/master/addons/network/scripts/07-extra-sphinx.sh | sh 
