#!/usr/bin/env python3
# Author: Satoshi Hirose modified from Rocky Slavin's great work (https://github.com/rslavin/slack2discord)
# Slack message history importer for Discord: all channels are imported from Slack message history directory
import json
import os
import time
import requests
import discord
from datetime import datetime
from discord.ext import commands

THROTTLE_TIME_SECONDS = 1


def get_file_paths(file_path):
    """
    Returns a list of json files (either the path itself or nested files if the path is a directory).
    :param file_path: String path to directory or file
    :return: List of corresponding .json files
    """
    json_files = []
    # if directory, load files
    if os.path.isdir(file_path):
        json_files = [os.path.join(file_path, f) for f in os.listdir(file_path) if f.endswith(".json")]
    # if json file, load files
    elif file_path.endswith(".json"):
        json_files.append(file_path)
    return json_files

def fill_references(message, users, channels):
    """
    Fills in @mentions and #channels with their known display names
    :param message: Raw message to be filled with usernames and channel names instead of IDs
    :param users: Dictionary of user_id => display_name pairs
    :param channels: Dictionary of channel_id => channel_name pairs
    :return: Filled message string
    """
    for cid, name in channels.items():
        message = message.replace(f"<#{cid}>", f"#{name}")
    for uid, name in users.items():
        # just a preference to see <@uid> become @name
        message = message.replace(f"<@{uid}>", f"@{name}")
        # also noticed that replacing uid alone in "<@uid>" was turning into "<@name" without the '>', which looked odd
        message = message.replace(f"{uid}", f"{name}")
    return message

def register_commands():
    @bot.command(pass_context=True)
    async def import_all_channels(ctx, *args):
        """
        Import .json files in each Slack channel dicrectory in the specified path,
        Export each channel's text and attachted files to a Discord channel wih identical name.
        The directory path, which include user.json and channels.json should be specified.
        Optionally give a category channel ID in which to create the text channels.
        :param ctx:
        :param path:
        :param category id (optional):
        :return:
        """
        parentpath=args[0]
        """
        users = get_display_names(json_file_paths)
        Generates a dictionary of user_id => display_name pairs
        :param json_file_paths: List of paths being parsed
        :return: Dictionary or None if no file is found
        """
        print("Dictionary of user_id => display_name")
        users = {}
        user_file_path = f"{parentpath}/users.json"
        with open(user_file_path, encoding="utf-8") as f:
            users_json = json.load(f)
            for user in users_json:
                users[user['id']] = (
                    user['profile']['display_name'] if user['profile']['display_name'] else user['profile']['real_name'])
                print(f"\tUser ID: {user['id']} -> Display Name: {users[user['id']]}")

        """
        Generates a dictionary of channel_id => channel_name pairs
        :param json_file_paths: List of paths being parsed
        :return: Dictionary or None if no file is found
        """
        print("Dictionary of channel_id => channel_name")
        channels = {}
        channel_file_path =f"{parentpath}/channels.json"
        with open(channel_file_path, encoding="utf-8") as f:
            channels_json = json.load(f)
            for channel in channels_json:
                channels[channel['id']] = channel['name']
                print(f"\tChannel ID: {channel['id']} -> Channel Name: {channels[channel['id']]}")
                
        category_id = int(args[1]) if len(args) > 0 else None
        if category_id:
            category = ctx.guild.get_channel(category_id)
            category_name = category.name

        """
        Loop for channles
        """
        for cid, name in channels.items():
            path=f"{parentpath}{os.sep}{name}"
            if category_id:
                print(f"Import '{path}' to channel '#{name}' in category '{category_name}' ({category_id})")
                discord_channel = await category.create_text_channel(name)
            else:
                print(f"Import '{path}' to channel '#{name}'")
                discord_channel = await ctx.guild.create_text_channel(name)
            """
            Loop for json files
            """
            json_file_paths = get_file_paths(path)
            for json_file in sorted(json_file_paths):
                with open(json_file, encoding="utf-8") as f:
                    """
                    Loop for message files
                    """
                    for message in json.load(f):
                        # get post time stamp
                        if all(key in message for key in ['ts']):
                            timestamp = datetime.fromtimestamp(float(message['ts'])).strftime(
                                '%m/%d/%Y at %H:%M:%S')
                        else:
                            timestamp ="Time Unknown"
                    
                        # get username
                        if all(key in message for key in ['user_profile']):
                            if message['user_profile']['display_name']:
                                username = message['user_profile']['display_name']
                            else:
                                username = message['user_profile']['real_name']
                        elif all(key in message for key in ['user']):
                            # ran into an exception when message had no key 'user'
                            username = fill_references(message['user'], users, channels)
                        else:
                            # could be "@Unknown User" or similar
                            username = "@None"

                        # get message text
                        if all(key in message for key in ['text']):
                            text = fill_references(message['text'], users, channels)
                            # in Discored, the preview is surpressed when http link enclosed in <>
                            # to avoid this issue, I put the below 3 lines.
                            # this should also affect the other text.
                            text =text.replace('<http',' http' )
                            text =text.replace('>',' ' )
                            text =text.replace('|http',' http' )
                        else:
                            text ="\n"
                        
                        # send message text (modified on 20220805)
                        post_text =f"**{username}** *({timestamp})*\n{text}\n."
                        for i in range(round((len(text)+999)/2000)):
                            await discord_channel.send(post_text[(i*2000):((i+1)*2000-1)])
                        # forward attatched files
                        if all(key in message for key in ['files']):
                            flist = message['files']
                            for files in flist:
                                try:
                                    durl =files['url_private']
                                    url=durl.partition('?')[0]
                                    url=url.replace('\\','' )
                                    filename=os.path.basename(url)
                                    urlData = requests.get(durl).content
                                    with open(filename ,'wb') as ff: # wb でバイト型を書き込める
                                        ff.write(urlData)
                                        ff.close()
                                    try:
                                        await discord_channel.send(file=discord.File(filename))
                                        os.remove(filename)
                                    except Exception as e:
                                        print(f"\t{filename} upload failed")
                                        os.makedirs("unuploaded_files", exist_ok=True)
                                        os.rename(f"{filename}", f"unuploaded_files{os.sep}{filename}")
                                        await discord_channel.send(f"{filename} upload failed.")
                                except Exception as e:
                                    print(f"\t{timestamp} file download failed")
                        time.sleep(THROTTLE_TIME_SECONDS)
        print(f"Import complete")

if __name__ == "__main__":
    bot = commands.Bot(command_prefix="$")
    register_commands()
    bot.run(input("After Entering bot token, bot will be Ready!\nEnter Message in Discord channel as '$import_all_channels (directory name exported from slack)\n\n    Enter bot token: "))
