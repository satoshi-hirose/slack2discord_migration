# slack2discord_migration
Python code for migration from slack to discord.All history of the comments and attached files in all open channels in a Slack Workspace are forwarded to a Discord server. there are two options for the file forwarding procedure.

All history of the comments and **attached files** in all open channels in a Slack Workspace are forwarded to a Discord server.
there are two options for the file forwarding procedure.

   1. Directly upload the files to Discord. (suitable when most of the files are image or movie < 8MB)  
        - pros: unlimited file storage, can nicely preview the image or movie files 
        - cons: <8MB/file, cannot preview pdf etc. files, 
   2. Upload files to Google Drive and post URL link to discord. (suitable when many non-image/movie fiels > 8MB exist)  
        - pros: <50MB/file, can preview .pdf etc. as URL link 
        - cons: limited file storage (15GB with Google free account)


# How to use
## 1. Directly upload the files to Discord.
Rewrite Line 14 of Code.gs as `UPLOAD_TO_GOOGLE = False`
prepare clipboard (see below)

- preparation (perform once, even if you want to migrate multiple Workspaces)

    - Discord
    
	   create discord bot
      
		    1, login to https://discord.com/developers/applications
		    2, New Application 
     			    note: too simple name will cause an error something like "too many people use this name"
		            e.g. do not use 'test', 'test_hirose' is OK.
			    note: Cannot include "discord"
		    3. bot -> add bot -> yes, do it! -> Public Bot off -> Reset Token -> Copy -> keep the token somewhere hereafter, BOTTOKEN）
		    4, oAuth2->URL GEnerator -> bot -> Administrator -> Copy the link. -> keep the link somewhere　（hereafter, BOTLINK）


    - pip (Terminal)
   		
		    1, Download ZIP of this repository and unzip (CODE_DIRECTORY)
		    2, in terminal, install requirements `cd CODE_DIRECTORY; pip3 install -r requirements.txt" in terminal`

- preparation for each server

    - Discord
	 
      add the bot to Discord server
      
		    1. create a new server in Discord or choose target server, which you can admin.
		    2. open the BOTLINK with web browser -> add to server -> certification

    - Slack
     
	    create and download the data (admin right required)
      
		    1, Left click the workspace name -> settings & administration -> workspace setting 
              ->import/export data -> export -> Export date range "entire history" -> start export
		    2, wait for a while (slackbot will announce finish)
		    3, refresh the site (F5)
		    4, download the exports
		    5, unzip the downloaded file and create directory include all JSON file (JSON_DIRECTORY)

- run the script

    - python
    
		    1,[terminal] go to JSON_DIRECTORY
		    2, type "python3 [slack2discord_migration directory]/slack2discord_migration.py"
		    3, enter BOTTOKEN

    - Discord
    
		    1, right click "text channel" -> copy ID (CATEGORY_ID) (if not found, user settings -> advanced -> turn on developer mode )
		    2, in a text channel (e.g. general) in Discord, type "$import_all_channels ./ CATEGORY_ID"
		    3, wait a while (about [number of comment] x 1 sec)
		    optionally, you can run without CATEGORY_ID ("$import_all_channels ./")

## 2. Upload files to Google Drive and post URL link to discord.
Rewrite Line 14 of Code.gs as `UPLOAD_TO_GOOGLE = True`
prepare clipboard (see below)

- preparation

     the same as above

- preparation for each server

     in addition to above, 
    - Google Cloud Console
      
		    1. go https://console.cloud.google.com/home/dashboard -> My First Project (or a project name you have created)-> New Project -> create (! remember your project name: PROJECT_NAME)
		    2. Go to APIs overview -> ENABLE APIS AND SERVICES -> search "Google Drive API" -> ENABLE 
		    3. CREATE CREDENTIALS (if not found, CREDENTIALS -> CREATE CREDENTIALS ->  Help me choose)
		    4. Google Drive API -> User data -> enter 
		    5. Scopes -> save and continue -> Application type "Desktop app" -> create -> DOWNLOAD -> done -> rename the downloaded file as "client_secrets.json" (CLIENT_SECRETS_FILE)
		    6. OAuth consetnt screen -> test user -> add users -> YOURGOOGLEACCOUNT@gmail.com -> save
		        or PUBLISH APP

    - Google Drive
		    
		    1, Create a directory, where the attached files will be stored
		    2, Copy&Paste the diectoryID to GOOGLE_DRIVE_FILE_DIRECTORY_ID of the clipboard.
		    3, Share the directory with “anyone with the link” as “Viewer”

- run the script

    - python
    
		    1, put CLIENT_SECRETS_FILE in JSON_DIRECTORY
		    2,[terminal] go to JSON_DIRECTORY
		    3, type "python3 [slack2discord_migration directory]/slack2discord_migration.py"
		    4, enter GOOGLE_DRIVE_FILE_DIRECTORY_ID
		    3, enter BOTTOKEN

    - Discord
    
		    1, right click "text channel" -> copy ID (CATEGORY_ID) (if not found, user settings -> advanced -> turn on developer mode )
		    2, in a text channel (e.g. general) in Discord, type "$import_all_channels ./ CATEGORY_ID"
		    3, wait a while (about [number of comment] x 1 sec)
		    optionally, you can run without CATEGORY_ID ("$import_all_channels ./")

# Clipborad
 copy and paste below to text file before you start
 
 BOTTOKEN
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

BOTLINK
https://discord.com/api/oauth2/authorize?client_id=0000000000000000000000000&permissions=8&scope=bot

CODE_DIRECTORY
/Users/XXX/Downloads/slack2discord_migration-main

JSON_DIRECTORY 
* note: Original directory name with spaces can cause an unpleasant event. please rename 
/Users/XX/Downloads/XXXXXXXXXXXXXX


below are ony for 2. Upload files to Google Drive and post URL link to discord.

CLIENT_SECRETS_FILE
* note:  not "secret", but "secrets" 
rename as "client_secrets.json"

GOOGLE_DRIVE_FILE_DIRECTORY_ID
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
