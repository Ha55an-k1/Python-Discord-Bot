import discord
from discord.ext import commands
import random
import asyncio
import requests
import time
import json
from random import randint
from jikanpy import AioJikan
jikan_anime_url='https://api.jikan.moe/v3/anime/'
jikan_manga_url='https://api.jikan.moe/v3/manga/'
ent_type_url="https://myanimelist.net/topanime.php?type="


bot = commands.Bot(command_prefix = "!")
bot.activity = discord.Game(name="!uwu for commands")

#ready Event
@bot.event
async def on_ready():
    print('{0.user} is ready desu'.format(bot))


@bot.event
async def on_member_join(member):
    print(f'{member} has joined the server.')

@bot.event
async def on_member_remove(member):
    print(f'{member} has left the server.')








#_____________________________________________________
#COMMANDS
@bot.command()
async def uwu(ctx):
    embed = discord.Embed(
        title = ":fish_cake: UwU-bot - Created by Hassan :fish_cake:",
        description = "All available commands provided by UwU-bot.",
        color = 0X00F2FF
    )

    embed.set_thumbnail(url='https://ih1.redbubble.net/image.537854949.5551/ap,550x550,16x12,1,transparent,t.png')

    embed.add_field(
        name = "{0}ping".format(bot.command_prefix),
        value = "provides latency of the bot's response",
        inline = False
    )

    embed.add_field(
        name = "{0}echo <<message>>".format(bot.command_prefix),
        value = "echoes the message provided by the user",
        inline = False
    )

    embed.add_field(
        name = "{0}quote".format(bot.command_prefix),
        value = "Generates random weeb quote",
        inline = False
    )

    embed.add_field(
        name = "{0}8ball <<sentence>>".format(bot.command_prefix),
        value = "Ask a Question and get a random 8ball Response ",
        inline = False
    )

    embed.add_field(
        name = "{0}<<keyword>>".format(bot.command_prefix),
        value = "send a determined embedded gif\n ora ,muda ,bang ,mrstark ,snap ,chill ,wys",
        inline = False
    )

    embed.add_field(
        name = "{0}reg <<message>>".format(bot.command_prefix),
        value = "Converts alphabet to regional indicators",
        inline = False
    )

    embed.add_field(
        name = "{0}anime <<name>>".format(bot.command_prefix),
        value = "Retrieves MAL profile of anime searched",
        inline = False
    )
    embed.add_field(
        name = "{0}manga <<name>>".format(bot.command_prefix),
        value = "Retrieves MAL profile of manga searched",
        inline = False
    )

    embed.set_footer(text="!uwu for commands")

    await ctx.send(embed = embed)


@bot.command()
async def game(ctx,*,arg):
    await bot.change_presence(activity=discord.Game(name=arg))
    



#_____________________________________________________
#Random Gif Commands
@bot.command()
async def ora(ctx):
    txt0 = discord.Embed(title='ゴゴゴゴゴゴゴゴゴ\nOra Ora Ora Ora\nゴゴゴゴゴゴゴゴゴ', color=0X02A6FF)
    txt0.set_image(url='https://i.imgur.com/C3aWo0G.gif')
    await ctx.send(embed=txt0)

@bot.command()
async def muda(ctx):
    txt1 = discord.Embed(title='ゴゴゴゴゴゴゴゴゴ\nMuda Muda Muda Muda\nゴゴゴゴゴゴゴゴゴ',color=0XEEFF07)
    txt1.set_image(url='https://i.imgur.com/gbFWxNU.gif')
    await ctx.send(embed=txt1)

@bot.command()
async def bang(ctx):
    txt2 = discord.Embed(title="You're gonna carry that weight",color=0X8E0B2E)
    txt2.set_image(url='https://i.imgur.com/2LZW8X8.gif')
    await ctx.send(embed= txt2)

@bot.command()
async def mrstark(ctx):
    txt3= discord.Embed(title="I don't feel so good",color=0X56212F)
    txt3.set_image(url='https://i.imgur.com/1paUKNt.gif')
    await ctx.send(embed= txt3)


@bot.command()
async def snap(ctx):
    txt4= discord.Embed(title="Perfectly balanced, as all things should be",color=0X56212F)
    txt4.set_image(url='https://i.imgur.com/novvq8q.gif')
    await ctx.send(embed= txt4)


