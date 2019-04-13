
import smtplib, ssl


import netrc

#netrc = Netrc()  # parse ~/.netrc
# Get credentials

netrc           = netrc.netrc()

gmail_creds  = "smtp.gmail.com"

authTokens_gmail = netrc.authenticators(gmail_creds)


#print("User Name at remote host:%s"%(authTokens[0]))

#print("Account Password:%s"%(authTokens[1]))

#print("Password for the user name at remote host:%s"%(authTokens[2]))


smtp_server = "smtp.gmail.com"
port = 587  # For starttls
sender_email = authTokens_gmail[0] 
receiver_email = "dewiepedia@gmail.com"
password = authTokens_gmail[2]


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
