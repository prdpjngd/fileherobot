![​](https://telegra.ph/file/fbbf4413766a980126baa.jpg)
#  FileHeroBot - Telegram Bot 🤖

This a drive url shortener used to hide your original file ID and share with your friends. Powered by your google Drive API.

## Installing

### 1.  Simple Method 

STEP 1: Press 👉🏻 [![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)
STEP 2: get You App credentials from https://my.telegram.org/auth
STEP 3: put variable value in the heroku env. variables.
STEP 4: Boom!.... your done!


### 2. Legacy Way
Simply clone the repository and run the main file:

STEP 1:
```sh
git clone https://github.com/prdpjngd/fileherobot.git
cd fileherobot
virtualenv -p /usr/bin/python3 venv
source venv/bin/activate
pip install -r requirements.txt
```
STEP 2: Get You App credentials from https://my.telegram.org/auth 
STEP 3: Put your API ID & API HASH in Creds.py file.
STEP 4: Paste Your Bot Token In Creds.py 
STEP 5: Boom your Done... 


### How to get your  API ID & API HASH from https://my.telegram.org/auth 👇
```
STEP 1: Login with Your number in international format
STEP 2: Create App & copy API ID & API Hash of your app.
STEP 3: Go to Bot Father in telegram  and create a bot 
STEP 4: Generate Bot token and copy to creds.py file.
```

### Variable Explanations ---> these are Mandatory Variables

* `TG_BOT_TOKEN`: Telegram bot token , get from Botfather
* `API_ID`: APP API_ID get this from my.telegram.org
* `API_HASH`: APP API_HASH get this from my.telegram.org
