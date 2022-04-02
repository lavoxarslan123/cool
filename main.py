import disnake
from disnake import message
from disnake.ext import commands
from disnake.ext.commands import command, has_permissions, bot_has_permissions

# Intents
intents = disnake.Intents.default()
intents.members = True

# Ban Convert
class BannedMember(commands.Converter):
    async def convert(self, ctx, argument):
        if argument.isdigit():
            member_id = int(argument, base=10)
            try:
                return await ctx.guild.fetch_ban(disnake.Object(id=member_id))
            except disnake.NotFound:
                raise commands.BadArgument('This member has not been banned before.') from None

        ban_list = await ctx.guild.bans()
        entity = disnake.utils.find(lambda u: str(u.user) == argument, ban_list)

        if entity is None:
            raise commands.BadArgument('This member has not been banned before.')
        return entity


# Bot Prefix & Intents Enable
client = commands.Bot(command_prefix='.', intents=intents)
client.remove_command('help')

# Bot Status & Activity
@client.event
async def on_ready():
    await client.change_presence(status=disnake.Status.online,
                                 activity=disnake.Activity(type=disnake.ActivityType.watching,
                                                           name="discord.gg/larpc"))
    print('Bot is online!')

# Ping Command
@client.command(description="Pong!")
async def ping(ctx):
    await ctx.send(f"🏓 Pong! ``{round(client.latency * 1000)}ms``")


# ------------------------ Management Commands

# ---- Slowmode Command
@client.command()
@has_permissions(manage_messages=True)
async def setslowmode(ctx, seconds: int):
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f"Set the slowmode in this channel to {seconds} seconds!")

# ---- Channel Lock Command
@client.command()
@commands.has_permissions(manage_channels=True)
async def lock(ctx, channel: disnake.TextChannel=None):
    overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = False
    await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.send('This Channel is locked.')
@lock.error
async def lock_error(ctx, error):
    if isinstance(error,commands.CheckFailure):
        await ctx.send('You do not have permission to use this command!')

# ---- Channel Unlock Command
@client.command()
@commands.has_permissions(manage_channels=True)
async def unlock(ctx, channel: disnake.TextChannel=None):
    overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = True
    await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.send('This Channel is unlocked.')
@unlock.error
async def unlock_error(ctx, error):
    if isinstance(error,commands.CheckFailure):
        await ctx.send('You do not have permission to use this command!')

# ---- Banned Words Filter (Event)
@client.event
async def on_message(message):
    if message.author.bot:
        return

    if words := [word for word in message.content.split() if word.lower() in ("𝙽𝚒𝚐𝚐𝚎𝚛","n‎‎‎‎‎i‎‎‎‎g‎‎‎‎g‎‎‎‎e‎‎‎‎‎r‎‎‎‎","mf","nigga","nigger","retard","retarded","cum","cunt","motherfucker","kys","niggers","dick","vagina","penis")]:
        await message.delete()

        await message.channel.send(f"⚠ Hey {message.author.mention}! Please refer from using words like that! Continuing to do so may result in a punishment!", delete_after=10.0)
    await client.process_commands(message)

# ------------------------ Tags

@client.command()
async def gamecode(ctx):
    embed = disnake.Embed(title="")
    embed = disnake.Embed(color=000000, timestamp=ctx.message.created_at)
    embed.add_field(name="Hey! Thank you for being a part of our Community!",
                    value="Our Game Code is **LACaliRP**",
                    inline=False)
    await ctx.send(embed=embed)

@client.command()
async def staffapp(ctx):
    embed = disnake.Embed(title="")
    embed = disnake.Embed(color=000000, timestamp=ctx.message.created_at)
    embed.add_field(name="Hey! Thank you for being a part of our Community!",
                    value="You can apply to become a part of our Staff Team by filling out a form attached in **<#926817251280191569>**",
                    inline=False)
    await ctx.send(embed=embed)

