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
authTokens_sql = netrc.authenticators("localhost_sql_server")

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

	if depth_value <= 150:

		message = MIMEMultipart("alternative")
		message["From"] = sender_email
		message["To"] = receiver_email

		if depth_value <= 75.0:
			message["Subject"] = "Domestic Well VERY VERY low"
			message_html = """\
			<html><body>
				The well water level is very VERY low, Have you ordered water yet?
				
				<a href="http://dewie.ca/Heatpump/historical/well-historical.html">Link to Historical Data</a>
			</body></html>	
				"""

		elif depth_value <= 100.0:
			message["Subject"] = "Domestic Well Very Low"
			message_html = """\
			<html><body>
				The well water level is very VERY low, Order Water!
				
				<a href="http://dewie.ca/Heatpump/historical/well-historical.html">Link to Historical Data</a>
			</body></html>	"""

		else:
			message["Subject"] = "Domestic Well Low"
			message_html = """\
			<html><body>
				The well water level is getting low.
				
				<a href="http://dewie.ca/Heatpump/historical/well-historical.html">Link to Historical Data</a>
			</body></html>	"""

		# Create a secure SSL context

		message.attach(message_html)

		context = ssl.create_default_context()
		with smtplib.SMTP(smtp_server, port) as server:
			server.ehlo()  # Can be omitted
			server.starttls(context=context)
			server.ehlo()  # Can be omitted
			server.login(sender_email, password)
			server.sendmail(sender_email, receiver_email, message.as_string())
