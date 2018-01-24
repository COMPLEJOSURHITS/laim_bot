import discord, async, random, time, sqlite3, re, datetime, os
from discord.ext import commands
from .fortunas import fortunas
import bot.scraper as scraper
import bot.hchan as hchan

bot = commands.Bot(command_prefix="_")
dbf = "bot/files/laim.db"
init_time = None

@bot.event
async def on_ready():
    global init_time
    print("Bot Online")
    init_time = int(time.time())

@bot.command(pass_context=True)
async def ping(ctx):
    now = datetime.datetime.utcnow()
    delta = now-ctx.message.timestamp
    await bot.say(':ping_pong: Pong   ``%ims``' % delta.microseconds)

@bot.command(pass_context=True)
async def cn(ctx):
    try:
        await bot.edit_profile(username=ctx.message.content[4:])
    except:
        await bot.say("Rate limit error")
    await bot.delete_message(ctx.message)

@bot.command(pass_context=True)
async def test(ctx):
    global init_time
    present_time = int(time.time())
    running_time = present_time - init_time
    dias = 0
    horas = 0
    minutos = 0
    segundos = running_time
    while segundos >= 60:
        minutos+=1
        segundos-=60
    while minutos >= 60:
        horas+=1
        minutos-=60
    while horas >= 24:
        dias+=1
        horas-=24
    await bot.say("Bot corriendo desde hace %i dias %i horas %i minutos y %i segundos :)" % (
        dias,
        horas,
        minutos,
        segundos
        )
    )

@bot.command(pass_context=True)
async def echo(ctx):
    await bot.say(ctx.message.content[6:])
    await bot.delete_message(ctx.message)

@bot.command(pass_context=True)
async def quien(ctx):
    cmd = re.compile(r"_quien")
    def randomMember():
        mem=list(ctx.message.server.members)
        return mem[random.randint(0,len(mem)-1)]
    m=""
    for el in cmd.split(ctx.message.content+" "):
        if el:
            m=m+randomMember().name+el
    await bot.say(m)

@bot.command(pass_context=True)
async def ss(ctx):
    if int(ctx.message.server.id) == 301217828307075073:
        with open("bot/files/ss/"+random.choice(os.listdir("bot/files/ss")), "rb") as f:
            await bot.send_file(ctx.message.channel,f)
            f.close()
    else:
        await bot.say("comando no disponible en este servidor")

@bot.command(pass_context=True)
async def siono(ctx):
    await bot.say(random.choice(["Cy","\xf1o"]))

@bot.command(pass_context=True)
async def dank(ctx):
    await bot.say(":joy: :ok_hand:")

@bot.command(pass_context=True)
async def fortuna(ctx):
    f=re.compile(r"_fortuna ?(?P<patron>.*)")
    pat=f.match(ctx.message.content).groupdict()["patron"]
    if pat:
        patf=re.compile(".*%s.*" % pat)
        for el in fortunas:
            if patf.match(el):
                await bot.say(el)
                return
    elif int(ctx.message.server.id) == 301217828307075073:
        await bot.say(fortunas[random.randint(0,len(fortunas)-1)])
        return
    await bot.say(fortunas[random.randint(0,len(fortunas)-3)])

