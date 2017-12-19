// Copyright (c) 2017, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Team', {

	refresh: function(frm) {
		if(frm.doc.employee) {
			frm.add_custom_button(__('Make Timesheet'), function() {
				frappe.model.open_mapped_doc({
					method: "erpnext.projects.doctype.team.team.make_timesheet",
					frm: cur_frm
				})
			})
		}
	}
});	