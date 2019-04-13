import urllib.request, json
import mysql.connector
import datetime
import smtplib, ssl


import netrc

# Reads well depth information from NodeMCU sitting at the top of the well

# 2019-03-20 - Initial implementation
# 2019-04-13 - Added Email Alert
#			 -
# 			 -



#########################################################################
############ Main Program ###############################################
########################################################################

netrc = netrc.netrc()

authTokens_gmail = netrc.authenticators("smtp.gmail.com")
autoTokens_sql = netrc.authenticators("localhost_sql_server")

smtp_server = "smtp.gmail.com"
port = 587  # For starttls
sender_email = authTokens_gmail[0]
receiver_email = "dewiepedia@gmail.com"
password = authTokens_gmail[2]

url = "http://192.168.1.18/"
with urllib.request.urlopen(url) as url:
	data = json.loads(url.read().decode())
	print(data)
	print(data["sensors"]["1"]["value"])

	depth_value = data["sensors"]["1"]["value"]

	import mysql.connector

	mydb = mysql.connector.connect(
		host = "localhost",
		user = authTokens_sql[0],
		passwd = authTokens_sql[2],
		database = "heatpump"
	)

	mycursor = mydb.cursor()

	# Determine table name
	table_name = "well_values_" + datetime.datetime.now().strftime("%Y")

	sql = "INSERT INTO " + table_name + " (sensor, val) VALUES (1, " + str(depth_value) + ")"

	mycursor.execute(sql)
	mydb.commit()

	print(mycursor.rowcount, "record inserted.")

	if str(depth_value) <= 150:
		if str(depth_value) <= 75.0:
			# Create a secure SSL context
			message = """\
			Subject: Well water Very VERY low
	
			The well water level is very VERY low, Have you ordered water yet?"""

		elif str(depth_value) <= 100.0:
			message = """\
			Subject: Well water Very low

			The well water level is very low, Order Water"""

		else:
			message = """\
			Subject: Well water low

			The well water level is low"""

		context = ssl.create_default_context()
		with smtplib.SMTP(smtp_server, port) as server:
			server.ehlo()  # Can be omitted
			server.starttls(context=context)
			server.ehlo()  # Can be omitted
			server.login(sender_email, password)
			server.sendmail(sender_email, receiver_email, message)
