
import core

class ErrorsHandler(core.commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @core.commands.Cog.listener()
    async def on_application_command_error(self, ctx: core.discord.ApplicationContext, error: core.discord.DiscordException):

        if isinstance(error, core.discord.errors.CheckFailure):
            return await ctx.respond(f"Non hai i permessi per eseguire questo comando.", ephemeral=True)
        
        elif isinstance(error, core.discord.errors.Forbidden):
            return await ctx.respond(f"Non ho i permessi per eseguire questo comando.", ephemeral=False)
        
        raise error



def setup(client):
    client.add_cog(ErrorsHandler(client))