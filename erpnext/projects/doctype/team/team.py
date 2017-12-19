# -*- coding: utf-8 -*-
# Copyright (c) 2017, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.mapper import get_mapped_doc
from frappe.model.document import Document

class Team(Document):
	pass

@frappe.whitelist()
def make_timesheet(source_name, target_doc=None):
	target_doc = get_mapped_doc("Team", source_name,{
		"Team": {
			"doctype": "Timesheet",
			"field_map": {
				"is_team": "is_team",
				"team": "name"
			}},
		"Employee Team": {
			"doctype": "Employee Team",
			"field_map": {
			"team_details": "employee"
		}}
		}, target_doc)
	return target_doc