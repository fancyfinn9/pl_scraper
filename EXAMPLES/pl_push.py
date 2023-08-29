import pl_scraper as pl
import requests
import time

events = []

while True:
    print("Sending!")
    sent = 0
    fixture = pl.fixture(93337)
    for event in fixture["events"]:
        if event in events:
            pass
        else:
            events.append(event)
            data = ""
            
            if event["type"] == "G":
                title = "GOOOAAL! ("+pl.player(event["personId"])["name"]["display"]+", "+event["clock"]["label"][:-2]+")"
            elif event["type"] == "PS":
                if event["phase"] == "1": title = "KICKOFF at "+fixture["ground"]["name"]
                elif event["phase"] == "2": title = "2ND HALF BEGINS at "+fixture["ground"]["name"]
                else: title = "<Unknown Play Start event>"
            elif event["type"] == "PE":
                if event["phase"] == "1": title = "HALF-TIME at "+fixture["ground"]["name"]
                elif event["phase"] == "2": title = "FULL TIME at "+fixture["ground"]["name"]
                else: title = "<Unknown Play End event>"
            elif event["type"] == "S":
                title = "SUB "+event["description"]+" - "+pl.player(event["personId"])["name"]["display"]+" ("+event["clock"]["label"][:-2]+")"
            elif event["type"] == "B":
                try:
                    x = event["personId"]
                    if event["description"] == "Y":
                        title = "YELLOW CARD - "+pl.player(event["personId"])["name"]["display"]+" ("+event["clock"]["label"][:-2]+")"
                    elif event["description"] == "R":
                        title = "RED CARD - "+pl.player(event["personId"])["name"]["display"]+" ("+event["clock"]["label"][:-2]+")"
                except KeyError:
                    event["personId"] = "<Unknown player>"
                    if event["description"] == "Y":
                        title = "YELLOW CARD - "+event["personId"]+" ("+event["clock"]["label"][:-2]+")"
                    elif event["description"] == "R":
                        title = "RED CARD - "+event["personId"]+" ("+event["clock"]["label"][:-2]+")"
            else:
                title = "<Unknown event>"
            data = data+fixture["teams"][0]["team"]["club"]["shortName"]+" v "+fixture["teams"][1]["team"]["club"]["shortName"]
            data = data+"\n"+str(event["score"]["homeScore"])+"-"+str(event["score"]["awayScore"])
            try:
                requests.post("https://ntfy.sh/pl_notify",
                data=data,
                headers={
                    "Click": "https://premierleague.com/fixture/"+str(fixture["id"]),
                    "Title": title.encode('utf-8'),
                    "Tags": "soccer"
                })
            except requests.exceptions.InvalidHeader:
                print("ERROR!")
                print(title)
            sent += 1
            print(f" => Sent notification {event['time']['millis']}")
    print(f"Sent {sent} notifications")
    time.sleep(60)
