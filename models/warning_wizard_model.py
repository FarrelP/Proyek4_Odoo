from odoo import models, fields, api

class WarningWizard(models.TransientModel):
    _name="warning.wizard"
    date_out = fields.Date('Date Out', readonly=True)