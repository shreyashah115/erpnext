# -*- coding: utf-8 -*-
# Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and Contributors
# See license.txt
from __future__ import unicode_literals

import frappe
import unittest
from erpnext.hr.doctype.employee_onboarding.employee_onboarding import make_employee
from erpnext.hr.doctype.employee_onboarding.employee_onboarding import IncompleteTaskError

class TestEmployeeOnboarding(unittest.TestCase):
	def test_employee_onboarding_incomplete_task(self):
		_set_up()
		applicant = get_job_applicant()
		onboarding = frappe.new_doc('Employee Onboarding')
		onboarding.job_applicant = applicant.name
		onboarding.employee_name = 'Test Applicant'
		onboarding.company = '_Test Company'
		onboarding.designation = 'Researcher'
		onboarding.department = 'Research & Development - _TC'
		onboarding.append('activities', {
			'activity_name': 'Assign ID Card',
			'role': 'HR User',
			'required_for_employee_creation': 1
		})
		onboarding.append('activities', {
			'activity_name': 'Assign a laptop',
			'role': 'HR User' 
		})
		onboarding.status = 'Pending'
		onboarding.insert()
		onboarding.submit()
		self.assertEqual(onboarding.project, 'Employee Onboarding : Test Researcher - test@researcher.com')
		self.assertRaises(IncompleteTaskError, make_employee, onboarding.name)

	def test_employee_onboarding_completed_task(self):
		_set_up()
		applicant = get_job_applicant()
		onboarding = frappe.new_doc('Employee Onboarding')
		onboarding.job_applicant = applicant.name
		onboarding.employee_name = 'Test Applicant'
		onboarding.company = '_Test Company'
		onboarding.designation = 'Researcher'
		onboarding.department = 'Research & Development - _TC'
		onboarding.append('activities', {
			'activity_name': 'Assign ID Card',
			'role': 'HR User',
			'required_for_employee_creation': 1
		})
		onboarding.append('activities', {
			'activity_name': 'Assign a laptop',
			'role': 'HR User' 
		})
		onboarding.status = 'Pending'
		onboarding.insert()
		onboarding.submit()
		self.assertEqual(onboarding.project, 'Employee Onboarding : Test Researcher - test@researcher.com')
		project = frappe.get_doc('Project', 'Employee Onboarding : Test Researcher - test@researcher.com')
		project.tasks[0].status = 'Closed'
		project.save()
		onboarding.reload()
		self.assertTrue(make_employee(onboarding.name))

def get_job_applicant():
	if frappe.db.exists('Job Applicant', 'Test Researcher - test@researcher.com'):
		return frappe.get_doc('Job Applicant', 'Test Researcher - test@researcher.com')
	applicant = frappe.new_doc('Job Applicant')
	applicant.applicant_name = 'Test Researcher'
	applicant.email_id = 'test@researcher.com'
	applicant.status = 'Open'
	applicant.cover_letter = 'I am a great Researcher.'
	applicant.insert()
	return applicant

def _set_up():
	for doctype in ["Job Applicant", "Employee Onboarding Template", "Employee Onboarding", "Project", "Task"]:
		frappe.db.sql("delete from `tab{doctype}`".format(doctype=doctype))