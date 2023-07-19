
import discord
from discord.ext import commands, tasks
from datetime import datetime
import sqlite3
import time

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
    
    if not db_stash or not db_reque:
        db_stash = database()
        db_reque = int(time.time())
        print("register2")
        return db_stash
    if db_reque - int(time.time()) <= -30:
        d = check_db(db_stash)
        if not d:
            print("register1")
            db_stash = database()
            db_reque = int(time.time())
        return db_stash
    else:
        print("register3")
        return db_stash