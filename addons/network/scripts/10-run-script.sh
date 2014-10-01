#!/bin/bash
# file: 10-run-script.sh

cd /tmp
wget https://www.vauxoo.com/vauxoo_doc/static/html/_downloads/openerp-server
#Debo cambiar los parámetros manuales, sería interesante que la salida de los parametros
#anteriores templetizaran esto como un instalador pero con parametros cada usuario es diferente

echo "Edita las variables de tu instalacion CONFIGFILE/USER/DAEMON en /tmp/openerp-server"
