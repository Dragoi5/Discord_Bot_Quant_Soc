import os
import discord

import datetime
import pandas as pd

import matplotlib as mpl
import matplotlib.pyplot as plt

import time
from keep_alive import keep_alive

client = discord.Client(intents=discord.Intents.all())

msg_lim = 600


@client.event
async def on_ready():
  print("Bot online")
  print(client.user)


# resend a message if one is sent
@client.event
async def on_message(message):
  if message.author == client.user:
    return
  elif message.content.startswith("!MEMBER"):

    file = open('members.txt', 'a')
    file.write("Member id\tName\n")
    members = message.guild.members
    for i in members:
      output = str(i.id) + "\t"
      output += i.name + "\n"
      file.write(output)
    file.close()
  elif message.content.startswith("!DOWN"):

    channels = message.guild.text_channels
    file = open('file.txt', 'a')
    file.write("Message id\tAuthor id\tChannel id\tCreated\tMsg\n")
    file.close()
    for temp_channel in channels:
      file = open('file.txt', 'a')
      try:
        num_messages = 0
        lst_date = ""
        async for temp_message in temp_channel.history(limit=msg_lim,
                                                       oldest_first=True):
          output = str(temp_message.id) + "\t"
          output += str(temp_message.author.id) + "\t"
          output += str(temp_message.channel.id) + "\t"
          output += str(temp_message.created_at) + "\t"
          msg = str(temp_message.content)
          msg = msg.replace("\n", "\\ n")
          msg = msg.replace("\t", "\\t")
          output += msg + "\n"
          lst_date = temp_message.created_at
          file.write(output)
          num_messages += 1
        file.close()
        if (num_messages == msg_lim):
          await recursive_download(temp_message, lst_date, msg_lim)
        await message.channel.send("Finished downloading stats, " +
                                   str(num_messages) +
                                   " messages info downloaded from " +
                                   temp_channel.name)
      except Exception as error:
        file.close()
        print(str(temp_channel.name) + " - " + str(error))
        if "Too Many Requests" in str(error):
          time.sleep(60)
          channels.append(temp_channel)
  elif message.content.startswith("!STATS"):
    


async def recursive_download(message, lst, msg_total):
  print(msg_total)
  file = open('file.txt', 'a')
  num_messages = 0
  lst_date = ""
  async for temp_message in message.channel.history(limit=msg_lim,
                                                    after=lst,
                                                    oldest_first=True):
    output = str(temp_message.id) + "\t"
    output += str(temp_message.author.id) + "\t"
    output += str(temp_message.channel.id) + "\t"
    output += str(temp_message.created_at) + "\t"
    msg = str(temp_message.content)
    msg = msg.replace("\n", "\\n")
    msg = msg.replace("\t", "\\t")
    output += msg + "\n"
    lst_date = temp_message.created_at
    file.write(output)
    num_messages += 1
  file.close()
  if num_messages == msg_lim:
    await recursive_download(message, lst_date, msg_total + msg_lim)
  else:
    num_messages -= num_messages
    num_messages += msg_lim


keep_alive()
my_secret = os.environ['my_secret']
client.run(my_secret)