@client.command()
async def appeal(ctx):
    embed = disnake.Embed(title="")
    embed = disnake.Embed(color=000000, timestamp=ctx.message.created_at)
    embed.add_field(name="Hey! Thank you for being a part of our Community!",
                    value="You can appeal a punishment at our [Appeal Hub.](https://forms.gle/jBnUJ99bcLk7Gfp1A)",
                    inline=False)
    await ctx.send(embed=embed)

@client.command()
async def mafias(ctx):
    embed = disnake.Embed(title="")
    embed = disnake.Embed(color=000000, timestamp=ctx.message.created_at)
    embed.add_field(name="Hey! Thank you for being a part of our Community!",
                    value="You can apply to become a part of our Official Mafias at https://discord.gg/Cfcr8JpkQ4!",
                    inline=False)
    await ctx.send(embed=embed)

# ------------------------ Others

@client.command()
async def membercount(ctx):
    embed = disnake.Embed(title="")
    embed = disnake.Embed(color=000000, timestamp=ctx.message.created_at)
    embed.add_field(name="👥 Member Count",
                        value=f"There are currently **{ctx.guild.member_count} Members** in this server!",
                        inline=False)
    await ctx.send(embed=embed)


# some commands

@client.command(aliases=["whois"])
async def userinfo(ctx, member: disnake.Member = None):
    if not member:  # if member is no mentioned
        member = ctx.message.author  # set member as the author
    roles = [role for role in member.roles]
    embed = disnake.Embed(timestamp=ctx.message.created_at,
                          title=f"User Info - {member}")
    embed.set_thumbnail(url=member.avatar.url)
    embed.set_footer(text=f"Requested by {ctx.author}")

    embed.add_field(name="Display Name:", value=member.display_name, inline=False)
    embed.add_field(name="ID:", value=member.id, inline=False)

    embed.add_field(name="Created Account On:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"), inline=False)
    embed.add_field(name="Joined Server On:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"), inline=False)
    print(member.top_role.mention)
    await ctx.send(embed=embed)

# WELCOME IN CHANNEL
@client.event
async def on_member_join(member):
    if member.guild.name == 'Los Angeles Roleplay Community':  #type your server name
        channel = client.get_channel(925700658257084456)
        await channel.send(f'{member.mention} just joined **{member.guild.name}**! They are our ``{member.guild.member_count}th`` member, please give them a warm welcome! 😄')
        role = disnake.utils.get(member.guild.roles, name="Member")
        await member.add_roles(role)
    else:
        return

# MODERATION COMMANDS

# MUTE COMMAND
@client.command()
@commands.has_permissions(kick_members=True)
async def mute(ctx, member: disnake.Member, *, reason =None):

    muted_role = disnake.utils.get(ctx.guild.roles, name="LARPC Muted")

    await member.add_roles(muted_role)
    print(member)
    print("has been muted for")
    print(reason)
    await ctx.send(f"{member} is succesfully muted!")
    await member.send(f"You have been muted in **{ctx.guild.name}** for **{reason}**!")
    channel = client.get_channel(801446246954827808)
    await channel.send(f"{member} has been **muted** by {ctx.author} for **{reason}**!")

# UNMUTE COMMAND
@client.command()
@commands.has_permissions(kick_members=True)
async def unmute(ctx, member: disnake.Member):

    muted_role = disnake.utils.get(ctx.guild.roles, name="LARPC Muted")

    await member.remove_roles(muted_role)
    print(member)
    print("has been succesfully unmuted")
    await ctx.send(f"{member} is succesfully unmuted!")
    await member.send(f"You have been unmuted in **{ctx.guild.name}**!")
    channel = client.get_channel(801446246954827808)
    await channel.send(f"{member} has been **unmuted** by {ctx.author}!")

