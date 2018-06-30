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
    length = fields.Integer('Length(m)')
    width = fields.Integer('Width(m)')
    total_space_taken = fields.Integer()
    date_in = fields.Date('Date In', default=datetime.today(), readonly=True)
    date_out = fields.Date('Date Out')
    description = fields.Text('')
    total_price = fields.Integer('Total Price')
    qty = fields.Integer('Quantity')
    state = fields.Selection(
        [('new', 'New'), ('iw', 'In Warehouse'), ('out', 'Out')],
        string='Status',
        readonly=True,
        copy=False,
        index=True,
        track_visibility='onchange',
        default='new',
    )
    calculated_day = fields.Integer()

    @api.onchange(
        'total_price',
        'date_out',
        'length',
        'width',
        'qty',
    )
    def calculate_date(self):
        if self.date_in and self.date_out:
            d1 = datetime.strptime(str(self.date_in), '%Y-%m-%d')
            d2 = datetime.strptime(str(self.date_out), '%Y-%m-%d')
            d3 = d2 - d1
            self.calculated_day = d3.days
            self.total_space_taken = self.length * self.width*math.ceil(self.qty / 3.0)
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
    
    @api.onchange('date_out')
    def call_warning(self):
        if self.calculated_day < 0:
            mes = {
                'title': 'Invalid value of date in',
                'message': 'The date must not more past than the current date'
            }
            self.date_out = False
            return {'warning':mes}
        # wizard_form = self.env.ref('Custom Warehouse.wizard_view,False')
        # view_id = self.env['warning.wizard']
        # param = {'date_out':self.date_out}
        # new = view_id.create(param)
        # return{
        #     'name':'Test',
        #     'type':'ir.actions.act_window',
        #     'res_model':'warning.wizard',
        #     'res_id':new.id,
        #     'view_id':wizard_form.id,
        #     'view_type':'form',
        #     'view_mode':'form',
        #     'target':'new',
        #     'context': self.env.context
        # }
