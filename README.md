# slack2discord_migration
python code for migration from slack to discord.

# How to use

- preparation

    - Discord
    
	   create discord bot
      
		    1, login to https://discord.com/developers/applications
		    2, New Application 
     			    note: too simple name will cause an error something like "too many people use this name"
		            e.g. do not use 'test', 'test_hirose' is OK.
		    3. bot -> add bot -> yes, do it! -> Public Bot off -> Reste Token -> Copy -> keep the token somewhere hereafter, BOTTOKEN）
		    4, oAuth2->URL GEnerator -> bot -> Administrator -> Copy the link. -> keep the link somewhere　（hereafter, BOTLINK）

    - pip
   
		    1, go to slack2discord_migration directory
		    2, install requirements (terminal: go to "pip install -r requirements.txt" in terminal)


- preparation for each server

    - Discord
	 
      add the bot to Discord server
      
		    1. create a new server in Discord
		    2. open the BOTLINK with web browser -> add to server -> certification

    - Slack
     
	    create and download the data (admin right required)
      
		    1, right click the workspace name -> settings & administration -> workspace setting 
              ->import/export data -> export -> Export date range "entire history" -> start export
		    2, wait for a while (slackbot will announce when finished)
		    3, refresh the site (F5)
		    4, download the exports
		    5, unzip the downloaded file

    - python
    
		    1,[terminal] go to the unzipped directory
		    2, type "python3 [slack2discord_migration directory]/slack2discord_migration.py"
		    3, enter BOTTOKEN

    - Discord
    
		    1, in text channel in Discord, type "$import_all_channels ./"
		    2, wait a while (about [number of comment] x 1 sec)

