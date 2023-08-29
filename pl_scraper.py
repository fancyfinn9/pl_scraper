import requests
import json



######## CONFIG ########

useragent = True    # Should not be changed! 

##### END OF CONFIG ####






if useragent == True:
    agent = "pl_scraper"
else:
    agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"

def request(url="https://premierleague.com"):
    try:
        page = requests.get(url, headers={"User-Agent": agent}).text
        return page
    except requests.exceptions.ConnectionError as e:
        print(f">> Can't connect to \"{url}\"! Please check your internet connection <<")
        raise Exception("Please see top of error message")

def raw():
    page = request()
    
    return page

def file():
    page = request()
    
    with open("page.txt", "w") as f:
        f.write(page)
        f.close()
    return True

def teams():
    page = request()
    
    teams = []
    spanstart = 0
    while True:
        start = page.find("<li class=\"clubList__club\">",spanstart)
        if start != -1:
            spanstart = page.find("<span class=\"name\">", start)+19
            spanend = page.find("</span>", spanstart)
            teams.append(page[spanstart:spanend])
        else: break
    return teams

def matchweek():
    page = request()
    
    matchweek = {"matches":[]}
    
    start = page.find("<div class=\"fixtures-abridged-header__title\">")+45
    end = page.find("</div>", start)
    matchweek["id"] = int(page[start:end].strip()[10:11])
    
    datastart = 0
    while True:
        start = page.find("<a class=\"match-fixture match-fixture--abridged js-match-abridged\"", datastart)
        if start != -1:
            match = {"teams":{"home":{},"away":{}}, "score":{}}
            
            datastart = page.find("data-matchid=\"", start)+14
            dataend = page.find("\"", datastart)
            match["id"] = int(page[datastart:dataend])
            
            datastart = page.find("data-kickoff=\"", start)+14
            dataend = page.find("\"", datastart)
            match["timestamp"] = int(page[datastart:dataend])
            
            datastart = page.find("<div class=\"match-fixture__team match-fixture__team--home\">", start)+111
            dataend = page.find("</span>", datastart)
            match["teams"]["home"]["tiny"] = page[datastart:dataend]
            
            datastart = page.find("<div class=\"match-fixture__team match-fixture__team--away\">", start)+111
            dataend = page.find("</span>", datastart)
            match["teams"]["away"]["tiny"] = page[datastart:dataend]
            
            matchpage = request(url="https://premierleague.com/match/"+str(match["id"]))
            matchstart = matchpage.find("<div class=\"mcTabsContainer\" data-script=\"pl_match-centre\" data-widget=\"match-tabs\" data-fixture=")+98
            matchend = matchpage.find("'>", matchstart)
            matchdata = json.loads(matchpage[matchstart:matchend])
            
            match["teams"]["home"] = matchdata["teams"][0]["team"]
            match["teams"]["away"] = matchdata["teams"][1]["team"]
            
            match["completeness"] = matchdata["kickoff"]["completeness"]
            
            try:
                match["clock"] = matchdata["clock"]
            except KeyError:
                match["clock"] = None
            
            try:
                match["result"] = matchdata["outcome"]
            except KeyError:
                match["result"] = None
            
            try:
                match["score"]["home"] = matchdata["teams"][0]["score"]
                match["score"]["away"] = matchdata["teams"][1]["score"]
            except KeyError:
                match["score"]["home"] = None
                match["score"]["away"] = None
            
            matchweek["matches"].append(match)
        else: break
    matchweek["matches"] = sorted(matchweek["matches"], key=lambda match: match["timestamp"])
    return matchweek

def fixture(matchid):
    matchpage = request(url="https://premierleague.com/match/"+str(matchid))
    matchstart = matchpage.find("<div class=\"mcTabsContainer\" data-script=\"pl_match-centre\" data-widget=\"match-tabs\" data-fixture=")+98
    matchend = matchpage.find("'>", matchstart)
    matchdata = json.loads(matchpage[matchstart:matchend])
            
    return matchdata

