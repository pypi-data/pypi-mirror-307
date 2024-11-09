# asmek-authcogs

Alliance Auth cogs for Astrum Mechanica
This is built to replace some functionality of some of the *AA-Discordbot* as well as add other features.
This will not work without <https://apps.allianceauth.org/apps/detail/allianceauth-discordbot> installed!

> **Warning**
> This is built for ASMEK specifically. **If you aren't us, you probably shouldn't use this. There will be no warning of updates or changes!**
> However it is slowly being modified to contain less hardcoded values so personal use isn't off the table.

## Current cogs

| Cog     | Description                                                                                                                 |
| ------- | --------------------------------------------------------------------------------------------------------------------------- |
| `about` | about the authbot                                                                                                           |
| `auth`  | links to various areas in the auth(*HARDCODED* to specific areas and some statements, should tie them to installed modules) |
| `links` | links to various useful sites, cuz we forget them all the time.                                                             |
| `hr`    | thread based recuritment. Various commands to sync characters                                                               |
| `siege` | region status alert indicator thing!                                                                                        |

## Future cogs and features

| Cog           | Purpose                                                                                  |
| ------------- | ---------------------------------------------------------------------------------------- |
| `price check` | price check in trade hubs and null hubs. base discord bot cog only checks jita and amarr |

- Incorporate adming page access
- move recruit messages to database
- perms for HR cog??

## Install

- Ensure you have installed and configured the Alliance Auth DiscordBot, <https://apps.allianceauth.org/apps/detail/allianceauth-discordbot>
- Install the app with your venv active

```bash
pip install asmek-authcogs
```

- Add `'asmek_authcogs',` to your INSTALLED_APPS list in local.py.
- Add the below lines to your `local.py` settings file, adjust for which cogs you want. Settings for specific cogs are found in cog setup.

```python
## Settings for Asmek Authcogs
ASMEK_AUTHCOGS_COGS = [
    "asmek_authcogs.cogs.about",  # make sure to remove the about cog from aadiscordbot if using this
    "asmek_authcogs.cogs.auth",
    "asmek_authcogs.cogs.links",
    "asmek_authcogs.cogs.siege",
    "asmek_authcogs.cogs.hr",
]
```

- Run migrations `python manage.py migrate`
- Gather your static files `python manage.py collectstatic` (There should be none from this app)
- Restart your auth

## Cog setup and usage

### About Cog

Accessed using `/about`

- Add the below lines to your `local.py` settings file, adjusting for your usage.

```python
ASMEK_BOT_NAME = "ASMEK Authbot: The Omnissiah"  # name to show up in about
ASMEK_BOT_DESCRIPTION = "Some spooky watching you description"  # description for about
```

All settings are currently hardcoded

### Auth Cog

- Add the below lines to your `local.py` settings file, adjusting for your usage.

```python
ASMEK_ALLIANCE_ID = "123"
ASMEK_ALLIANCE_NAME = "alliance name"
ASMEK_ALLIANCE_URL = "alliance url"
```

Those will create the link for `/auth alliance`
Accessed using `/auth` followed by one of the below
Hardcoded links:
Audit - Character audit (not member audit)
Buyback - The buyback module
Fittings - The fittings Module
Home - Do i really need to explain??
Wiki - The simplewiki module ( NOT WIKIJS)

> This cog still needs some work to make it more customizable and generate links based on individual setups

### Links Cog

A group needs to be given the `link.manage_links` perm in order to manage links
This cog conatins 2 seperate commands
`/links` is used to manage links, and `/link` is used to display a link

/Links
Add - you will be brought to a pop up to add a name, url, description, and optional image for a link
Edit - you will be brought to a popup to edit a link (current links will populate in menu)
Delete - you will be asked to delete a link (current links will populate in menu)
List - will list all current links

/Link
will generate a list of all your links and upon making a selection will return the information

### HR Cog

Recruit channel, corp roleid, hr roleid, and recruit msg 1 are all required!
Additional recruit messages are optional and technically unlimited.
Messages below are what asmek uses as an example, a few points to note when modifying.

- the 2 pairs of {} in msg 1 are mandatory. The first set is to ping the recruit, the second set is to ping the HR team, in order to pull them into the thread.

- the messages must be enclosed in quotes ""

- `\n` is used for line breaks

- Discord formatting can be added

- Add the below lines to your `local.py` settings file, adjusting for your usage.

