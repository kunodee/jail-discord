
import core

class Jail(core.commands.Cog):
    def __init__(self, bot: core.discord.Bot):
        self.bot = bot

    @core.commands.slash_command(name="jail", description="Jail a user.")
    @core.decorators.can_ban()
    async def jail(self, ctx: core.discord.ApplicationContext, user: core.discord.Option(core.discord.User, "username"), reason: core.discord.Option(str, "reason", required=False)):

        await ctx.defer(ephemeral=True)

        if ctx.user.id == user.id:
            return await ctx.followup.send(f"You cant jail yourself!", ephemeral=True)

        database = core.database()
        result = database.get_user(str(user.id))
        if result:
            database._close()
            return await ctx.followup.send(f"{user.mention} is already jailed!", ephemeral=True)
        
        roles = [str(role.id) for role in user.roles]
        admin = ctx.user.id
        reason = "No reason provided." if not reason else reason
        logChannel = self.bot.get_channel(core.config.log_prigione)

        await user.edit(roles=[])
        await user.add_roles(core.discord.utils.get(ctx.guild.roles, id=core.config.jailed_role))

        embed = core.discord.Embed(
            description=f"🆕 **New member jailed**ㆍ #JAIL\n\n💣 _Member_ ㆍ {user.mention} `{user.id}`\n💦 _Reason_ ㆍ {reason}\n❄️ _Admin_ ㆍ {ctx.user.mention} `{ctx.user.id}`",
            colour=0x00b0f4,
            timestamp=core.datetime.now()
        )
        if ctx.guild.icon:
            embed.set_thumbnail(url=ctx.guild.icon.url)

        if isinstance(logChannel, core.discord.TextChannel):
            c = await logChannel.send(embed=embed)

        database.jail(user.id, roles, admin, reason, core.datetime.now())
        database._close()

        await ctx.followup.send(f"{user.mention} successfully jailed!\n{c.jump_url}", ephemeral=True)

def setup(client):
    client.add_cog(Jail(client))