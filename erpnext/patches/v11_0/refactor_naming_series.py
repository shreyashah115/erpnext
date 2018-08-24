# Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import print_function, unicode_literals

import frappe
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

doctype_series_map = {
	'Additional Salary': 'HR-ADS-.YY.-.MM.-',
	'Appraisal': 'HR-APR-.YY.-.MM.',
	'Asset': 'ACC-ASS-.YYYY.-',
	'Attendance': 'HR-ATT-.YYYY.-',
	'Auto Repeat': 'SYS-ARP-.YYYY.-',
	'Blanket Order': 'MFG-BLR-.YYYY.-',
	'C-Form': 'ACC-CF-.YYYY.-',
	'Campaign': 'SAL-CAM-.YYYY.-',
	'Clinical Procedure': 'HLC-CPR-.YYYY.-',
	'Course Schedule': 'EDU-CSH-.YYYY.-',
	'Customer': 'CUST-.YYYY.-',
	'Delivery Note': 'MAT-DN-.YYYY.-',
	'Delivery Trip': 'MAT-DT-.YYYY.-',
	'Driver': 'HR-DRI-.YYYY.-',
	'Employee': 'HR-EMP-',
	'Employee Advance': 'HR-EAD-.YYYY.-',
	'Expense Claim': 'HR-EXP-.YYYY.-',
	'Fee Schedule': 'EDU-FSH-.YYYY.-',
	'Fee Structure': 'EDU-FST-.YYYY.-',
	'Fees': 'EDU-FEE-.YYYY.-',
	'Inpatient Record': 'HLC-INP-.YYYY.-',
	'Installation Note': 'MAT-INS-.YYYY.-',
	'Instructor': 'EDU-INS-.YYYY.-',
	'Issue': 'ISS-.YYYY.-',
	'Journal Entry': 'ACC-JV-.YYYY.-',
	'Lab Test': 'HLC-LT-.YYYY.-',
	'Landed Cost Voucher': 'MAT-LCV-.YYYY.-',
	'Lead': 'CRM-LEAD-.YYYY.-',
	'Leave Allocation': 'HR-LAL-.YYYY.-',
	'Leave Application': 'HR-LAP-.YYYY.-',
	'Maintenance Schedule': 'MAT-MSH-.YYYY.-',
	'Maintenance Visit': 'MAT-MVS-.YYYY.-',
	'Material Request': 'MAT-MR-.YYYY.-',
	'Member': 'NPO-MEM-.YYYY.-',
	'Opportunity': 'CRM-OPP-.YYYY.-',
	'Packing Slip': 'MAT-PAC-.YYYY.-',
	'Patient': 'HLC-PAT-.YYYY.-',
	'Patient Encounter': 'HLC-ENC-.YYYY.-',
	'Patient Medical Record': 'HLC-PMR-.YYYY.-',
	'Payment Entry': 'ACC-PAY-.YYYY.-',
	'Payment Request': 'ACC-PRQ-.YYYY.-',
	'Production Plan': 'MFG-PP-.YYYY.-',
	'Project Update': 'PROJ-UPD-.YYYY.-',
	'Purchase Invoice': 'ACC-PINV-.YYYY.-',
	'Purchase Order': 'PUR-ORD-.YYYY.-',
	'Purchase Receipt': 'MAT-PRE-.YYYY.-',
	'Quality Inspection': 'MAT-QA-.YYYY.-',
	'Quotation': 'SAL-QTN-.YYYY.-',
	'Request for Quotation': 'PUR-RFQ-.YYYY.-',
	'Sales Invoice': 'ACC-SINV-.YYYY.-',
	'Sales Order': 'SAL-ORD-.YYYY.-',
	'Sample Collection': 'HLC-SC-.YYYY.-',
	'Shareholder': 'ACC-SH-.YYYY.-',
	'Stock Entry': 'MAT-STE-.YYYY.-',
	'Stock Reconciliation': 'MAT-RECO-.YYYY.-',
	'Student': 'EDU-STU-.YYYY.-',
	'Student Applicant': 'EDU-APP-.YYYY.-',
	'Supplier': 'SUP-.YYYY.-',
	'Supplier Quotation': 'PUR-SQTN-.YYYY.-',
	'Supplier Scorecard Period': 'PU-SSP-.YYYY.-',
	'Timesheet': 'TS-.YYYY.-',
	'Vehicle Log': 'HR-VLOG-.YYYY.-',
	'Warranty Claim': 'SER-WRN-.YYYY.-',
	'Work Order': 'MFG-WO-.YYYY.-'
}

def execute():
	series_to_set = get_series()
	for doctype, opts in series_to_set.items():
		set_series(doctype, opts["options"], opts["default"])

def set_series(doctype, options, default):
	make_property_setter(doctype, "naming_series", "options", options, "Text")
	if not default: return
	make_property_setter(doctype, "naming_series", "default", default, "Text")

def get_series():
	series_to_set = {}

	for doctype in doctype_series_map:
		if not frappe.db.exists('DocType', doctype):
			continue
		if not frappe.db.a_row_exists(doctype):
			continue
		if not frappe.db.has_column(doctype, 'naming_series'):
			continue
		series_to_preserve = filter(None, get_series_to_preserve(doctype))
		default_series = get_default_series(doctype)
		print('first', series_to_preserve)
		if not series_to_preserve:
			continue
		existing_series = (frappe.get_meta(doctype).get_field("naming_series").options or "").split("\n")
		existing_series = filter(None, [d.strip() for d in existing_series])

		# set naming series property setter
		series_to_preserve = list(set(series_to_preserve + existing_series))
		print(series_to_preserve)
		print(doctype)
		if series_to_preserve:
			series_to_set[doctype] = {"options": "\n".join(series_to_preserve), "default": default_series}

	return series_to_set

def get_series_to_preserve(doctype):
	series_to_preserve = frappe.db.sql_list("""select distinct naming_series from `tab{doctype}`""".format(doctype=doctype))
	series_to_preserve.sort()
	return series_to_preserve

def get_default_series(doctype):
	default_series = (frappe.get_meta(doctype).get_field("naming_series").default or "")
	return default_series