```python
ASMEK_RECRUIT_CHANNEL = "123"
ASMEK_CORP_ROLEID = "123"
ASMEK_HR_ROLEID = "123"
ASMEK_RECRUIT_MSG_1 = "Welcome {}! \n\nThis is your private thread for moving through the recruitment process with Astrum Mechanica. We are excited to have you here! \n\nThe {} is here and can assist with any questions you may have during the process.\n\nA few important points to note before you continue with the application process:\n- We are apart of the LAWN alliance and a member of the IMPERIUM coalition\n- A full ESI caracter audit needs to be completed for **ALL** of your toons\n- A voice interview must be completed as part of the application process\n- You must be able to communicate via voice comms\n- We have a **2 Million** skill point minimum\n- We do not have a specialty, we participate in all aspects of EVE\n\nIf you wish to continue with your application, please follow the instructions below!\n\n****Step 1 - Login to Auth:****\n1) Proceed to <https://asmek.space>\n2) Login using your **MAIN** character\n3) Enter your email address\n\nYou should now be on the main dashboard page.\n\n Click the :white_check_mark: below to continue to step 2 of 4."
ASMEK_RECRUIT_MSG_2 = "****Step 2 - Register Characters & ESI Tokens:****\n1) Click on **Character Audit** on the left-hand menu.\n2) Click on the **Blue +** in the top right corner\n3) Login and allow the requested token\n4) Repeat step #3 for **ALL** of your characters\n5) Once you have completed step #4, if any characters are yellow push the green refresh icon in the top right corner.\n\nYou should now see all of your characters displayed as green and the various navigation areas will populate with your information.\n\n Click the :white_check_mark: below to continue to step 3 of 4."
ASMEK_RECRUIT_MSG_3 = "****Step 3 - Link your Auth and Discord accounts:****\n1) Click on **Services** on the left-hand menu.\n2) On the **Discord** row that is displayed, click the chekmark button under **Action**.\n3) If you're not already logged into Discord in your browser,you'll be asked to log in.\n4) Once logged in, you'll be presented with a screen asking you to authorize ASMEK Authbot to have limited access to your Discord account. Click **Authorize**.\n\nOnce that's done, your Auth and Discord acounts should be fully linked.\n\n Click the :white_check_mark: below to continue to step 4 of 4."
ASMEK_RECRUIT_MSG_4 = "****Step 4 - Fill out an application:****\n1) Click on **Applications** on the left-hand menu.\n2)Click **Create Application** in the top right of the page.\n3) Click the **Astrum Mechanica** button in the middle of the page.\n4) Answer the questions contained in the application, then click **Submit** at the bottom of the page.\n\n When done, click the :white_check_mark: below."
ASMEK_RECRUIT_MSG_5 = "**Thank you for considering joining us and submitting your application!\n\nThe HR team has been alerted of your completed application, and should review it shortly. Please allow atleast **24 hours** for someone to look over your application and submitted characters. If there are any questions or concerns, someone will reach out to you in this thread.\n\nThe HR team will reach out to schedule an interview, if they choose to continue your application."
```

### Siege Cog

- Add the below lines to your `local.py` settings file, adjusting for your usage.

```python
ASMEK_SIEGE_CHANNEL = "123"  # channel for siege status
```

- The channel used for this should have permission set for no typing only viewing. You might have to set this from server owner.
- The channel should be completely empty with no existing chat.

You can change the status, along with the channel name, by typing `/siege` in any channel and choosing a corresponding colour(not color). It also includes preset messages but you can optionally type in a message as well(ie 30 man gang!).
We have this set as a role all on its own and give it out as needed.
In general the images are self explanatory, however we keep the beehive information partially opsec. See brackets below for how we explain it to general line members.
Recommended usage for imperium:

- Green: Beehive is up! All caps can be out. (General line members: you are as safe as humanly possible)
- Amber: Beehive is down! Only rorqs should be out. (General line members: its nullsec pay attention)
- Red: Everyone should dock up! (General line members: dock the fuck up!)

## Settings (local.py)

| Setting                 | Default | Description                                                                                                                                                               |
| ----------------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ASMEK_ALLIANCE_ID`     |         | alliance id                                                                                                                                                               |
| `ASMEK_ALLIANCE_NAME`   |         | alliance name to display on embeds                                                                                                                                        |
| `ASMEK_ALLIANCE_URL`    |         | URL for alliances auth system                                                                                                                                             |
| `ASMEK_SIEGE_CHANNEL`   |         | Discord channel id for siege alerts                                                                                                                                       |
| `ASMEK_RECRUIT_CHANNEL` |         | Discord channel id for recruitment threads                                                                                                                                |
| `ASMEK_CORP_ROLEID`     |         | Discord Role id for corp members, this prevents members from trying to apply (Should preferably be the 'members' role)                                                    |
| `ASMEK_HR_ROLEID`       |         | Discord Role id for HR team, or the role to ping for recruits and also who can use the HR commands(not sure why i don't have the ability to use it tied to perms but meh) |
| `ASMEK_RECRUIT_MSG_1`   |         | The first message to send in the private thread. **REQUIRED**                                                                                                             |
| `ASMEK_RECRUIT_MSG_#`   |         | Additional message to send upon clicking the check mark. Sequentially numbered.                                                                                           |

## Permissions

| Perm                  | Description                       |
| --------------------- | --------------------------------- |
| link.manage_links     | Can manage links in the links cog |
| general.siege_control | Can use siege commands            |
