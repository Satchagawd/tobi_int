import requests
import os
import warnings
from datetime import datetime
warnings.filterwarnings('ignore')
        

#### Variables ####
api_key = "RGAPI-74a8d7fe-ee9d-4c42-9d70-561f1f727068"
gameName = "Schadra"
tagLine = "EUW"

#### GET_PUUID ####
r = requests.get(f"https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}?api_key={api_key}", verify=False)
data = r.json()
puuid = data["puuid"]

#### GET_MATCHES ####
e = requests.get(f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=20&api_key={api_key}", verify=False)
matchids = e.json()

matchcollection = []
need_check = []

#### CHECK IF NEW MATCHES ####
try:
    with open(os.path.dirname(__file__) + (f"/matchids{gameName}.txt"),"r", encoding='utf-8') as file:
        for line in file:
            matchcollection.append(line.strip())
except FileNotFoundError:
    with open(os.path.dirname(__file__) + (f"/matchids{gameName}.txt"),"w+", encoding='utf-8') as file:
        file.write("\n")
    
with open(os.path.dirname(__file__) + (f"/matchids{gameName}.txt"),"a+", encoding='utf-8') as file:        
    for entry in matchids:
        if entry not in matchcollection:
            need_check.append(entry)
            file.write("\n")
            file.write(entry)
if len(need_check) == 0:
    with open(os.path.dirname(__file__) + "/log.txt", "a+") as file:
        file.write("\n")
        file.write("No NEW matches... going to sleep again")
        file.write("   Timestamp: ")
        file.write(str(datetime.now()))
    print("No NEW matches... going to sleep again")
else:
    print("NEW MATCHES:")

def match_get_data(id,gameName):
    matchr = requests.get(f"https://europe.api.riotgames.com/lol/match/v5/matches/{id}?api_key={api_key}", verify=False)
    matchdata = matchr.json()
    datapool = matchdata["info"]
    participants = datapool["participants"]
    gamemode = datapool["gameMode"]
    names = {}
    i = 0
    for entry in participants:
        if "riotIdGameName" in entry:
            names[entry["riotIdGameName"]] = i
            i += 1

    name_number = names[gameName]

    total_dd = participants[name_number]["totalDamageDealtToChampions"]
    total_dt = participants[name_number]["totalDamageTaken"]
    if participants[name_number]["win"] == True:
        win = "won"
    else:
        win = "lost"
    if participants[name_number]["win"] == True:
        msg = ":clap: :clap: :tada:"
    else:
        msg = ":rage: :rage: :rage:"

    #s_name = participants[name_number]["summonerName"]
    rid_name = participants[name_number]["riotIdGameName"]
    total_k = participants[name_number]["kills"]
    total_d = participants[name_number]["deaths"]
    gold = participants[name_number]["goldEarned"]
    champ = participants[name_number]["championName"]
    role = participants[name_number]["role"]
    pen = participants[name_number]["pentaKills"]
    time_played = participants[name_number]["timePlayed"]
    assists = participants[name_number]["assists"]
    if pen > 0:
        penta = (f"  :fire: :fire: :fire: PEEEEENNTTAAAAAKKIIIIILL :fire: :fire: :fire:  ({pen})")
    else: penta = ""

    returnstring = (f"{rid_name} played a {gamemode} on {champ} as {role} and {win} with {total_k} Kills :fist:, {total_d} Deaths :skull: and {assists} Assists :family: after {int(time_played/60)} min. Total Damage Dealt: {total_dd} Damage Taken: {total_dt} Gold earned: {gold}:coin:. {msg}!!!{penta}")
    """
    try:
        with open(os.path.dirname(__file__) + "/log.txt", "w+") as file:
            for entry in participants[name_number]:
                file.write(entry)
                file.write("      :     ")
                file.write(str(participants[name_number][entry]))
                file.write("\n")
    except UnicodeEncodeError:
        pass
    """
    ###########werid test####
    """
    for i in range(0, len(list(names))):
        try:
            with open(os.path.dirname(__file__) + "/testdata.txt", "a+") as file:
                    file.write("\n")
                    file.write("\n")
                    file.write("\n")
                    file.write("riotIdGameName")
                    file.write("\n")
                    file.write(str(participants[i]["riotIdGameName"]))
                    file.write("\n")
                    file.write("kills")
                    file.write("\n")
                    file.write(str(participants[i]["kills"]))
                    file.write("\n")
                    file.write("D-Dealt")
                    file.write("\n")
                    file.write(str(participants[i]["totalDamageDealtToChampions"]))
                    file.write("\n")
                    file.write("D-Taken")
                    file.write("\n")
                    file.write(str(participants[i]["totalDamageTaken"]))
                    file.write("\n")
                    file.write("deaths")
                    file.write("\n")
                    file.write(str(participants[i]["deaths"]))
                    file.write("\n")
                    file.write("goldEarned")
                    file.write("\n")
                    file.write(str(participants[i]["goldEarned"]))
                    file.write("\n")
                    file.write("championName")
                    file.write("\n")
                    file.write(str(participants[i]["championName"]))
                    file.write("\n")
                    file.write("role")
                    file.write("\n")
                    file.write(str(participants[i]["role"]))
                    file.write("\n")
                    file.write("pentaKills")
                    file.write("\n")
                    file.write(str(participants[i]["pentaKills"]))
                    file.write("\n")
                    file.write("timePlayed")
                    file.write("\n")
                    file.write(str(participants[i]["timePlayed"]))
                    file.write("\n")
                    file.write("assists")
                    file.write("\n")
                    file.write(str(participants[i]["assists"]))
                    file.write("\n")

        except UnicodeEncodeError:
            pass
        """
    with open(os.path.dirname(__file__) + "/log.txt", "a+") as file:
        file.write("\n")
        file.write(returnstring)
        file.write("\n")
        file.write("Timestamp: ")
        file.write(str(datetime.now()))

    return returnstring

#### NEUE MATCHES BEARBEITEN ####
##################################################

#   HIER ANSTATT PRINT DISCORD BOT-INTEGRATION   #

##################################################
for entry in need_check:
    id = entry
    print(match_get_data(id,gameName))


    



