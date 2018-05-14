# -*- coding: utf-8 -*-
from odoo import models,fields,api
from datetime import datetime
class wrModel(models.Model):
    _name = 'wr.model'
    _description = 'wrmodel'

    #Deskripsi model

    name = fields.Char('Name', required=True)
    owner = fields.Char('Owner', required=True)
    goods_size = fields.Integer();
    date_in = fields.Date('Date In')
    date_out = fields.Date('Date Out')
    description = fields.Text('')
    total_price = fields.Integer(string="Total price")
    qty = fields.Integer('Quantity')

    @api.onchange('date_in', 'date_out','total_price','goods_size')
    def calculate_date(self):
        if self.date_in and self.date_out:
            d1=datetime.strptime(str(self.date_in),'%Y-%m-%d') 
            d2=datetime.strptime(str(self.date_out),'%Y-%m-%d')
            d3=d2-d1
            self.total_price = d3.days*3300*self.goods_size
