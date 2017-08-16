QUnit.module('Buying');

QUnit.test("test: purchase order", function(assert) {
	assert.expect(11);
	let done = assert.async();

	frappe.run_serially([
		() => {
			return frappe.tests.make('Purchase Order', [
				{supplier: 'Test Supplier'},
				{company: 'Wind Power LLC'},
				{is_subcontracted: 'No'},
				{buying_price_list: 'Test-Buying-USD'},
				{currency: 'USD'},
				{items: [
					[
						{"item_code": 'Test Product 4'},
						{"schedule_date": frappe.datetime.add_days(frappe.datetime.now_date(), 1)},
						{"expected_delivery_date": frappe.datetime.add_days(frappe.datetime.now_date(), 5)},
						{"qty": 5},
						{"uom": 'Unit'},
						{"rate": 100},
						{"warehouse": 'Stores - WP'}
					]
				]},

				{tc_name: 'Test Term 1'},
				{terms: 'This is a term.'}
			]);
		},

		() => {
			// Get supplier details
			assert.ok(cur_frm.doc.supplier_name == 'Test Supplier', "Supplier name correct");
			assert.ok($('div.control-value.like-disabled-input.for-description').text().includes('Contact 3'), "Contact display correct");
			assert.ok(cur_frm.doc.contact_email == 'test@supplier.com', "Contact email correct");
			// Get item details
			assert.ok(cur_frm.doc.items[0].item_name == 'Test Product 4', "Item name correct");
<<<<<<< HEAD
			assert.ok(cur_frm.doc.items[0].description == 'Test Product 4', "Description correct")
=======
			assert.ok(cur_frm.doc.items[0].description == 'Test Product 4', "Description correct");
>>>>>>> f6544e95d41e38416e4a9f5d43ff382704a681d0
			assert.ok(cur_frm.doc.items[0].qty == 5, "Quantity correct");
			// Calculate total
			assert.ok(cur_frm.doc.total == 500, "Total correct");
			// Get terms
			assert.ok(cur_frm.doc.terms == 'This is a term.', "Terms correct");
		},

		() => cur_frm.print_doc(),
		() => frappe.timeout(1),
		() => {
			assert.ok($('.btn-print-print').is(':visible'), "Print Format Available");
			assert.ok($('div > div:nth-child(5) > div > div > table > tbody > tr > td:nth-child(4) > div').text().includes('Test Product 4'), "Print Preview Works");
		},

		() => cur_frm.print_doc(),
		() => frappe.timeout(1),

		() => frappe.tests.click_button('Submit'),
		() => frappe.tests.click_button('Yes'),
		() => frappe.timeout(0.3),

		() => {
			assert.ok(cur_frm.doc.status == 'To Receive and Bill', "Submitted successfully");
		},

		() => done()
	]);
});