#!/bin/bash
#! file: 11-make-service.sh 

mv /tmp/openerp-server /etc/init.d
chmod 755 /etc/init.d/openerp-server
chown root: /etc/init.d/openerp-server
update-rc.d openerp-server defaults
