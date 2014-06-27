# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2008 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import time
from openerp.osv import fields, osv
from openerp.tools.translate import _
import logging
_logger = logging.getLogger(__name__)

try:
    import digitalocean
except ImportError:
    _logger.warning('Impossible import digitalocean library')

#---------------------------------------------------------
# Type of hardware: Printers, Screens, HD, ....
#---------------------------------------------------------


class network_hardware_type(osv.Model):
    _name = "network.hardware.type"
    _description = "Hardware type"
    _columns = {
        'name': fields.char('Type of material',
                            size=64,
                            translate=True,
                            required=True),
        'networkable': fields.boolean('Networkable hardware'),
    }
    _defaults = {
        'networkable': lambda *a: False,
    }

#--------------------------------------------------------------
# A network is composed of all kind of networkable materials
#--------------------------------------------------------------


class network_network(osv.Model):
    _name = 'network.network'
    _description = 'Network'
    _columns = {
        'type': fields.selection([('intranet', 'Intranet'),
                                ('dedicated', 'Dedicated')],
                                'Type of network', required=True,
                                help='Intranet: Internal network'
                                'Dedicated: digitalocean, amazon, iweb, etc'),
        'name': fields.char('Network name', size=64, required=True),
        'range': fields.char('Address range', size=128),
        'user_id': fields.many2one('res.users', 'Onsite Contact person'),
        'contact_id': fields.many2one('res.partner', 'Partner'),
        'gateway': fields.char('Gateway', size=100),
        'dns': fields.char('DNS', size=100,
                           help="List of DNS servers, separated by commas"),
        'public_ip_address': fields.char('Public IP address', size=100),
        'public_domain': fields.char('Public domain', size=100),
        'material_ids': fields.one2many('network.material',
                                        'network_id',
                                        'Members'),
        'client_id': fields.char('Client ID', 250,
                                help='Client Id to connect'),
        'api_key': fields.char('API Key', 250,
                                help='Api Key to connect'),
        'state': fields.selection([('draft', 'Draft'),
                                   ('tested', 'Connection Tested'),
                                   ('synced', 'Synced'),
                                   ('cancel', 'Cancel')], 'State',
                                   required=True, 
                                   help='State of the syncronization process '
                                   'if it applies')
    }

    _defaults = {
            'type': 'intranet',
            'state': 'draft'
    }

    def test_key(self, cr, uid, ids, context=None):
        obj = self.browse(cr, uid, ids, context=context)
        for i in  obj:
            try:
                manager = digitalocean.Manager(client_id=i.client_id,
                        api_key=i.api_key)
                my_droplets = manager.get_all_droplets()
            except Exception as inst:
                raise osv.except_osv(
                    _('Error !'),
                    _('Error with the conection to digitalocean. %s' % str(inst)))
        return self.write(cr, uid, ids, {'state': 'tested'}, context=context)

    def sync_servers(self, cr, uid, ids, context=None):
        obj = self.browse(cr, uid, ids, context=context)
        for i in obj:
            if i.state=='tested':
                manager = digitalocean.Manager(client_id=i.client_id,
                        api_key=i.api_key)
                my_droplets = manager.get_all_droplets()
                for droplet in my_droplets:
                    self.write(cr, uid, i.id,
                            {'material_ids': [(0, 0, {'name': droplet.name})]}) 
            else:
                raise osv.except_osv(
                    _('Error !'),
                    _('You must test the connection first'))
        return self.write(cr, uid, ids, {'state': 'synced'}, context=context)


def _calc_warranty(*args):
    now = list(time.localtime())
    now[0] += 1
    return time.strftime('%Y-%m-%d', tuple(now))

#----------------------------------------------------------
# Materials; computer, printer, switch, ...
#----------------------------------------------------------


