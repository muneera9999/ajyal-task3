# -*- coding: utf-8 -*-
###################################################################################
#    A part of Educational ERP Project <https://www.educationalerp.com>
#
#    Cybrosys Technologies Pvt. Ltd.
#    Copyright (C) 2018-TODAY Cybrosys Technologies (<https://www.cybrosys.com>).
#    Author: Treesa Maria Jude(treesa@cybrosys.in)
#
#    This program is free software: you can modify
#    it under the terms of the GNU Affero General Public License (AGPL) as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
###################################################################################

from odoo import models, fields, api, _
# from odoo.exceptions import ValidationError, Warning as UserError
from odoo.exceptions import ValidationError,   UserError

class EducationTimeTable(models.Model):
	_name = 'education.timetable'
	_description = 'Timetable'


	active = fields.Boolean('Active', default=True)
	name = fields.Char(compute='get_name')
	# class_division = fields.Many2one('education.division', string='Class', domain="[('academic_year_id', '=', academic_year)]",required=True)
	class_division = fields.Many2one('education.class.division', string='Class', domain="[('academic_year_id', '=', academic_year)]",required=True)
	class_name = fields.Many2one('education.class', string="Standard")
	division_name = fields.Many2one('education.division', string='Division')
	academic_year = fields.Many2one('education.academic.year', string='Academic Year', default=lambda self: self._get_default(),readonly=True,store=True)
	timetable_sat = fields.One2many('education.timetable.schedule', 'timetable_id',
									domain=[('week_day', '=', '0')])
	timetable_sun= fields.One2many('education.timetable.schedule', 'timetable_id',
									domain=[('week_day', '=', '1')])
	timetable_mon = fields.One2many('education.timetable.schedule', 'timetable_id',
									domain=[('week_day', '=', '2')])
	timetable_tue = fields.One2many('education.timetable.schedule', 'timetable_id',
									 domain=[('week_day', '=', '3')])
	timetable_wed = fields.One2many('education.timetable.schedule', 'timetable_id',
									domain=[('week_day', '=', '4')])
	timetable_thur = fields.One2many('education.timetable.schedule', 'timetable_id',
									domain=[('week_day', '=', '5')])
	timetable_fri = fields.One2many('education.timetable.schedule', 'timetable_id',
									domain=[('week_day', '=', '6')])
	company_id = fields.Many2one('res.company', string='School',
								 default=lambda self: self.env['res.company']._company_default_get())
	@api.model
	def _get_default(self):
		""" To get current academic year from academic year model """
		year = self.env['education.academic.year'].search([])
		year_id=0
		for x in year:
			if(x.active==True):
				year_id=x.id
		return year_id

	# @api.model ##### muneera when academic year isn't inputted (so it wont make an error)
	# def _get_default(self): ##### muneera
	# 	current_year = self.env['education.academic.year'].search([('active', '=', True)], limit=1)
	# 	return current_year.id if current_year else False

	def get_name(self):
		"""To generate name for the model"""
		for i in self:
			i.name = str(i.class_division.name) + "/" + str(i.academic_year.name)

	@api.onchange('class_division')
	@api.constrains('class_division')
	def onchange_class_division(self):
		"""To get class and division details from Class Division model"""
		for i in self:
			i.class_name = i.class_division.class_id
			i.division_name = i.class_division.division_id
			# i.academic_year = i.class_division.academic_year_id
			# i.write({'academic_year': i.class_division.academic_year_id})


class EducationTimeTableSchedule(models.Model):
	_name = 'education.timetable.schedule'
	_description = 'Timetable Schedule'
	_rec_name = 'period_id'

	period_id = fields.Many2one('timetable.period', string="Period", required=True)
	check_period = fields.Boolean(string='Period Type',compute='_check_period_type', store=True)
	time_from = fields.Float(string='From', required=True,
							 index=True, help="Start and End time of Period.")
	time_till = fields.Float(string='Till', required=True)
	subject = fields.Many2one('education.subject', string='Subjects')
	faculty_id = fields.Many2one('education.faculty', string='Faculty')
	week_day = fields.Selection([
		('0', 'Saturday'),
		('1', 'Sunday'),
		('2', 'Monday'),
		('3', 'Tuesday'),
		('4', 'Wednesday'),
		('5', 'Thursday'),
		('6', 'Friday'),
	], 'Week day', required=True)
	timetable_id = fields.Many2one('education.timetable', required=True,store=True)
	class_division = fields.Many2one('education.class.division', string='Class', readonly=True)
	company_id = fields.Many2one('res.company', string='School',
								 default=lambda self: self.env['res.company']._company_default_get())
	# _sql_constraints = [('faculty_uniq', 'unique(faculty_id,week_day,period_id)',
	# 					 'This teacher has a lecture in the same time!')]
		
	@api.constrains('faculty_id')
	# @api.constrains('faculty_id', 'week_day', 'period_id')
	def _check_faculty_id(self):
		for record in self:
			# record_ids = self.env['education.timetable.schedule'].search([('id','=', self.env.context.get('active_id'))])
			record_ids = self.env['education.timetable.schedule'].search([('id','>=',0)])
			for rec in record_ids:
				if rec.id != self.id:
				# raise ValidationError(rec)
					if rec.faculty_id == self.faculty_id and rec.week_day == self.week_day and rec.period_id == self.period_id:
						raise ValidationError("This teacher has a lecture in the same time!")
					

	@api.model
	def create(self, vals):
		"""Automatically stores division details fetched from timetable"""
		res = super(EducationTimeTableSchedule, self).create(vals)
		res.class_division = res.timetable_id.class_division.id
		return res

	@api.onchange('period_id')
	def onchange_period_id(self):
		"""Gets the start and end time of the period"""
		for i in self:
			i.time_from = i.period_id.time_from
			i.time_till = i.period_id.time_to


	@api.depends('period_id')
	def _check_period_type(self):
		for rec in self:
			for period in rec.period_id:
				if period.activity == True:
					self.check_period = True
				else:
					self.check_period = False


class TimetablePeriod(models.Model):
	_name = 'timetable.period'
	_description = 'Timetable Period'

	name = fields.Char(string="Name", required=True,)
	time_from = fields.Float(string='From', required=True,
							 index=True, help="Start and End time of Period.")
	time_to = fields.Float(string='To', required=True)
	company_id = fields.Many2one('res.company', string='School',
								 default=lambda self: self.env['res.company']._company_default_get())
	activity = fields.Boolean(string='Activity')