
class Financials():

	def __init__(self, fv_key, fv_values, reportType, reportedDate):
		self.name = fv_key
		self.value = fv_values['value']
		self.filingPeriod = fv_values['filingPeriod']
		self.reportType = reportType
		self.reportedDate = reportedDate