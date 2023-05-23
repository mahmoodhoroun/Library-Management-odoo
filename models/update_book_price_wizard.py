from odoo import fields, models

class UpdateBookPriceWizard(models.TransientModel):
    _name = 'update.book.price.wizard'
    _description = 'Update Book Price Wizard'

    new_price = fields.Float(string='New Price', required=True)
    book_ids = fields.Many2many('library.book', string='Books')

    def update_book_prices(self):
        self.book_ids.write({'price': self.new_price})
        return {'type': 'ir.actions.act_window_close'}