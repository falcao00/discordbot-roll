from contextlib import nullcontext

import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import dice

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f"EITA PORRA VAI CARAI, {bot.user.name}")

@bot.event
async def on_member_join(member):
    await member.send(f"Iae poha, {member.name}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if "shit" in message.content.lower():
        await message.delete()
        await message.channel.send(f"{message.author.mention} dont use that world")
    await bot.process_commands(message)


@bot.command()
async def hello(ctx):
    hope = dice.roll('1d12')
    fear = dice.roll('1d12')
    await ctx.send(f"Sua roalgem foi: {ctx.author.mention}! " + "Esperança: " + str(hope) + " Medo: " + str(fear) + " TOTAL: " + str(hope[0]+fear[0]))

@bot.command()
async def r(ctx, arg):
    index = str(arg).find('+')
    if index != -1:
        fistroll = str(arg)[0:index]
        bonus = str(arg)[index+1:len(str(arg))]
    else:
        fistroll = str(arg)
        bonus = str( 0 )
    dice1 = dice.roll(fistroll)
    if dice1[0] >= dice1[1]:
        typeroll = "esperança"
    else:
        typeroll = "medo"

    await ctx.reply(f"Rolagem Teste: " + str(dice1)+ " Total: " + str(dice1[0]+dice1[1]+int(bonus)) + " Esperança/Medo: " + typeroll + " BONUS: " + bonus)

@bot.command()
async def rt(ctx, arg, totalroll=None):
    inicio = 0
    rolls = []
    sinal = []
    bonus = []
    for i in str(arg):
        index = str(arg).find('+', inicio, len(str(arg)))
        if index == -1:
            index = str(arg).find('-', inicio, len(str(arg)))

        if index != -1:
            sinal.append(str(arg)[index])

        if index != -1:
            fistroll = str(arg)[inicio:index]
            dado = dice.roll(fistroll)
            if str(dado) == fistroll:
                bonus.append(fistroll)
                inicio = index + 1
                continue
            rolls.append(dado)
            inicio = index+1
            print(rolls)
        else:
            lastroll = str(arg)[inicio:]
            dado = dice.roll(lastroll)
            if str(dado) == lastroll:
                bonus.append(lastroll)
                break
            rolls.append(dado)
            print(rolls)
            break

    #calculando a rolagem total
    finalresult = 0
    mark = 0
    index_sinal = 0
    for x in rolls:
        temp = 0
        # x é a instancia da primeira rolagem #
        for z in x: #iterando em cima da primeira rolagem
            temp += z
            print(z)
        if mark == 1:
            print (sinal[index_sinal])
            if sinal[index_sinal] == '+':
                finalresult += temp
            if sinal[index_sinal] == '-':
                finalresult -= temp
            sinal.pop(index_sinal)
        if mark == 0:
            mark = 1 #não é mais a primeira rolagem
            finalresult += temp


    #tratamento de bonus
    for y in bonus:
        if sinal[index_sinal] == '+':
            finalresult += int(y)
        if sinal[index_sinal] == '-':
            finalresult -= int(y)
        sinal.pop(index_sinal)

    print("finalresult: " + str(finalresult))

    # armazenando a lista de rolagem para exibição
    listrollfinal = []
    for k in rolls:
        for h in k:
            listrollfinal.append(h)
            print(listrollfinal)

    await ctx.reply(f"` {str(finalresult)} ` " + " <------ " + str(listrollfinal) + " + " + str(bonus))

@bot.command()
async def dh(ctx, arg: str = ""):
    dice1 = dice.roll('2d12')
    resultdice = sum(dice1)
    if not arg:
        total = resultdice
    else:
        if str(arg[0]) == '+':
            total = resultdice + int(str(arg[1:]))
        elif str(arg[0]) == '-':
            total = resultdice - int(str(arg[1:]))
        else:
            total = resultdice
    if dice1[0] > dice1[1]:
        fearhope = 'Hope'
    elif dice1[0] == dice1[1]:
        fearhope = 'Critical Hope'
    else:
        fearhope = 'Fear'
    print(f"`{total}` <---- {resultdice}{arg}|  {dice1}")
    await ctx.reply(f"` {total} ` <---- {dice1} {arg} |  {fearhope} ")



bot.run(token, log_handler=handler, log_level=logging.DEBUG)