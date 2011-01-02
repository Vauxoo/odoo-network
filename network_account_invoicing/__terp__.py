# -*- coding: utf-8 -*-
##############################################################################
#
#    network_extension module for OpenERP
#    Copyright (C) 2008 Zikzakmedia S.L. (http://zikzakmedia.com)
#       Jordi Esteve <jesteve@zikzakmedia.com> All Rights Reserved.
#    Copyright (C) 2009 SYLEAM (http://syleam.fr)
#       Christophe Chauvet <christophe.chauvet@syleam.fr> All Rights Reserved.
#
#    This file is a part of network_extension
#
#    network_extension is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    network_extension is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    "name" : "Network Account Invoicing",
    "version" : "1.0",
    "author" : "Zikzakmedia SL",
    "category" : "Enterprise Specific Modules/Information Technology",
    "website": "www.zikzakmedia.com",
    "license" : "GPL-3",
    "depends" : ["network","account_invoicing"],
    'init_xml': [],
    "demo_xml" : [],
    "update_xml" : [
        "network_account_invoicing_view.xml",
    ],
    "description": """
        Relation Network with Invoicing.
        Relation Materials with Invoicing.
        Relation Software with Invoicing.
    """,
    "active" : False,
    "installable": True
}
