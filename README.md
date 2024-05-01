# mr-renamerbot

<p align="center">
  <a href="https://github.com/Akshay-code-space/mr-renamerbot/stargazers">
    <img src="https://img.shields.io/github.com/Akshay-code-space/mr-renamerbot?style=social">
  </a>
  <a href="https://github.com/Akshay-code-space/mr-renamerbot/fork">
    <img src="https://img.shields.io/github.com/Akshay-code-space/mr-renamerbot?label=Fork&style=social">
  </a>
</p>

## Overview

This is a multi-purpose Telegram bot that provides various functionalities including:

- Renaming Telegram files into different formats
- Converting files into video format
- Supporting custom captions and permanent thumbnails
- Enforcing subscription to a targeted chat

## Deploy

### Heroku

You can easily deploy the bot to Heroku by clicking the button below:

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://github.com/Akshay-code-space/mr-renamerbot)

### Local Server

To deploy the bot on your own server, follow these steps:

1. Clone this repository to your local machine.
2. Install the required dependencies by running `pip install -r requirements.txt`.
3. Obtain the following credentials:
   - `TG_BOT_TOKEN`: Your Bot Token obtained from [@BotFather](https://t.me/botfather).
   - `UPDATE_CHANNEL`: A channel username (without @) used for ForceSubscribe.
   - `APP_ID` and `API_HASH`: Obtain these from [Telegram's website](http://www.my.telegram.org) or [@UseTGXBot](http://www.telegram.dog/UseTGXBot).
4. Set up these credentials in your environment variables or directly in the code.
5. Run the bot script using `python main.py`.

## Support

For any issues or questions related to the bot, feel free to open an issue on GitHub or reach out to the maintainer.

