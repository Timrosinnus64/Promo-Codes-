# Promo Code for Dexes
Here is a code that allows to add promo codes to the dexes

## Installation Guide
This is the guide on how to install Promo Codes into your own dex :D

### Step 1 Make a Folder
In Ballsdex/packages create a folder titled "promocode"

### Step 2 Download the files
Download the ```cog.py``` and ```__init.py__``` files and post them in the promocode file

### Step 3 Load them to the bot
For the newer version of the dex (2.22.0 and beyond):
1. Locate config.yml
2. Post "ballsdex/packages/promocode
3. Save the file
For the Older versions (Below 2.22.0):
1. Locate "bot.py" file in ballsdex/core
2. Put "promocode: in:
   ```py
   PACKAGES = ["config", "players", "countryballs", "info", "admin", "trade", "balls"]
   ```
It should look like this:
   ```py
   PACKAGES = ["config", "players", "countryballs", "info", "admin", "trade", "balls", "promocode"]
   ```
3. Save the file

Now only think left is doing ```docker compose down``` and ```docker compose up``` or ```docker compose up -d```

Enjoy!

## Small Guide on adding Promo Codes
```promo_codes``` - This is where you add your promo codes

Y - year

M - Month

D - Day
demonstration:
```py
promo_codes = {
     "YOURPROMOCODEHERE":{"country": "COLLECTIBLENAMEHERE",
                          "expires": datetime(Y, M, D,),
                         }
}
```

## Support
If you see any flaws or bugs or want to contribute, contact me through discord or open an [GitHub repository](https://github.com/Timrosinnus64/Promo-Codes).
