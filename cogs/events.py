
import core
import colorama
colorama.init(autoreset=True)

class Events(core.commands.Cog):
    def __init__(self, bot: core.discord.Bot):
        self.bot = bot

    @core.commands.Cog.listener()
    async def on_member_join(self, member: core.discord.Member):
        
        database = core.database()
        
        result = database.get_user(str(member.id))
        if not result:
            return
        
        await member.edit(roles=[])
        await member.add_roles(core.discord.utils.get(member.guild.roles, id=core.config.jailed_role))

    @core.commands.Cog.listener()
    async def on_ready(self):
        print(colorama.Fore.RED + "(!) Successfully connected with " + colorama.Fore.BLUE + str(self.bot.user) + colorama.Fore.GREEN + " (developed by github.com/kunodee)")

    @core.commands.Cog.listener()
    async def on_member_update(self, before, after):

        if before.roles == after.roles:
            return
        
        await core.asyncio.sleep(1) # wait for be sure that he's not getting unjailed

        database = core.get_database()
        valid = core.check_db(database)
        if not valid:
            database = core.database()
        
        user = database.get_user(after.id)
        if not user:
            return
        
        await after.edit(roles=[core.discord.utils.get(after.guild.roles, id=core.config.jailed_role)])

        

def setup(client):
    client.add_cog(Events(client))