@bot.command(pass_context=True)
async def chan(ctx):
    message = ctx.message
    fm = await bot.send_message(message.channel,scraper.main_screen())
    msg = await bot.wait_for_message(author=message.author,timeout=15,check=lambda c: c.content[0]=='/')
    if not(msg):
        await bot.delete_message(fm)
        return
    await bot.delete_message(fm)
    response = scraper.goto_board(msg.content.strip())
    if response["error"]:
        fm = await bot.send_message(message.channel,response["content"])
        time.sleep(5)
        await bot.delete_message(fm)
        return
    else:
        fm = await bot.send_message(message.channel,response["content"][0])
        i=1
        hilos = list(response["content"][1])
        while True:
            el = hilos[i-1]
            page = await bot.send_message(message.channel,el)
            if i>1:
                await bot.add_reaction(page,"\u25C0")#anterior
            if i<15:
                await bot.add_reaction(page,"\u25B6")#siguiente
            await bot.add_reaction(page,"\u2611")#seleccionar
            await bot.add_reaction(page,"\u274E")#quitar
            opc = await bot.wait_for_reaction(
                    ["\u25C0","\u25B6","\u2611","\u274E"],user=message.author,message=page,timeout=15)
            if not(opc):
                await bot.delete_message(fm)
                await bot.delete_message(page)
                return
            else:
                await bot.delete_message(page)
                if opc.reaction.emoji=="\u25C0":
                    i-=1
                    pass
                elif opc.reaction.emoji=="\u25B6":
                    i+=1
                    pass
                elif opc.reaction.emoji=="\u2611":
                    break
                elif opc.reaction.emoji=="\u274E":
                    return
        await bot.delete_message(fm)
        ids=i
        i=0
        imgs = list(scraper.get_thread_files(response["threads"][ids]["post_url"]))
        page = await bot.send_message(message.channel,"loading...")
        while True:
            img = imgs[i]
            await bot.edit_message(page,(("image %i of %i\n" % (i+1,len(imgs)))+img))
            if i>0:
                await bot.add_reaction(page,"\u25C0")#anterior
            if i<len(imgs)-1:
                await bot.add_reaction(page,"\u25B6")#siguiente
            await bot.add_reaction(page,"\u2611")#seleccionar
            await bot.add_reaction(page,"\u274E")#quitar
            opc = await bot.wait_for_reaction(
                    ["\u25C0","\u25B6","\u2611","\u274E"],user=message.author,message=page,timeout=15)
            if not(opc):
                for emoji in ["\u25C0","\u25B6","\u2611","\u274E"]:
                    try:
                        await bot.remove_reaction(page,emoji,
                            discord.member.utils.find(lambda m: m.id == "401391614838439936",
                                message.channel.server.members
                                )
                            )
                    except:
                        pass
                return
            else:
                emoji=opc.reaction.emoji
                try:
                    await bot.remove_reaction(page,emoji,message.author)
                except:
                    pass
                if emoji=="\u25C0":
                    i=i-1
                    pass
                elif emoji=="\u25B6":
                    i+=1
                    pass
                elif emoji=="\u2611":
                    for e in ["\u25C0","\u25B6","\u2611","\u274E"]:
                        try:
                            await bot.remove_reaction(page,e,
                                discord.member.utils.find(lambda m: m.id == "401391614838439936",
                                    message.channel.server.members
                                    )
                                )
                        except:
                            pass
                    return
                elif emoji=="\u274E":
                    await bot.delete_message(page)
                    return
        return

@bot.command(pass_context=True)
async def hispa(ctx):
    global hchan
    message = ctx.message
    fm = await bot.send_message(message.channel,hchan.main_screen())
    msg = await bot.wait_for_message(author=message.author,timeout=20,check=lambda c: c.content[0]=='/')
    await bot.delete_message(fm)
    if not(msg):
        return
    response = hchan.goto_board(msg.content.strip())
    if response["error"]:
        fm = await bot.send_message(message.channel,response["content"])
        time.sleep(5)
        await bot.delete_message(fm)
        return
    else:
        fm = await bot.send_message(message.channel,response["content"][0])
        i=1
        hilos = list(response["content"][1])
        while True:
            el = hilos[i-1]
            page = await bot.send_message(message.channel,el)
            if i>1:
                await bot.add_reaction(page,"\u25C0")#anterior
            if i<15:
                await bot.add_reaction(page,"\u25B6")#siguiente
            await bot.add_reaction(page,"\u2611")#seleccionar
            await bot.add_reaction(page,"\u274E")#quitar
            opc = await bot.wait_for_reaction(
                    ["\u25C0","\u25B6","\u2611","\u274E"],user=message.author,message=page,timeout=15)
            if not(opc):
                await bot.delete_message(fm)
                await bot.delete_message(page)
                return
            else:
                await bot.delete_message(page)
                if opc.reaction.emoji=="\u25C0":
                    i-=1
                    pass
                elif opc.reaction.emoji=="\u25B6":
                    i+=1
                    pass
                elif opc.reaction.emoji=="\u2611":
                    break
                elif opc.reaction.emoji=="\u274E":
                    return
        await bot.delete_message(fm)
        ids=i
        i=0
        imgs = list(hchan.get_thread_files(response["threads"][ids]["post_url"]))
        page = await bot.send_message(message.channel,"cargando...")
        while True:
            img = imgs[i]
            await bot.edit_message(page,(("Imagen %i de %i\n" % (i+1,len(imgs)))+img))
            if i>0:
                await bot.add_reaction(page,"\u25C0")#anterior
            if i<len(imgs)-1:
                await bot.add_reaction(page,"\u25B6")#siguiente
            await bot.add_reaction(page,"\u2611")#seleccionar
            await bot.add_reaction(page,"\u274E")#quitar
            opc = await bot.wait_for_reaction(
                    ["\u25C0","\u25B6","\u2611","\u274E"],user=message.author,message=page,timeout=35)
            if not(opc):
                for emoji in ["\u25C0","\u25B6","\u2611","\u274E"]:
                    try:
                        await bot.remove_reaction(page,emoji,
                            discord.member.utils.find(lambda m: m.id == "401391614838439936",
                                message.channel.server.members
                                )
                            )
                    except:
                        pass
                return
            else:
                emoji=opc.reaction.emoji
                try:
                    await bot.remove_reaction(page,emoji,message.author)
                except:
                    pass
                if emoji=="\u25C0":
                    i=i-1
                    pass
                elif emoji=="\u25B6":
                    i+=1
                    pass
                elif emoji=="\u2611":
                    for e in ["\u25C0","\u25B6","\u2611","\u274E"]:
                        try:
                            await bot.remove_reaction(page,e,
                                discord.member.utils.find(lambda m: m.id == "401391614838439936",
                                    message.channel.server.members
                                    )
                                )
                        except:
                            pass
                    return
                elif emoji=="\u274E":
                    await bot.delete_message(page)
                    return
        return

