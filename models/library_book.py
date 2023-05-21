from odoo import fields, models,api
from odoo.exceptions import UserError , ValidationError


class LibraryBook(models.Model):
    _name = "library.book"
    _description = "Library Book"    

    name = fields.Char(required=True)
    isbn = fields.Integer()
    author_ids = fields.Many2one("library.author")
    publication_date = fields.Date()
    price = fields.Integer()


    _sql_constraints = [
        ('isbn_unique', 'UNIQUE(isbn)', 'isbn must be unique.'),
        ]
