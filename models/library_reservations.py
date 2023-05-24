from odoo import fields, models,api
from odoo.exceptions import UserError , ValidationError
from datetime import date

import logging

_logger = logging.getLogger(__name__)


class LibraryReservations(models.Model):
    _name = "library.reservations"

    book_id = fields.Many2one("library.book")
    count_book = fields.Integer(compute="_compute_book")
    date_from = fields.Date(string="From Date")
    borrowing_period = fields.Integer(compute="_compute_borrowing_period", store=True)
    return_date = fields.Date(string="Return Date")
    partner_id = fields.Many2one("res.partner")
    price = fields.Float(readonly=True, compute="_compute_price")
    state = fields.Selection(
         string="State",
         selection=[('draft', 'Draft'), ('posted', 'Posted'), ('paid', 'Paid'), ('canceled','Canceled')]
    )
    sequence_number = fields.Char(string="Sequence Number", readonly=True, copy=False)


    @api.depends("book_id")
    def _compute_book(self):
        for record in self:
            record.count_book = len(record.book_id)
            _logger.info("*******************************************************")


    @api.depends('book_id')
    def _compute_price(self):
        for record in self:
            record.price = record.book_id.price

    @api.depends("date_from", "return_date")
    def _compute_borrowing_period(self):
        for record in self:
            if record.date_from and record.return_date:
                today = date.today()

                if record.date_from < today:
                    raise UserError("Reservation start date cannot be in the past")

                if record.return_date < record.date_from:
                    raise UserError("Return date cannot be earlier than the reservation start date")

                record.borrowing_period = (record.return_date - record.date_from).days
            else:
                record.borrowing_period = 0


            
    @api.model
    def create(self, values):
        sequence = self.env['ir.sequence'].next_by_code('library.reservations') or '/'
        values['sequence_number'] = sequence

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
                'book_id': record.book_id.id,
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
            record.state = "paid"
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
            
    def open_related_books(self):
        invoices = self.env['account.move'].search([('book_id', 'in', self.book_id.ids)])
        action = self.env.ref('library_management.action_invoice_book').read()[0]
        action['domain'] = [('id', 'in', invoices.ids)]
        return action