class network_material(osv.Model):
    _name = 'network.material'
    _description = 'Material'
    _inherit = [
        'mail.thread',
        'ir.needaction_mixin',
    ]
    _track = {
        'name': {
            'network.mt_material_new': lambda self, cr, uid, obj, ctx=None:
            obj.name,
        },
        'user_id': {
            'network.mt_material_assigned': lambda self, cr, uid, obj, ctx=None: obj.user_id and obj.user_id.id,
        },
    }
    _columns = {
        'name': fields.char('Device Name', required=True,
                            help="Unique identicator to have as reference.",
                            track_visibility='onchange'),
        'ip_addr': fields.char('IP Address', required=False,
                               help="Unique identicator to have as reference.",
                               track_visibility='onchange'),
        'mac_addr': fields.char('MAC addresss', size=17),
        'partner_id': fields.related('network_id', 'contact_id',
                                     type='many2one', relation='res.partner',
                                     string='Partner', readonly=True),
        'network_id': fields.many2one('network.network', 'Network',
                                      help="Network where this hardware is "
                                      "linked to: i.e. DigitalOcean"
                                      " joe@vauxoo.com"),
        'supplier_id': fields.many2one('res.partner', 'Supplier',
                                       help="Partner to who we are buying "
                                       "services running on this "
                                       " device: Be careful it is only for "
                                       "invoicing purpose."),
        'date': fields.date('Installation Date'),
        'warranty': fields.date('Warranty deadline'),
        'type': fields.many2one('network.hardware.type',
                                'Hardware type'),
        'note': fields.text('Notes'),
        'parent_id': fields.many2one('network.material',
                                     'Parent Material'),
        'child_id': fields.one2many('network.material', 'parent_id',
                                    'Childs Materials'),
        'software_id': fields.one2many('network.software',
                                       'material_id',
                                       'Installed Software'),
        'change_ids': fields.one2many('network.changes',
                                      'machine_id',
                                      'Changes on this machine'),
        'network_information_ids': fields.one2many('network.information',
                                                   'hardware_id',
                                                   'IP Hostname Information'),
        'user_id': fields.many2one('res.users',
                                   'Assigned To',
                                   track_visibility='onchange'),
        'color': fields.integer('Color Index', select=True,
                                help="Green: On Line, Red: OffLine, Orange: "
                                "Under controlled"
                                " mantainance")
    }
    _defaults = {
        'date': lambda *a: time.strftime('%Y-%m-%d'),
        'warranty': _calc_warranty,
        'user_id': lambda s, c, u, i, ctx=None: u,
    }


class network_information(osv.Model):
    _name = 'network.information'
    _description = 'Network Information'
    _rec_name = "hostname"
    _order = "hostname asc"

    _columns = {
        'hostname': fields.char('Hostname', required=True),
        'ip_addr': fields.char('IP', required=True),
        'hardware_id': fields.many2one('network.material',
                                       'Machine'),
    }

#----------------------------------------------------------
# Changes on this machine
#----------------------------------------------------------


class network_changes(osv.Model):
    _name = 'network.changes'
    _description = 'Network changes'

    _columns = {
        'name': fields.char('Short Description', size=64,
                            required=True),
        'description': fields.text('Long Description'),
        'date': fields.datetime('Change date'),
        'machine_id': fields.many2one('network.material',
                                      'Machine'),
        'user_id': fields.many2one('res.users', 'User', required=True),
        'task_id': fields.many2one('project.task', 'Task',
                                   required=False,
                                   help="""May be the task must be delegated
                                   from a bigger project and
            set of changes, be sure link correctly the task itself to
            understand the features / reasons why this update was done"""),
    }

    _defaults = {
        'date': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
        'user_id': lambda self, cr, uid, ctx: uid,
    }

    _order = 'date desc'

#----------------------------------------------------------
# Type of Software; LDAP, Tiny ERP, Postfix
#----------------------------------------------------------


class network_soft_type(osv.Model):
    _name = "network.software.type"
    _description = "Software type"
    _columns = {
        'name': fields.char('Composant Name',
                            size=64,
                            translate=True,
                            required=True),
        'note': fields.text('Notes'),
    }

#----------------------------------------------------------
# A software installed on a material
#----------------------------------------------------------


