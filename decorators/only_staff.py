import core

def can_ban():
    def predicate(ctx: core.discord.ApplicationContext):

        if ctx.author.guild_permissions.administrator:
            return True

        role_ids = [role.id for role in ctx.author.roles]
        required_roles = [role.id for role in ctx.guild.roles if role.id in core.config.can_ban]

        return any(role_id in required_roles for role_id in role_ids)

    return core.commands.check(predicate)