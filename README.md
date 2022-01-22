# Telegram-wallpaper-bot
Bot for downloading pictures from sites and publishing them in telegram channels.

Create bot only to Russian with using library the pyTelegramBotAPI. Processing images work with using library the PIL. Also have program functions created me.
In the near future I want to develop a user-friendly interface for using the bot.

# Fast start

1. Download repository <br>
`git clone https://github.com/Karabok-coder/Telegram-wallpaper-bot.git`
2. Navigate to the directory <br>
`cd Telegram-wallpaper-bot`
3. Start main.py <br>
`python main.py`
<br>

In folder with main.py open <b>"constants.py"</b> and change <b>"token"</b> from you.
Him need get from <b>@BotFather</b> in the Telegram.

Code woking to Python 3.9 and to  latest version libraries on the times 2022.01.21.

# Libraries
<b>PIL</b> - pip install Pillow <br>
<b>glob</b> - pip install glob2 <br>
<b>re</b> - standart librari Python <br>
<b>telebot</b> - pip install pyTelegramBotAPI <br>
<b>types</b> - standart librari Python <br>
<b>requests</b> - pip install requests <br>
<b>beautifulsoup</b> - pip install beautifulsoup4 <br>

# Folders
"config" - in him data to output stats bot. <br>
"download_photo" - need for download photo which how document (without compression) to bot. <br>
"electronic" - two photos devices for edit images. <br>
"photos" - saved download photos.<br>
"processed_photo" - seved processed photo.<br>

# Files in "config" 
"Number Page" - numbers downloads pages from sites. <br>
"Stats" - stores data about successful downloads file and not successful downloads file and like, dislike photo. <br>
"IDPhotoNow" - stores data about id photo which need set in name photo, at downloads photos (at saved photos in a folder - "photos").<br>
"IDPhotoChannel" - stores number about photo which set in name photo, at a send in channel. <br>
"Channel Target" - stores number channel where sended photos. <br>
