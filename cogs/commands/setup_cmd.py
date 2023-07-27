
import core

class MyModal(core.discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(core.discord.ui.InputText(label="How much is " + str(core.randrange(10)) + " + " + str(core.randrange(10)) + " ?"))

    async def callback(self, interaction: core.discord.Interaction):

        try:
            text = self.children[0].label
            first = int(text.split(" ")[3].replace(" ", ""))
            secnd = int(text.split(" ")[5].replace(" ", ""))
            answer = int(self.children[0].value)
        except:
            embed = core.discord.Embed(title="🍃ㆍVerification System", description="_Woops! It looks like the answer is not correct. Try again!_\nIf you got any problems, contact server administrators!", colour=0xc800ff, timestamp=core.datetime.now())
            embed.set_footer(text="Developed by kunode", icon_url="https://avatars.githubusercontent.com/u/45669555?v=4")
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        
        if answer != first + secnd:
            embed = core.discord.Embed(title="🍃ㆍVerification System", description="_Woops! It looks like the answer is not correct. Try again!_\nIf you got any problems, contact server administrators!", colour=0xc800ff, timestamp=core.datetime.now())
            embed.set_footer(text="Developed by kunode", icon_url="https://avatars.githubusercontent.com/u/45669555?v=4")
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        
        """await interaction.user.add_roles(core.discord.utils.get(interaction.user.guild.roles, id=979331516201046116))
        await interaction.user.remove_roles(core.discord.utils.get(interaction.user.guild.roles, id=979331635436716032))"""
        embed = core.discord.Embed(title="🍃ㆍVerification System", description="<a:successo:1091528923365523626> __Successfully verified! Now you gained the access of all the channels!_", colour=0xc800ff, timestamp=core.datetime.now())
        embed.set_footer(text="Developed by kunode", icon_url="https://avatars.githubusercontent.com/u/45669555?v=4")
        await interaction.response.send_message(embed=embed, ephemeral=True)

class VerifyButton(core.discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @core.discord.ui.button(label="Verify Here", custom_id="persistent_view:verify_button", emoji="<a:claimed:1128406640719311061>", style=core.discord.ButtonStyle.primary)
    async def button_callback(self, button, interaction):
        await interaction.response.send_modal(MyModal(title="Verification Question"))

    @core.discord.Cog.listener()
    async def on_ready(self):
        if not self.captcha_persi:
            self.bot.add_view(VerifyButton())
            self.captcha_persi = True


class setupCmd(core.commands.Cog):
    def __init__(self, bot: core.discord.Bot):
        self.bot = bot

    @core.commands.slash_command(name="setup", description="⚙️ㆍ Start the setup of the guild")
    async def setups(
        self, 
        ctx: core.discord.ApplicationContext, 
        channel: core.discord.Option(core.discord.TextChannel, description="Channel of the verification (must be setupped that have to be seen by the not verified roles)"),
        log_category: core.discord.Option(core.discord.CategoryChannel, description="Category where all the logs will be"),
        not_verified: core.discord.Option(core.discord.Role, description="Role that have to be given to the user when he join"),
        verified: core.discord.Option(core.discord.Role, description="Role that have to be given to the user after he got verified"),
        state: core.discord.Option(str, choices=['State 1', 'State 2'], description="State of verification")
    ):
        
        embed = core.discord.Embed(
            title="⚙️ ㆍ Setup Verification",
            description=f"ㆍ_Channel_ » {channel.mention}\nㆍ_Log Category_ » {log_category.mention}\nㆍ_Not verified role_ » {not_verified.mention}\nㆍ_Verified role_ » {verified.mention}\nㆍ_State_ » {state}",
            colour=0xff00f7,
            timestamp=core.datetime.now()
        )
        embed.set_footer(text="Developed by kunode", icon_url="https://avatars.githubusercontent.com/u/45669555?v=4")
        await ctx.respond(embed=embed)

        embed = core.discord.Embed(
            title="🍃ㆍVerification System",
            description="_Hi there! To gain access to all the channels of the server, press the button below!_\nIf there are some errors, contact the server administrators.",
            colour=0xc800ff,
            timestamp=core.datetime.now()
        )

        embed.set_footer(text="Developed by kunode", icon_url="https://avatars.githubusercontent.com/u/45669555?v=4")

        if state == "State 1":
            button = core.discord.ui.Button(label="🔗 Verify Here", url=core.config.rso_auth, style=core.discord.ButtonStyle.link)
            view = core.discord.ui.View()
            view.add_item(button)
            await channel.send(embed=embed, view=view)
        else:
            await channel.send(embed=embed, view=VerifyButton())

def setup(client):
    client.add_cog(setupCmd(client))