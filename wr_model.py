# -*- coding: utf-8 -*-
from odoo import models,fields,api
import math
from datetime import datetime
class wrModel(models.Model):
    _name = 'wr.model'
    _description = 'wrmodel'

    #Deskripsi model

    name = fields.Char('Package Name', required=True)

    #variabel ini entar munculnya pas di report invoice. bukan disini harusnya
    sequence_id = fields.Char('Sequence ID', readonly=True)
    
    owner = fields.Char('Owner', required=True)
    length = fields.Integer('Length(m)')
    width = fields.Integer('Width(m)')
    total_space_taken = fields.Integer()
    date_in = fields.Date('Date In')
    date_out = fields.Date('Date Out')
    description = fields.Text('')
    total_price = fields.Integer(string="Total price")
    qty = fields.Integer('Quantity')
    state = fields.Selection([
        ('new', 'New'),
        ('iw', 'In Warehouse'),
        ('out', 'out'),
        ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='new')

    @api.onchange('date_in', 'date_out','total_price','length','width','qty')
    def calculate_date(self):
        if self.date_in and self.date_out:
            d1=datetime.strptime(str(self.date_in),'%Y-%m-%d') 
            d2=datetime.strptime(str(self.date_out),'%Y-%m-%d')
            d3=d2-d1
            self.total_space_taken = self.length*self.width*math.ceil(self.qty/3.0)
            self.total_price = d3.days*3300*self.total_space_taken
    
    @api.multi
    def submit_new_goods(self):
        self.state = 'iw'
		
    @api.multi
    def submit_goods_out(self):
        self.state = 'out'
    
    #Override method
    @api.model
    def create(self, vals):
        vals['sequence_id'] = self.env['ir.sequence'].next_by_code('seq.inv')
        return super(wrModel, self).create(vals)
