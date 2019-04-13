
import smtplib, ssl


import netrc

netrc = Netrc()  # parse ~/.netrc
# Get credentials



smtp_server = "smtp.gmail.com"
port = 587  # For starttls
sender_email = netrc['smtp.gmail.com']['login']
password = netrc['smtp.gmail.com']['password']


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
