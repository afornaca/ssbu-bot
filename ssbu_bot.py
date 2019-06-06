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
    '''
    Returns framedata for all moves for one character
    '''
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


@client.command(aliases=['move'])
async def search_by_move(ctx, *, move):
    '''
    Prints each character's total frames for one move ordered least to greatest
    '''
    char_list = [chars[0] for chars in cursor.execute("SELECT Character FROM ssbuData")]
    move_data = [data[0] for data in cursor.execute("SELECT {} FROM ssbuData".format(move))]

    # convert to float so it sorts least to greatest rather than alphabetical
    move_data = [float(z) for z in move_data]
    new_list = list(zip(char_list, move_data))
    # sorts by the second element in the tuple which is all the float values
    new_list = sorted(new_list, key=lambda x: x[1])
    last_list = []
    for y in new_list:
        # takes off the '.0' at the end
        # using .strip('.0') was making 50.0 -> 5 for Zelda on !move Nair
        last_list.append(y[0] + ": " + str(y[1])[:-2])
    await ctx.send('Note: Values of -1 show that total frames cannot be calculated for that move')
    await ctx.send('\n'.join(last_list))


@client.command()
async def waluigi(ctx):
    '''
    life is pain
    '''
    await ctx.send('Add me to smash pls ;_;')


client.run(TOKEN)


