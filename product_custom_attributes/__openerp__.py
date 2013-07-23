# -*- encoding: utf-8 -*-
###############################################################################
#                                                                             #
#   product_custom_attributes for OpenERP                                     #
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



{
    'name': 'product_custom_attributes',
    'version': '0.1',
    'category': 'Generic Modules/Others',
    'license': 'AGPL-3',
    'description': u"""
    This module add the posibility to create easily custom field on product.
    Each product can be link to an attributes set (like camera, fridge...)
    And each attributs have custom fields (for example you don't need the same field for a frigde and a camera)
    for Version 7

    本模块可以让你轻松管理产品的自定义属性。每个产品绑定一个属性集合（相机，冰箱...）。
    每个属性集合有它特有的字段（例如你不想冰箱和相机使用同一个字段）。

    支持 OpenERP v7
    """,
    'author': 'Akretion,ShineIT',
    'website': 'http://www.akretion.com/,http://www.openerp.cn/',
    'depends': ['product','stock'],
    'init_xml': [],
    'update_xml': [
           'ir_model_view.xml',
           'product_attribute_view.xml',
           'product_view.xml',
    ],
    'demo_xml': [],
    'installable': True,
    'active': False,
}

