# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe

from frappe.model.document import Document

class Department(Document):
	def validate(self):
		self.validate_employee_leave_approver()
		self.validate_employee_expense_approver()

	def validate_employee_leave_approver(self):
		for l in self.get("leave_approvers")[:]:
			if "Leave Approver" not in frappe.get_roles(l.leave_approver):
				frappe.get_doc("User", l.leave_approver).add_roles("Leave Approver")

	def validate_employee_expense_approver(self):
		for e in self.get("expense_approvers")[:]:
			if "Expense Approver" not in frappe.get_roles(e.expense_approver):
				frappe.get_doc("User", e.expense_approver).add_roles("Expense Approver")