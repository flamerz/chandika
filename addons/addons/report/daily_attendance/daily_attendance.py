from __future__ import unicode_literals
import frappe

from frappe.utils import nowdate

def execute(filters=None):
	columns, data = [],[]


	date = nowdate()
	if filters.get("date"):
		date = filters.get("date")
		

	columns = [
		"Employee ID:Link/Employee:200",
		"Employee Name:Data:240",
		"Check In:Data:200",
		"Check Out:Data:200",
		"Total Working Hrs:Int:150"
	]

	data = frappe.db.sql("""
			SELECT
				emp.`employee`, emp.`employee_name`
				, MAX(IF(ec.log_type = "IN",DATE_FORMAT(ec.time,"%H:%i:%s"),"")) `checkin`
				, MAX(IF(ec.log_type = "OUT",DATE_FORMAT(ec.time,"%H:%i:%s"),"")) `checkout`
				, timestampdiff(hour,min(ec.`time`),max(ec.time)) `Total Working Hours`
			FROM `tabEmployee` `emp`
			LEFT JOIN `tabEmployee Checkin` `ec` on ec.employee = emp.name AND DATE(time) = "{}"
			
			GROUP BY employee

		""".format(date))
	return columns, data