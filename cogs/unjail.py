
import core

class Free(core.commands.Cog):
    def __init__(self, bot: core.discord.Bot):
        self.bot = bot

    @core.commands.slash_command(name="free", description="Unjail a user")
    @core.decorators.can_ban()
    async def free(self, ctx: core.discord.ApplicationContext, user: core.discord.Option(core.discord.User, "username")):

        await ctx.defer(ephemeral=True)

        if ctx.user.id == user.id:
            return await ctx.followup.send(f"You cant unjail yourself", ephemeral=True)

        database = core.database()
        result = database.get_user(str(user.id))
        if not result:
            database._close()
            return await ctx.followup.send(f"{user.mention} is not jailed", ephemeral=True)
        
        roles = result[2].split(',')
        roles = [core.discord.utils.get(ctx.guild.roles, id=int(roleid)) for roleid in roles]
        logChannel = self.bot.get_channel(core.config.log_prigione)

        await user.edit(roles=[])
        for role in roles:
            if(role.id in core.config.staffers):
                continue
            try: await user.add_roles(role)
            except: pass

        embed = core.discord.Embed(
            description=f"🆕 **New member unjailed**ㆍ #JAIL\n\n💣 _Member_ ㆍ {user.mention} `{user.id}`\n❄️ _Admin_ ㆍ {ctx.user.mention} `{ctx.user.id}`",
            colour=0x00b0f4,
            timestamp=core.datetime.now()
        )
        if ctx.guild.icon:
            embed.set_thumbnail(url=ctx.guild.icon.url)

        if isinstance(logChannel, core.discord.TextChannel):
            c = await logChannel.send(embed=embed)

        database.unjail(user.id)
        database._close()

        await ctx.followup.send(f"{user.mention} successfully unjailed!\n{c.jump_url}", ephemeral=True)



def setup(client):
    client.add_cog(Free(client))