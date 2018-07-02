from odoo import api,models,fields

class LocationModel(models.Model):
    _name = 'location.model'
    _description = 'locmodel'

    name = fields.Char('Location Name', required=True)