# KICK COMMAND
@client.command(description="kicks a user with specific reason (only admins)") #kick
@commands.has_permissions(kick_members=True)
async def kick (ctx, member:disnake.Member=None, *, reason =None):
 try:
    if (reason == None):
        await ctx.channel.send("You have to specify a reason!")
        return
    if (member == ctx.message.author or member == None):
        await ctx.send("You cannot kick yourself!")

    message = f"You have been kicked from **{ctx.guild.name}** for **{reason}**!"
    await member.send(message)
    await ctx.guild.kick(member, reason=reason)
    print(member)
    print("has been kicked for")
    print(reason)
    await ctx.channel.send(f"{member} is succesfully kicked!")
    channel = client.get_channel(801446246954827808)
    await channel.send(f"{member} has been **kicked** by {ctx.author} for **{reason}**!")
 except:
    await ctx.send(f"I cannot kick {member}! *(I am unable to kick a bot / an owner).*")

# BAN COMMAND ####################################################################################
@client.command(description="Bans a user with specific reason (only admins)") #ban
@commands.has_role("Administrative Staff")
async def ban (ctx, member:disnake.User=None, *, reason =None):
 try:
    if (reason == None):
        await ctx.channel.send("You have to specify a reason!")
        return
    if (member == ctx.message.author or member == None):
        await ctx.send("You cannot ban yourself!")

    message = f"You have been banned from **{ctx.guild.name}** for **{reason}**! You may be able to appeal your ban at https://forms.gle/BnPpawExhFtNGwT3A!"
    await member.send(message)
    await ctx.guild.ban(member, reason=reason)
    print(member)
    print("has been banned for")
    print(reason)
    await ctx.channel.send(f"{member} is succesfully banned for {reason}! Jeez.")
    channel = client.get_channel(801446246954827808)
    await channel.send(f"{member} has been **banned** by {ctx.author} for **{reason}**!")
 except:
    await ctx.send(f"I cannot ban {member}! *(I am unable to bam a bot / an owner).*")

# UN BAN COMMAND
@client.command(description="UN BANS a user with specific reason (only admins)") #ban
@commands.has_permissions(ban_members=True)
async def unban (ctx, user:disnake.User=None, *, reason =None):
 try:
    if (reason == None):
        await ctx.channel.send("You have to specify a reason!")
        return
    if (user == ctx.message.author or user == None):
        await ctx.send("You cannot unban yourself / you are not banned!")

    await ctx.guild.unban(user, reason=reason)
    print(user)
    print(reason)
    await ctx.channel.send(f"{user} is **succesfully unbanned** for {reason}!")
    channel = client.get_channel(801446246954827808)
    await channel.send(f"{user} has been **unbanned** by {ctx.author} for **{reason}**!")
 except:
    await ctx.send(f"Error 404: I cannot unban {user}!")

# pinging
@client.command()
@commands.has_role("Ping Perms")
async def partnerping(message):
        await message.channel.send(f"Hey <@&928584599800520744>! Make sure to check this server out!")

@client.command()
@commands.has_role("Administrative Staff")
async def ssu(message):
    await message.channel.send(f"<@&928584369042505748> Hello people!\nWe're doing a Server Startup!\nCome join and help us startup this amazing server!\nㅤ\nCome join Emergency Response Liberty County and join our server!\n**Server name:** ``Los Angeles Roleplay I Strict I Custom Livery``\n**Code:** ``LACaliRP``\nㅤ\nhttps://media.discordapp.net/attachments/927859882420490240/930412721424437288/unknown.png")

@client.command()
@commands.has_role("Staff Team Trainer")
async def trainingping(message):
        await message.channel.send(f"<@&926820990829350922>")

@client.command()
@commands.has_role("Administrative Staff")
async def purge(ctx, amount=5):
	await ctx.channel.purge(limit=25)




# Token
client.run('OTIyNTEwMzQ5MTQyNDcwNjU2.YcCgtg.ihyYnxB-yNDrHQVzdbCCYcXskOI')


