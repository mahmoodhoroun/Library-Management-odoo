from odoo import fields, models,api
from odoo.exceptions import UserError , ValidationError


class LibraryAuthor(models.Model):
    _name = "library.author"
    _description = "Library Author"    

    name = fields.Char(required=True)
    birth_date = fields.Date()
    book_ids = fields.One2many("library.book", "author_ids")
    total_books = fields.Float(compute="_compute_total_books")


    @api.depends("book_ids")
    def _compute_total_books(self):
        for record in self:
            record.total_books = len(record.book_ids)

    
