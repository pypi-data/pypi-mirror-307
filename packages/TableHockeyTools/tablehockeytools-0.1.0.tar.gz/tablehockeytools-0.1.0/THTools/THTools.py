import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

## gets the ranking points for a player
def GetPlayerPoints(player_id):

    points_url = 'https://stiga.trefik.cz/ithf/ranking/player.aspx?id=' + str(player_id)


    #    headers = {
    #        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    #        'accept-language': 'en-US,en;q=0.9',
    #   }

    response_points = requests.get(points_url)
    response_points.raise_for_status()

    soup = BeautifulSoup(response_points.content, 'html.parser')

    points_label = soup.find(string="Points")
    if points_label:
        points_value = points_label.find_next("td").string.strip()
        return points_value
    else:
        print("ERR: Points value not found.")


## this is not complete, need to add the rest of the functions
def GetPlayerRank(player_id):
    player_pos_url = "http://www.ithf.info/stiga/ithf/ranking/getrank.asmx/GetRank?ID="+str(player_id)


    response = requests.get(player_pos_url)
    rank = ET.fromstring(response.content).text
    return rank


## gets the player id from the player's name, last name first then first name. THIS REQUIRES THE FULL NAME AND RETUNRS ONLY THE FIRST ENTRY
def GetPlayerID(player_name):
    url = 'https://stiga.trefik.cz/ithf/ranking/playerID.txt'
    
    response = requests.get(url)
    response.raise_for_status()
    
    lines = response.text.splitlines()
    
    for line in lines:
        columns = line.split('\t')
        if len(columns) > 1:
            player_id, full_name = columns[0], columns[1]
            if full_name.lower() == player_name.lower():
                return player_id 

    print(f"WARN:could not find a {player_name}, check for spelling mistakes. Remember to write last name first then first name.")