@bot.command(aliases=["lofi"])
async def chill(ctx):
    await ctx.send("https://www.youtube.com/watch?v=hHW1oY26kxQ")

@bot.command()
async def wys(ctx):
    await ctx.message.delete()
    await ctx.send("**Wys shordy** :smiling_imp:")


#_____________________________________________________
#REGIONAL CHARACTER CONVERTER
@bot.command(aliases=['type','letter'])
async def reg(ctx,*,arg):
    charlist = list(arg.lower())
    arr=[]
    reg_str=""
    for x in charlist:
        if x==' ':
            arr.append("    ")
        elif not ord(x)>=97 and ord(x)<=112:
            arr.append(":question:")
        else:
            x = ":regional_indicator_" + x + ":"
            arr.append(x)
    i=0
    while i < len(arr):
     reg_str += arr[i]
     i+=1
    
    await ctx.message.delete()
    await ctx.send("{0}: {1}".format(ctx.message.author.mention,reg_str))






#_____________________________________________________
#STOP COMMAND
@bot.command(aliases=['stahp','die'])
async def halt(ctx):
    aID = 366327373530136586
    if ctx.message.author.id == aID:
        await ctx.message.delete()
        endcard = await ctx.channel.send("OwO im outtie :skull:")
        time.sleep(.5)
        await endcard.delete()
        await bot.logout()


#_____________________________________________________
#Echo command
@bot.command(aliases=['print','Transcript_show'])
async def echo(ctx,*,arg):
    await ctx.send(arg)



#_____________________________________________________
#ping command to return latency
@bot.command()
async def ping(ctx):
    await ctx.send(f'>>{round(bot.latency*1000)}ms')






#_____________________________________________________
#ANIME MAL PROFILE Retrieval
# Implemented using JikanPy  
@bot.command()
async def anime(ctx,*,ans):
    aio_jikan = AioJikan()
    search_result = await aio_jikan.search(search_type='anime',query=ans)
    
    #Id Retrieval
    mal_id =search_result['results'][0]['mal_id']

    main_url=jikan_anime_url+'{}'.format(mal_id)

    anime_json=requests.get(main_url).json()
    
    #Metadata
    eng_title =  anime_json['title_english']
    jap_title = anime_json['title_japanese']
    main_title =anime_json['title']

    medium=anime_json['type']
    type_url= ent_type_url +'{}'.format(medium.lower())

    anime_url=anime_json['url']
    image_url = anime_json['image_url']
    synopsis = anime_json['synopsis']
    episodes =  anime_json['episodes']
    score =anime_json['score']
    status = anime_json['status']
    premier = anime_json['premiered']

    studio_name = anime_json['studios'][0]['name']
    studio_url= anime_json['studios'][0]['url']

    licensor_name=anime_json['licensors'][0]['name']
    licensor_url= anime_json['licensors'][0]['url']

<<<<<<< HEAD
    air_date= anime_json['aired'].get('string')


