from odoo import exceptions, _
from openerp.exceptions import Warning
from odoo import models, fields, api
import smtplib


class notification(models.Model):
   _name = 'service.notification'
   description = fields.Text(string="Description")
   subject = fields.Text(string="Subject")

   @api.multi
   def send_mail(self):
        partner = self.env['res.partner'].search([])
        for part in partner:      
            mail_values = {
              'email_from': 'techspawn2016.tester@gmail.com',
              'email_to': part.email,
              'subject': self.subject,
              'body_html': self.description,
              # 'notification': True,
            }
            mail = self.env['mail.mail'].create(mail_values)
            mail.send()

        raise Warning('Email Sent')


class contactselect(models.Model):
  _name='addcontact'


  contact = fields.Many2many('res.partner', string="Partner")

  @api.multi
  def send_selected_mail(self):
      mail_obj = self.contact
      for fmail in mail_obj:      
          mail_val = {
          'email_from': 'techspawn2016.tester@gmail.com',
          'email_to': fmail.email,
          'subject': 'Site is under maintenance',
          'body_html': 'We will notify you shortly...',
          # 'notification': True,
          }
          mail = self.env['mail.mail'].create(mail_val)
          mail.send()

      raise Warning('Email Sent')





