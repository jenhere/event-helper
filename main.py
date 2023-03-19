import discord
import asyncio
from discord.ext import commands
from datetime import datetime
from decouple import config
EH_BOT_TOKEN = config('BOT_TOKEN')

intents = discord.Intents.all()
client = commands.Bot(command_prefix='eh!', intents=intents)
 
@client.event
async def on_ready():
  await client.tree.sync()
  print("Success! Bot is connected to Discord")

@client.tree.command(name='startwatching', description='Starts watching attendees on a specified voice channel')
async def watch_attendee(interaction: discord.Interaction, vc: discord.VoiceChannel, minimum_minutes: int = 3):
    # Describe the parameter
    """my command description
    Args:
        minimum_minutes (int): Minimum minutes a member should spent on VC before get listed as attendee
    """
    pass

    # Get the voice channel specified by vcid
    if vc is None:
        await interaction.response.send_message(f'Error: voice channel `{vc.id}` not found.')
        return

    # Get a list of members currently in the voice channel
    members = [m for m in vc.members]

    if not members:
        await interaction.response.send_message(f'Error: no members found in voice channel <#{vc.id}>.')
        return

    # Create a message containing a list of members in the voice channel
    attendee_list = '\n'.join([f'<@{m.id}> `{m.name}#{m.discriminator}`' for m in members])
    msg = await interaction.response.send_message(f'Attendees in voice channel <#{vc.id}> `{vc.id}`:\n{attendee_list}')

    # List of unverified members with member id and time joining
    unv_members_time = []
    unv_members = []

    # Start a task to periodically check for new members in the voice channel
    async def attendee_check():
        await client.wait_until_ready()
        while True:
            for vcm in vc.members:
                if vcm not in unv_members and vcm not in members:
                    t = datetime.now()
                    id_jointime = [[vcm, t.strftime('%d/%m/%y %H:%M:%S')]]
                    unv_members_time.extend(id_jointime)
                    unv_members.append(vcm)
                    print("added "+str(vcm.name)+" in unv_members_time. Time: "+str(id_jointime))

            new_members = []
            for um in unv_members_time:
                um1 = um[1]
                um0 = um[0]
                um1_obj = datetime.strptime(um1, '%d/%m/%y %H:%M:%S')
                if (datetime.now() - um1_obj).total_seconds()/60 >= minimum_minutes and um0 not in members and um0 in vc.members:
                    new = [um0]
                    new_members = [m for m in new]
                    print("added "+str(um0.name)+"to attendee list")

            members.extend(new_members)
            print("new_members:")
            print(new_members)
            if len(new_members) > 0:
                attendee_list = '\n'.join([f'<@{m.id}> `{m.name}#{m.discriminator}`' for m in members])
                await interaction.edit_original_response(content=f'Attendees in voice channel <#{vc.id}> `{vc.id}`:\n{attendee_list}')
            await asyncio.sleep(30)

    client.loop.create_task(attendee_check(), name=str(vc.id))

@client.tree.command(name='stopwatching', description='Stops watching attendees on a specified voice channel')
async def stop_attendee(interaction: discord.Interaction, vc:discord.VoiceChannel):
    # Stop any running tasks for the specified voice channel
    if vc is None:
        await interaction.response.send_message(f'Error: voice channel `{vc.id}` not found.')
        return
    
    for task in asyncio.all_tasks():
        if task.get_name() == str(vc.id):
            task.cancel()
            await interaction.response.send_message(f"Stopped watching vc <#{vc.id}>")
        else:
            await interaction.response.send_message(f"There's no task watching <#{vc.id}>")

@client.tree.command(name='ping', description='ping if the meeting helper bot is active')
async def ping(interaction: discord.Interaction):
  #Send message to prove the bot is active
  await interaction.response.send_message('Hello, Im active.')
          
client.run(EH_BOT_TOKEN)
