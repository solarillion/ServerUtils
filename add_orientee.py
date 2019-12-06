# Author: Nanda H Krishna (https://github.com/nandahkrishna)
# Use this program to add orientees to the Hyouka and TARS Firebase databases

import datetime
import pyrebase
import slack
from credentials import *

print("Name: ", end="")
name = input()
print("Email: ", end="")
email = input()
print("GitHub: ", end="")
github = input()
print("Group: ", end="")
group = input()

tars = slack.WebClient(keys["slack"])
users = tars.users_list().data["members"]
slack_id = ""

for member in members:
	if member["is_bot"]:
		pass
	elif member["profile"]["email"] == email:
		slack_id = member["id"]

print("Slack ID: " + slack_id)

tars_fb_config = {
  "apiKey": keys["tars_fb_key"],
  "authDomain": keys["tars_fb_ad"],
  "databaseURL": keys["tars_fb_url"],
  "storageBucket": keys["tars_fb_sb"]
}
tars_fb = pyrebase.initialize_app(tars_fb_config)

hyouka_fb_config = {
  "apiKey": keys["hyouka_fb_key"],
  "authDomain": keys["hyouka_fb_ad"],
  "databaseURL": keys["hyouka_fb_url"],
  "storageBucket": keys["hyouka_fb_sb"]
}
hyouka_fb = pyrebase.initialize_app(hyouka_fb_config)

join = datetime.date.today()

tars_db = tars_fb.database()
tars_db.child("orientee").child(slack_id).update({"name": name, "github": github, "group": group, "join": join, "progress": "py1", "py_fin": "None", "g_fin": "None", "p_fin": "None"})
hyouka_db = hyouka_fb.database()
hyouka_db.child(github).update({"name": name, "group": group, "progress": "py1", "slack": slack_id})

print("Added " + name + " to the databases.")
