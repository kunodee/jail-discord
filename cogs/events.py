
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
        

def setup(client):
    client.add_cog(Events(client))