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
		with open('configuration.json', 'r') as c: # - Open 'configuration.json' file containing work data. Fetch extensions load & log details. -
			configuration = json.load(c); 
			appName = configuration['name'];
			log = configuration['developer']['log'];
			defaults = configuration['values']['defaults'];
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
			if log['notices']:
				print(f'By configuration joined guild: {interaction.guild.name}; {interaction.guild.id}');
			members = len([m for m in interaction.guild.members if not m.bot]); # - Get members count excluding bots. -
			time = Time();
			roles = {};
			for r in interaction.guild.roles:
				if r != interaction.guild.default_role and not r.managed:
					#roles[r.id] = self.client.database.escape.string(r.name); # - Adapting string to don't cause errors while inputting to DB. TODO: Do something to indicate that it was addapted. -
					roles[r.id] = r.name;
			payload = { "id": interaction.guild.id,
				"prefix": defaults['prefix'], # - TODO/DONE/: Check what to do to input string containing ' or ", then maybe add name field -
				"language": defaults['language'],
				"roles": roles,
			};
			self.client.database.insert(table = 'guilds.properties',
					    payload = payload);
			embed.add.field(name = "Record", value = "Updated", inline = False)
			
		await interaction.response.send_message(embed=embed, ephemeral=True)
		
async def setup(client: commands.Bot) -> None:
	await client.add_cog(Setup(client))