=======
>>>>>>> 3902125d9ee1d65d8b4e877f8010cf2c0eb7c14c
    #Genres
    g_name=[];g_url=[]
    for each in anime_json['genres']:
        g_name.append(each.get('name'))
        g_url.append(each.get('url'))
    genre_string=", ".join(g_name)
    
    #Producers
    pro_name=[];pro_url=[]
    for each in anime_json['producers']:
        pro_name.append(each.get('name'))
        pro_url.append(each.get('url'))
    pro_string=", ".join(pro_name)    

    #Jikan CLOSE()--------------(T^T)
    await aio_jikan.close()
    
    if synopsis.endswith('[Written by MAL Rewrite]'):
        paralen=round(len(synopsis)/2)
        synopsis=synopsis[:-paralen]
        synopsis=synopsis+'...'

    #Embed
    anime_embed= discord.Embed(title=" :tv: :ramen:", color=0X00F2FF)
    anime_embed.set_thumbnail(url=image_url)

    anime_embed.add_field(
        name="**Title:**",
        value=main_title,
        inline=False
    )
    anime_embed.add_field(
        name="**English:**",
        value=eng_title,
        inline=False
    )
    anime_embed.add_field(
        name="**Japanese:**",
        value=jap_title,
        inline=False
    )
    anime_embed.add_field(
        name="**Type:**",
        value="[{}]({})".format(medium.upper(),type_url),
        inline=False
    )
    anime_embed.add_field(
        name="**Episodes:**",
        value=episodes,
        inline=False
    )
    anime_embed.add_field(
        name="**Status:**",
        value=status,
        inline=False
    )
    anime_embed.add_field(
        name="**Aired:**",
        value=air_date,
        inline=False
    )
    anime_embed.add_field(
        name="**Premiered:**",
        value=premier,
        inline=False
    )
    anime_embed.add_field(
        name="**Score:**",
        value=score,
        inline=False
    )
    anime_embed.add_field(
        name="**Producer:**",
        value=pro_string,
        inline=False
    )
    anime_embed.add_field(
        name="**Licensor:**",
        value="[{0}]({1})".format(licensor_name,licensor_url),
        inline=False
    )
    anime_embed.add_field(
        name="**Studio:**",
        value="[{0}]({1})".format(studio_name,studio_url),
        inline=False
    )

    anime_embed.add_field(
        name="**Genre:**",
        value=genre_string,
        inline=False
    )

    anime_embed.add_field(
        name="**Synopsis:**",
        value="*{0}*[read more]({1})".format(synopsis,anime_url),
        inline=False
    )
    anime_embed.set_footer(icon_url='https://i.imgur.com/03Y0GUM.png',text="Provided by JikanPy")
    
    await ctx.send(embed=anime_embed)
    

#______________________________________________________________
#MANGA MAL Profile Retrieval
@bot.command()
async def manga(ctx,*,ans):
    aio_jikan = AioJikan()
    search_result = await aio_jikan.search(search_type='manga',query=ans)
    
    #Id retrieval
    mal_id =search_result['results'][0]['mal_id']

    main_url=jikan_manga_url+'{}'.format(mal_id)

    manga_json=requests.get(main_url).json()
    
    #Metadata
    eng_title = manga_json['title_english']
    jap_title = manga_json['title_japanese']
    main_title =manga_json['title']
    manga_url=manga_json['url']

    medium=manga_json['type']
    type_url=ent_type_url +'{}'.format(medium.lower())
    
    image_url = manga_json['image_url']
    synopsis = manga_json['synopsis']
    volumes =  manga_json['volumes']
    chapters=manga_json['chapters']
    score =manga_json['score']
    status = manga_json['status']
    published = manga_json['published'].get('string')

    serial = manga_json['serializations'][0]['name']
    serial_url= manga_json['serializations'][0]['url']

    paralen=round(len(synopsis)/2)
    synopsis=synopsis[:-paralen]
    synopsis=synopsis+'...'

    #Genres
    g_name=[];g_url=[]
    for each in manga_json['genres']:
        g_name.append(each.get('name'))
        g_url.append(each.get('url'))
    genre_string=", ".join(g_name)

    #Authors
    a_name=[];a_url=[]
    for each in manga_json['authors']:
        a_name.append(each.get('name'))
        a_url.append(each.get('url'))
    author_string=", ".join(a_name)
    

    #Jikan CLOSE()--------------(T^T)
    await aio_jikan.close()
    
    #Embed
    manga_embed=discord.Embed(title=":notebook_with_decorative_cover: :coffee:",color=0X00F2FF)
    manga_embed.set_thumbnail(url=image_url)
    manga_embed.add_field(
        name="**Title:**",
        value=main_title,
        inline=False
    )
    manga_embed.add_field(
        name="**Japanese:**",
        value=jap_title,
        inline=False
    )
    manga_embed.add_field(
        name="**English:**",
        value=eng_title,
        inline=False
    )
    manga_embed.add_field(
        name="**Type:**",
        value="[Manga]({})".format(type_url),
        inline=False
    )
    manga_embed.add_field(
        name="**Volumes:**",
        value=volumes,
        inline=False
    )
    manga_embed.add_field(
        name="**Chapters:**",
        value=chapters,
        inline=False
    )
    manga_embed.add_field(
        name="**Status:**",
        value=status,
        inline=False
    )
    manga_embed.add_field(
        name="**Published:**",
        value=published,
        inline=False
    )
    manga_embed.add_field(
        name="**Genre:**",
        value=genre_string,
        inline=False
    )
    manga_embed.add_field(
        name="**Authors:**",
        value=author_string,
        inline=False
    )
    manga_embed.add_field(
        name="**Serialization:**",
        value="[{0}]({1})".format(serial,serial_url),
        inline=False
    )
    manga_embed.add_field(
        name="**Synopsis:**",
        value="*{0}*[read more]({1})".format(synopsis,manga_url),
        inline=False
    )
    manga_embed.set_footer(icon_url='https://i.imgur.com/03Y0GUM.png',text="Provided by JikanPy")
    await ctx.send(embed=manga_embed)




