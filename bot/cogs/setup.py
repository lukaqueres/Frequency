import discord, json
from discord import app_commands
from discord.ext import commands
from discord.app_commands.checks import has_permissions, cooldown

from packets.time import Time
from packets.discord import PIEmbed
from packets.error import CommandOnCooldown

class Setup(commands.Cog): # commands.GroupCog / app_commands.Group
	def __init__(self, client: commands.Bot) -> None:
		self.client = client
		self.cooldown = commands.CooldownMapping.from_cooldown(1, 600, commands.BucketType.guild)
		#self.check = Checks
		super().__init__()
		
	setup = app_commands.Group(name="setup", description="Setup - specified commands.")

	@has_permissions(administrator=True)
	@cooldown(1, 600, key=lambda i: (i.guild_id, i.user.id))
	@setup.command(name="refresh", description="Check for accurate & refresh guild data for service setup")
	async def conf_sub_refresh(self, interaction: discord.Interaction) -> None:
		embed = PIEmbed(
			title="Setup",
			description="Refresh"
		);
		#embed.set_thumbnail(url=self.client.user.avatar)
		DBRoles = self.client.database.select(
			table = 'guilds.properties', 
			condition = {"id": interaction.guild_id}, 
			columns = ["roles"]);
		if DBRoles:
			guildRoles = {};
			for r in interaction.guild.roles:
				if r != interaction.guild.default_role and not r.managed:
					guildRoles[r.id] = r.name;
			DBRoles = {int(k): v for k, v in DBRoles.items()} # - After SELECT keys are string instead of int, failing `==` -
			DBrefresh = False;
			if len(DBRoles) == len(guildRoles):
				for k, v in DBRoles.items():
					if guildRoles[k] == v:
						pass;
					else:
						DBrefresh = True;
						break;
				
			else:
				DBrefresh = True;
			if DBrefresh:
				payload = {"roles": guildRoles};
				self.client.database.update(
					table = 'guilds.properties', 
					payload = payload, 
					condition = {"id": interaction.guild.id}
				);
				rolesStatus = "*Synchronized*"
			else:
				rolesStatus = "*Accurate*"
			embed.add.field(name = "Record", value = rolesStatus, inline = False)
		else:
			self.client.log.notify(f'Configurationed guild: {interaction.guild.name}; {interaction.guild.id}');
			self.client.database.predefined.add_new_guild(interaction.guild);
			embed.add.field(name = "Record", value = "Updated", inline = False)
			
		await interaction.response.send_message(embed=embed, ephemeral=True)
		
async def setup(client: commands.Bot) -> None:
	await client.add_cog(Setup(client))