@bot.command(pass_context=True)
async def t(ctx):
    cmd = re.compile(r"_t (?P<tag>\w+) ?(?P<content>.*)")
    t = cmd.match(ctx.message.content)
    if t:
        db = sqlite3.connect(dbf)
        if t.groupdict()["content"] == "*delete":
            cur = db.execute("SELECT user FROM Tags WHERE tag IS '%s'" % t.groupdict()["tag"])
            try:
                user = next(cur)[0]
                if int(ctx.message.author.id) == user:
                    db.execute("DELETE FROM Tags WHERE tag IS '%s'" % t.groupdict()["tag"])
                    db.commit()
                    await bot.say("Tag '%s' eliminado correctamente" % t.groupdict()["tag"])
                else:
                    await bot.say("Tu no puedes eliminar este tag")
            except:
                await bot.say("Ese tag ni existe we")
        elif t.groupdict()["content"]:
            cur = db.execute("SELECT user FROM Tags WHERE tag IS '%s'" % t.groupdict()["tag"])
            try:
                user = next(cur)[0]
                if int(ctx.message.author.id) == user:
                    db.execute("UPDATE Tags SET content = '%s' WHERE tag IS '%s'" % (
                        t.groupdict()["content"],
                        t.groupdict()["tag"]
                        )
                    )
                    db.commit()
                    await bot.say("Tag '%s' actualizado correctamente" % t.groupdict()["tag"])
                else:
                    await bot.say("Tu no puedes actualizar este tag")
            except:
                db.execute("INSERT INTO Tags VALUES ('%s','%s',%i)" % (
                    t.groupdict()["tag"],
                    t.groupdict()["content"],
                    int(ctx.message.author.id)
                    )
                )
                db.commit()
                await bot.say("Tag '%s' creado correctamente." % t.groupdict()["tag"])
        else:
            cur = db.execute("SELECT content FROM Tags WHERE tag IS '%s'" % t.groupdict()["tag"])
            try:
                content = next(cur)[0]
                await bot.say(content)
                cur.close()
            except:
                await bot.say("No existe el tag '%s'" % t.groupdict()["tag"])
        db.close()      
    elif ctx.message.content.strip().lower() == "_t *list":
        db = sqlite3.connect(dbf)
        cur = db.execute("SELECT tag FROM Tags ORDER BY user")
        l="```\n"
        for el in cur:
            l+=el[0]+"\n"
        await bot.say(l+"```")
        db.close()
    else:
        await bot.say("""No, asi no funciona
            ```
Usa '_t test Hola Mundo' para crear o actualizar un tag
Usa '_t test' para ver el contenido de un tag
Usa '_t test *delete' para borrar un tag
Usa '_t *list' para ver la lista de tags
            ```
            """)

@bot.event
async def on_message(message):
    if message.content.startswith("_/amigos/"):
        with open('bot/files/amigos2017final.png', 'rb') as f:
            await bot.send_file(message.channel, f)
            f.close()
    await bot.process_commands(message) 

#Luis Albizo 13/01/18
