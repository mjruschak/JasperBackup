#JasperBackup

Authored by [Michael Ruschak](http://www.mikeruschak.com/). Named after the cute Black Lab I used to walk for the neighbors accross the street when I was a kid. Not to random since my servers are named after dogs.

This program backs up your MySQL database and home directories to Dropbox. Can optionally be run as a cron job nightly. Email notifications will be sent at the end of the scripts execution. I host my sites with Linode and use their backup service however I didn't want to depend on them alone.

##Requirements
I reccomend you install and configure a Python virtual environment for this script.

- Python 2.6 or above
- Dropbox Python SDK 1.5.1 or above

##Configuration

I reccomend you create an app in Dropbox yourself. At this time I have not published my Dropbox app for this program. Please configure the APP_KEY and APP_KEY_SECRET accordingly.

The script needs to be run manually the first time in order to obtain the OAUTH_KEY and OAUTH_KEY_SECRET. The process is as simple as running the script and then going to the url the program asks you to go to. This URL will request a token and allow the Dropbox app to access your account. The token information will print out for you to copy down.

###MySQL Configuration (Optional)
To backup your MySQL database you must setup a user that only has enough priviledges to backup all the databases.

`GRANT LOCK TABLES, SELECT ON *.* TO 'backup'@'localhost' IDENTIFIED BY 'password-for-user';`

After this setup the MYSQL_USERNAME and MYSQL_PASSWORD variables in the Python script.

To run the script simply `python Backup.py` in your virtual environment.