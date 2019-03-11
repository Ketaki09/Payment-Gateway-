import sys
import MySQLdb
sys.path.append('./config')

from config.database_config import connection_details

filter_keys = ['c_no','c_name','c_cvv','c_expiry_month','c_expiry_year','c_limit']

class CCDBManager:
	conn = None

	def __init__(self):
		self.conn = MySQLdb.connect(connection_details['host'], connection_details['username'], connection_details['password'], connection_details['database'],connection_details['port'])

	def __del__(self):
		self.conn.close()

	def get(self, filters):
		try:
			if filters is None:
				return "Invalid filters!"
			if not isinstance(filters, dict):
				return "Invalid filter data type!"
			
			filter_query = ""
			filtered_data = self.validate(filters)

			if not len(filtered_data):
				return "Please provide valid filters!"

			query = "select * from creditcardserver where "
			for item in filtered_data:
				filter_query+=item
				filter_query+="="
				if isinstance(filtered_data[item], str):
					filter_query+=('"'+filtered_data[item]+'"')
				else:
					filter_query+=str(filtered_data[item])
				filter_query+=" AND "
			filter_query = filter_query[:-5]
			query+=filter_query + ";"

			cursor = self.conn.cursor()
			cursor.execute(query)
			rows = cursor.fetchall()
			cursor.close()
			return rows

		except:
			return "Database Error!"


	def insert(self, data):
		try:
			if data is None:
				return "Invalid data!"
			if not isinstance(data, dict):
				return "Invalid data type!"

			insert_keys = []
			insert_values = []
			filtered_data = self.validate(data)
			query = "insert into creditcardserver ("
			filter_query = "values ("
			for item in filtered_data:
				query+=(item+",")
				filter_query+="%s,"
				insert_values.append(filtered_data[item])
			filter_query = filter_query[:-1]
			query = query[:-1]
			query+=") "+filter_query + ");"

			cursor = self.conn.cursor()
			cursor.execute(query, insert_values)
			self.conn.commit()
			cursor.close()
			return cursor.lastrowid

		except:
			return "Database Error!"


	def validate(self, filters):
		filtered_data = {}
		for item in filters:
			if item in filter_keys:
				filtered_data[item] = filters[item]
		return filtered_data



#--------------------Test---------------------------------

# creditcardserver = creditcardserver()
# data = {
#  	'c_no' : "123211221211121221",
#  	'c_name': "Sahil",
#  	'c_cvv': "022",
#  	'c_expiry_month':"02",
#  	'c_expiry_year':"2018",
# 	'c_limit': "50000"
# }
# print(creditcardserver.insert(data))
# data = {
# 	'c_name' : "Sahil"
# }
# print(creditcardserver.get(data))
# del creditcardserver

#---------------------------------------------------------