from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    book_ids = fields.One2many('library.book', 'partner_id', string='Books')
