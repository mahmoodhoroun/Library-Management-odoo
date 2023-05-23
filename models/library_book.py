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
    # reservations_id = fields.One2many("library.reservations", "book_id")
    copies = fields.Integer()
    # total  = fields.Integer(compute="_count_book_salary")
    partner_id = fields.Many2one("res.partner")

    _sql_constraints = [
        ('isbn_unique', 'UNIQUE(isbn)', 'isbn must be unique.'),
        ]
    
    # @api.depends("copies", "price")
    # def _count_book_salary(self):
    #     mount = 0
    #     for record in self:
    #         mount += record.price * record.copies
    #     raise UserError(mount)

    @api.model
    def print_library_book_report(self):
        all_books = self.search([])
        # raise UserError(all_books)
        data = {
            'docs': all_books,
            'total_price': sum(book.price * book.copies for book in all_books),
        }
        return self.env.ref('library_management.action_report_library_book').report_action(self, data=data)
        


    