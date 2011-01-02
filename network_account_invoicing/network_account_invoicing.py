# -*- coding: utf-8 -*-
##############################################################################
#
#    network_extension module for OpenERP
#    Copyright (C) 2008 Zikzakmedia S.L. (http://zikzakmedia.com)
#       Raimon Esteve <resteve@zikzakmedia.com> All Rights Reserved.
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

from osv import osv
from osv import fields
from tools.translate import _

class network_material(osv.osv):
    _inherit = "network.material"
    _columns = {
        'agreement_id': fields.many2one('inv.agreement','Agreement'),
        'agreement_state': fields.related('agreement_id', 'state', type='char', size="64", string='State', readonly=True),
    }

network_material()

class network_network(osv.osv):
    _inherit = "network.network"
    _columns = {
        'agreement_id': fields.many2one('inv.agreement','Agreement'),
        'agreement_state': fields.related('agreement_id', 'state', type='char', size="64", string='State', readonly=True),
    }

network_network()

class network_software(osv.osv):
    _inherit = "network.software"
    _columns = {
        'agreement_id': fields.many2one('inv.agreement','Agreement'),
        'agreement_state': fields.related('agreement_id', 'state', type='char', size="64", string='State', readonly=True),
    }

network_software()
