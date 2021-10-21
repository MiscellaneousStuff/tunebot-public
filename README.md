# Tunebot

## About

Rhythm bot clone for discord written in Python and uses YouTube to get
media files.

## Usage

You need a `.env` file within the same directory as `main.py` to use
this script. The `.env` file needs the following format.

```
DISCORD_TOKEN=THIS_IS_THE_API_FROM_THE_DISCORD_BOT_DEV_PAGE
DISCORD_GUILD=REPLACE_THIS_WITH_DISCORD_SERVER_NAME
DISCORD_RYTHM_CHANNEL_ID=REPLACE_THIS_WITH_CHANNEL_ID_TO_SEND_STATUS_UPDATES
DISCORD_RYTHM_VOICE_ID=REPLACE_THIS_WITH_VOICE_CHANNEL_TO_PLAY_SONGS
```

## Commands

```
!play <query> - Searches youtube using the query and plays the top result
!resume - Resumes playing of the video if it has been paused
!stop - Stops playing the video
!pause - Pauses the video, can be resumed later
```