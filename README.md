# Google Drive Backup

An automatable Python script that incrementally backs up a folder to Google Drive using the Drive API.

# Set Up

* Turn on the Drive API by pressing the Enable the Drive API button on https://developersgooglecom/drive/api/v3/quickstart/python to create a new Cloud Platform project and automatically enable the Drive API

* In the resulting dialog click DOWNLOAD CLIENT CONFIGURATION and save the file credentials.json to the directory containing the script 

* Install the Google Client Library by running 

        pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

* Run the script and a new tab/window will open and ask you to log in to your Google account and verify the script
 
* Once verification is complete create a folder within your Google Drive where you want your backed up files to be stored 
 
* Assign the Google Drive folder name to the drive_folder_name variable in the script
 
* Get the path of the folder you want to backup and assign it to the path variable in the script
 
* Run the script and the files within your folder and subfolders will be backed up to your Google Drive folder

* To create an automated schedule for Google Drive backups create a scheduled task in Task Scheduler on Windows or a cron job on Linux/Mac