class network_software(osv.Model):
    _name = "network.software"
    _description = "Software"
    _columns = {
        'name': fields.char('Composant Name', size=64, required=True),
        'material_id': fields.many2one('network.material', 'Material'),
        'type': fields.many2one('network.software.type',
                                'Software Type', required=True, select=1),
        'version': fields.char('Software version', size=32),
        'logpass': fields.one2many('network.software.logpass',
                                   'software_id', 'Login / Password'),
        'email': fields.char('Contact Email', size=32),
        'date': fields.date('Installation Date', size=32),
        'note': fields.text('Notes'),
        'service_ids': fields.one2many('network.service', 'software_id',
                                       string='Service'),
        'network_id': fields.related('material_id', 'network_id',
                                     type='many2one',
                                     relation='network.network',
                                     string='Network',
                                     readonly=True),
        'partner_id': fields.related('material_id', 'partner_id',
                                     type='many2one',
                                     relation='res.partner',
                                     string='Partner',
                                     readonly=True),
    }

    def _default_material(self, cursor, user, context=None):
        if not context.get('material_id', False):
            return False
        value = context['material_id']
        return value

    _defaults = {
        'material_id': lambda obj, cursor, user, context: obj._default_material(cursor, user, context=context),
    }

#------------------------------------------------------------
# Couples of login/password
#------------------------------------------------------------


class network_software_logpass(osv.Model):
    _name = "network.software.logpass"
    _description = "Software login"
    _rec_name = 'login'
    _columns = {
        'login': fields.char('Login', size=64, required=True),
        'password': fields.char('Password', size=64, required=True),
        'software_id': fields.many2one('network.software',
                                       'Software', required=True),
        'name': fields.char('Name', size=100),
        'note': fields.text('Note'),
        'material': fields.related('software_id', 'material_id',
                                   type='many2one',
                                   relation='network.material',
                                   string='Material',
                                   readonly=True),
        'encrypted': fields.boolean('Encrypted'),
        'superuser': fields.boolean('Super User'),
    }

    _defaults = {
        'encrypted': lambda obj, cursor, user, context: False,
    }

    def onchange_password(self, cr, uid, ids, encrypted, context={}):
        return {'value': {'encrypted': False}}

    def encrypt_password(self, cr, uid, ids, context=None):
        for rec in self.browse(cr, uid, ids):
            try:
                from Crypto.Cipher import ARC4
            except ImportError:
                raise osv.except_osv(
                    _('Error !'), _('Package python-crypto no installed.'))

            if not rec.encrypted:
                obj_enc_password = self.pool.get(
                    'network.encrypt.password')
                dom = [('create_uid', '=', uid), ('write_uid', '=', uid)]
                enc_password_ids = obj_enc_password.search(cr, uid, dom)
                encrypt_password_id = enc_password_ids and enc_password_ids[
                    0] or False
                if encrypt_password_id:
                    passwordkey = obj_enc_password.browse(
                        cr, uid, encrypt_password_id).name
                    enc = ARC4.new(passwordkey)
                    try:
                        encripted = base64.b64encode(enc.encrypt(rec.password))
                    except UnicodeEncodeError:
                        break
                    self.write(cr, uid, [rec.id],
                               {'password': encripted, 'encrypted': True})
                else:
                    raise osv.except_osv(
                        _('Error !'), _('Not encrypt/decrypt password'
                                        ' has given.'))
        return True

    def decrypt_password(self, cr, uid, ids, context=None):
        for rec in self.browse(cr, uid, ids):
            try:
                from Crypto.Cipher import ARC4
            except ImportError:
                raise osv.except_osv(
                    _('Error !'), _('Package python-crypto no installed.'))

            if rec.encrypted:
                obj_encrypt_password = self.pool.get(
                    'network.encrypt.password')
                enc_password_ids = obj_encrypt_password.search(
                    cr, uid, [('create_uid', '=', uid),
                              ('write_uid', '=', uid)])
                encrypt_password_id = enc_password_ids and enc_password_ids[
                    0] or False
                if encrypt_password_id:
                    passwordkey = obj_encrypt_password.browse(
                        cr, uid, encrypt_password_id).name
                    dec = ARC4.new(passwordkey)
                    try:
                        desencripted = dec.decrypt(
                            base64.b64decode(rec.password))
                        unicode(desencripted, 'ascii')
                        raise osv.except_osv(
                            rec.login + _(' password:'), desencripted)
                    except UnicodeDecodeError:
                        raise osv.except_osv(
                            _('Error !'), _('Wrong encrypt/decrypt password.'))
                else:
                    raise osv.except_osv(
                        _('Error !'), _('Not encrypt/decrypt '
                                        'password has given.'))
        return True

