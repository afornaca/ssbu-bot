import sqlite3
from discord.ext import commands
import os

TOKEN = os.getenv('BOT_TOKEN')
prefix = ("!", "?")
client = commands.Bot(command_prefix=prefix)

conn = sqlite3.connect('data.sqlite')
cursor = conn.cursor()


@client.event
async def on_ready():
    print("I'm online :)")


@client.event
async def on_message(message):
    # uncomment below if I want message content printed in console
    # print("The message says: ", message.content)
    await client.process_commands(message)


@client.command()
async def characters(ctx):
    '''
    Print character list in order of appearance
    '''
    # Sending to discord iteratively is slower than my mile time...
    # Made a string separated by newlines from the list contents before sending
    # Doing this is almost instant, as is sending a single string to discord

    # SELECT {column} FROM {table}
    curs = conn.execute('''
                        SELECT Character
                        FROM ssbuData
                        ''')
    data = curs.fetchall()
    data_list = []

    # note: row[0] is the first index of the tuple
    for row in data:
        data_list.append(row[0])
    chars = '\n'.join(data_list)
    await ctx.send(chars)


@client.command()
async def alphabetical(ctx):
    '''
    Print character list in alphabetical order
    '''
    curs = conn.execute('''
                            SELECT Character
                            FROM ssbuData
                            ''')
    data = curs.fetchall()
    data_list = []

    # note: row[0] is the first index of the tuple
    for row in data:
        data_list.append(row[0])
    data_list.sort()
    chars = '\n'.join(data_list)
    await ctx.send(chars)


@client.command(aliases=['search', 'char', 'searchchar'])
async def search_by_name(ctx, *, name):
    curs = conn.execute('''
                        SELECT Nair, Fair, Bair, Uair, Dair, Jab, Ftilt, Utilt, Dtilt, 
                        DashAttack, Fsmash, Usmash, Dsmash, Neutralb, Sideb, 
                        Upb, Downb, Grab, DashGrab
                        FROM ssbuData
                        WHERE Character = (?)''', (name,))

    moves = ['Nair: ', 'Fair: ', 'Bair: ', 'Uair: ', 'Dair: ', 'Jab: ', 'Ftilt: ', 'Utilt: '
                , 'Dtilt: ', 'DashAttack: ', 'Fsmash: ', 'Usmash: ', 'Dsmash: ', 'Neutralb: '
                , 'Sideb: ', 'Upb: ', 'Downb: ', 'Grab: ', 'DashGrab: ']
    data = curs.fetchall()
    tup = ()
    for x in data:
        tup = x
    values = list(tup)

    # append to a new list that we will print as a string all at once rather than sending each
    # move one at a time since this way feels almost instant
    combined = []
    for i, j in zip(moves, values):
        combined.append(i + j.strip('.0'))
    await ctx.send(
                    'Total frames per move for: ' + name + '\n' +
                    '\n'.join(combined) +
                    '\n\nNote: If a value returns as -1, then total frames cannot be calculated.')


@client.command()
async def waluigi(ctx):
    '''
    life is pain
    '''
    await ctx.send('Add me to smash pls ;_;')


client.run(TOKEN)


