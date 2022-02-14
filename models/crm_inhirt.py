from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re

from odoo.exceptions import UserError


class crminhiart(models.Model):
    _inherit = 'res.partner'
    test = fields.Char()
    related_patient_id = fields.Many2one('hms.patients', ondelete='restrict')

    def unlink(self):
        print(self.related_patient_id, '-----------------------------------------')

        if len(self.related_patient_id) != 0 :
            print(self.related_patient_id, '-----------------------------------------')
            raise UserError('cannot delete ')