#Idea taken from Rye2021-CS-Discord Python bot
#8ball command
@bot.command(aliases=["8ball","question"])
async def _8ball(ctx,*,question):
    response=[]
    #yeet
    response.append(":slight_smile: It is certain :slight_smile:")
    response.append(":slight_smile: It is decidedly so :slight_smile:")
    response.append(":slight_smile: Without a doubt :slight_smile:")
    response.append(":slight_smile: Yes - definitely :slight_smile:")
    response.append(":weary: Yeetus Maximus :weary:")
    response.append(":weary: Ye ")
    response.append(":slight_smile: You may rely on it :slight_smile:")
    response.append(":slight_smile: As I see it, yes :slight_smile:")
    response.append(":slight_smile: Most likely :slight_smile:")
    response.append(":slight_smile: Outlook good :slight_smile:")
    response.append(":slight_smile: Yes :slight_smile:")
    response.append(":slight_smile: Signs point to yes :slight_smile:")
    #meh
    response.append(":no_mouth: Reply hazy, try again :no_mouth:")
    response.append(":no_mouth: uhh.. bad connection :no_mouth:")
    response.append(":no_mouth: Better not tell you now :no_mouth:")
    response.append(":no_mouth: Cannot predict now :no_mouth:")
    response.append(":no_mouth: Whatever you say bud :no_mouth:")
    #negative
    response.append(":pensive: I don't know what to tell you :pensive:")
    response.append(":pensive:")
    response.append("::sweat_smile: well goodluck with that :sweat_smile:")
    response.append(":pensive: Don't count on it :pensive:")
    response.append(":pensive: My reply is no :pensive:")
    response.append(":pensive: My sources say no :pensive:")
    response.append(":pensive: I wanna say yes but.. :pensive:")
    response.append(":pensive: Very doubtful :pensive:")
    await ctx.send(":8ball: {0} :8ball:\n\n {1} ".format(question,(random.choice(response))))



