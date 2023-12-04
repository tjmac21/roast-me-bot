import discord
from discord.ext import commands
import os
import openai
import requests
from random import randrange
from dotenv import load_dotenv

load_dotenv()
D_TOKEN = os.getenv('DISCORD_CLIENT_TOKEN')
O_TOKEN = os.getenv('OPEN_AI_API_KEY')
E_TOKEN = os.getenv('ELEVEN_LABS_KEY')

client = openai.OpenAI(api_key=O_TOKEN)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

audio_file_name = "boom_torched.mp3"

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
        'goofy': 'shitty',
        'Frick': 'Fuck',
        'Friggin': 'Fuckin',
        'Frig': 'Fuck',
        'Goofball': 'Dumbass',
        'Goofballs': 'Dumbasses',
        'Goof ball': 'Dumbass',
        'Goof balls': 'Dumbasses',
        'Little turd': 'Shit head',
        'Goofy': 'Shitty',
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text

def describe_image(image, voice):
    print(voice['name'])
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

    return response.choices[0].message.content

async def generate_speech(text, voice):
    print(f"Start: Generating Speech with voice {voice['name']}")

    options = {
        'headers': {
            'Content-Type': 'application/json',
            'xi-api-key': E_TOKEN,
        },
        'json': {
            'model_id': 'eleven_multilingual_v2',
            'text': text,
            'voice_settings': {
                'similarity_boost': 0.75,
                'stability': 0.3,
                'use_speaker_boost': False,
                'style': 0.65,
            },
        }
    }

    response = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{voice['id']}/stream", **options)
    response.raise_for_status()
    print(f"Got audio")

    with open(audio_file_name, "wb") as file:
        for chunk in response.iter_content(chunk_size=128):
            file.write(chunk)

def on_completion():
    print("Thread has completed its work.")

sys_text = 'You poke fun at the person in this photo. Make it short. Do not insert any new line characters no matter what'
user_text = 'Describe this photo of a person. Go into detail about 3 features and exaggerate. Be snarky and funny. Use "goof ball", "Frickin", "little turd" and "Frig off" a lot."'
prompts = {
    '0': {
        'name': 'Deadpool',
        'id': 'f0TRKXA9OQ8ILrnmF1fm',
        'system': f'You are Deadpool from the marvel universe. {sys_text}',
        'user': user_text,
    },
    '1': {
        'name': 'Ricky',
        'id': '3qZDRKqCY8ll5KNyyLRl',
        'system': f'You are Ricky from the Trailer Park Boys. {sys_text}',
        'user': user_text,
    },
    '2': {
        'name': 'JBP',
        'id': 'V9nC7Bqw4GjxaBTsMm6m',
        'system': f'You are acclaimed psychologist Jordan Peterson. {sys_text}',
        'user': user_text,
    },
    '3': {
        'name': 'Timmy',
        'id': '6ptjZxFVHXmWyqnKfkKc',
        'system': f'You are Tim Robinsons from I Think You Should Leave. {sys_text}',
        'user': user_text,
    },
    '4': {
        'name': 'Carr',
        'id': 'sZgZtQg2GC6Pm2H4sCL2',
        'system': f'You are acclaimed standup Jimmy Carr. {sys_text}',
        'user': user_text,
    },
    '5': {
        'name': 'Regina',
        'id': 'iDiQQSQMZh66NJzRZeoB',
        'system': f'You are Regina George from Mean Girls. {sys_text}',
        'user': user_text,
    },
}

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='roast', help='Torchin\' your a$$ mfer 😈😈😈')
async def roast(ctx):
    try:
        attachment=ctx.message.attachments[0]
    except Exception as e:
        await ctx.reply("Please upload with an image")
        return
    
    image_url = str(attachment.url)
    voice_prompt = prompts[str(randrange(0, 6))]

    retries = 0
    max_retries = 2
    while retries < max_retries:
        description = describe_image(image_url, voice_prompt)
        retries = retries + 1
        if not description.startswith('I\'m sorry') and not description.startswith('Mesa sorry') and not description.startswith('Sorry'):
            break
        voice_prompt = prompts[str(randrange(0, 6))]

    print('Description\n')
    print(str(description))

    if not description:
        await ctx.reply("No description")
        return
    
    if description.startswith('I\'m sorry') or description.startswith('Mesa sorry') or description.startswith('Sorry'):
        await ctx.reply(f"{description} Please try again.")
        return

    massaged_text = massage_text(description)
    await generate_speech(massaged_text, voice_prompt)
    await ctx.reply(massaged_text, file=discord.File(audio_file_name), mention_author=False)

bot.run(D_TOKEN)