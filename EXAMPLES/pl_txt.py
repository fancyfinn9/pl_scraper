import pl_scraper as pl
import time





###### CONFIG ######

fixtureid = 93337
dire = "obs"

####################





def write(file, content):
    name = dire+"/"+file+".txt"
    with open(name, "w") as f:
        f.write(str(content))
        f.close()
        

print("Script start!")

match = pl.fixture(fixtureid)

write("home_abbr", match["teams"][0]["team"]["club"]["abbr"])
write("away_abbr", match["teams"][1]["team"]["club"]["abbr"])

print("Loop start!")

while True:
    match = pl.fixture(fixtureid)
    
    write("home_score", match["teams"][0]["score"])
    write("away_score", match["teams"][1]["score"])
    clock = match["clock"]["label"][:-3]
    if "+" in clock:
        added = "+"+clock[4:]
    else:
        added = "+0"
    clock = clock[:2]+"'"
    
    write("clock", clock)
    write("clock_added", added)
    
    time.sleep(60)
    print("Looped!")

