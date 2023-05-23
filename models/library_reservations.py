from odoo import fields, models,api
from odoo.exceptions import UserError , ValidationError
from datetime import date



class LibraryReservations(models.Model):
    _name = "library.reservations"

    book_id = fields.Many2one("library.book")
    date_from = fields.Date(string="From Date")
    borrowing_period = fields.Integer()
    return_date = fields.Date(string="Return Date")
    partner_id = fields.Many2one("res.partner")
    price = fields.Float(readonly=True, compute="_compute_price")
    state = fields.Selection(
         string="State",
         selection=[('draft', 'Draft'), ('posted', 'Posted')]
    )

    @api.depends('book_id')
    def _compute_price(self):
        for record in self:
            record.price = record.book_id.price



            
    @api.model
    def create(self, values):
        book = self.env['library.book'].browse(values.get('book_id'))

        # Subtract one from the number of copies
        if book.copies > 0:  
            book.copies -= 1
            values['state'] = 'draft'

            return super(LibraryReservations, self).create(values)
        else:
            raise UserError("All copies of this book are reserved")
        
    
    def unlink(self):
        # Get the book record
        book = self.book_id

        # Add one to the number of copies
        book.copies += 1

        # Delete the reservation record(s)
        return super(LibraryReservations, self).unlink()

    def action_posted(self):
         for record in self:
              record.state = "posted"





    def create_invoice(self):
        for record in self:
                move_vals = {
                    'move_type': 'out_invoice',
                    'partner_id': record.partner_id.id,
                    'book_id': record.id,
                }
                move = self.env['account.move'].create(move_vals)
                
                # Add invoice lines
                line1_vals = {
                    'name': 'reservation Price',
                    'quantity': 1,
                    'price_unit': record.price,
                    'move_id': move.id,
                }
                move.invoice_line_ids.create([line1_vals])
    @api.model
    def return_reservations(self):
        today = date.today()

        # Find reservations with return_date equals today
        reservations = self.search([('return_date', '=', today)])

        for reservation in reservations:
            # Add one to the number of book copies
            reservation.book_id.copies += 1

            # Delete the reservation
            reservation.unlink()
            
        