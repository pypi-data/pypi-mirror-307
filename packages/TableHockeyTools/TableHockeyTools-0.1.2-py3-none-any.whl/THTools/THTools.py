import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET




def THlog(message, mode="info"):
    class TextColors:
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKCYAN = '\033[96m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'

    if mode == "info":
        print(f"{TextColors.OKBLUE}INFO: {message}{TextColors.ENDC}")
    elif mode == "warning":
        print(f"{TextColors.WARNING}WARN: {message}{TextColors.ENDC}")
    elif mode == "error":
        print(f"{TextColors.FAIL}ERROR:{message}{TextColors.ENDC}")

## gets the ranking points for a player
def GetPlayerPoints(player_ids=None, player_names=None, return_mode="list", verbose=False, supress_warnings=False):
    if return_mode not in ["list", "dict", "single"]:
        THlog("return_mode must be either 'single', 'list' or 'dict'", "error")
        return
    if return_mode == "list":
        points_values = []
    elif return_mode == "dict":
        points_values = {}

    player_ids = [player_ids] if type(player_ids) is not list else player_ids
    player_names = [player_names] if type(player_names) is not list else player_names

    if not ((player_ids[0] is None )^(player_names[0] is None)):
        THlog("Please provide either a player ID or a player name.", "error")
        return
    
    if player_ids[0] is None:
        player_ids = GetPlayerID(player_names, return_mode="list") #gets player ids from player names
        
        if verbose:
            THlog(f"Found player ids {player_ids}", "info")
 
    for id, name in zip(player_ids, player_names):
        points_url = 'https://stiga.trefik.cz/ithf/ranking/player.aspx?id=' + id

        response_points = requests.get(points_url)
        response_points.raise_for_status()

        soup = BeautifulSoup(response_points.content, 'html.parser')

        points_label = soup.find(string="Points")

        if points_label:
            points_value = points_label.find_next("td").string.strip() #gets the value of the points from the html
            if return_mode == "list":
                points_values.append(points_value)
            elif return_mode == "dict":
                points_values[name] = points_value
            else:
                return points_value
        elif not supress_warnings:
            THlog(f"Could not find points for player {name}.", "warning")
        if len(points_values) == 0 and len(player_names) > 1:
            THlog(f"could not find any points values for {player_names}", "error")
    return points_values


## gets the open ranking for a player, output is a list or key-value pair depending on return_mode
def GetPlayerRank(player_ids=None, player_names=None, return_mode="list", verbose=False, supress_warnings=False):
    if return_mode not in ["list", "dict", "single"]:
        THlog("return_mode must be either 'single', 'list' or 'dict'", "error")
        return
    if return_mode == "list":
        ranks = []
    elif return_mode == "dict":
        ranks = {}

    player_ids = [player_ids] if type(player_ids) is not list else player_ids
    player_names = [player_names] if type(player_names) is not list else player_names

    if not ((player_ids[0] is None )^(player_names[0] is None)):
        THlog("Please provide either a player ID or a player name.", "error")
        return
    
    if player_ids[0] is None:
        player_ids = GetPlayerID(player_names, return_mode="list") #gets player ids from player names

        if verbose:
            THlog(f"Found player ids {player_ids}", "info")

    for id, name in zip(player_ids, player_names):
        player_pos_url = "http://www.ithf.info/stiga/ithf/ranking/getrank.asmx/GetRank?ID="+str(id) 
        if verbose:
            THlog(f"Requesting url {player_pos_url}", "info")

        response = requests.get(player_pos_url) #request url
        response.raise_for_status()
        rank = ET.fromstring(response.content).text
        if rank == "-": #if no rank is found the response from the server is "-"
            if not supress_warnings:
                THlog(f"no rank for {name}", "warning")
            continue
        else:
            if return_mode == "list":
                ranks.append(rank)
            elif return_mode == "dict":
                ranks[name] = rank
            else:
                return rank
    return ranks


## gets the player id from the player's name, last name first then first name. 
def GetPlayerID(player_names, return_mode="single", verbose=False, supress_warnings=False):
    if return_mode not in ["dict", "list", "single"]:
        THlog("return_mode must be either 'dict', 'list' or 'single'", "error")
        return
    if return_mode == "list":
        player_ids = []
    elif return_mode == "dict":
        player_ids = {}
    else:
        player_ids = 0

    url = 'https://stiga.trefik.cz/ithf/ranking/playerID.txt'
    
    response = requests.get(url)
    response.raise_for_status()
    
    lines = response.text.splitlines()
    if player_names is None:
        THlog("Please provide either a player name or a list of player names.", "error")
        return
    if player_names.__class__.__name__ == "str":
        player_names = [player_names]
    for player_name in player_names:
        for line in lines:
            columns = line.split('\t')
            if len(columns) > 1:
                player_id, full_name = columns[0], columns[1]
                if full_name.lower().__contains__(player_name.lower()):
                    if verbose:
                        THlog(f"Found player {full_name} with ID {player_id}", "info")
                    
                    if return_mode == "list":
                        player_ids.append(player_id)
                    elif return_mode == "dict":
                        player_ids[full_name] = player_id
                    else:
                        return int(player_id)

        if len(player_ids) == 0 and len(player_names) > 1 and not supress_warnings:
            THlog(f"could not find a {player_name}, check for spelling mistakes.", "warning")
    if len(player_ids) == 0:
        THlog("No player IDs found.", "error")
        return
    return player_ids


##opposite of GetPlayerID, gets the player name from the player's id
def GetPlayerName(player_ids, return_mode="single", verbose=False, supress_warnings=False):
    if return_mode not in ["dict", "list", "single"]:
        THlog("return_mode must be either 'single', 'list' or 'dict'", "error")
        return
    if return_mode == "list":
        player_names = []
    elif return_mode == "dict":
        player_names = {}
    else:
        player_names = 0

    url = 'https://stiga.trefik.cz/ithf/ranking/playerID.txt'
    
    response = requests.get(url)
    response.raise_for_status()
    
    lines = response.text.splitlines()
    if player_ids is None:
        THlog("Please provide either a player name or a list of player names.", "error")
        return
    if player_ids.__class__.__name__ == "str":
        player_ids = [player_ids]

    for id in player_ids:
        for line in lines:
            columns = line.split('\t')
            if len(columns) > 1:
                player_id, full_name = columns[0], columns[1]
                if player_id == id:
                    if verbose:
                        THlog(f"Found player {full_name} with ID {player_id}", "info")
                    
                    if return_mode == "list":
                        player_names.append(full_name)
                    elif return_mode == "dict":
                        player_names[full_name] = player_id
                    else:
                        return full_name

        if len(player_names) == 0 and len(player_ids) > 1 and not supress_warnings:
            THlog(f"could not find id {id}, check for spelling mistakes.", "warning")
    if len(player_names) == 0:
        THlog("No player names found.", "error")
        return
    return player_names


    