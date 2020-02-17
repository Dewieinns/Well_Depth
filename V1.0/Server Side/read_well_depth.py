#from urllib import request, json
#import urllib2.request, json 
#from urllib2 import urlopen
#import urllib
#from urllib import urlopen 
from urllib.request import urlopen
import json

#import requests
import mysql.connector
import datetime
import smtplib, ssl

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


import netrc

# Reads well depth information from NodeMCU sitting at the top of the well

# 2019-03-20 - Initial implementation
# 2019-04-13 - Added Email Alert
# 2020-01-26 - After running out of water yesterday I adjusted warning thresholds.
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

warning_1 = 160		# 2020-01-26 - Changed from 150 to 160
warning_2 = 110		# 2020-01-26 - Changed from 100 to 110
warning_3 = 75		# 2020-01-26 - Changed from 
cutoff_point = 60	# NOT USED YET

url = "http://192.168.1.115/"
#with urllib.request.urlopen(url) as url:
#with urllib2.request.urlopen(url) as url:
#with urllib.urlopen(url) as url:
url = urlopen(url)
#with urllib2.urlopen(url) as url:
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


if depth_value <= warning_1:
	print("Well water getting low, send an email message")
	message = MIMEMultipart("alternative")
	message["From"] = sender_email
	message["To"] = receiver_email

	if depth_value <= cutoff_point:
		message["Subject"] = "Domestic Well Cutoff point met"
		message_html = """\
                       <html><body>
                               The well water level is at the point where it has run out of water. This is where we would turn off power to the pump<br />
                               <br />
                               <a href="http://dewie.ca/Heatpump/historical/well-historical.html">Link to Historical Data</a>
                       </body></html>
                               """
	if depth_value <= warning_3:
		message["Subject"] = "Domestic Well VERY VERY low"
		message_html = """\
		<html><body>
			The well water level is very VERY low, Have you ordered water yet?<br />
			<br />
			<a href="http://dewie.ca/Heatpump/historical/well-historical.html">Link to Historical Data</a>
		</body></html>	
			"""

	elif depth_value <= warning_2:
		message["Subject"] = "Domestic Well Very Low"
		message_html = """\
		<html><body>
			The well water level is very VERY low, Order Water!<br />
			<br />
			<a href="http://dewie.ca/Heatpump/historical/well-historical.html">Link to Historical Data</a>
		</body></html>	"""

	else:
		message["Subject"] = "Domestic Well Low"
		message_html = """\
		<html><body>
			The well water level is getting low.<br />
			<br />
			<a href="http://dewie.ca/Heatpump/historical/well-historical.html">Link to Historical Data</a>
		</body></html>	"""

	# Create a secure SSL context
	message_MIME = MIMEText(message_html, "html")
	message.attach(message_MIME)

	context = ssl.create_default_context()
	with smtplib.SMTP(smtp_server, port) as server:
		server.ehlo()  # Can be omitted
		server.starttls(context=context)
		server.ehlo()  # Can be omitted
		server.login(sender_email, password)
		server.sendmail(sender_email, receiver_email, message.as_string())
	print("Email sent")