#----------------------------------------------------------
# Protocol (ssh, http, smtp, ...)
#----------------------------------------------------------


class network_protocol(osv.Model):

    """
    Protocol (ssh, http, smtp, ...)
    """
    _name = "network.protocol"
    _description = "Protocol"

    _columns = {
        'name': fields.char('Name', size=64, required=True, select=1),
        'description': fields.char('Description', size=256, translate=True),
        'port': fields.integer('Port',
                               help='Default port defined '
                               'see(http://goo.gl/ldwcuY)',
                               required=True),
        'protocol': fields.selection([
                                    ('tcp', 'TCP'),
                                    ('udp', 'UDP'),
                                    ('both', 'Both'),
                                    ('other', 'Other')],
                                    'Protocol', required=True),
    }

#----------------------------------------------------------
# Services
#----------------------------------------------------------


class network_service(osv.Model):

    """
    Services
    """
    _name = "network.service"
    _description = "Service Network"

    _columns = {
        'name': fields.char('Name', size=64, select=1),
        'software_id': fields.many2one('network.software', 'Software', required=True),
        'material': fields.related('software_id', 'material_id', type='many2one', relation='network.material', string='Material', readonly=True),
        'protocol_id': fields.many2one('network.protocol', 'Protocol', select=1),
        'path': fields.char('Path', size=100),
        'port': fields.integer('Port', required=True, select=2),
        'public_port': fields.integer('Public port', select=2, help="Sometimes public and private ports are different."),
        'private_url': fields.char('Private URL', size=256),
        'public_url': fields.char('Public URL', size=256),
    }

    def _compute_public_url(self, cr, uid, ids, context=None):
        for rec in self.browse(cr, uid, ids):
            if not rec.protocol_id or not rec.software_id:
                continue
            protocol = rec.protocol_id.name + "://"
            port = rec.port and ":" + str(rec.port) or ""
            public_port = rec.public_port and ":" + str(rec.public_port) or ""
            path = rec.path and rec.path or ""

            # Compute Private URL from Material IP
            ip_address = rec.software_id.material_id.ip_addr
            if ip_address:
                service2 = protocol + ip_address + port + path
                self.write(cr, uid, [rec.id], {'private_url': service2})

            # Compute Public URL from Network IP
            if not rec.software_id.material_id.network_id:
                continue
            public_ip_address = rec.software_id.material_id.network_id.public_ip_address
            public_domain = rec.software_id.material_id.network_id.public_domain
            if public_domain:
                service1 = protocol + public_domain + public_port + path
                self.write(cr, uid, [rec.id], {'public_url': service1})
            elif public_ip_address:
                service1 = protocol + public_ip_address + public_port + path
                self.write(cr, uid, [rec.id], {'public_url': service1})

        return True

    def onchange_port(self, cr, uid, ids, port, context={}):
        if not port:
            return {}
        return {'value': {'public_port': port}}


class network_encrypt_password(osv.TransientModel):

    """
    Password encryption
    """
    _name = 'network.encrypt.password'
    _description = 'Password encryption'

    _columns = {
        'name': fields.char('Encrypt/Decrypt password', size=100),
    }

    def create(self, cr, uid, vals, context=None):
        encrypt_password_ids = self.search(
            cr, uid, [('create_uid', '=', uid), ('write_uid', '=', uid)], context=context)
        self.unlink(cr, uid, encrypt_password_ids, context=context)
        return super(osv.osv_memory, self).create(cr, uid, vals, context=context)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
