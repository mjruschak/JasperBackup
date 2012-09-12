# ----
# Created by: Michael Ruschak
# Website: http://www.mikeruschak.com/
# Version 1.0
# Company: Ruschak Development (http://www.ruschakdevelopment.com)
# ----

import sys, os, subprocess, socket
from dropbox import client, rest, session
from datetime import date

# Dropbox Configuration
APP_KEY = ''
APP_SECRET = ''
ACCESS_TYPE = 'app_folder'
OAUTH_TOKEN = ''
OAUTH_TOKEN_SECRET = ''

MYSQL_USERNAME = 'backup'
MYSQL_PASSWORD = 'readonly'

if (APP_KEY == '' or APP_SECRET == ''):
	print "You must setup an app on Dropbox and configure your App Keys."
	sys.exit()

sess = session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)

if (OAUTH_TOKEN == '' or OAUTH_TOKEN_SECRET == ''):
	request_token = sess.obtain_request_token()
	url = sess.build_authorize_url(request_token)
	print "Please go to this URL to authorize this application to access your Dropbox account: ", url
	print "Once you have completed this please press enter to continue."
	raw_input()
	access_token = sess.obtain_access_token(request_token)
	print "Here is your token. You must change the programs settings to your token."
	print "OAUTH_TOKEN = " + access_token.key
	print "OAUTH_TOKEN_SECRET = " + access_token.secret

else:
	sess.set_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

	client = client.DropboxClient(sess)

	print "Linked account: ", client.account_info()

	hostname = socket.getfqdn()
	backup_archive = "server-backup-" + date.today().strftime("%m-%d-%Y") + '.tar.gz'
	database_archive = "database-backup-" + date.today().strftime("%m-%d-%Y")

	mysqldump_cmd = 'mysqldump -u' + MYSQL_USERNAME + ' -p"' + MYSQL_PASSWORD + '" --opt --flush-logs --all-databases | gzip > /home/mruschak/DatabaseDumps/sql-' + database_archive + '.gzip'

	subprocess.call(mysqldump_cmd, shell=True)
	subprocess.call('/bin/tar czf /tmp/' + backup_archive + ' /home', shell=True)

	client.file_create_folder(hostname)

	backup_file = open('/tmp/' + backup_archive, 'rb')
	backup_file_bytes = os.path.getsize('/tmp/' + backup_archive)
	uploader = client.get_chunked_uploader(backup_file, backup_file_bytes)

	while uploader.offset < backup_file_bytes:
		try:
			upload = uploader.upload_chunked()
		except rest.ErrorResponse, e:
			print "Error occurred. Please try again."

	uploader.finish(hostname + '/' + backup_archive)

	subprocess.call('rm /tmp/' + backup_archive, shell=True)

	print "BACKUP COMPLETED"

print "DONE"