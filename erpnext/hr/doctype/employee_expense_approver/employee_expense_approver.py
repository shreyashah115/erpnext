# -*- coding: utf-8 -*-
# Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


from __future__ import unicode_literals
import frappe

from frappe.model.document import Document

class EmployeeExpenseApprover(Document):
	pass

def get_approvers(doctype, txt, searchfield, start, page_len, filters):
	return get_approver_list(filters.get("user"))

def get_approver_list(name):
	return frappe.db.sql("""select user.name, user.first_name, user.last_name from
		tabUser user where user.enabled and user.name != %s""", name or "")
