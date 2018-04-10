// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Department', {

	onload: function() {
		this.frm.set_query("leave_approver", "leave_approvers", function(doc) {
			return {
				query:"erpnext.hr.doctype.employee_leave_approver.employee_leave_approver.get_approvers",
				filters:{
					user: doc.user_id
				}
			}
		});
		this.frm.set_query("expense_approver", "expense_approvers", function(doc) {
			return {
				query:"erpnext.hr.doctype.employee_expense_approver.employee_expense_approver.get_approvers",
				filters:{
					user: doc.user_id
				}
			}
		});
	}
});
