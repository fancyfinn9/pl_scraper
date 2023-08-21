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
            
            matchpage = request(url="https://premierleague.com/match/"+str(match["id"]), headers={"User-Agent": agent})
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

def fixture(matchid=93337):
    matchpage = request(url="https://premierleague.com/match/"+str(matchid))
    matchstart = matchpage.find("<div class=\"mcTabsContainer\" data-script=\"pl_match-centre\" data-widget=\"match-tabs\" data-fixture=")+98
    matchend = matchpage.find("'>", matchstart)
    matchdata = json.loads(matchpage[matchstart:matchend])
            
    print(matchdata["teams"][0]["team"])
    print(matchdata["teams"][1]["team"])
    return True