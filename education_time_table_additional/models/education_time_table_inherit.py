from odoo import models, fields, api

class EducationTimeTableInherit(models.Model):
    _inherit = 'education.timetable'
    
    schedule_ids= fields.One2many('education.timetable.schedule','timetable_id')
	
 
class EducationTimeTableScheduleInherit(models.Model):
    _inherit = 'education.timetable.schedule'
	
    description =fields.Char()
	
    principal_id = fields.Many2one('res.users', compute='_compute_principal', store=True)
	
    # @api.depends('company_id')
    def _compute_principal(self):
           for record in self:
                   if record.company_id and record.company_id.principal_id:
                    record.principal_id = record.company_id.principal
                   else:
                    record.principal_id = False


class ResUsers(models.Model):
    _inherit='res.users'
    is_principal = fields.Boolean(string='Is Principal')

class ResCompany(models.Model):
    _inherit='res.company'

    principal_id = fields.Many2one('res.users', string='Principal')
