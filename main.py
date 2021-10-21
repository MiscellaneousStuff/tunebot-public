from discord.ext.commands.errors import CommandInvokeError
from youtubesearchpython import VideosSearch
import os

import discord
from discord.ext.commands import bot
from discord.ext import commands
from dotenv import load_dotenv

from youtube_dl import YoutubeDL

def get_id(url):
    url = url.split("=")
    url = url[1]
    return url

def get_url(query):
    videosSearch = VideosSearch(query, limit = 1)
    results = videosSearch.result()
    results = results["result"]
    link = results[0]["link"]
    return link

def vid_exists(vid_id):
    if os.path.exists(f"./{vid_id}.mp3"):
        return True
    else:
        return False

def download_vid(url, vid_id):
    os.system(f'youtube-dl --extract-audio --audio-format mp3 {url} --output "{vid_id}.%(ext)s"')

bot = commands.Bot(command_prefix="!")


class TuneBot(commands.Cog):

    def __init__(self, guild, rythm_channel_id, voice_id):
        self.guild = guild
        self.rythm_channel_id = int(rythm_channel_id)
        self.voice_id = int(voice_id)
        self.voice = None
        self.song_queue = []
        self.cur_song_info = None
        super(TuneBot, self).__init__()

    async def on_ready(self):      
        for guild in self.guilds:
            if guild.name == self.guild:
                break
            print(
                f'{self.user} is connected to the following guild:\n'
                f'{guild.name}(id: {guild.id})'
            )

        rythm_channel = self.get_channel(self.rythm_channel_id)
        await rythm_channel.send(f"{self.user} joined to play music.")        

    @commands.command(pass_context=True)
    async def pause(self, ctx):
        channel = bot.get_channel(self.rythm_channel_id)
        if self.voice.is_playing():
            self.voice.pause()
            await channel.send(f'Pausing: {self.cur_song_info["title"]}')
    
    @commands.command(pass_context=True)
    async def resume(self, ctx):
        if self.voice.is_paused():
            self.voice.resume()
            await channel.send(f'Resuming: {self.cur_song_info["title"]}')

    @commands.command(pass_context=True)
    async def queue(self, ctx):
        channel = bot.get_channel(self.rythm_channel_id)
        await channel.send(self.song_queue)

    async def handle_connection(self):
        # Handle disconnected
        channel = bot.get_channel(self.voice_id)
        voice = discord.utils.get(bot.voice_clients, guild=self.guild)
        print('handle conn:', channel, voice, bot.voice_clients)

        # Connect to voice channel
        try:
            if not voice is None:
                if not voice.is_connected():
                    voice = await channel.connect()
            else:
                voice = await channel.connect()
            self.voice = voice
        except Exception as e:
            print('Err:', e)

        return channel, voice

    @commands.command(pass_context=True)
    async def clear(self, ctx):
        self.song_queue = []

    @commands.command(pass_context=True)
    async def play(self, ctx, *args):
        # Handle currently playing music
        if self.voice:
            if self.voice.is_playing():
                self.voice.stop()

        # Handle connection issues
        await self.handle_connection()

        # Get query
        query = " ".join(args)

        # Download video from YouTube
        url = get_url(query)
        vid_id = get_id(url)
        print(f'vid_exists({vid_id}):', vid_exists(vid_id))
        if not vid_exists(vid_id):
            download_vid(url, vid_id)

        # Print YouTube URL and YouTube Video ID
        print(url, vid_id)

        # Get audio source
        src = f"./{vid_id}.mp3"
        audio_source = discord.FFmpegPCMAudio(src)

        # Play music
        if self.voice:
            if not self.voice.is_playing():
                self.voice.play(audio_source, after=None)

        channel = bot.get_channel(self.rythm_channel_id)

        # Print video information
        with YoutubeDL({}) as ydl:

            info_dict = ydl.extract_info(url, download=False)
            video_title = info_dict.get('title', None)
            video_url = info_dict.get("url", None)
            self.cur_song_info = {
                "title": video_title,
                "url": video_url
            }
            await channel.send(f'Playing {self.cur_song_info["title"]}')

if __name__ == "__main__":
    # args = parser.parse_args()

    load_dotenv()
    TOKEN      = os.getenv('DISCORD_TOKEN')
    GUILD      = os.getenv('DISCORD_GUILD')
    CHANNEL_ID = os.getenv('DISCORD_RYTHM_CHANNEL_ID')
    VOICE_ID   = os.getenv('DISCORD_RYTHM_VOICE_ID')

    bot.add_cog(TuneBot(GUILD, CHANNEL_ID, VOICE_ID))
    bot.run(TOKEN)