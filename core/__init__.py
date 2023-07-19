
import discord
from discord.ext import commands, tasks
from datetime import datetime
import sqlite3
import time
import asyncio

from config_ import config
from .database_ import database
import decorators

db_stash = None
db_reque = None

def check_db(db: database):
    try:
        db.cur.execute("SELECT 1")
        return True
    except Exception as err:
        print(err)
        return False

def get_database() -> database:
    global db_stash, db_reque
    
    if db_stash == None or db_reque == None:
        db_stash = database()
        db_reque = int(time.time())
        return db_stash
    if db_reque - int(time.time()) <= -30:
        d = check_db(db_stash)
        if not d:
            db_stash = database()
            db_reque = int(time.time())
        return db_stash
    else:
        return db_stash