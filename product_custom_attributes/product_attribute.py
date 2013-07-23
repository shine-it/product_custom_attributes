# -*- encoding: utf-8 -*-
###############################################################################
#                                                                             #
#   product_custom_attributes for OpenERP                                      #
#   Copyright (C) 2011 Akretion Benoît GUILLOT <benoit.guillot@akretion.com>  #
#   Copyright (C) 2013  ShineIT<contact@openerp.cn>                          #
#                                                                             #
#   This program is free software: you can redistribute it and/or modify      #
#   it under the terms of the GNU Affero General Public License as            #
#   published by the Free Software Foundation, either version 3 of the        #
#   License, or (at your option) any later version.                           #
#                                                                             #
#   This program is distributed in the hope that it will be useful,           #
#   but WITHOUT ANY WARRANTY; without even the implied warranty of            #
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the             #
#   GNU Affero General Public License for more details.                       #
#                                                                             #
#   You should have received a copy of the GNU Affero General Public License  #
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.     #
#                                                                             #
###############################################################################

from openerp.osv.orm import Model
from openerp.osv import fields
from openerp.osv.osv import except_osv
from openerp.tools.translate import _
from unidecode import unidecode # Debian package python-unidecode

class attribute_option(Model):
    _name = "attribute.option"
    _description = "Attribute Option"
    _order="sequence"

    _columns = {
        'name': fields.char('Name', size=128, translate=True, required=True),
        'attribute_id': fields.many2one('product.attribute', 'Product Attribute', required=True),
        'sequence': fields.integer('Sequence'),
    }


class product_attribute(Model):
    _name = "product.attribute"
    _description = "Product Attribute"
    _inherits = {'ir.model.fields': 'field_id'}
    _columns = {
        'field_id': fields.many2one('ir.model.fields', 'Ir Model Fields', required=True, ondelete="cascade"),
        'attribute_type': fields.selection([('char','Char'),
                                            ('text','Text'),
                                            ('select','Select'),
                                            ('multiselect','Multiselect'),
                                            ('boolean','Boolean'),
                                            ('integer','Integer'),
                                            ('date','Date'),
                                            ('datetime','Datetime'),
                                            ('binary','Binary'),
                                            ('float','Float'),
                                            # for many2one and many2many
                                            ('m2o', 'Many2One'),
                                            ('m2m', 'Many2Many')],
                                           'Type', required=True),
        # for many2one and many2many
        'option_relation': fields.many2one('ir.model', 'Relation'),
        'serialized': fields.boolean('Field serialized',
                                     help="If serialized, the field will be stocked in the serialized field: "
                                     "attribute_custom_tmpl or attribute_custom_variant depending on the field based_on"),
        'based_on': fields.selection([('product_template','Product Template'),
                                      ('product_product','Product Variant')],
                                     'Based on', required=True),
        'option_ids': fields.one2many('attribute.option', 'attribute_id', 'Attribute Option'),
        'create_date': fields.datetime('Created date', readonly=True),
        }

    def create(self, cr, uid, vals, context=None):
        model_obj = self.pool.get('ir.model')
        if vals.get('based_on') == 'product_template':
            vals['model_id'] = model_obj.search(cr, uid, [('model', '=', 'product.template')], context=context)[0]
            serial_name = 'attribute_custom_tmpl'
        else:
            vals['model_id'] = model_obj.search(cr, uid, [('model', '=', 'product.product')], context=context)[0]
            serial_name = 'attribute_custom_variant'
        if vals.get('serialized'):
            vals['serialization_field_id'] = self.pool.get('ir.model.fields').search(cr, uid, [('name', '=', serial_name)], context=context)[0]
        if vals['attribute_type'] == 'select':
            vals['ttype'] = 'many2one'
            vals['relation'] = 'attribute.option'
        # for many2one and many2many
        elif vals['attribute_type'] == 'm2o' or vals['attribute_type'] == 'm2m':
            vals['ttype'] = vals['attribute_type'] == 'm2o' and 'many2one' or 'many2many'
            option_model = model_obj.browse(cr, uid, vals['option_relation'])
            vals['relation'] = option_model.model
        elif vals['attribute_type'] == 'multiselect':
            vals['ttype'] = 'many2many'
            vals['relation'] = 'attribute.option'
            if not vals.get('serialized'):
                raise except_osv(_('Create Error'), _("The field serialized should be ticked for a multiselect field !"))
        else:
            vals['ttype'] = vals['attribute_type']
        vals['state'] = 'manual'
        return super(product_attribute, self).create(cr, uid, vals, context)

    def onchange_field_description(self, cr, uid, ids, field_description, context=None):
        name = 'x_'
        if field_description:
            name = unidecode('x_%s' % field_description).rstrip().replace(' ', '_').lower()
        return  {'value' : {'name' : name}}


class attribute_location(Model):
    _name = "attribute.location"
    _description = "Attribute Location"
    _order="sequence"
    _inherits = {'product.attribute': 'attribute_id'}
    _columns = {
        'attribute_id': fields.many2one('product.attribute', 'Product Attribute', required=True, ondelete="cascade"),
        'attribute_set_id': fields.related('attribute_group_id', 'attribute_set_id', type='many2one', relation='attribute.set', string='Attribute Set', store=True, readonly=True),
        'attribute_group_id': fields.many2one('attribute.group', 'Attribute Group', required=True),
        'sequence': fields.integer('Sequence'),
        }


class attribute_group(Model):
    _name= "attribute.group"
    _description = "Attribute Group"
    _order="sequence"

    _columns = {
        'name': fields.char('Name', size=128, required=True),
        'attribute_set_id': fields.many2one('attribute.set', 'Attribute Set', required=True),
        'attribute_ids': fields.one2many('attribute.location', 'attribute_group_id', 'Attributes'),
        'sequence': fields.integer('Sequence'),
    }

    def create(self, cr, uid, vals, context=None):
        for attribute in vals['attribute_ids']:
            if attribute[2] and not attribute[2].get('attribute_set_id'):
                attribute[2]['attribute_set_id'] = vals['attribute_set_id']
        return super(attribute_group, self).create(cr, uid, vals, context)

class attribute_set(Model):
    _name = "attribute.set"
    _description = "Attribute Set"
    _columns = {
        'name': fields.char('Name', size=128, required=True),
        'attribute_group_ids': fields.one2many('attribute.group', 'attribute_set_id', 'Attribute Groups'),
        }

