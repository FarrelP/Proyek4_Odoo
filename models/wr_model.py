#!/usr/bin/python
# -*- coding: utf-8 -*-

from odoo import models, fields, api
import math
from datetime import datetime

class wrModel(models.Model):
    _name = 'wr.model'
    name = fields.Char('Package Name', required=True)
    sequence_id = fields.Char('Sequence ID', readonly=True)
    owner = fields.Char('Owner', required=True)
    dimen_length = fields.Integer('Length', default=False)
    dimen_width = fields.Integer('Width', default=False)
    total_space_taken = fields.Integer()
    date_in = fields.Date('Date In', default=datetime.today(), readonly=True)
    date_out = fields.Date('Date Out')
    description = fields.Text('')
    total_price = fields.Integer('Total Price')
    qty = fields.Integer('Quantity', default=False)
    state = fields.Selection(
        [('new', 'New'), ('iw', 'In Warehouse'), ('out', 'Out')],
        string='Status',
        readonly=True,
        copy=False,
        index=True,
        track_visibility='onchange',
        default='new',
    )
    location = fields.Selection(
        [('place1', 'Place 1'), ('place2', 'Place 2'), ('place3', 'Place 3')],
        string='Location',
        required=True,
        default='place1',
    )
    calculated_day = fields.Integer()

    @api.onchange(
        'total_price',
        'date_out',
        'dimen_length',
        'dimen_width',
        'width',
        'qty',
    )
    def calculate_date(self):
        if self.date_in and self.date_out:
            d1 = datetime.strptime(str(self.date_in), '%Y-%m-%d')
            d2 = datetime.strptime(str(self.date_out), '%Y-%m-%d')
            d3 = d2 - d1
            self.calculated_day = d3.days
            self.total_space_taken = self.dimen_length * self.dimen_width*math.ceil(self.qty / 3.0)
            self.total_price = d3.days * 3300 * self.total_space_taken

    @api.multi
    def submit_new_goods(self):
        self.state = 'iw'
    
    @api.multi
    def submit_goods_out(self):
        self.state = 'out'

    @api.model
    def create(self, vals):
        vals['sequence_id'] = self.env['ir.sequence'].next_by_code('seq.inv')
        return super(wrModel, self).create(vals)
    
    @api.onchange('dimen_length')
    def validate_length(self):
        if self.dimen_length < 0:
            self.dimen_length = False
            mes = {
                    'title': 'Invalid value',
                    'message': 'Negative number and zero value are not allowed.'
                }
            return {'warning':mes}
    
    @api.onchange('dimen_width')
    def validate_width(self):
        if self.dimen_width < 0:
            self.dimen_width = False
            mes = {
                    'title': 'Invalid value',
                    'message': 'Negative number and zero value are not allowed.'
                }
            return {'warning':mes}
    
    @api.onchange('qty')
    def validate_quantity(self):
        if self.qty < 0:
            self.qty = False
            mes = {
                    'title': 'Invalid value',
                    'message': 'Negative number and zero value are not allowed.'
                }
            return {'warning':mes}
    
    @api.onchange('date_out')
    def call_warning(self):
        if self.calculated_day < 0:
            mes = {
                'title': 'Invalid value of date in',
                'message': 'The date must not more past than the current date'
            }
            self.date_out = False
            return {'warning':mes}
