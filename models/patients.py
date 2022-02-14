from odoo import models, fields, api
from datetime import date
from odoo.exceptions import ValidationError
import re

from odoo.exceptions import UserError


class HmsPatients(models.Model):
    _name = 'hms.patients'
    _rec_name = 'First_name'
    state = fields.Selection([
        ('Default', 'Default'),
        ('Undetermined', 'Undetermined'),
        ('Good', 'Good'),
        ('Fair', 'Fair'),
        ('Serious', 'Serious'),
    ], default='Default')
    First_name = fields.Char()
    Last_name = fields.Char()
    Email = fields.Char()
    Birth_date = fields.Date()
    History = fields.Html()
    CR_ratio = fields.Float()
    Blood_type = fields.Selection([
        ('A', 'A'),
        ('B', 'B'),
        ('O', 'O')
    ])
    PCR = fields.Boolean()
    Image = fields.Image()
    Address = fields.Text()
    Age = fields.Integer(compute='_calc_student_age')
    departments_id = fields.Many2one('hms.departments')
    doctor_id = fields.Many2many('hms.doctors', 'doctor_patient')
    Capacity = fields.Integer(related="departments_id.Capacity")
    departments_name = fields.Char(related="departments_id.name")
    crm_ids = fields.One2many('res.partner', 'related_patient_id')
    website=fields.Char(related="crm_ids.website")


    def _calc_student_age(self):
        for rec in self:
            rec.Age=date.today().year - self.Birth_date.year
    @api.onchange('Birth_date')
    def _onchange(self):
        if self.Birth_date:
            self.Age = date.today().year - self.Birth_date.year
            if self.Age <= 30:
                self.PCR = True
                return {
                    'warning': {
                        'title': 'Alert',
                        'message': 'PCR has been check '
                    }

                }

    def Undetermined(self):
        self.state = 'Undetermined'

    def Good(self):
        self.state = 'Good'

    def Fair(self):
        self.state = 'Fair'

    def Serious(self):
        self.state = 'Serious'

    @api.onchange('Email')
    def validate_mail(self):
        if self.Email:
            match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.Email)
            count_email = self.search_count([('Email', '=', self.Email)])
            print(count_email,"---------------------------------------------------------------------------------")
            if count_email >= 1 and self.Email is not False:
                raise ValidationError('The email already registered, please use another email!')

            if match == None:
                raise ValidationError('Not a valid E-mail ID')

    # _sql_constraints = [
    #     ('Duplicate email', 'UNIQUE(First_name)', 'this email exist')
    #
    # ]
    # @api.onchange('Age')
    # def _onchange(self):
    #     if self.Age <= 30:
    #         self.PCR=True
    #         return {
    #             'warning':{
    #                 'title':'Alert',
    #                 'message':'PCR has been check '
    #             }
    #
    #
    #         }