##_____________________________________________________
#Anime Quote generator
@bot.command(aliases=["weeb"])
async def quote(ctx):
    qts=[]
    qts.append("\"The world isn't perfect. But it's there for us, doing the best it can....that's what makes it so damn beautiful.\"\n~ Roy Mustang (Full Metal Alchemist)")
    qts.append("\"To know sorrow is not terrifying. What is terrifying is to know you can't go back to happiness you could have.\"\n~ Matsumoto Rangiku (Bleach)")
    qts.append("\"We are all like fireworks: we climb, we shine and always go our separate ways and become further apart. But even when that time comes, let's not disappear like a firework and continue to shine.. forever.\"\n~ Hitsugaya Toshiro (Bleach)")
    qts.append("\"Those who break the rules are scum, that's true, but those who abandon their friends are worse than scum.\"\n~ Kakashi Hatake (Naruto)")
    qts.append("\"A Shinobi's life is not measured by how they lived but rather what they managed to accomplish before their death.\"\n~ Jiraiya (Naruto)")
    qts.append("\"When a man learns to love, he must bear the risk of hatred.\"\n~ Madara Uchiha (Naruto)")
    qts.append("\"There's no advantage to hurrying through life.\"\n~ Shikamaru Nara (Naruto)")
    qts.append("\"If you don’t share someone’s pain, you can never understand them.\"\n~ Nagato (Naruto)")
    qts.append("\"In this world, wherever there is light – there are also shadows. As long as the concept of winners exists, there must also be losers. The selfish desire of wanting to maintain peace causes wars, and hatred is born to protect love.\"\n~ Madara Uchiha (Naruto)")
    qts.append("\"Never give up without even trying. Do what you can, no matter how small the effect it may have!\"\n~ Onoki (Naruto)")
    qts.append("\"Perhaps the companionship of an evil person is preferable to loneliness.\"\n~ Gaara (Naruto)")
    qts.append("\"I could say I’m not sad, but I’d be lying. The problem is the world won’t let me stay a kid forever, so I can’t lie around crying about it either.\"\n~ Shikamaru Nara (Naruto)")
    qts.append("\"A lesson without pain is meaningless. For you cannot gain something without sacrificing something else in return. But once you have recovered it and made it your own... You will gain an irreplaceable Fullmetal heart.\"\n~ Edward Elric (Fullmetal Alchemist)")
    qts.append("\"When do you think people die? When they are shot through the heart by the bullet of a pistol? No. When they are ravaged by an incurable disease? No. When they drink a soup made from a poisonous mushroom!? No! It’s when they are forgotten.\"\n~ Dr Hiluluk (One Piece)")
    qts.append("\"You are already dead.\"\n~ Kenshirou (Fist of the North Star)")
    qts.append("\"If a miracle only happens once, then what is it called the second time?\"\n~ Ichigo Kurosaki (Bleach)")
    qts.append("\"I’m not fighting because I want to win, I’m fighting because I have to win.\"\n~ Ichigo Kurosaki (Bleach)")
    qts.append("\"Look around Eren, at these big ass trees.\"\n~ Levi Ackermen (Attack on Titan)")
    qts.append("\"People die when they are killed.\"\n~ Shiro Emiya (Fate/Stay Night)")
    qts.append("\"This is the magic item that suppresses my mighty magical powers. If I were ever to take this off, a great catastrophe would surely befall this world… Well, that was a lie. I just wear it for looks.\"\n~ Megumin (Konosuba)")
    qts.append("\"WRYYYYYY!\"\n~ DIO (JoJo's Bizarre Adventure)")
    qts.append("\"MUDA MUDA MUDA MUDA MUDAAA!\"\n~ DIO (JoJo's Bizarre Adventure)")
    qts.append("\"In this world, there’s no such thing as 'failure' in the first place. The one who knows the 'ways to win' more than anyone is also the one who’s experienced the most 'mistakes'. In other words… You could say 'failure' is equal to 'success'… Couldn’t you?\"\n~ Toriko (Toriko)")
    qts.append("\"If you can’t do something, then don’t. Focus on what you can do.\"\n~ Shiroe (Log Horizon)")
    qts.append("\"No matter how deep the night, it will always turn to day.\"\n~ Brook (One Piece)")
    qts.append("\"Compared to the \"righteous\" greed of the rulers, the criminals of the world seem much more honorable. When scum rules the world, only more scum is born.\"\n~ Eustass Captain Kid (One Piece)")
    qts.append("\"Stop counting only those things you have lost! What is gone, is gone! So ask yourself this. What is there... that still remains to you?!\"\n~ Jinbei (One Piece)")
    qts.append("\"To true friendship, how long you've known each other means nothing.\"\n~ - Bon Clay")
    qts.append("\"If you lose credibility by just admitting fault, then you didn’t have any in the first place.\"\n~ Fujitora (One Piece)")
    qts.append("\"Fools who don’t respect the past are likely to repeat it.\"\n~ Nico Robin (One Piece)")
    qts.append("\"It doesn’t matter who your parents were. Everyone is a child of the sea.\"\n~ Edward NewGate (One Piece)")
    qts.append("\"If you want to get to know someone, find out what makes them angry.\"\n~ Gon Freecss (HunterXHunter)")
    qts.append("\"You should enjoy the little detours to the fullest. Because that's where you'll find the things more important than what you want.\"\n Ging Freecss (HunterXHunter)")
    qts.append("\"It takes a mere second for treasure to turn to trash.\"\n~ Hisoka (HunterXHunter)")
    qts.append("\"When I say it doesn't hurt me, that means I can bear it.\"\n~ Killua Zoldyck (HunterXHunter)")
    qts.append("\"We cannot go back to the past, no matter how hard we try. No matter how wonderful it was. The past is nothing but the past.\"\n~ Eikichi Onizuka (Great Teacher Onizuka)")
    qts.append("\"A brat who is afraid to be hurt isn't qualified to love someone.\"\n~ Eikichi Onizuka (Great Teacher Onizuka)")
    qts.append("\"Give a kid a smoke and he'll be happy for a day. Teach him how to smoke... he'll be happy for his whole shortened life.\"\n~ Eikichi Onizuka (Great Teacher Onizuka)")
    qts.append("\"Fear is freedom! Subjugation is liberation! Contradiction is truth! Those are the facts of this world! And you will all surrender to them, you pigs in human clothing!\"\n~Satsuki Kiryuuin (Kil la Kill)")
    qts.append("\"You can't judge how beautiful a girl really is by the way she looks.\"\n~Usagi Tsukino (Sailer Moon)")
    qts.append("\"I am the bone of my sword Steel is my body and fire is my blood I have created over a thousand blades Unknown to Death, Nor known to Life Have withstood pain to create many weapons Yet, those hands will never hold anything So as I pray, Unlimited Blade Works.\"\n~ Archer (Fate/stay night:Unlimited Blade Works)")
    qts.append("\"Dreams breathe life into men and can cage them in suffering. Men live and die by their dreams but long after they're abandoned, they still smolder deep in men's hearts.\"\n~ Griffith (Berserk)")
    qts.append("\"Arrogance destroys the footholds of victory.\n~ Byakuya Kuchiki (Bleach)")
    qts.append("\"Those who stand at the top determine what's wrong and what's right! This very place is neutral ground! Justice will prevail, you say? But of course it will! Whoever wins this war becomes justice!\"\n~ Don Quixote Doflamingo (One Piece)")
    qts.append("\"Whatever you lose, you'll find it again. But what you throw away you'll never get back.\"\n~ Kenshin Himura (Rurouni Kenshin: Meiji Kenkaku Romantan)")
    qts.append("\"I am the hope of the universe. I am the answer to all living things that cry out for peace. I am protector of the innocent. I am the light in the darkness. I am truth. Ally to good! Nightmare to you!\"\n~ Son Goku (Dragon Ball Z)")
    qts.append("\"Religion, ideology, resources, land, spite, love or just because… No matter how pathetic the reason, it’s enough to start war. War will never cease to exist… reasons can be thought up after the fact… Human nature pursues strife.\"\n~ Pain (Naruto)")
    qts.append("\"Thinking you’re no-good and worthless is the worst thing you can do\"\n~ Nobito (Doraemon)")
    qts.append("\"When I was a kid, I saw Mona Lisa from my grammar school art book....The fist time I saw her, with her hands on her knee...how do I say this...I had a boner...\"\n~ Yoshikage Kira (JoJo's Bizarre Adventure)")
    qts.append("\"WRYYYYYY!\"\n~ DIO (JoJo's Bizarre Adventure)")
    qts.append("\"Nice watch. Too bad you won't be able to tell the time after I break it. Break your face that is.\"\n~ Jotaro Kujo (JoJo's Bizarre Adventure)")
    qts.append("\"What a beautiful duwang.\"\n~ Yoshikage Kira (JoJo's Bizarre Adventure)")
    qts.append("\"ORA ORA ORA ORA ORA ORA ORA ORA ORA ORA ORA ORA ORA ORA ORA ORA\"\n~ Jotaro Kujo (JoJo's Bizarre Adventure)")
    qts.append("\"Yare Yare Daze\"\n~ Jotaro Kujo (JoJo's Bizarre Adventure)")
    qts.append("\"They say the tongue is the root of all misfortune.\"\n~ Rukia Kuchiki (Bleach)")
    qts.append("\"Death and pain are just a small price to pay for the enjoyment of battle!\"\n~ Kenpachi Zaraki (Bleach)")
    qts.append("\"Fear is necessary for evolution. The fear that could be destroyed at any moment.\"\n~ Sosuke Aizen (Bleach)")
    qts.append("\"I hate perfection. To be perfect is to be unable to improve any further.\"\n~ Kurotsuchi Mayuri (Bleach)")
    qts.append("\"Bang!\"\n~ Spike Spiegel (Cowboy Bebop)")
    qts.append("\"You're gonna carry that weight.\"\n~ EndCard (Cowboy Bebop)")
    qts.append("\"Sometimes questions are complicated, and answers are simple.\n~ L Lawliet (Deathnote)")
    qts.append("\"Time flows constantly, it doesn’t care about the people who are struggling. The World cannot be changed With pretty words alone.\"\n~ Lelouch Lamperouge (Code Geass: Lelouch of the Rebellion)")
    qts.append("\"If you feel yourself hitting up against your limit, remember for what cause you clench your fists! Remember why you started down this path, and let that memory carry you beyond your limit.\"\n~Shimura Nana (My Hero Academia)")
    qts.append("\"A dropout will beat a genius through hard work.\"\n~ Rock Lee (Naruto)")
    qts.append("\"When a man faces fear, his soul is tested. What he was born to seek... what he was born to achieve... his true nature will become clear.\"\n~ Shougo Makishima (Psycho Pass)")
    qts.append("\"Keep the past, for all intents and purposes, where it is.\"\n~ Rintaro Okabe (Steins Gate)")
    qts.append("\"There's a limit to the amount of pleasure a person can obtain. But pleasure brought out by intellect is infinite.\"\n~ Touma Kouzaburou (Psycho Pass)")
    qts.append("\"When you entrust so much of your everyday life to those electronic devices, the argument that you aren't a cyborg isn't very convincing.\"\n~ Toyohisa Senguji (Psycho Pass)")
    qts.append("\"I think the only time people really have value is when they act according to their own will.\"\n~ Shougo Makishima (Psycho Pass)")
    qts.append("\"A perfect plan doesn’t mean having everything go within expectations. A perfect plan is achieved when it has the plasticity needed to flexibly deal with troubles.\"\n~ Shougo Makishima (Psycho Pass)")
    qts.append("\"For a pregnant woman to give birth, she’s gotta feel the pain of pulling a watermelon out of her nostril. For an artist to create a masterpiece, he’s gotta feel the pain of pulling entire galaxies out of his ass.\"\n~ Gintoki Sakata (Gintama)")
    qts.append("\"Now all that is left is the destruction of the earth, but I think it would be a waste to destroy it. The food of this planet is very delicious.\"\n~ Beerus(Dragonball Super)")
    qts.append("\"The ocean is so salty because everyone pees in it.\"\n~ Son Goku (Dragonball Z)")
    qts.append("\"False tears bring pain to others. A false smile brings pain to yourself.\"\n~CC (Code Geass: Lelouch of the Rebellion)")
    qts.append("\"The only ones who should kill are those who are prepared to be killed!\"\n~ Lelouch Lamperouge (Code Geass: Lelouch of the Rebellion)")
    qts.append("\"Humans all behave the same way, like idiots. They all forget that someday, they’re gonna die, so the moment they come face to face with death, they cling to life.\"\n~ Ginti (Death Parade)")
    qts.append("\"Shinichi, upon researching the concept of demons, I believe that, among all life, humans are the closest thing to it. Although humans kill and eat a wide variety of life forms, my kind eat merely one or two kinds at most. We are quite frugal in comparison.\"\n~ Migi (Parasyte the Maxim)")
    qts.append("\"All men are not created equal. This was the reality I learned about society at the young age of four. And that was my first and last setback\"\n~ Midoriya Izuku (My Hero Academia)")
    qts.append("\"Stop pitying yourself.Pity yourself, and life becomes an endless nightmare.\"\n~ Dazai Osamu (Bungo Stray Dogs)")
    qts.append("\"Human Strength exist to be shared with those who are in the depths of despair\"\n~ Nakajima Atsushi (Bungo Stray Dogs)")
    qts.append("\"What did you say? Depending on your answer, I may have to kick your ass!\"\n~ Joseph Joestar (JoJo's Bizarre Adventure)")
    qts.append("\"Arrivederci.\"\n~ Bruno Bucciarati (JoJo's Bizarre Adventure)")
    qts.append("\"He's... mocking me! But Jotaro,. Leaving a bad taste in your mouth, or living your life without regrets. That reasoning is as compelling as rat shit in the bathroom and it will be your demise! I, Dio, have no such thoughts. Within my mind but one simple thought. Just one! To be victorious and rule! That is all. That is all I need to feel satisfaction! How I do it doesn't matter!\"\n~ Dio Brando (Jojo's Bizarre Adventure)")
    random.shuffle(qts)
    quote = qts[randint(0,len(qts)-1)]
    quote_arr = quote.split("~")
    e= discord.Embed(title="!quote",
    description=quote_arr[0],
    color=0X00D2DC)

    e.set_footer(icon_url='https://i.imgur.com/03Y0GUM.png',text=quote_arr[1])
    await ctx.send(embed= e)


bot.run('token')
