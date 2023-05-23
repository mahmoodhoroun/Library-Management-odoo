from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    book_id = fields.Many2one("library.book", string="Book")