def player(playerid):
    player = {"name":{"display":"","first":"","last":"","dob":"","age":0,"height":0,"country":""}, "club":{"club":{"name":"","id":0},"position":"","number":""}, "history":[]}
    history = {"season":"","club":{},"apps":0,"subs":0,"goals":0}
    club = {}
    
    playerpage = request(url="https://premierleague.com/players/"+str(playerid)+"/player/overview")
    
    datastart = playerpage.find("<img class=\"player-overview__flag-icon\" src=\"https://resources.premierleague.com/premierleague/flags/")+165
    dataend = playerpage.find("</span>", datastart)
    player["name"]["country"] = playerpage[datastart:dataend]
    
    datastart = playerpage.find("<div class=\"player-header__name-first\">")+39
    if datastart-39 == -1:
        player["name"]["first"] = ""
    else:
        dataend = playerpage.find("</div>", datastart)
        player["name"]["first"] = playerpage[datastart:dataend].strip()
    
    datastart = playerpage.find("<div class=\"player-header__name-last\">")+38
    dataend = playerpage.find("</div>", datastart)
    player["name"]["last"] = playerpage[datastart:dataend].strip()
    
    player["name"]["display"] = player["name"]["first"]+" "+player["name"]["last"]
    
    datastart = playerpage.find("<div class=\"player-overview__label\">Date of Birth</div>")+111
    dataend = playerpage.find("</div>", datastart)
    player["name"]["dob"] = playerpage[datastart:dataend].strip()[:10]
    player["name"]["age"] = playerpage[datastart:dataend].strip()[13:15]

    datastart = playerpage.find("<div class=\"player-overview__label\">Height</div>")+104
    dataend = playerpage.find("</div>", datastart)
    player["name"]["height"] = playerpage[datastart:dataend]
    
    searchstart = playerpage.find("<div class=\"player-overview__label\">Club</div>")
    datastart = playerpage.find("/overview\">", searchstart)+13
    dataend = playerpage.find("<span", datastart)
    player["club"]["club"]["name"] = playerpage[datastart:dataend].strip()
    
    datastart = playerpage.find("<a href=\"/clubs/", searchstart)+16
    dataend = playerpage.find("/", datastart)
    player["club"]["club"]["id"] = playerpage[datastart:dataend]
    
    datastart = playerpage.find("<div class=\"player-overview__label\">Position</div>")+106
    dataend = playerpage.find("</div>", datastart)
    player["club"]["position"] = playerpage[datastart:dataend]

    datastart = playerpage.find("<div class=\"player-header__player-number player-header__player-number--small\">")+78
    dataend = playerpage.find("</div>", datastart)
    player["club"]["number"] = playerpage[datastart:dataend]
    
    searchstart = 0
    while True:
        start = playerpage.find("<tr class=\"table player-club-history__table-row\">",searchstart)
        if start != -1:
            searchstart = playerpage.find("<td class=\"player-club-history__season\"><p>", start)+43
            searchend = playerpage.find("</p></td>", searchstart)
            history["season"] = playerpage[searchstart:searchend]
              
            searchstart = playerpage.find("<a href=\"/clubs/", start)+16
            searchend = playerpage.find("/", searchstart)
            club["id"] = playerpage[searchstart:searchend]
            
            searchstart = playerpage.find("<span class=\"player-club-history__team-name player-club-history__team-name--long\">", start)+82
            searchend = playerpage.find("</span>", searchstart)
            club["name"] = playerpage[searchstart:searchend]
            
            history["club"] = club.copy()            
            
            searchstart = playerpage.find("<td class=\"player-club-history__appearances\">", start)+54
            searchend = playerpage.find("<span", searchstart)
            history["apps"] = playerpage[searchstart:searchend].strip()
            
            searchstart = playerpage.find("<span class=\"appearances--sub\">(", start)+32
            searchend = playerpage.find(")", searchstart)
            history["subs"] = playerpage[searchstart:searchend]
            
            searchstart = playerpage.find("<td class=\"player-club-history__goals\">", start)+48
            searchend = playerpage.find("</td>", searchstart)
            history["goals"] = playerpage[searchstart:searchend].strip()
            
            player["history"].append(history.copy())
        else: break

    
    return player
