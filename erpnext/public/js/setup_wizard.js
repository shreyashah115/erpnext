frappe.provide("erpnext.setup");

frappe.pages['setup-wizard'].on_page_load = function(wrapper) {
	if(frappe.sys_defaults.company) {
		frappe.set_route("desk");
		return;
	}
};

frappe.setup.on("before_load", function () {
	erpnext.setup.slides_settings.map(frappe.setup.add_slide);
});

erpnext.setup.slides_settings = [
	{
		// Domain
		name: 'domain',
		domains: ["all"],
		title: __('Select your Domain'),
		fields: [
			{
				fieldname: 'domain', label: __('Domain'), fieldtype: 'Select',
				options: [
					{ "label": __("Distribution"), "value": "Distribution" },
					{ "label": __("Manufacturing"), "value": "Manufacturing" },
					{ "label": __("Retail"), "value": "Retail" },
					{ "label": __("Services"), "value": "Services" },
					{ "label": __("Education"), "value": "Education" },
					{"label": __("Healthcare (beta)"), "value": "Healthcare"}
				], reqd: 1
			},
		],
		// help: __('Select the nature of your business.'),
		onload: function (slide) {
			slide.get_input("domain").on("change", function () {
				frappe.setup.domain = $(this).val();
				frappe.wizard.refresh_slides();
			});
		},
	},

	{
		// Organisation
		name: 'organisation',
		domains: ["all"],
		title: __("Your Organization"),
		icon: "fa fa-building",
		// help: (frappe.setup.domain === 'Education' ?
		// 	__('The name of the institute for which you are setting up this system.') :
		// 	__('The name of your company for which you are setting up this system.')),
		fields: [
			{
				fieldname: 'company_tagline',
				label: __('What does it do?'),
				fieldtype: 'Data',
				placeholder: frappe.setup.domain === 'Education' ?
					__('e.g. "Primary School" or "University"') :
					__('e.g. "Build tools for builders"'),
				reqd: 1
			},
			{ fieldname: 'bank_account', label: __('Bank Name'), fieldtype: 'Data', reqd: 1 },
			{
				fieldname: 'chart_of_accounts', label: __('Chart of Accounts'),
				options: "", fieldtype: 'Select'
			},

			{ fieldtype: "Section Break", label: __('Financial Year') },
			{ fieldname: 'fy_start_date', label: __('Start Date'), fieldtype: 'Date', reqd: 1 },
			{ fieldtype: "Column Break" },
			{ fieldname: 'fy_end_date', label: __('End Date'), fieldtype: 'Date', reqd: 1 },
		],

		onload: function (slide) {
			this.load_chart_of_accounts(slide);
			this.bind_events(slide);
			this.set_fy_dates(slide);
		},

		validate: function () {
			// validate fiscal year start and end dates
			if (this.values.fy_start_date == 'Invalid date' || this.values.fy_end_date == 'Invalid date') {
				frappe.msgprint(__("Please enter valid Financial Year Start and End Dates"));
				return false;
			}
			return true;
		},

		set_fy_dates: function (slide) {
			var country = frappe.wizard.values.country;

			if (country) {
				var fy = erpnext.setup.fiscal_years[country];
				var current_year = moment(new Date()).year();
				var next_year = current_year + 1;
				if (!fy) {
					fy = ["01-01", "12-31"];
					next_year = current_year;
				}

				var year_start_date = current_year + "-" + fy[0];
				if (year_start_date > frappe.datetime.get_today()) {
					next_year = current_year;
					current_year -= 1;
				}
				slide.get_field("fy_start_date").set_value(current_year + '-' + fy[0]);
				slide.get_field("fy_end_date").set_value(next_year + '-' + fy[1]);
			}
		},


		load_chart_of_accounts: function (slide) {
			var country = frappe.wizard.values.country;

			if (country) {
				frappe.call({
					method: "erpnext.accounts.doctype.account.chart_of_accounts.chart_of_accounts.get_charts_for_country",
					args: { "country": country },
					callback: function (r) {
						if (r.message) {
							slide.get_input("chart_of_accounts").empty()
								.add_options(r.message);

							if (r.message.length === 1) {
								var field = slide.get_field("chart_of_accounts");
								field.set_value(r.message[0]);
								field.df.hidden = 1;
								field.refresh();
							}
						}
					}
				})
			}
		},

		bind_events: function (slide) {
			slide.get_input("fy_start_date").on("change", function () {
				var start_date = slide.form.fields_dict.fy_start_date.get_value();
				var year_end_date =
					frappe.datetime.add_days(frappe.datetime.add_months(start_date, 12), -1);
				slide.form.fields_dict.fy_end_date.set_value(year_end_date);
			});
		}
	}
];

// Source: https://en.wikipedia.org/wiki/Fiscal_year
// default 1st Jan - 31st Dec

erpnext.setup.fiscal_years = {
	"Afghanistan": ["12-20", "12-21"],
	"Australia": ["07-01", "06-30"],
	"Bangladesh": ["07-01", "06-30"],
	"Canada": ["04-01", "03-31"],
	"Costa Rica": ["10-01", "09-30"],
	"Egypt": ["07-01", "06-30"],
	"Hong Kong": ["04-01", "03-31"],
	"India": ["04-01", "03-31"],
	"Iran": ["06-23", "06-22"],
	"Italy": ["07-01", "06-30"],
	"Myanmar": ["04-01", "03-31"],
	"New Zealand": ["04-01", "03-31"],
	"Pakistan": ["07-01", "06-30"],
	"Singapore": ["04-01", "03-31"],
	"South Africa": ["03-01", "02-28"],
	"Thailand": ["10-01", "09-30"],
	"United Kingdom": ["04-01", "03-31"],
};

// var test_values_edu = {
// 	"language": "english",
// 	"domain": "Education",
// 	"country": "India",
// 	"timezone": "Asia/Kolkata",
// 	"currency": "INR",
// 	"first_name": "Tester",
// 	"email": "test@example.com",
// 	"password": "test",
// 	"company_name": "Hogwarts",
// 	"company_abbr": "HS",
// 	"company_tagline": "School for magicians",
// 	"bank_account": "Gringotts Wizarding Bank",
// 	"fy_start_date": "2016-04-01",
// 	"fy_end_date": "2017-03-31"
// }
