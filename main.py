
import core

intents = core.discord.Intents.all()
client  = core.discord.Bot("k!", intents=intents, status=core.discord.Status.do_not_disturb, activity=core.discord.Streaming(name="Developed by Kunode", url="https://discord.gg/Nthz5mNXRw"))

###
## cogs import
###

files = ["cogs.jail", "cogs.events", "cogs.errors", "cogs.unjail"]

for file in files:
    try:
        client.load_extension(file)
    except Exception as err:
        print(f"[!] Error while loading {file} -> {str(err)}")

client.run(core.config.BOT_TOKEN)