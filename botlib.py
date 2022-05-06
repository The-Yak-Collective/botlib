## parts from here: https://gist.github.com/Rapptz/c4324f17a80c94776832430007ad40e6#slash-commands-and-context-menu-commands

    



from discord.ext import tasks, commands
import discord
import asyncio
import os
import re
import subprocess
import time
import datetime
from dotenv import load_dotenv

import sqlite3

HOME_DIR="/home/yak/robot/slashayak/"
USER_DIR="/home/yak/"

load_dotenv(USER_DIR+'.env')

conn=sqlite3.connect(HOME_DIR+'slashayakdatabase.db') #the connection should be global. 

db_c = conn.cursor()


def checkon_database(): 
#check if table exists in DB. if not, create it
#this function is RIPE for automation, which would also be carried over to "on message"
    db_c.execute('''SELECT count(name) FROM sqlite_master WHERE type='table' AND name='prompts' ''')
    if db_c.fetchone()[0]!=1:
        db_c.execute('''CREATE TABLE prompts (promptid INTEGER PRIMARY KEY, creatorid text, contents text, filled int, createdat int, filledat int, chan int, mlink text)''') 
        #filled=is it active
        #most items will not be used...
        conn.commit()


async def splitsend(ch,st,codeformat):
#send data in chunks smaller than 2k
#might it have a bug of dropping last space and last line?
    if len(st)<1900: #discord limit is 2k and we want some play)
        if codeformat:
            await ch.send('```'+st+'```')
        else:
            await ch.send(st)
    else:
        x=st.rfind('\n',0,1900)
        if codeformat:
            await ch.send('```'+st[0:x]+'```')
        else:
            await ch.send(st[0:x])
        await splitsend(ch,st[x+1:],codeformat)
