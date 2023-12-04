import discord
from discord.ext import commands
import os
import openai
from random import randrange
from dotenv import load_dotenv

load_dotenv()
D_TOKEN = os.getenv('DISCORD_CLIENT_TOKEN')
O_TOKEN = os.getenv('OPEN_AI_API_KEY')

client = openai.OpenAI(api_key=O_TOKEN)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)


def massage_text(text):
    replacements = {
        ',': '',
        'frick': 'fuck',
        'friggin': 'fuckin',
        'frig': 'fuck',
        'goofball': 'dumbass',
        'goofballs': 'dumbasses',
        'goof ball': 'dumbass',
        'goof balls': 'dumbasses',
        'little turd': 'shit head',
        'Frick': 'Fuck',
        'Friggin': 'Fuckin',
        'Frig': 'Fuck',
        'Goofball': 'Dumbass',
        'Goofballs': 'Dumbasses',
        'Goof ball': 'Dumbass',
        'Goof balls': 'Dumbasses',
        'little turd': 'shit head'
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text

def describe_image(image, voice):
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        max_tokens=100,
        messages=[
            {
                "role": "system",
                "content": voice['system'],
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": voice['user'],
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image,
                        },
                    },
                ],
            },
        ]
    )
    print("Chat Completion")
    print(response.choices[0])

    return response.choices[0].message.content

prompts = {
    '0': {
        'name': 'Deadpool',
        'id': '5pOjOeJ82iGHKnqIMFHV',
        'system': 'You are Deadpool from the marvel universe. You poke fun at the person in this photo. Make it short.',
        'user': 'Describe this photo of a person. Go into detail about 3 features and exaggerate. Be snarky and funny. Use "goof ball", "Frickin", "little turd" and "Frig off" a lot."',
    },
    '1': {
        'name': 'Ricky',
        'id': '5pOjOeJ82iGHKnqIfFHV',
        'system': 'You are Ricky from the Trailer Park Boys. You poke fun at the person in this photo. Make it short.',
        'user': 'Describe this photo of a person. Go into detail about 3 features and exaggerate. Be snarky and funny. Use "goof ball", "Frickin", "little turd" and "Frig off" a lot."',
    },
    '2': {
        'name': 'Cartman',
        'id': '5rOjOeJ82iGHKnqIfFHV',
        'system': 'You are Eric Cartman from South Park. You poke fun at the person in this photo. Make it short.',
        'user': 'Describe this photo of a person. Go into detail about 3 features and exaggerate. Be snarky and funny. Use "goof ball", "Frickin", "little turd" and "Frig off" a lot."',
    },
    '3': {
        'name': 'Dangerfield',
        'id': '6rOjOeJ82iGHKnqIfFHV',
        'system': 'You are acclaimed standup Rodney Dangerfield. You poke fun at the person in this photo. Make it short.',
        'user': 'Describe this photo of a person. Go into detail about 3 features and exaggerate. Be snarky and funny. Use "goof ball", "Frickin", "little turd" and "Frig off" a lot."',
    },
    '4': {
        'name': 'Carr',
        'id': '6rOjOeJ82iGHKnqIfFHV',
        'system': 'You are acclaimed standup Jimmy Carr. You poke fun at the person in this photo. Make it short.',
        'user': 'Describe this photo of a person. Go into detail about 3 features and exaggerate. Be snarky and funny. Use "goof ball", "Frickin", "little turd" and "Frig off" a lot."',
    },
    '5': {
        'name': 'regina',
        'id': '6rOjOeJ82iGHKnqIfFHV',
        'system': 'You are Regina George from Mean Girls. You poke fun at the person in this photo. Make it short.',
        'user': 'Describe this photo of a person. Go into detail about 3 features and exaggerate. Be snarky and funny. Use "goof ball", "Frickin", "little turd" and "Frig off" a lot."',
    },
}

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='roast', help='Torchin\' your a$$ mfer 😈😈😈')
async def roast(ctx):
    try:
        attachment=ctx.message.attachments[0]
        image_url = str(attachment.url)
        voice_prompt = prompts[str(randrange(0, 6))]
        description = describe_image(image_url, voice_prompt)
        print('Description\n')
        print(str(description))
        if not description:
            raise Exception('No description')

        massaged_text = massage_text(description)
        await ctx.send(massaged_text, tts=True)
    except Exception as e:
        await ctx.send("Please upload with an image")

bot.run(D_TOKEN)